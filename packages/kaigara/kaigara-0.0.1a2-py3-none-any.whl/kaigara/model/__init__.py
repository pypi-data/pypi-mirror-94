"""
The :mod:`kaigara.model` module implements a variety of theoretical morphological models of molluscan shells.
"""

from ._raup_model import RaupModelSimulator, RaupModelEqns

__all__ = ['RaupModelEqns',
           'RaupModelSimulator']