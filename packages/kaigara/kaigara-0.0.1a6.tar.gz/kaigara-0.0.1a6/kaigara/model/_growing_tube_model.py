"""Growing Tube model"""

# Author: Koji Noshita <noshita@morphometrics.jp>
# License: ISC

import numbers

import numpy as np
import sympy as sym

from scipy.spatial.transform import Rotation

from ..base import GeneratingCurveModel, SimulatorMixin, EqnsMixin

class GrowingTubeModelSimulator(GeneratingCurveModel, SimulatorMixin):
    def __init__(self, E = 0.02, C = 0.4, T = 0.06, 
                 r0 = 1, p0 = np.zeros(3), R0 = np.diag(np.ones(3))
                ):
        
        self.E = E
        self.C = C
        self.T = T
        self.r0 = r0
        self.p0 = p0
        self.R0 = R0
        
    def __normalize(self, vec):
        norm = np.linalg.norm(vec)
        return vec/norm
    
    @property
    def E(self):
        return self.__E
    
    @property
    def E_Okamoto1988(self):
        return self.__E_Okamoto1988
    
    @E.setter
    def E(self, E):
        if isinstance(E, numbers.Real) or np.all(np.isfinite(E)):
            self.__E = E
            self.__E_Okamoto1988 = np.exp(E)
        else:
            raise ValueError("-inf < E < inf")
            
    @E_Okamoto1988.setter
    def E_Okamoto1988(self, E_Okamoto1988):
        if isinstance(E, numbers.Real) or np.all(E > 0):
            self.__E = np.log(E_Okamoto1988)
            self.__E_Okamoto1988 = E_Okamoto1988
        else:
            raise ValueError("-inf < E < inf")
   
    @property
    def C(self):
        return self.__C
    
    @C.setter
    def C(self, C):
        if isinstance(C, numbers.Real) or np.all(np.isfinite(C)):
            self.__C = C
        else:
            raise ValueError("-inf < C < inf")
            
    @property
    def T(self):
        return self.__T
    
    @T.setter
    def T(self, T):
        if isinstance(T, numbers.Real) or np.all(np.isfinite(T)):
            self.__T = T
        else:
            raise ValueError("-inf < T < inf")
     
    @property
    def r0(self):
        return self.__r0
    
    @r0.setter
    def r0(self, r0):
        if r0 > 0:
            self.__r0 = r0
        else:
            raise ValueError("r0 > 0")
    
    @property
    def R0(self):
        return self.__R0
    
    @R0.setter
    def R0(self, R0):
        R0_arr = np.array(R0)
        
        if np.array_equal(np.linalg.inv(R0_arr), R0_arr.transpose()) & (np.linalg.det(R0_arr) == 1):
            self.__R0 = R0
        else:
            raise ValueError("R0 is a rotation matrix.")
            
    def _generate_generating_spiral(self, s):
        
        E_g = self.E
        C_g = self.C
        T_g = self.T
        r0 = self.r0
        p0 = self.p0
        R0 = self.R0
        
        
        r = r0*np.exp(E_g*s)
        D = np.sqrt(C_g**2+T_g**2)
        
        ED3E2pD2 = E_g*D**3*(E_g**2 + D**2)
        expEs = np.exp(E_g*s)
        sinDs = np.sin(D*s)
        cosDs = np.cos(D*s)
    

        P = r0*D*(((D**2) * (T_g**2) + (E_g**2) * (T_g**2) + C_g**2 * E_g**2 * cosDs 
                   + E_g*D*(C_g**2)*sinDs)*expEs - D**2 * (E_g**2 + T_g**2))/ED3E2pD2
        Q = r0*C_g*D*E_g*(-expEs*(C_g**2 + T_g**2)*cosDs 
                          + D*(D + expEs*E_g*sinDs))/ED3E2pD2
        R = r0*C_g*T_g*D*(((E_g**2) + (D**2) - (E_g**2) * cosDs - E_g*D*sinDs)*expEs - D**2)/ED3E2pD2

        

        px, py, pz = np.transpose(p0 + np.transpose(np.dot(R0, np.array([P, Q, R]))))
        
        return px, py, pz



    def compute(self, s, phi):
        
        E_g = self.E
        C_g = self.C
        T_g = self.T
        r0 = self.r0
        R0 = self.R0
        delta_g = 0
        gamma_g = 0
        px, py, pz = self._generate_generating_spiral(s)
        
        r = r0*np.exp(E_g*s)
        D = np.sqrt(C_g**2+T_g**2)
        
        ED3E2pD2 = E_g*D**3*(E_g**2 + D**2)
        expEs = np.exp(E_g*s)
        sinDs = np.sin(D*s)
        cosDs = np.cos(D*s)
        
        ##
        ## Generating Curve
        ##
        xi1 = np.dot(
            R0,
            np.array([(T_g**2 + C_g**2*cosDs)/D**2, C_g*sinDs/D, C_g*T_g*(1 - cosDs)/D**2])
        ).transpose()
        xi2 = np.dot(
            R0,
            np.array([(-C_g*sinDs/D), cosDs, T_g*sinDs/D])
        ).transpose()
        xi3 = np.dot(
            R0,
            np.array([(C_g*T_g*(1 - cosDs))/D**2, (-T_g*sinDs)/D, (C_g**2+T_g**2*cosDs)/D**2])
        ).transpose()

        xi1 = np.apply_along_axis(self.__normalize, 1, xi1)
        xi2 = np.apply_along_axis(self.__normalize, 1, xi2)
        xi3 = np.apply_along_axis(self.__normalize, 1, xi3)

        rot2 = Rotation.from_rotvec(delta_g*xi2).as_matrix()
        rot3 = Rotation.from_rotvec(gamma_g*xi3).as_matrix()
        rot_g = np.array([np.dot(rot3[i], rot2[i]) for i in range(len(rot2))])

        xi1_i  = np.array([self.__normalize(np.dot(rot_g[i], xi1[i])) for i in range(len(xi1))])
        xi2_i  = np.array([self.__normalize(np.dot(rot_g[i], xi2[i])) for i in range(len(xi2))])
        xi3_i  = np.array([self.__normalize(np.dot(rot_g[i], xi3[i])) for i in range(len(xi3))])

        xi1_i = np.apply_along_axis(self.__normalize, 1, xi1_i)
        xi2_i = np.apply_along_axis(self.__normalize, 1, xi2_i)
        xi3_i = np.apply_along_axis(self.__normalize, 1, xi3_i)

        gencurves = []
        for i in range(len(xi1_i)):
            rot1i = Rotation.from_rotvec(np.tensordot(phi, xi1_i[i],axes=0)).as_matrix()
            gencurve = [r[i]*np.dot(rot1i[j], xi2_i[i]) for j in range(len(rot1i))]
            gencurves.append(gencurve)

        gencurves = np.array(gencurves)

        ##
        ## Surface
        ## 
        X, Y, Z = np.array([np.array([px, py, pz]).transpose()[i] + gencurves[i] for i in range(len(gencurves))]).transpose()

        return(X.transpose(), Y.transpose(), Z.transpose())
    
    
    
    
class GrowingTubeModelEqns(GeneratingCurveModel, EqnsMixin):
    def __init__(self, 
                 E = sym.Function("E")(sym.Symbol("s")), 
                 C = sym.Function("C")(sym.Symbol("s")), 
                 T = sym.Function("T")(sym.Symbol("s")), 
                 r0 = sym.Symbol("r_0"), 
                 p0 = sym.Matrix.zeros(3), R0 = sym.Matrix.diag([1,1,1], unpack=True), 
                 s = sym.Symbol("s"), phi = sym.Symbol("phi")):
        
        self.E = E
        self.C = C
        self.T = T
        self.r0 = r0
        self.p0 = p0
        self.R0 = R0
        self.s = s
        self.phi = phi
        
        self.r = sym.Function("r")
        
        xi1 = sym.Function("xi_1")
        xi2 = sym.Function("xi_2")
        xi3 = sym.Function("xi_3")
        self.Xi = sym.Lambda(s, sym.Matrix([xi1(s), xi2(s), xi3(s)]))
        
    @property
    def E(self):
        return self.__E
    
    @E.setter
    def E(self, E):
        self.__E = E
        
    @property
    def C(self):
        return self.__C
    
    @C.setter
    def C(self, C):
        self.__C = C
            
    @property
    def T(self):
        return self.__T
    
    @T.setter
    def T(self, T):
        self.__T = T
     
    @property
    def r0(self):
        return self.__r0
    
    @r0.setter
    def r0(self, r0):
        self.__r0 = r0
        
    @property
    def p0(self):
        return self.__p0
    
    @r0.setter
    def p0(self, p0):
        self.__p0 = p0
    
        
    @property
    def R0(self):
        return self.__R0
    
    @R0.setter
    def R0(self, R0):
        self.__R0 = R0
    
    def _generate_generating_spiral(self, **params):
        E = self.E
        C = self.C
        T = self.T
        r0 = self.r0
        p0 = self.p0
        R0 = self.R0
        s = self.s
        
        r = r0*sym.exp(E*s)
        D = sym.sqrt(C**2+T**2)

        ED3E2pD2 = E*D**3 * (E**2 + D**2)
        expEs = sym.exp(E_g*s)
        sinDs = sym.sin(D*s)
        cosDs = stm.cos(D*s)

        ##
        ## Growth Trajectory
        ##
        P = r0*D*(((D**2) * (T**2) + (E**2) * (T**2) + C**2 * E**2 * cosDs 
                   + E*D*(C**2)*sinDs)*expEs - D**2 * (E**2 + T**2))/ED3E2pD2
        Q = r0*C*D*E_g*(-expEs*(C**2 + T**2)*cosDs 
                          + D*(D + expEs*E*sinDs))/ED3E2pD2
        R = r0*C*T*D*(((E**2) + (D**2) - (E**2) * cosDs - E*D*sinDs)*expEs - D**2)/ED3E2pD2

        p = sym.Lambda(s,p0 + R0*sym.Matrix([P, Q, R]))
        
        return p
        
    def calculate_generating_spiral(self, **params):
        """
        Args:
        """
        return self._generate_generating_spiral(**params)
        
    def _define(self):
        
        E = self.E
        C = self.C
        T = self.T
        r0 = self.r0
        p0 = self.p0
        R0 = self.R0
        s = self.s
        Xi = self.Xi
        
        #
        # Tube growth
        #
        eq_tb = sym.Eq(sym.Derivative(self.r(s), s), E*self.r(s))
        
        #
        # Frenet-Serret formulas
        #
        
        FSCoef = sym.Matrix([[0, C,0],
                             [-C, 0, T],
                             [0, -T,0]])

        eq_fsf_l = sym.Derivative(sym.UnevaluatedExpr(Xi(s)),s)
        eq_fsf_r = sym.UnevaluatedExpr(FSCoef)*sym.UnevaluatedExpr(Xi(s))
        
        return {"tube growth": eq_tb, 
                "Frenet-Serret formulas": sym.Eq(eq_fsf_l, eq_fsf_r)}
        
    @property
    def definition(self):
        
        return self._define()