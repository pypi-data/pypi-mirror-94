import torch
import pyro
import pyro.distributions as dist
from pyro.contrib import autoname

from . import constants
from . import util
from . import exceptions
from . import core


forecast = core.forecast
redefine = core.redefine


def register_block(
    name,
    fn_addr_param,
    model_fn,
):
    """
    ```
    def register_block(
        name,
        fn_addr_param,
        model_fn,
    ):
    ```

    Registers a new block at runtime

    *Args*:

    + `name (str)`: name of the new block (class)
    + `fn_addr_param (dict)`: functional address parameterization; see documentation
        of `core.construct_init` for required structure
    + `model_fn (callable)`: the implementation of the likelihood-function portion
        of `Block._model`. An example implementation, here for a (determininstic)
        quadratic trend, is shown below:

        ```
        def model_fn(x):
            alpha, beta, gamma = core.name_to_definite(x, "alpha", "beta", "gamma")

            with autoname.scope(prefix=constants.dynamic):
                t = torch.linspace(x.t0, x.t1, x.t1 - x.t0)
                path = pyro.deterministic(
                    x.name + "-" + constants.generated,
                    alpha + t * beta + t.pow(2) * gamma
                )
            return path
        ```

        The call to `core.name_to_definite` takes care of calling `pyro.sample` if
        the parameters are defined as pyro distributions, calls model methods if
        the parameters are defined as `Block`s, and so on.
    """
    init_fn = core.construct_init(fn_addr_param)
    # NOTE: below relies on register_address_component called in construct_init
    function_addresses = set(fn_addr_param.keys())
    NewClass = type(
        name,
        (core.Block,),
        {"_function_addresses": function_addresses, "_model": model_fn},
    )
    NewClass.__init__ = core._closure_init(init_fn)
    globals()[name] = NewClass


class GaussianNoise(core.NoiseBlock):
    """
    ```
    def __init__(
        self,
        dgp,
        data=None,
        name=None,
        t0=0,
        t1=2,
        size=1,
        scale=None,
    ):
    ```

    A noise block (time series likelihood function) that assumes a centered normal observation process.

    The likelihood function for this block is

    $$
    p(x | \mathrm{dgp}, \mathrm{scale}) = \prod_{t=t_0}^{t_1} \mathrm{Normal}(x_t | \mathrm{dgp}_t, \mathrm{scale}_t)
    $$

    *Args:*

    + `scale (Block || torch.tensor || pyro.distributions)`:

    See `NoiseBlock` for definitions of other parameters
    """

    def __init__(
        self,
        dgp,
        data=None,
        name=None,
        t0=0,
        t1=2,
        size=1,
        scale=None,
    ):
        super().__init__(
            dgp,
            data=data,
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )

        setattr(
            self, constants.scale, scale or dist.LogNormal(0.0, 1.0).expand((size,))
        )
        self._maybe_add_blocks(getattr(self, constants.scale))

    def _model(
        self,
        size=1,
    ):
        scale = core._obj_name_to_definite(self, constants.scale, likelihood=True)

        latent = self.dgp.model()
        obs = pyro.sample(
            self.name + "-" + constants.obs,
            dist.Normal(
                latent,
                scale,
            ),
            obs=self.data,
        )
        util.clear_cache(self.dgp)
        return obs


class PoissonNoise(core.NoiseBlock):
    """
    ```
    def __init__(
        self,
        dgp,
        data=None,
        name=None,
        t0=0,
        t1=2,
        size=1,
    ):
    ```

    A noise block (time series likelihood function) that assumes a Poisson observation process.

    This observation process is suitable for use with count (or other non-negative integer) data that
    does not exhibit over- or under-dispersion (in practice, if the log ratio of mean to variance of the observed data
    is not too far away from zero).

    The likelihood function for this block is

    $$
    p(x | \mathrm{dgp}) = \prod_{t=t_0}^{t_1} \mathrm{Poisson}(x_t | \mathrm{dgp}_t)
    $$

    The $\mathrm{dgp}$ needs to be non-negative because it is used as the rate function of the Poisson likelihood.
    Consider using `.softplus(...)` or `.exp(...)` on an unconstrained `Block`.

    *Args:*

    See `NoiseBlock` for definitions of arguments.
    """

    def __init__(
        self,
        dgp,
        data=None,
        name=None,
        t0=0,
        t1=2,
        size=1,
    ):
        super().__init__(
            dgp,
            data=data,
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )

    def _model(
        self,
        size=1,
    ):
        latent = self.dgp.model()
        obs = pyro.sample(
            self.name + "-" + constants.obs,
            dist.Poisson(
                latent,
            ),
            obs=self.data,
        )
        util.clear_cache(self.dgp)
        return obs


class DiscriminativeGaussianNoise(core.NoiseBlock):
    """
    ```
    def __init__(
        self,
        dgp,
        X=None,
        y=None,
        name=None,
        t0=0,
        t1=2,
        size=1,
        scale=None,
    ):
    ```

    A discriminative noise block used for dynamic regression.

    The observation likelihood is given by

    $$
    p(x | \mathrm{dgp}, \mathrm{scale}) =
        \prod_{t=t_0}^{t_1} \mathrm{Normal}(x_t | X_t \mathrm{dgp}_t, \mathrm{scale}_t),
    $$

    where $X_t \mathrm{dgp}_t$ should be interpreted as batched matrix multiplication,
    i.e., $\mathrm{loc}_{it} = X_{ijt}\mathrm{dgp}_{jt}$.

    *Args:*

    + `X (torch.tensor)`: shape `(size, dims, time)`
    + `y (None || torch.tensor)`: if not `None`, shape `(size, time)`

    See `GaussianNoise` for definitions of other parameters
    """

    def __init__(
        self,
        dgp,
        X=None,
        y=None,
        name=None,
        t0=0,
        t1=2,
        size=1,
        scale=None,
    ):
        super().__init__(
            dgp,
            data=y,
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )

        assert type(X) == torch.Tensor
        assert len(X.shape) == 3
        self.X = X
        setattr(
            self, constants.scale, scale or dist.LogNormal(0.0, 1.0).expand((size,))
        )
        self._maybe_add_blocks(getattr(self, constants.scale))

    def _model(
        self,
    ):
        (scale,) = core.name_to_definite(self, "scale")
        loc = torch.einsum("ijk, jk -> ik", self.X, self.dgp())
        obs = pyro.sample(
            self.name + "-" + constants.obs,
            dist.Normal(
                loc,
                scale,
            ),
            obs=self.data,
        )
        util.clear_cache(self.dgp)
        return obs


class RandomWalk(core.Block):
    """
    ```
    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        loc=None,
        scale=None,
        ic=None,
    ):
    ```

    A (biased) normal random walk dgp.

    The generative model for this process is

    $$
    z_t = z_{t - 1} + \mathrm{loc}_t + \mathrm{scale}_t w_t,\ z_0 = \mathrm{ic},
    $$

    for $t = t_0,...,t_1$. Here, $\mathrm{loc}$ is the dgp for the location parameter and
    $\mathrm{scale}$ is the dgp for the scale parameter. These processes may be other `Block`s,
    `torch.tensor`s, or `pyro.distributions` objects, and the interpretation of
    $\mathrm{loc}_t$ or $\mathrm{scale}_t$ will change accordingly.
    The initial condition, $\mathrm{ic}$, can be either a `torch.tensor` or `pyro.distributions` object.
    The term $w_t$ is a standard normal variate.

    *Args:*

    + `loc (Block || torch.tensor || pyro.distributions)`: location parameter
    + `scale (Block || torch.tensor || pyro.distributions)`: scale parameter
    + `ic (torch.tensor || pyro.distributions)`: initial condition

    See `Block` for definitions of other parameters.
    """

    _function_addresses = {constants.loc, constants.scale, constants.ic}

    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        loc=None,
        scale=None,
        ic=None,
    ):
        super().__init__(
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )

        setattr(self, constants.loc, loc or dist.Normal(0.0, 1.0).expand((size,)))
        setattr(
            self, constants.scale, scale or dist.LogNormal(0.0, 1.0).expand((size,))
        )
        setattr(self, constants.ic, ic or dist.Normal(0.0, 1.0).expand((size,)))
        self._maybe_add_blocks(
            getattr(self, constants.loc),
            getattr(self, constants.scale),
        )

        self.has_fast_mode = True

    def _model(
        self,
        size=1,
        fast=False,
    ):
        loc = core._obj_name_to_definite(self, constants.loc)
        scale = core._obj_name_to_definite(self, constants.scale)
        ic = core._obj_name_to_definite(self, constants.ic, flag_on_block=True)

        if not fast:
            path = torch.empty((self.size, self.t1 - self.t0))
            path[:, 0] = ic

        with autoname.scope(prefix=constants.dynamic):
            if not fast:
                for t in range(self.t0 + 1, self.t1):
                    # time shifted forward for variable identification
                    this_noise = pyro.sample(
                        self.name + f"-{constants.noise}-{t}",
                        dist.Normal(0.0, 1.0).expand((self.size,)),
                    )
                    t -= self.t0  # shift back for indexing
                    path[:, t] = path[:, t - 1] + loc[:, t] + scale[:, t] * this_noise
            else:
                noise = pyro.sample(
                    self.name + f"-{constants.noise}",
                    dist.Normal(0.0, 1.0).expand((self.size, self.t1 - self.t0)),
                )
                path = ic.unsqueeze(-1) + (loc + scale * noise).cumsum(dim=-1)
            path = pyro.deterministic(self.name + f"-" + constants.generated, path)
        return path

    def __repr__(
        self,
    ):
        string = f"RandomWalk({getattr(self, constants.loc)}, {getattr(self, constants.scale)}, {getattr(self, constants.ic)})"
        return core._add_fns_to_repr(self, string)


class CCSDE(core.Block):
    """
    ```
    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        loc=None,
        scale=None,
        dt=None,
        ic=None,
    ):
    ```

    A constant-coefficient Euler-Maruyama stochastic differential equation dgp.

    The generative model for this process is

    $$
    z_t = z_{t - 1} + \mathrm{dt}_t \mathrm{loc}_t + \sqrt{\mathrm{dt}_t} \mathrm{scale}_t  w_t,\ z_0 = \mathrm{ic},
    $$

    for $t = t_0, ..., t_1$. Here, $\mathrm{loc}$ is the dgp for the location parameter,
    $\mathrm{scale}$ is the dgp for the scale parameter, and $\mathrm{dt}$ is the dgp for the time
    discretization. These processes may be other `Block`s,
    `torch.tensor`s, or `pyro.distributions` objects, and the interpretation of
    $\mathrm{loc}_t$, $\mathrm{scale}_t$, and $\mathrm{dt}_t$ will change accordingly.
    The initial condition, $\mathrm{ic}$, can be either a `torch.tensor` or `pyro.distributions` object.
    The term $w_t$ is a standard normal variate.

    *Args:*

    + `loc (Block || torch.tensor || pyro.distributions)`: location parameter
    + `scale (Block || torch.tensor || pyro.distributions)`: scale parameter
    + `dt (Block || torch.tensor || pyro.distributions)`: time discretization parameter
    + `ic (torch.tensor || pyro.distributions)`: initial condition

    See `Block` for definitions of other parameters.
    """

    _function_addresses = {constants.loc, constants.scale, constants.ic, constants.dt}

    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        loc=None,
        scale=None,
        dt=None,
        ic=None,
    ):
        super().__init__(
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )

        setattr(self, constants.loc, loc or dist.Normal(0.0, 1.0).expand((size,)))
        setattr(
            self, constants.scale, scale or dist.LogNormal(0.0, 1.0).expand((size,))
        )
        setattr(self, constants.ic, ic or dist.Normal(0.0, 1.0).expand((size,)))
        setattr(self, constants.dt, dt or 0.01 * torch.ones(1))
        self._maybe_add_blocks(
            getattr(self, constants.loc),
            getattr(self, constants.scale),
            getattr(self, constants.dt),
        )

        self.has_fast_mode = True

    def _model(
        self,
        size=1,
        fast=False,
    ):
        loc = core._obj_name_to_definite(self, constants.loc)
        scale = core._obj_name_to_definite(self, constants.scale)
        dt = core._obj_name_to_definite(self, constants.dt)
        ic = core._obj_name_to_definite(self, constants.ic, flag_on_block=True)

        path = torch.empty((self.size, self.t1 - self.t0))
        path[:, 0] = ic

        with autoname.scope(prefix=constants.dynamic):
            if not fast:
                for t in range(self.t0 + 1, self.t1):
                    # time shifted forward for variable identification
                    this_noise = pyro.sample(
                        self.name + f"-{constants.noise}-{t}",
                        dist.Normal(0.0, 1.0).expand((self.size,)),
                    )
                    t -= self.t0  # shift back for indexing
                    path[:, t] = (
                        path[:, t - 1]
                        + dt[:, t] * loc[:, t]
                        + scale[:, t] * this_noise * dt[:, t].sqrt()
                    )
            else:
                noise = pyro.sample(
                    self.name + f"-{constants.noise}",
                    dist.Normal(0.0, 1.0).expand((self.size, self.t1 - self.t0)),
                )
                path = ic.unsqueeze(-1) + (loc * dt + scale * dt.sqrt() * noise).cumsum(
                    dim=-1
                )

            path = pyro.deterministic(self.name + "-" + constants.generated, path)
        return path

    def __repr__(
        self,
    ):
        string = f"CCSDE({getattr(self, constants.loc)}, {getattr(self, constants.scale)}, {getattr(self, constants.dt)}, {getattr(self, constants.ic)})"
        return core._add_fns_to_repr(self, string)


class GlobalTrend(core.Block):
    """
    ```
    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        alpha=None,
        beta=None,
    ):
    ```

    A global (linear) trend dgp.

    The generative model for this process is

    $$
    z_t = \\alpha + \\beta t,
    $$

    for $t = t_0, ..., t_1$. Here, $\\alpha$ is the dgp for the intercept parameter
    and $\\beta$ is the dgp for the slope parameter. These processes may be other `Block`s,
    `torch.tensor`s, or `pyro.distributions` objects, and the interpretation of
    $\\alpha$ and $\\beta$ will change accordingly.

    *Args:*

    + `alpha (Block || torch.tensor || pyro.distributions)`: intercept parameter
    + `beta (Block || torch.tensor || pyro.distributions)`: slope parameter

    See `Block` for definitions of other parameters.
    """

    _function_addresses = {constants.alpha, constants.beta}

    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        alpha=None,
        beta=None,
    ):
        super().__init__(
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )

        setattr(self, constants.alpha, alpha or dist.Normal(0.0, 1.0).expand((size,)))
        setattr(self, constants.beta, beta or dist.Normal(0.0, 1.0).expand((size,)))
        self._maybe_add_blocks(
            getattr(self, constants.alpha), getattr(self, constants.beta)
        )

    def _model(
        self,
        size=1,
    ):
        alpha = core._obj_name_to_definite(self, constants.alpha)
        beta = core._obj_name_to_definite(self, constants.beta)

        with autoname.scope(prefix=constants.dynamic):
            t = torch.linspace(self.t0, self.t1, self.t1 - self.t0)
            path = pyro.deterministic(
                self.name + "-" + constants.generated, alpha + t * beta
            )
        return path


class SmoothSeasonal(core.Block):
    """
    ```
    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        phase=None,
        amplitude=None,
        lengthscale=None,
        cycles=1,
    ):
    ```

    A smooth seasonal block.

    The generative model for this process is

    $$
    z_t = \mathrm{amplitude}_t\
    \cos\left(\mathrm{phase}_t + \\frac{2\pi\ \mathrm{cycles}\ t}{\mathrm{lengthscale}_t}\\right)
    $$

    for $t = t_0, ..., t_1$. Here, $\mathrm{amplitude}$ is the dgp for the amplitude,
    $\mathrm{phase}$ is the dgp for the phase, and
    $\mathrm{lengthscale}$ is the parameter for the lengthscale.
    These processes may be other `Block`s,
    `torch.tensor`s, or `pyro.distributions` objects, and the interpretation of
    these parameters will change accordingly.

    This block is experimental and may be removed in a future release.

    *Args:*

    + `phase (Block || torch.tensor || pyro.distributions)`: phase of the sinusoidal functionn
    + `amplitude (Block || torch.tensor || pyro.distributions)`: amplitude of the siusoidal function
    + `lengthscale (Block || torch.tensor || pyro.distributions)`: lengthscale of the sinusoidal function;
        corresponds to $L$ in $A \cos(\\varphi + 2\pi n t / L)$s
    + `cycles (int)`: number of cycles of ths sinusoidal to complete over the interval
        $[0, L)$

    See `Block` for definitions of other parameters.
    """

    _function_addresses = {constants.phase, constants.amplitude, constants.lengthscale}

    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        phase=None,
        amplitude=None,
        lengthscale=None,
        cycles=1,
    ):
        super().__init__(
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )
        setattr(self, constants.phase, phase or dist.Normal(0.0, 1.0).expand((size,)))
        setattr(
            self,
            constants.amplitude,
            amplitude or dist.LogNormal(3.0, 1.0).expand((size,)),
        )
        setattr(
            self,
            constants.lengthscale,
            lengthscale or dist.LogNormal(5.0, 2.0).expand((size,)),
        )
        self._maybe_add_blocks(
            getattr(self, constants.phase),
            getattr(self, constants.amplitude),
            getattr(self, constants.lengthscale),
        )
        assert type(cycles) is int
        self.cycles = cycles

    def _model(
        self,
    ):
        phase, amplitude, lengthscale = core.name_to_definite(
            self, constants.phase, constants.amplitude, constants.lengthscale
        )
        with autoname.scope(prefix=constants.dynamic):
            t = torch.linspace(self.t0, self.t1, self.t1 - self.t0)
            path = pyro.deterministic(
                self.name + "-" + constants.generated,
                amplitude
                * (phase + 2 * torch.pi * self.cycles * t / lengthscale).cos(),
            )
        return path


class AR1(core.Block):
    """
    ```
    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        alpha=None,
        beta=None,
        scale=None,
    ):
    ```

    An autoregressive block of order 1.

    The data generating process for this block is

    $$
    z_t = \\alpha_t + \\beta_t z_{t-1} + \mathrm{scale}_t w_t,
    $$

    for $t = t_0,...,t_1$ and $w_t \sim \\text{Normal}(0, 1)$.
    Here, $\\alpha$ is the dgp for the intercept parameter,
    $\\beta$ is the dgp for the slope parameter, and $\mathrm{scale}$ is the dgp for the
    scale parameter. These processes may be other `Block`s,
    `torch.tensor`s, or `pyro.distributions` objects, and the interpretation of
    these parameters will change accordingly.

    *Args*:

    + `alpha (Block || torch.Tensor || pyro.distributions)`: the intercept parameter
    + `beta (Block || torch.Tensor || pyro.distributions)`: the slope parameter
    + `scale (Block || torch.Tensor || pyro.distributions)`: the noise scale parameter

    See `Block` for definitions of other parameters.
    """

    _function_addresses = {constants.alpha, constants.beta, constants.scale}

    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        alpha=None,
        beta=None,
        scale=None,
        ic=None,
    ):
        super().__init__(
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )
        setattr(self, constants.alpha, alpha or dist.Normal(0.0, 1.0).expand((size,)))
        setattr(self, constants.beta, beta or dist.Uniform(0.0, 1.0).expand((size,)))
        setattr(
            self, constants.scale, scale or dist.LogNormal(0.0, 1.0).expand((size,))
        )
        setattr(self, constants.ic, ic or dist.Normal(0.0, 1, 0).expand((size,)))
        self._maybe_add_blocks(
            getattr(self, constants.alpha),
            getattr(self, constants.beta),
            getattr(self, constants.scale),
        )

    def _model(self, fast=False):
        alpha, beta, scale = core.name_to_definite(
            self, constants.alpha, constants.beta, constants.scale
        )
        ic = core._obj_name_to_definite(self, constants.ic, flag_on_block=True)
        with autoname.scope(prefix=constants.dynamic):
            if not fast:
                path = torch.empty((self.size, self.t1 - self.t0))
                last_x = ic
                path[:, 0] = last_x
                for t in range(self.t0 + 1, self.t1):
                    t_ix = t - self.t0
                    x = pyro.sample(
                        f"{self.name}-{constants.noise}-{t}",
                        dist.Normal(
                            alpha[:, t_ix] + beta[:, t_ix] * last_x, scale[:, t_ix]
                        ).expand((self.size,)),
                    )
                    path[:, t_ix] = x
                    last_x = x
            else:
                return self._model(fast=False)
            path = pyro.deterministic(f"{self.name}-{constants.generated}", path)
        return path


class MA1(core.Block):
    """
    ```
    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        beta=None,
        loc=None,
        scale=None,
    ):
    ```

    A moving average block of order 1.

    The data generating process for this block is

    $$
    z_t = \mathrm{loc}_t + \mathrm{scale}_t w_t + \\beta_t \mathrm{scale}_{t - 1} w_{t-1},
    $$

    for $t = t_0,...,t_1$ and $w_t \sim \\text{Normal}(0, 1)$.
    Here, $\mathrm{loc}$ is the dgp for the location parameter,
    $\mathrm{scale}$ is the dgp for the scale parameter, and $\\beta$ is the dgp for the
    FIR filter. These processes may be other `Block`s,
    `torch.tensor`s, or `pyro.distributions` objects, and the interpretation of
    these parameters will change accordingly.


    **NOTE**: from the definition of the dgp, $\mathrm{scale}$ has dimensionality
    $(N, t_1 - t_0 + 1)$, where the $+1$ is due to the lagged noise term on the $t = t_0$
    value.

    *Args*:

    + `beta (Block || torch.Tensor || pyro.distributions)`: the FIR filter parameter
    + `loc (Block || torch.Tensor || pyro.distributions)`: the location parameter
    + `scale (Block || torch.Tensor || pyro.distributions)`: the noise scale parameter.
        Note that, if `scale` subclasses `Block`, it must have time dimensionality one higher
        than this block

    See `Block` for definitions of other parameters.
    """

    _function_addresses = {constants.beta, constants.loc, constants.scale}

    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        beta=None,
        loc=None,
        scale=None,
    ):
        super().__init__(
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )
        setattr(self, constants.beta, beta or dist.LogNormal(0.0, 1.0).expand((size,)))
        setattr(self, constants.loc, loc or dist.Normal(0.0, 1.0).expand((size,)))
        setattr(
            self, constants.scale, scale or dist.LogNormal(0.0, 1.0).expand((size,))
        )
        self._maybe_add_blocks(
            getattr(self, constants.beta),
            getattr(self, constants.loc),
            getattr(self, constants.scale),
        )
        self.has_fast_mode = True

    def _model(
        self,
        fast=False,
    ):
        beta, loc = core.name_to_definite(self, constants.beta, constants.loc)
        self.t0 -= 1
        (scale,) = core.name_to_definite(self, constants.scale)
        self.t0 += 1
        with autoname.scope(prefix=constants.dynamic):
            if not fast:
                path = torch.empty((self.size, self.t1 - self.t0))
                last_noise = pyro.sample(
                    f"{self.name}-{constants.noise}-m1",
                    dist.Normal(0.0, scale[..., 0]),  # kludge
                )
                for t in range(self.t0, self.t1):
                    t_ix = t - self.t0
                    this_noise = pyro.sample(
                        f"{self.name}-{constants.noise}-{t}",
                        dist.Normal(0.0, scale[..., t_ix]),
                    )
                    this_value = (
                        loc[..., t_ix] + this_noise + beta[..., t_ix] * last_noise
                    )
                    path[:, t_ix] = this_value
                    last_noise = this_noise
            else:
                noise = pyro.sample(
                    f"{self.name}-{constants.noise}",
                    dist.Normal(0.0, 1.0).expand((self.size, self.t1 - self.t0 + 1)),
                )
                noise *= scale
                path = loc + noise[..., 1:] + beta * noise[..., :-1]
            path = pyro.deterministic(f"{self.name}-{constants.generated}", path)
        return path


class DiscreteSeasonal(core.Block):
    """
    ```
    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        n_seasons=2,
        seasons=None,
    ):
    ```

    A discrete seasonal block that represents the most basic form of discrete seasonality.

    The data generating process for this block is

    $$
    z_t = \\theta_{t \mod s},\ s = 1,...,S,
    $$

    where $S$ is the total number of seasons and $\\theta = (\\theta_1,...,\\theta_S)$ are the
    seasonality components. Currently, $\\theta$ can be only a `pyro.distributions` instance or a
    `torch.Tensor`, though that might change in a future release.

    *Args:*

    + `n_seasons (int)`: number of discrete seasons
    + `seasons (pyro.distributions || torch.Tensor)`: season values

    See `Block` for definitions of other parameters.
    """

    def __init__(
        self,
        name=None,
        t0=0,
        t1=2,
        size=1,
        n_seasons=2,
        seasons=None,
    ):
        super().__init__(
            name=name,
            t0=t0,
            t1=t1,
            size=size,
        )
        assert n_seasons >= 2
        self.n_seasons = n_seasons
        setattr(
            self,
            constants.seasons,
            seasons
            or dist.Normal(0.0, 1.0).expand(
                (
                    size,
                    n_seasons,
                )
            ),
        )
        self._maybe_add_blocks(getattr(self, constants.seasons))

    def _model(
        self,
    ):
        seasons = core._obj_name_to_definite(self, constants.seasons, season=True)
        t = torch.linspace(self.t0, self.t1, self.t1 - self.t0)
        which_seasons = torch.remainder(t, self.n_seasons)
        these_seasons = seasons[..., which_seasons.type(torch.LongTensor)]
        with autoname.scope(prefix=constants.dynamic):
            path = pyro.deterministic(
                f"{self.name}-{constants.generated}", these_seasons
            )
        return path
