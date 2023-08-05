""" Helper functions to make distributed training easy
"""

import builtins
import os as python_os
import warnings
from functools import wraps
from typing import Callable, Optional

from torch import distributed
from torch.cuda import device_count

from homura.liblog import get_logger
from .environment import get_args, get_environ

logger = get_logger("homura.distributed")
original_print = builtins.print


def is_horovod_available() -> bool:
    warnings.warn("horovod is no longer supported by homura", DeprecationWarning)
    return False


def is_distributed_available() -> bool:
    return distributed.is_available()


def is_distributed() -> bool:
    """ Check if the process is distributed by checking the world size is larger than 1.
    """

    return get_world_size() > 1


def get_local_rank() -> int:
    """ Get the local rank of the process, i.e., the process number of the node.
    """

    return int(get_environ('LOCAL_RANK', 0))


def get_global_rank() -> int:
    """ Get the global rank of the process. 0 if the process is the master.
    """

    return int(get_environ('RANK', 0))


def is_master() -> bool:
    return get_global_rank() == 0


def get_num_nodes() -> int:
    """ Get the number of nodes. Note that this function assumes all nodes have the same number of processes.
    """

    if not is_distributed():
        return 1
    else:
        return get_world_size() // device_count()


def get_world_size() -> int:
    """ Get the world size, i.e., the total number of processes.
    """

    return int(python_os.environ.get("WORLD_SIZE", 1))


def _print_if_master(self, *args, sep=' ', end='\n', file=None) -> None:
    if is_master():
        original_print(self, *args, sep=sep, end=end, file=file)


def distributed_print(self, *args, sep=' ', end='\n', file=None) -> None:
    """ print something on any node
    """
    if is_distributed():
        self = f"[rank={get_global_rank()}] {self}"
    original_print(self, *args, sep=sep, end=end, file=file)


def init_distributed(use_horovod: bool = False,
                     backend: Optional[str] = None,
                     init_method: Optional[str] = None,
                     disable_distributed_print: str = False
                     ) -> None:
    """ Simple initializer for distributed training. This function substitutes print function with `_print_if_master`.

    :param use_horovod: If use horovod as distributed backend
    :param backend: backend of torch.distributed.init_process_group
    :param init_method: init_method of torch.distributed.init_process_group
    :param disable_distributed_print:
    :return: None
    """

    if not is_distributed_available():
        raise RuntimeError('Distributed training is not available on this machine')

    if use_horovod:
        raise DeprecationWarning("horovod is no longer supported by homura")

    # default values
    backend = backend or "nccl"
    init_method = init_method or "env://"

    if not is_distributed():
        raise RuntimeError(f"For distributed training, use `python -m torch.distributed.launch "
                           f"--nproc_per_node={device_count()} {get_args()}` ...")

    if not distributed.is_initialized():
        distributed.init_process_group(backend=backend, init_method=init_method)
    logger.info("Distributed initialized")

    if not disable_distributed_print:
        builtins.print = _print_if_master


def if_is_master(func: Callable
                 ) -> Callable:
    """ Wraps void functions that are active only if it is the master process::

    @if_is_master
    def print_master(message):
        print(message)

    :param func: Any function
    """

    @wraps(func)
    def inner(*args, **kwargs) -> None:
        if is_master():
            return func(*args, **kwargs)

    return inner
