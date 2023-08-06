from .commonfactors import Factor

class BondValue(Factor):

    def __init__(self, i, N, Z, r):

        self.Z = Z
        self.r = r
        super().__init__(i,N)

    def bond_value(self):
        ''' Calculate the bond value based on interest rate, matureness period,
            face value, and bond rate .
                                  
        Args:
            None

        Return: bond value (float) '''    

        Z = self.Z
        r = self.r
        return  Z*super().P_GIVEN_F() + r*Z*super().P_GIVEN_A()   

       