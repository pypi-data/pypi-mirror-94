import abc
import collections

import torch
import pyro
import pyro.distributions as dist
from pyro.contrib import autoname

from . import constants
from . import effects
from . import util
from . import exceptions


def redefine(
    block,
    attribute,
    obj,
):
    """
    ```
    def redefine(
        block,
        attribute,
        obj,
    ):
    ```

    Redefines an attribute of a block to the passed object

    *Args:*

    + `block (Block)`
    + `attribute (str)`
    + `obj (Block || torch.tensor || pyro.distributions)`
    """
    assert hasattr(block, attribute)
    block._maybe_remove_blocks(getattr(block, attribute))
    setattr(block, attribute, obj)
    block._maybe_add_blocks(getattr(block, attribute))


def register_address_component(
    name,
    expand,
    domain=None,
):
    """
    ```
    def register_address_component(
        name,
        expand,
        domain=None,
    ):
    ```

    Registers a new functional address component and metadata.

    Addresses in `stsb3` look like `x/y-z` or `y-z`, where `x` is a context coomponent,
    `y` is the name of the rv, and `z` describes its function. `register_address_component`
    allows for runtime definition of `z` address components for use in new blocks or
    structure search algorithms.

    *Args:*

    + `name (str)`: the name. E.g., already-defined names include `loc`, `scale`, and `amplitude`
    + `expand (bool)`: whether objects whose address contains this component can be expanded using
        `Block`s
    + `domain (None || tuple)`: if `expand`, must be a tuple in `constants.DOMAINS` (i.e.,
        one of `(-inf, inf)`, `(0, inf)`, or `(0, 1)`)

    This function is *not* safe -- if `name` already exists in `constants`, this will overwrite
    its definition and properties.
    """
    assert domain in constants.DOMAINS or not expand
    setattr(constants, name, name)
    constants.ADDRESS_COMPONENT_PROPERTIES[name] = {
        constants.expand: expand,
        constants.domain: domain,
    }


def _is_pyro_dist(obj):
    return "pyro.distributions" in str(type(obj))


def _make_id(obj, name):
    if not name:
        curr_num = type(obj).num
        type(obj).num += 1
        return str(type(obj)) + str(curr_num)
    return name


def _make_2d(obj, size, t0, t1):
    if type(obj) is float:
        obj = torch.tensor([obj]).view((-1, 1))
    else:
        obj = obj.view((-1, 1))
    obj = obj * torch.ones((size, t1 - t0))
    return obj


def _add_fns_to_repr(obj, string):
    if obj.apply_funcs != list():
        for fn in obj.apply_funcs:
            string = f"{constants.APPLY_FUNC_NAMES[fn]}({string})"
    return string


def _apply_fns(obj, draws):
    for fn in obj.apply_funcs:
        draws = fn(draws)
    return draws


def _leaf_arg_error(name, obj):
    string = f"{name} must subclass Block, be a pyro.distributions"
    string += (
        f" object, or be a torch.tensor, but instead got type({name}) = {type(obj)}"
    )
    return string


def _noblock_leaf_arg_error(name, obj):
    string = f"{name} must be a pyro.distributions"
    string += (
        f" object, or be a torch.tensor, but instead got type({name}) = {type(obj)}"
    )
    return string


def _is_block(obj):
    return issubclass(type(obj), Block)


def _obj_name_to_definite(
    obj, name, flag_on_block=False, likelihood=False, season=False
):
    # TODO: multimethods?
    if season:
        return _obj_name_to_definite_season(obj, name)
    elif flag_on_block:
        return _obj_name_to_definite_fob(obj, name)
    elif likelihood:
        return _obj_name_to_definite_likelihood(obj, name)

    attr = getattr(obj, name)
    partial_address = getattr(constants, name)

    if _is_pyro_dist(attr):
        sample_statment = pyro.sample(
            obj.name + "-" + partial_address,
            attr,
        )
        definite = _make_2d(sample_statment, obj.size, obj.t0, obj.t1)
    elif type(attr) is torch.Tensor:
        definite = _make_2d(attr, obj.size, obj.t0, obj.t1)
    elif _is_block(attr):
        definite = attr.model()
    else:
        raise ValueError(_leaf_arg_error(partial_address, attr))

    return definite


def _obj_name_to_definite_season(obj, name):
    attr = getattr(obj, name)
    partial_address = getattr(constants, name)
    if _is_pyro_dist(attr):
        definite = pyro.sample(
            obj.name + "-" + partial_address,
            attr,
        )
    elif type(attr) is torch.Tensor:
        definite = attr
    else:
        raise AttributeError("Currently seasons must be a tensor or pyro dist")
    return definite


def _obj_name_to_definite_likelihood(obj, name):
    attr = getattr(obj, name)
    partial_address = getattr(constants, name)

    if _is_pyro_dist(attr):
        with autoname.scope(prefix=constants.likelihood):
            sample_statment = pyro.sample(
                obj.name + "-" + partial_address,
                attr,
            )
        definite = sample_statment.unsqueeze(-1)
    elif type(attr) is torch.Tensor:
        definite = attr * torch.ones((obj.size, 1))
    elif _is_block(attr):
        definite = attr.model()
    else:
        raise ValueError(_leaf_arg_error(partial_address, attr))

    return definite


def _obj_name_to_definite_fob(obj, name):
    attr = getattr(obj, name)
    partial_address = getattr(constants, name)

    if _is_pyro_dist(attr):
        definite = pyro.sample(
            obj.name + "-" + partial_address,
            attr,
        )
    elif type(attr) is torch.Tensor:
        definite = attr
    else:
        raise ValueError(_noblock_leaf_arg_error(partial_address, attr))

    return definite


def forecast(dgp, samples, *args, Nt=1, nsamples=1, design_tensors=dict(), **kwargs):
    """
    ```
    def forecast(dgp, samples, *args, Nt=1, nsamples=1, **kwargs):
    ```

    Forecasts the root node of the DGP forward in time.

    *Args:*

    + `dgp (Block)`: the root node to forecast forward
    + `samples (dict)`: `{semantic site name: value}` The value tensors should have shape
        `(m, n, T)`, where `m` is the number of samples, `n` is the batch size, and `T` is the
        length of the time series
    + `*args`: any additional positional arguments to pass to `dgp.model`
    + `Nt (int):` number of timesteps for which to generate forecast. Forecast is generated from
        `t1 + 1` to `t1 + 1 + Nt`.
    + `nsamples (int)`: number of samples to draw from the forecast distribution
    + `design_tensors (Dict[str, torch.Tensor])`:
    + `**kwargs`: any additional keyword arguments to pass to `dgp.model`
    """
    # iterate through the dict, conditioning as necessary
    draws = list()
    forecast_effect = effects.ForecastEffect(dgp, Nt=Nt, design_tensors=design_tensors)
    # NOTE: ignores CI portion of graph, causing key errors below
    # TODO: should this behavior be changed?
    name2block = util.get_name2block_from_root(dgp)

    with forecast_effect:
        stem2var_val = _forecast_setattrs(0, samples, name2block, init=True)
        draws.append(dgp.model(*args, **kwargs))
        for n in range(1, nsamples):
            # n = n % max possible length
            _forecast_setattrs(n, samples, name2block)
            draws.append(dgp.model(*args, **kwargs))
    _forecast_replaceattrs(name2block, stem2var_val)
    return torch.stack(draws)


def _forecast_setattrs(n, samples, name2block, init=False):
    if init:
        stem2var_val = collections.defaultdict(list)

    for name in samples.keys():
        # deal with the initial conditions
        if "-" + constants.ic in name:
            # get the -generated value with this as its ic
            stem = name.split("-" + constants.ic)[0]
            # NOTE: silences key errors from CI portion of graph
            # TODO: is this desired behavior
            if stem in name2block.keys():
                if init:
                    stem2var_val[stem].append(
                        (constants.ic, getattr(name2block[stem], constants.ic))
                    )
                gen_key = constants.dynamic + "/" + stem + "-" + constants.generated
                value = samples[gen_key][n, :, -1].detach()
                setattr(name2block[stem], constants.ic, value)
        # deal with the dynamic random variables
        elif _forecast_is_marginalized_var(name):
            continue
        # everything else
        else:
            stem, variable = name.split("-")
            # NOTE: silences key errors from CI portion of graph
            # TODO: is this desired behavior
            if stem in name2block.keys():
                if init:
                    stem2var_val[stem].append(
                        (variable, getattr(name2block[stem], variable))
                    )
                value = samples[name].squeeze()[n].detach()
                setattr(name2block[stem], variable, value)
    if init:
        return stem2var_val


def _forecast_replaceattrs(name2block, stem2var_val):
    for stem, to_set in stem2var_val.items():
        block = name2block[stem]
        for (variable, orig_value) in to_set:
            setattr(block, variable, orig_value)


def _forecast_is_marginalized_var(name):
    c1 = constants.dynamic + "/" in name
    c2 = constants.likelihood + "/" in name
    c3 = constants.obs in name
    return any(
        (
            c1,
            c2,
            c3,
        )
    )


def _is_observable_block(block):
    return hasattr(block, "data")


def _generic_init(self, init_fn, name=None, t0=0, t1=2, size=1, **kwargs):
    """
    ```
    def _generic_init(self, init_fn, name=None, t0=0, t1=2, size=1, **kwargs)
    ```

    Generic portion of init function for dynamically-created blocks

    *Args*:

    + `init_fn (callable)`: defines the implementation-specific portion of the
        constructor

    For other argument documentation, see `Block`
    """
    Block.__init__(
        self,
        name=name,
        t0=t0,
        t1=t1,
        size=size,
    )
    init_fn(self, **kwargs)


def _closure_init(init_fn):
    """
    ```
    def closure_init(init_fn):
    ```

    Generates a complete constructor given only the implementation-specific
    portion
    """
    return lambda self, **kwargs: _generic_init(self, init_fn, **kwargs)


def construct_init(fn_addr_param):
    """
    ```
    def construct_init(fn_addr_param):
    ```

    Constructs an implementation-specific constructor given a parameter
        specification dictionary.

    *Args:*

    + `fn_addr_params (dict)`: `{function_address: parameters}`.
        parameters` is a `dict` with structure

        ```
            {
                "expand": bool,
                "domain": domain defined in constants,
                "default": Block || torch.tensor || pyro.distributions
            }
        ```
    """
    for fn_addr, params in fn_addr_param.items():
        if not hasattr(constants, fn_addr):
            register_address_component(fn_addr, params["expand"], params["domain"])

    def _init_fn(self, **kwargs):
        for fn_addr in fn_addr_param.keys():
            if fn_addr not in kwargs.keys():
                kwargs[fn_addr] = None
        for k, v in kwargs.items():
            setattr(self, k, v or fn_addr_param[k]["default"])
            self._maybe_add_blocks(getattr(self, k))

    return _init_fn


def name_to_definite(
    skeleton,
    *names,
):
    """
    ```
    def name_to_definite(skeleton, *names,):
    ```

    Makes the names associated with the block skeleton into `torch.tensor`s
        according to the skeleton's current interpretation.

    *Args:*

    + `skeleton (Block-like)`: an incompletely-constructed block. The block will be
        incompletely constructed because the definition of this method is part of
        the block's definition.
    + `*names (List[str])`: names to make definite

    *Returns:*

    + `tuple` of `torch.tensor` corresponding to the passed names.
    """
    return tuple(
        _obj_name_to_definite(skeleton, getattr(constants, name)) for name in names
    )


class Block(abc.ABC):
    """Base class that all STS blocks should subclass.

    Defines a number of useful modeling constructs and methods, such as
        deterministic transformations.
    """

    num = 0

    def __init__(self, name=None, t0=0, t1=2, size=1, is_cached=False, *args, **kwargs):
        self.name = _make_id(self, name)
        self.t0 = t0
        self.t1 = t1
        self.size = size

        self.apply_funcs = list()
        self._prec = list()
        self._succ = list()

        # replay / memoization
        self.is_cached = is_cached
        self.cache = None

        # speeding up inference if possible
        # it is always safe to assume a block does not have fast mode
        self.has_fast_mode = False

    @property
    def has_fast_mode(
        self,
    ):
        return self._has_fast_mode

    @has_fast_mode.setter
    def has_fast_mode(self, mode):
        assert (
            type(mode) is bool
        ), f"type(mode) must be bool, but you passed {type(mode)}"
        self._has_fast_mode = mode

    def model(self, *args, **kwargs):
        """
        ```
        def model(self, *args, **kwargs):
        ```

        Draws a batch of samples from the block.

        *Args:*

        + `args`: optional positional arguments
        + `kwargs`: optional keyword arguments

        *Returns:*

        + `draws` (torch.tensor) sampled values from the block
        """
        if self.is_cached:
            if self.cache is None:
                if self.has_fast_mode:
                    draws = self._model(*args, fast=self.has_fast_mode, **kwargs)
                else:
                    draws = self._model(*args, **kwargs)
                self.cache = draws  # cache in untransformed space
                result = _apply_fns(self, draws)
            else:
                result = _apply_fns(self, self.cache)
        else:
            if self.has_fast_mode:
                result = _apply_fns(
                    self, self._model(*args, fast=self.has_fast_mode, **kwargs)
                )
            else:
                result = _apply_fns(self, self._model(*args, **kwargs))
        return result

    def _maybe_add_blocks(self, *args):
        """
        ```
        def _maybe_add_blocks(self, *args):
        ```

        Adds parameters to prec and succ if they subclass Block.

        *Args:*

        + `args`: iterable of (name, parameter, bound)
        """
        for arg in args:
            if _is_block(arg):
                if arg not in self._prec:
                    self._prec.append(arg)
                if arg not in self._succ:
                    arg._succ.append(self)

    def _maybe_remove_blocks(self, *args):
        for arg in args:
            if _is_block(arg):
                if arg in self._prec:
                    self._prec.remove(arg)
                if arg in self._succ:
                    arg._succ.remove(self)

    def clear_cache(
        self,
    ):
        """Clears the block cache.

        This method does *not* alter the cache mode.
        """
        self.cache = None

    @abc.abstractmethod
    def _model(self, *args, **kwargs):
        ...

    def __add__(self, right):
        assert _is_block(right)
        return AddBlock(self, right)

    def __radd__(self, left):
        assert left == 0, "Don't directly sum numbers with Blocks!"
        return self

    def __iadd__(self, right):
        assert _is_block(right)
        return AddBlock(self, right)

    def __mul__(self, right):
        assert _is_block(right)
        return MultiplyBlock(self, right)

    def __imul__(self, right):
        assert _is_block(right)
        return MultiplyBlock(self, right)

    def __len__(
        self,
    ):
        return self.t1 - self.t0

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

    def _transform(self, arg, *args):
        """Defines a transform from a string argument.

        Currently the following string arguments are supported:

        + exp
        + log
        + logit
        + invlogit
        + tanh
        + arctanh
        + invlogit
        + logit
        + floor
        + sin
        + cos
        + softplus
        + diff (lowers time dimemsion by 1)
        + logdiff (lowers time dimension by 1)

        The resulting transform will be added to the transform stack iff
        it is not already at the top of the stack.

        *Args:*

        + `arg (str)`: one of the above strings corresponding to function

        *Returns:*

        `self (stsb.Block)`
        """
        func = constants.APPLY_FUNCS[arg]
        if func in self.apply_funcs:
            if func != self.apply_funcs[-1]:
                self.apply_funcs.append(func)
        else:
            self.apply_funcs.append(func)
        return self

    def log(self):
        """`x -> log x`

        Block paths must be positive for valid output.
        """
        return self._transform("log")

    def exp(self):
        """`x -> exp(x)`"""
        return self._transform("exp")

    def tanh(self):
        """`x -> tanh(x)`, i.e. `x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))`"""
        return self._transform("tanh")

    def arctanh(self):
        """`x -> arctanh(x)`, i.e. `x -> 0.5 log ((1 + x) / (1 - x))`"""
        return self._transform("arctanh")

    def invlogit(self):
        """`x -> 1 / (1 + exp(-x))`"""
        return self._transform("invlogit")

    def logit(self):
        """`x -> log(x / (1 - x))`"""
        return self._transform("logit")

    def floor(self):
        """`x -> x - [[x]]`, where `[[.]]` is the fractional part operator"""
        return self._transform("floor")

    def sin(self):
        """`x -> sin x`"""
        return self._transform("sin")

    def cos(self):
        """`x -> cos x`"""
        return self._transform("cos")

    def softplus(self):
        """`x -> log(1 + exp(x))`"""
        return self._transform("softplus")

    def diff(self):
        """`x -> x[1:] - x[:-1]`

        Note that this lowers the time dimension from T to T - 1.
        """
        return self._transform("diff")

    def logdiff(self):
        """`x -> log x[1:] - log x[:-1]`

        Note that this lowers the time dimension from T to T - 1.
        """
        return self._transform("logdiff")

    def prec(self):
        """Returns the predecessor nodes of `self` in the (implicit) compute graph

        *Returns:*

        `_prec (list)`: list of predecessor nodes
        """
        return self._prec

    def succ(self):
        """Returns the successor nodes of `self` in the (implicit) compute graph

        *Returns:*

        `_succ (list)`: list of successor nodes
        """
        return self._succ


class AddBlock(Block):
    """Represents the result of adding two blocks toogether.

    `.model(...)` is computed as `x ~ p(x); y ~ p(y); x + y`

    *Args:*

    + `left (Block)`
    + `right (Block)`
    """

    def __init__(self, left, right, *args, **kwargs):
        name = f"Add({left.name}, {right.name})"
        super().__init__(name=name, *args, **kwargs)
        self.left = left
        self.right = right

        self._maybe_add_blocks(
            self.left,
            self.right,
        )

    def _model(self, *args, **kwargs):
        left = self.left.model(*args, **kwargs)
        right = self.right.model(*args, **kwargs)
        with autoname.scope(prefix=constants.dynamic):
            added = pyro.deterministic(
                self.name + f"-" + constants.generated, left + right
            )
        return added

    def __repr__(
        self,
    ):
        string = f"Add({self.left}, {self.right})"
        return _add_fns_to_repr(self, string)


class MultiplyBlock(Block):
    """Represents the result of multiplying two blocks toogether.

    `.model(...)` is computed as `x ~ p(x); y ~ p(y); x * y`

    *Args:*

    + `left (Block)`
    + `right (Block)`
    """

    def __init__(self, left, right, *args, **kwargs):
        name = f"Multiply({left.name}, {right.name})"
        super().__init__(name=name, *args, **kwargs)
        self.left = left
        self.right = right

        self._maybe_add_blocks(
            self.left,
            self.right,
        )

    def _model(self, *args, **kwargs):
        left = self.left.model(*args, **kwargs)
        right = self.right.model(*args, **kwargs)
        with autoname.scope(prefix=constants.dynamic):
            added = pyro.deterministic(
                self.name + f"-" + constants.generated, left * right
            )
        return added

    def __repr__(
        self,
    ):
        string = f"Multiply({self.left}, {self.right})"
        return _add_fns_to_repr(self, string)


class NoiseBlock(Block):
    """Base class for all likelihood function-type blocks

    Implements a number of inference wrappers to Pyro implementations.

    *Args:*

    + `dgp (Block)`: the latent data-generating process for which `self` serves as a
        likelihood function
    + `data (None || torch.tensor)`: the observed data. If `data is None`, then using the
        noise block is equivalent to drawing from the prior of a state space model
    + `name (None || str)`: a unique name of the block. If `name is None`, a unique name will be
        automatically generated

    For other argument documentation, see `Block`
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
        super().__init__(name=name, t0=t0, t1=t1)
        self.dgp = dgp
        self.data = data
        self._maybe_add_blocks(dgp)

        self.guide = None
        self.mcmc = None
        self.posterior = False

    def fit(self, method="advi", method_kwargs=dict(), verbosity=0.01):
        """
        ```
        def fit(self, method="nf_block_ar", method_kwargs=dict(), verbosity=0.01):
        ```

        Fits a guide (variational posterior) to the model.

        Wraps multiple Pyro implementations of variational inference. To minimize noise
            in the estimation you should follow the Pyro guidelines about marginalizing
            out discrete latent rvs, etc.

        *Args:*

        + `method (str)`: one of "advi", "low_rank", or "nf_block_ar".
            + `"advi"`: fits a diagonal normal distribution in unconstrained latent space
            + `"low_rank"`: fits a low-rank multivariate normal in unconstrained latent space.
                Unlike the diagonal normal, this guide can capture some nonlocal dependence in
                latent rvs.
            + `"nf_block_ar"`: fits a normalizing flow block autoregressive neural density estimator
                in unconstrained latent space. This method uses two stacked block autoregressive NNs.
                See [the Pyro docs](http://docs.pyro.ai/en/stable/distributions.html#pyro.distributions.transforms.BlockAutoregressive)
                for more details about this.
        + `method_kwargs (dict)`: optional keyword arguments to pass to Pyro's inference capabilities. If no
            keyword arguments are specified, sane defaults will be passed instead. Some arguments could include:
            + `"niter"`: number of iterations to run optimization (default `1000`)
            + `"lr"`: the learning rate (default `0.01`)
            + `"loss"`: the loss function to use (default `"Trace_ELBO"`)
            + `"optim"`: the optimizer to use (default `"AdamW"`)
        + `verbosity (float)`: status messages are printed every `int(1.0 / verbosity)` iterations
        """
        if method == "advi":
            if method_kwargs == dict():
                method_kwargs = {
                    "niter": 1000,
                    "lr": 0.01,
                    "loss": "Trace_ELBO",
                    "optim": "AdamW",
                }
            self._fit_autoguide(
                pyro.infer.autoguide.AutoDiagonalNormal(self.model),
                **method_kwargs,
                verbosity=verbosity,
            )
        elif method == "low_rank":
            if method_kwargs == dict():
                method_kwargs = {
                    "niter": 1000,
                    "lr": 0.01,
                    "loss": "Trace_ELBO",
                    "optim": "AdamW",
                }
            self._fit_autoguide(
                pyro.infer.autoguide.AutoLowRankMultivariateNormal(self.model),
                **method_kwargs,
                verbosity=verbosity,
            )
        elif method == "nf_block_ar":

            def transform_init(*args, **kwargs):
                return dist.transforms.iterated(
                    2,
                    dist.transforms.block_autoregressive,
                    *args,
                    **kwargs,
                )

            guide = pyro.infer.autoguide.AutoNormalizingFlow(
                self.model,
                transform_init,
            )
            if method_kwargs == dict():
                method_kwargs = {
                    "niter": 1000,
                    "lr": 0.01,
                    "loss": "Trace_ELBO",
                    "optim": "AdamW",
                }
            self._fit_autoguide(
                guide,
                **method_kwargs,
                verbosity=verbosity,
            )
        else:
            raise NotImplementedError(exceptions._fit_method_exception_msg(method))

    def _fit_autoguide(
        self,
        guide,
        niter=1000,
        lr=0.005,
        loss="Trace_ELBO",
        optim="Adam",
        verbosity=0.01,
    ):
        self.posterior = True
        verbosity = int(1.0 / verbosity)
        optim = getattr(pyro.optim, optim)({"lr": lr})
        loss = getattr(pyro.infer, loss)()
        svi = pyro.infer.SVI(self.model, guide, optim, loss=loss)

        ###
        pyro.clear_param_store()
        ###

        for i in range(niter):
            loss = svi.step() / self.data.shape[-1]

            if i % verbosity == 0:
                print(f"On iteration {i}, loss = {loss}")

        self.guide = guide

    def sample(
        self,
        nsamples=100,
        thin=0.1,
        burnin=500,
    ):
        """
        ```
        def sample(
            self,
            nsamples=100,
            thin=0.1,
            burnin=500,
        ):
        ```

        Sample from the model's posterior using the Pyro implementation of the No-U Turn Sampler

        This could take a *very long time* for long time series. It is recommended to use `.fit(...)`
            instead.

        *Args:*

        + `nsamples (int)`: number of desired samples *after burn in and thinning*
        + `thin (float)`: every `int(1.0 / thin)` sample is kept
        + `burnin (int)`: `samples[burnin:]` are kept
        """
        self.posterior = True
        total_to_sample = int(1.0 / thin) * nsamples + burnin
        kernel = pyro.infer.NUTS(self.model)
        mcmc = pyro.infer.MCMC(kernel, num_samples=total_to_sample)
        mcmc.run()
        self.mcmc = mcmc

    def prior_predictive(
        self,
        nsamples=1,
    ):
        """
        ```
        def prior_predictive(
            self,
            nsamples=1,
        ):
        ```

        Draws from the prior predictive distribution of the graph with `self` as the root

        *Args:*

        + `nsamples (int)`: number of samples to draw

        *Returns:*

        `samples (torch.tensor)`
        """
        if self.posterior:
            raise ValueError(
                "Model already fit / sampled, call .posterior_predictive(...) instead"
            )
        old_data = self.data
        self.data = None
        prior = pyro.infer.Predictive(self.model, num_samples=nsamples)
        samples = prior()
        self.data = old_data
        return samples

    def posterior_predictive(
        self,
        nsamples=1,
    ):
        """
        ```
        def posterior_predictive(
            self,
            nsamples=1,
        ):
        ```

        Draws from the posterior predictive distribution of the graph with `self` as the root

        *Args:*

        + `nsamples (int)`: number of samples to draw

        *Returns:*

        `samples (torch.tensor)`
        """
        if not self.posterior:
            raise ValueError(
                "Model not fit / sampled, call .prior_predictive(...) instead"
            )
        old_data = self.data
        self.data = None
        if self.mcmc is not None:
            posterior = pyro.infer.Predictive(
                self.model,
                posterior_samples=self.mcmc.get_samples(),
                num_samples=nsamples,
            )
        elif self.guide is not None:
            posterior = pyro.infer.Predictive(
                self.model, guide=self.guide, num_samples=nsamples
            )
        samples = posterior()
        self.data = old_data
        return samples
