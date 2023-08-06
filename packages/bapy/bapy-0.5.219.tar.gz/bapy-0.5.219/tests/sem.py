#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module."""
import enum
import inspect
from typing import Union

from bapy import Sem, ic, Path


class Log(enum.Enum):
    A: Union[int, enum.auto] = enum.auto()

#
# def pr():
#     ic(Sem.init())
#
#     ic(Sem.asdict())
#     ic(Sem.attrs())
#     ic(Sem.default_attr())
#     ic(Sem.default_dict())
#     ic(Sem.default_value())
#     ic(Sem.values())
#     for item in Sem:
#         ic(item.describe, item.status)
#     ic(Sem.ATLAS.sem, type(Sem.ATLAS.sem))
#
#     (Path.cwd() / '.env').write_text(f'BAPY_{Sem.default_attr()}=10')
#
#     ic(Sem.asdict())
#     ic(Sem.attrs())
#     ic(Sem.default_attr())
#     ic(Sem.default_dict())
#     ic(Sem.default_value())
#     ic(Sem.values())
#     for item in Sem:
#         ic(item.describe, item.status)
#
# pr()
#
# from bapy import path
#
# pr()
# __all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]
