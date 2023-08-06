import math 

class Factor():

    def __init__(self, i, N):
        self.i = i
        self.N = N

    def P_GIVEN_F(self):
        ''' Calculate the present worth factor given the present amount.
                                  (P/F,i%,N)
        Args:
            None

        Return: P given F factor (P/F,i%,N) '''

        return ((1+self.i)**(-(self.N)))

    def F_GIVEN_A(self):#       
        ''' Calculate the future worth factor given the annual amount.
                                  (F/A,i%,N)
        Args:
            None

        Return: F given A factor (F/A,i%,N) '''
      
        return ((1+self.i)**self.N - 1)/self.i    

    def P_GIVEN_A(self):#
        ''' Calculate the present worth factor given the annual amount.
                                  (P/A,i%,N)
        Args:
            None

        Return: P given A factor (P/A,i%,N) '''

        return ((1 + self.i)**self.N - 1)/(self.i*(1+self.i)**self.N)

    def P_GIVEN_G(self):#
        ''' Calculate the present value factor of a uniform gradient series.
                                  (P/G,i%,N)
        Args:
            None

        Return: P given G factor (P/G,i%,N) '''

        return (1/self.i)*((((1+self.i)**self.N -1)/(self.i*(1+self.i)**self.N))-(self.N/(1+self.i)**self.N))   

    def A_GIVEN_G(self):
        ''' Calculate the annual value factor of a uniform gradient series.
                                  (A/G,i%,N)
        Args:
            None

        Return: A given G factor (A/G,i%,N) '''

        return (1/self.i)-(self.N/((1+self.i)**self.N - 1))     