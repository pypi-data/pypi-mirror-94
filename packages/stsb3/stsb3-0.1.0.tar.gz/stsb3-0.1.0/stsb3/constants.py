import torch


torch.pi = torch.acos(torch.zeros(1)).item() * 2


APPLY_FUNCS = {
    "log": torch.log,
    "exp": torch.exp,
    "tanh": torch.tanh,
    "invtanh": torch.atanh,
    "invlogit": lambda x: 1.0 / (1.0 + torch.exp(-1.0 * x)),
    "logit": lambda x: torch.log(x / (1.0 - x)),
    "floor": torch.floor,
    "sin": torch.sin,
    "cos": torch.cos,
    "softplus": lambda x, limit=30.0: torch.where(
        x < limit,
        torch.log1p(torch.exp(-torch.abs(x))) + torch.max(x, torch.zeros(1)),
        x,
    ),
    "diff": lambda x: x[..., 1:] - x[..., :-1],
    "logdiff": lambda x: torch.log(x[..., 1:]) - torch.log(x[..., :-1]),
}

APPLY_FUNC_NAMES = {v: k for k, v in APPLY_FUNCS.items()}


# address components
# for convenience, these are built-in
# users can add them with setattr(constants, "thing", value)
# this would all be much easier in julia
dynamic = "dynamic"
ic = "ic"
generated = "generated"
obs = "obs"
loc = "loc"
scale = "scale"
noise = "noise"
dt = "dt"
alpha = "alpha"
beta = "beta"
plate = "plate"
period = "period"
phase = "phase"
amplitude = "amplitude"
likelihood = "likelihood"
lengthscale = "lengthscale"
seasons = "seasons"

inf = float("inf")
neg_inf = -1.0 * inf
real = (neg_inf, inf)
half_line = (0, inf)
zero_one = (0, 1)
DOMAINS = {real, half_line, zero_one}

expand = "expand"
domain = "domain"

ADDRESS_COMPONENT_PROPERTIES = {
    dynamic: {expand: False},
    ic: {expand: True, domain: real},
    generated: {expand: False},
    obs: {expand: False},
    loc: {expand: True, domain: real},
    scale: {expand: True, domain: half_line},
    noise: {expand: False},
    dt: {expand: True, domain: half_line},
    alpha: {expand: True, domain: real},
    beta: {expand: True, domain: real},
    plate: {expand: False},
    period: {expand: True, domain: half_line},
    phase: {expand: True, domain: real},
    amplitude: {expand: True, domain: half_line},
    likelihood: {expand: False},
    lengthscale: {expand: True, domain: half_line},
    seasons: {expand: True, domain: real},
}
