import abc

import torch
import pyro

from . import util


def _effect_call(obj, fn):
    """Turns an effect handler defined as a context manager into a callable.

    *Args:*

    `obj (Effect)`: an effect

    `fn (callable)`: a callable
    """

    def wrapper(*args, **kwargs):
        obj.__enter__()
        result = fn(*args, **kwargs)
        obj.__exit__(None, None, None)  # NOTE: useless traceback etc.
        return result

    return wrapper


def _forecast_on(obj, Nt):
    """Fast-forwards a Block-like object from sample to forecast mode.

    This does two things:

    1. `t0 -> t1`
    2. `t1 -> t1 + Nt`

    *Args:*

    + `obj (Block)`: the block to forecast
    + `Nt (int)`: the number of timesteps to forecast
    """
    setattr(obj, "t0", obj.t1 + 1)
    setattr(obj, "t1", obj.t1 + Nt + 1)


def _forecast_off(
    obj,
    t0,
    t1,
):
    """Reverses a Block-like object from forecast to sample mode.

    This does two things:

    1. `t1 -> t0`
    2. `t0 -> old t0`

    *Args:*

    + `obj (Block)`: the block to forecast
    + `t0 (int)`: the original initial time
    + `t1 (int)`: the original final time
    """

    setattr(obj, "t0", t0)
    setattr(obj, "t1", t1)


class Effect(abc.ABC):
    """A context manager that changes the interpretation of an STS call."""

    def __init__(self, *args, **kwargs):
        ...

    def __call__(self, fn):
        return _effect_call(self, fn)


class ForecastEffect(Effect):
    """Effect handler for forecasting tasks.

    From start to finish, the forecast operation consists of

    + turning off caching
    + fast-forwarding time
    + (possibly) intervening on all free parameters
    + calling sample
    + (possibly) reverting free parameter values
    + reversing time
    + resuming caching

    *Args:*

    + `root (block)`: the root of the STS graph
    + `Nt (int)`: number of timesteps to forecast
    + `design_tensors (Dict[str, torch.Tensor])`:
    """

    def __init__(self, root, Nt=1, design_tensors=dict()):
        self.root = root
        self.Nt = Nt
        self.design_tensors = design_tensors

        self.nodes = util.get_nodes_from_root(self.root)
        self.t0s = list()
        self.t1s = list()
        self.fms = list()
        self.datas = dict()
        self.Xs = dict()

    def __enter__(
        self,
    ):
        for node in self.nodes:
            self.t0s.append(node.t0)
            self.t1s.append(node.t1)
            self.fms.append(node._has_fast_mode)

            # handle observations
            if hasattr(node, "data"):
                self.datas[node.name] = node.data
                node.data = None
            if hasattr(node, "X"):
                self.Xs[node.name] = node.X
                node.X = self.design_tensors[node.name]

            _forecast_on(node, self.Nt)
            node._has_fast_mode = False
        util.set_cache_mode(
            self.root, False
        )  # TODO: is this correct? NOTE no, it's not

    def __exit__(self, type, value, traceback):
        for node, t0, t1, fm in zip(self.nodes, self.t0s, self.t1s, self.fms):
            _forecast_off(
                node,
                t0,
                t1,
            )
            node._has_fast_mode = fm

            # handle observations
            if hasattr(node, "data"):
                node.data = self.datas[node.name]
            if hasattr(node, "X"):
                node.X = self.Xs[node.name]

        util.set_cache_mode(self.root, True)
