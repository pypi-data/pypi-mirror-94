"""Raup's model"""

# Author: Koji Noshita <noshita@morphometrics.jp>
# License: ISC

import numbers

import numpy as np
import sympy as sym

from ..base import GeneratingCurveModel, SimulatorMixin, EqnsMixin

class RaupModelSimulator(GeneratingCurveModel, SimulatorMixin):
    def __init__(self, W = 10**0.2, T = 1.5, D = 0.1, S = 1, r0 = 1):
        self.W = W
        self.T = T
        self.D = D
        self.S = S
        self.r0 = r0
        
    @property
    def W(self):
        return self.__W
    
    @W.setter
    def W(self,W):
        if W > 1:
            self.__W = W
        else:
            raise ValueError("W > 1")
            
    @property
    def T(self):
        return self.__T
    
    @T.setter
    def T(self,T):
        if isinstance(T, numbers.Real):
            self.__T = T
        else:
            raise ValueError("-inf < T < inf")
       
    @property
    def D(self):
        return self.__D
    
    @D.setter
    def D(self,D):
        if -1 < D:
            self.__D = D
        else:
            raise ValueError("-1 < D")
            
    @property
    def S(self):
        return self.__S
    
    @S.setter
    def S(self,S):
        if isinstance(S, numbers.Real):
            self.__S = S
        else:
            raise ValueError("-inf < S < inf")
    
    @property
    def r0(self):
        return self.__r0
    
    @r0.setter
    def r0(self,r0):
        if r0 > 0:
            self.__r0 = r0
        else:
            raise ValueError("0 < r0")
        
    def _generate_generating_spiral(self, theta: float):
        
        W = self.W
        T = self.T
        D = self.D
        r0 = self.r0
        
        w = r0*W**(theta/(2*np.pi))
        px = w * (2*D/(1 - D) + 1 )*np.cos(theta)
        py = w * (2*D/(1 - D) + 1 )*np.sin(theta)
        pz = w * 2*T*(D/(1 - D) + 1)
        
        return px, py, pz
    
    def compute_generating_spiral(self, theta: float):
        return self._generate_generating_spiral(theta)
            
    def compute(self, theta: float, phi: float):
        """
        
        """

        W = self.W
        T = self.T
        D = self.D
        S = self.S
        r0 = self.r0

        w = r0*W**(theta/(2*np.pi))
        
        X = w * (2*D/(1 - D) + 1 + np.cos(phi))*np.cos(theta)
        Y = w * (2*D/(1 - D) + 1 + np.cos(phi))*np.sin(theta)
        Z = w * (2*T*(D/(1 - D) + 1) + np.sin(phi)/S)
        
        return X, Y, Z

class RaupModelEqns(GeneratingCurveModel, EqnsMixin):
    def __init__(self, 
                 W = sym.Symbol("W"), T = sym.Symbol("T"), D = sym.Symbol("D"), S = sym.Symbol("S"), 
                 r0 = sym.Symbol("r_0"), theta = sym.Symbol("theta"), phi = sym.Symbol("phi")):
        self.W = W
        self.T = T
        self.D = D
        self.S = S
        self.r0 = r0
        self.theta = theta
        self.phi = phi
        
        self.__definition = self._define(W = self.W, T = self.T , D = self.D, S = self.S,
                                          r0 = self.r0, theta = self.theta, phi = self.phi)
        
    def _generate_generating_spiral(self, **params):
        W = params.get("W") if params.get("W") else self.W
        T = params.get("T") if params.get("T") else self.T
        D = params.get("D") if params.get("D") else self.D
        r0 = params.get("r0") if params.get("r0") else self.r0
        theta = params.get("theta") if params.get("theta") else self.theta
        
        w = W**(theta/(2*sym.pi))
        denom = -1+D
        eqns = sym.Matrix([
            -((1+D)*r0*w*sym.cos(theta))/denom,
            -((1+D)*r0*w*sym.sin(theta))/denom,
            (2*r0*T*w)/denom
        ])
        return eqns
    
    def calculate_generating_spiral(self, **params):
        """
        Args:
        """
        return self._generate_generating_spiral(**params)
    
    @property
    def definition(self):
        return self.__definition
    
    def _define(self, **params):
        W = self.W
        T = self.T
        D = self.D
        S = self.S
        r0 = self.r0
        theta = self.theta
        phi = self.phi
        
        u = sym.Function("u")
        
        definition = sym.Eq(u(theta, phi),
                            sym.UnevaluatedExpr(r0) * sym.UnevaluatedExpr(W**(theta/(2*sym.pi)))* sym.UnevaluatedExpr(
                                sym.Matrix(
                                    [
                                        [sym.cos(theta), -sym.sin(theta), 0], 
                                        [sym.sin(theta), sym.cos(theta), 0], 
                                        [0, 0, 1]
                                    ])) * (
                                sym.UnevaluatedExpr(sym.Matrix(
                                    [ sym.cos(phi), 0, sym.UnevaluatedExpr(sym.UnevaluatedExpr(1/S)*sym.sin(phi))]
                                )) 
                                + sym.UnevaluatedExpr(
                                    sym.Matrix([2*D/(1-D)+1, 0, 2*T*(D/(1-D)+1)])
                                )
                            )
                           )
        return definition
    
#     def solve(self, **params):

#         sol = self._define(**params)

#         return sol
    
    def to_tex(self, simplified = False):
        """
        
        """
        return sym.latex(self.calculate())  