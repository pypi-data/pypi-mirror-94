"""Base classes for all models"""

# Author: Koji Noshita <noshita@morphometrics.jp>
# License: ISC

from abc import ABCMeta, abstractmethod

from . import __version__

##
## Theoretical morphological models
##

class BaseModel(metaclass=ABCMeta):
#     @abstractmethod
    def set_params(self):
        pass

#     @abstractmethod
    def get_params(self):
        pass
    
class GeneratingCurveModel(BaseModel):
    """Base class for all generating curve models in kaigara."""
    
    @abstractmethod
    def _generate_generating_spiral(self):
        """
        Call this function via `compute_generating_spiral` (in `Simulator`) 
        or `calculate_generating_spiral` (in `Eqns`).
        """
        pass
    
##
## Mixins
##

class SimulatorMixin:
    """Mixin class for all simulators in kaigara."""
    @abstractmethod
    def compute(self):
        pass

class EqnsMixin:
    """Mixin class for all equations in kaigara."""
    
    @property
    @abstractmethod
    def definition(self):
        """
        """
        pass
    
#     @abstractmethod
#     def solve(self):
#         pass
    
    @abstractmethod
    def to_tex(self):
        pass
