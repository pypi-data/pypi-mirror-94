import copy
from typing import Iterator

import torch
from torch import nn


def exponential_moving_average_(base: torch.Tensor,
                                update: torch.Tensor,
                                momentum: float) -> torch.Tensor:
    """ Inplace exponential moving average of `base` tensor

    :param base: tensor to be updated
    :param update: tensor for updating
    :param momentum:
    :return: exponential-moving-averaged `base` tensor
    """

    return base.mul_(momentum).add_(update, alpha=1 - momentum)


class EMA(nn.Module):
    """ Exponential moving average of a given model. ::

    model = EMA(original_model, 0.99999)

    """

    def __init__(self,
                 original_model: nn.Module,
                 momentum: float = 0.999):
        super().__init__()
        if not (0 <= momentum <= 1):
            raise ValueError(f"Invalid momentum: {momentum}")
        self.momentum = momentum

        self._original_model = original_model
        self._ema_model = copy.deepcopy(original_model)
        for p in self._ema_model.parameters():
            p.requires_grad_(False)

    @property
    def original_model(self) -> nn.Module:
        return self._original_model

    @property
    def ema_model(self) -> nn.Module:
        return self._ema_model

    def parameters(self, recurse: bool = True) -> Iterator[nn.Parameter]:
        # this makes it simple, but may incur unexpected behavior
        return self._original_model.parameters(recurse)

    def requires_grad_(self, requires_grad: bool = True):
        return self._original_model.requires_grad_(requires_grad)

    @torch.no_grad()
    def _update(self):
        # _foreach_** is n times faster than for loops
        o_p = [p.data for p in self._original_model.parameters() if isinstance(p, torch.Tensor)]
        e_p = [p.data for p in self._ema_model.parameters() if isinstance(p, torch.Tensor)]
        torch._foreach_mul_(e_p, self.momentum)
        torch._foreach_add_(e_p, o_p, alpha=1 - self.momentum)

        # some buffers are integer for counting etc.
        o_b = [b for b in self._original_model.buffers() if isinstance(b, torch.Tensor) and torch.is_floating_point(b)]
        if len(o_b) > 0:
            e_b = [b for b in self._ema_model.buffers() if isinstance(b, torch.Tensor) and torch.is_floating_point(b)]
            torch._foreach_mul_(e_b, self.momentum)
            torch._foreach_add_(e_b, o_b, alpha=1 - self.momentum)

    def forward(self, *args, **kwargs):
        if self.training:
            self._update()
            return self._original_model(*args, **kwargs)
        return self._ema_model(*args, **kwargs)

    def __repr__(self):
        s = f"EMA(beta={self.momentum},\n"
        s += f"  {self._original_model}\n"
        s += ")"
        return s
