"""
Regularizer class for that also supports GPU code

Michael Chen   mchen0405@berkeley.edu
David Ren      david.ren@berkeley.edu
March 04, 2018

Modified by Jiabei Zhu <zjb@bu.edu>
December, 2020
"""

import numpy as af
import numpy as np
# from opticaltomography import settings

np_complex_datatype = af_complex_datatype = np.complex128
np_float_datatype = af_float_datatype = np.float64


class ProximalOperator:
    def __init__(self, proximal_name):
        self.proximal_name = proximal_name

    def computeCost(self):
        pass

    def computeProx(self):
        pass

    def setParameter(self):
        pass

    def _boundRealValue(self, x, value=0, flag_project=True):
        """If flag is true, only values that are greater than 'value' are preserved"""
        if flag_project:
            x[x < value] = 0
        return x


class TotalVariationGPU(ProximalOperator):
    def __init__(self, **kwargs):
        proximal_name = "Total Variation"
        parameter = kwargs.get("total_variation_parameter", 1.0)
        maxitr = kwargs.get("total_variation_maxitr", 15)
        self.order = kwargs.get("total_variation_order", 1)
        self.pure_real = kwargs.get("pure_real", False)
        self.pure_imag = kwargs.get("pure_imag", False)
        self.pure_amplitude = kwargs.get("pure_amplitude", False)
        self.pure_phase = kwargs.get("pure_phase", False)

        # real part
        if kwargs.get("positivity_real", False):
            self.realProjector = lambda x: self._boundRealValue(x, 0, True)
            proximal_name = "%s+%s" % (proximal_name, "positivity_real")
        elif kwargs.get("negativity_real", False):
            self.realProjector = lambda x: -1.0 * self._boundRealValue(-1.0 * x, 0, True)
            proximal_name = "%s+%s" % (proximal_name, "negativity_real")
        else:
            self.realProjector = lambda x: x

        self.setParameter(parameter, maxitr)
        super().__init__(proximal_name)

    def setParameter(self, parameter, maxitr):
        self.parameter = parameter
        self.maxitr = maxitr

    def computeProx(self, x):
        x = self._computeProxReal(x, self.realProjector)
        return x


    def _computeTVNorm(self, x):
        x_norm = x ** 2
        x_norm = af.sum(x_norm, dim=3 if len(x.shape) == 4 else 2) ** 0.5
        x_norm[x_norm < 1.0] = 1.0
        return x_norm

    def _filterD(self, x, axis):
        if axis == 0:
            dx = x - af.shift(x, 1, 0, 0)
        elif axis == 1:
            dx = x - af.shift(x, 0, 1, 0)
        else:
            dx = x - af.shift(x, 0, 0, 1)

        return dx

    def _filterDT(self, x):
        DTx = self._indexLastAxis(x, 0) - af.shift(self._indexLastAxis(x, 0), -1, 0, 0) + \
              self._indexLastAxis(x, 1) - af.shift(self._indexLastAxis(x, 1), 0, -1, 0) + \
              self._indexLastAxis(x, 2) - af.shift(self._indexLastAxis(x, 2), 0, 0, -1)
        return DTx

    def _computeProxReal(self, x, projector):
        t_k = 1.0

        def _gradUpdate():
            grad_u_hat = x - self.parameter * self._filterDT(u_k1)
            return grad_u_hat

        if len(x.shape) == 3:
            u_k = af.constant(0.0, x.shape[0], x.shape[1], x.shape[2], 3, dtype=af_float_datatype)
            u_k1 = af.constant(0.0, x.shape[0], x.shape[1], x.shape[2], 3, dtype=af_float_datatype)
        # grad_u_hat = af.constant(0.0, x.shape[0], x.shape[1], x.shape[2], dtype = af_float_datatype)

        for iteration in range(self.maxitr):
            if iteration > 0:
                grad_u_hat = _gradUpdate()
            else:
                grad_u_hat = x.copy()

            grad_u_hat = projector(grad_u_hat)
            u_k1[:, :, :, 0] = self._indexLastAxis(u_k1, 0) + (
                        1.0 / 12 / self.parameter) * self._filterD(grad_u_hat, axis=0)
            u_k1[:, :, :, 1] = self._indexLastAxis(u_k1, 1) + (
                        1.0 / 12 / self.parameter) * self._filterD(grad_u_hat, axis=1)
            u_k1[:, :, :, 2] = self._indexLastAxis(u_k1, 2) + (
                        1.0 / 12 / self.parameter) * self._filterD(grad_u_hat, axis=2)
            grad_u_hat = None
            u_k1_norm = self._computeTVNorm(u_k1)
            if len(x.shape) == 2:  # 2D case
                u_k1[:, :, 0] /= u_k1_norm
                u_k1[:, :, 1] /= u_k1_norm
            if len(x.shape) == 3:  # 3D case
                u_k1[:, :, :, 0] /= u_k1_norm
                u_k1[:, :, :, 1] /= u_k1_norm
                u_k1[:, :, :, 2] /= u_k1_norm
            u_k1_norm = None
            t_k1 = 0.5 * (1.0 + (1.0 + 4.0 * t_k ** 2) ** 0.5)
            beta = (t_k - 1.0) / t_k1

            if len(x.shape) == 3:  # 3D case
                temp = u_k[:, :, :, 0].copy()
                if iteration < self.maxitr - 1:
                    u_k[:, :, :, 0] = u_k1[:, :, :, 0]
                u_k1[:, :, :, 0] = (1.0 + beta) * u_k1[:, :, :, 0] - beta * temp  # now u_hat
                temp = u_k[:, :, :, 1].copy()
                if iteration < self.maxitr - 1:
                    u_k[:, :, :, 1] = u_k1[:, :, :, 1]
                u_k1[:, :, :, 1] = (1.0 + beta) * u_k1[:, :, :, 1] - beta * temp
                temp = u_k[:, :, :, 2].copy()
                if iteration < self.maxitr - 1:
                    u_k[:, :, :, 2] = u_k1[:, :, :, 2]
                u_k1[:, :, :, 2] = (1.0 + beta) * u_k1[:, :, :, 2] - beta * temp
            temp = None

        grad_u_hat = projector(_gradUpdate())
        u_k = None
        u_k1 = None
        return grad_u_hat


class TotalVariationCPU(TotalVariationGPU):
    def _computeTVNorm(self, x):
        u_k1_norm = af.to_array(x)
        u_k1_norm[:] *= u_k1_norm
        u_k1_norm = af.sum(u_k1_norm, dim=3 if len(x.shape) == 4 else 2) ** 0.5
        u_k1_norm[u_k1_norm < 1.0] = 1.0
        return np.array(u_k1_norm)

    def computeProx(self, x):
        if self.pure_real:
            x = self._computeProxReal(np.real(x), self.realProjector) + 1.0j * 0.0
        elif self.pure_imag:
            x = 1.0j * self._computeProxReal(np.imag(x), self.imagProjector)
        else:
            x = self._computeProxReal(np.real(x), self.realProjector) \
                + 1.0j * self._computeProxReal(np.imag(x), self.imagProjector)
        return af.to_array(x)

    def _computeProxReal(self, x, projector):
        t_k = 1.0
        u_k = np.zeros(x.shape + (3 if len(x.shape) == 3 else 2,), dtype=np_float_datatype);
        u_k1 = u_k.copy()
        u_hat = u_k.copy()

        def _gradUpdate():
            u_hat_af = af.to_array(u_hat)
            if len(x.shape) == 2:
                DTu_hat = self._indexLastAxis(u_hat_af, 0) - af.shift(self._indexLastAxis(u_hat_af, 0), -1, 0) + \
                          self._indexLastAxis(u_hat_af, 1) - af.shift(self._indexLastAxis(u_hat_af, 1), 0, -1)
            elif len(x.shape) == 3:
                DTu_hat = self._indexLastAxis(u_hat_af, 0) - af.shift(self._indexLastAxis(u_hat_af, 0), -1, 0, 0) + \
                          self._indexLastAxis(u_hat_af, 1) - af.shift(self._indexLastAxis(u_hat_af, 1), 0, -1, 0) + \
                          self._indexLastAxis(u_hat_af, 2) - af.shift(self._indexLastAxis(u_hat_af, 2), 0, 0, -1)
            grad_u_hat = x - np.array(self.parameter * DTu_hat)
            return grad_u_hat

        for iteration in range(self.maxitr):
            if iteration > 0:
                grad_u_hat = _gradUpdate()
            else:
                grad_u_hat = x.copy()

            grad_u_hat = projector(grad_u_hat)
            u_k1[..., 0] = u_hat[..., 0] + (1.0 / 12.0 / self.parameter) * (grad_u_hat - np.roll(grad_u_hat, 1, axis=0))
            u_k1[..., 1] = u_hat[..., 1] + (1.0 / 12.0 / self.parameter) * (grad_u_hat - np.roll(grad_u_hat, 1, axis=1))
            if len(x.shape) == 3:
                u_k1[..., 2] = u_hat[..., 2] + (1.0 / 12.0 / self.parameter) * (
                            grad_u_hat - np.roll(grad_u_hat, 1, axis=2))
            u_k1_norm = self._computeTVNorm(u_k1)
            u_k1[:] /= u_k1_norm[..., np.newaxis]
            t_k1 = 0.5 * (1.0 + (1.0 + 4.0 * t_k ** 2) ** 0.5)
            beta = (t_k - 1.0) / t_k1
            u_hat = (1.0 + beta) * u_k1 - beta * u_k
            if iteration < self.maxitr - 1:
                u_k = u_k1.copy()
        return projector(_gradUpdate())


class Lasso(ProximalOperator):
    """||x||_1 regularizer, soft thresholding with certain parameter"""

    def __init__(self, parameter):
        super().__init__("LASSO")
        self.setParameter(parameter)

    def _softThreshold(self, x):
        if type(x).__module__ == "arrayfire.array":
            # POTENTIAL BUG: af.sign implementation does not agree with documentation
            x = (af.sign(x) - 0.5) * (-2.0) * (af.abs(x) - self.parameter) * (af.abs(x) > self.parameter)
        else:
            x = np.sign(x) * (np.abs(x) - self.parameter) * (np.abs(x) > self.parameter)
        return x

    def setParameter(self, parameter):
        self.parameter = parameter

    def computeCost(self, x):
        return af.norm(af.moddims(x, np.prod(x.shape)), norm_type=af.NORM.VECTOR_1)

    def computeProx(self, x):
        if type(x).__module__ == "arrayfire.array":
            x = self._softThreshold(af.real(x)) + 1.0j * self._softThreshold(af.imag(x))
        else:
            x = self._softThreshold(x.real) + 1.0j * self._softThreshold(x.imag)
        return x
