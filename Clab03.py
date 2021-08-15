import cv2
from random import randint
import random

class clab03():

    def __init__(self):
        self.length = 1000000
        self.b1 = self.wichmanhill(1000000)
        self.b2 = self.lfsr(1000000, '11001001', (8, 7, 6, 1))
        self.b3 = self.LCG(612, 5115, 7212)
        self.m1 = self.LCG(6, 55, 11)
        self.m2 = self.LCG(6, 55, 37)
        self.m3 = self.LCG(6, 55, 150)
        self.good = [self.b1, self.b2, self.b3]
        self.bad = [self.m1, self.m2, self.m3]

    def lfsr(self,lonFinal, seed, taps):
        # Resultado y sr con la semilla inicial
        res = ''
        sr = seed

        # Se acaba el ciclo cuando se llegue a la long requerida
        while len(res) < lonFinal:
            xor = 0

            # Hacemos xor con cada num en taps
            for t in taps:
                xor ^= int(sr[t-1]) 
            res += str(xor)
            
            # Contateno el xor al inicio de la cadena
            # y elimino uno de la cadena anterior
            sr = str(xor) + sr[:-1]

        return res

    def wichmanhill(self,size):
        
        k = ''
        a = 1
        b = 30000
        # Se generan los 3 numeros
        s1, s2, s3 = [randint(a, b) for _ in range(3)]
        for _ in range(size):
            s1 = (171*s1) % 30269
            s2 = (172*s2) % 30307
            s3 = (170*s3) % 30323
            v = ((s1/30269.0) + (s2/30307.0) + (s3/30323.0)) % 1  # Se genera el numero
            k += str(round(v))  # Se agrega el
        return k

    def xor(self,x1, xp):
        size = len(x1)
        if (size != len(xp)):
            return
        xored = ''
        # Ahora se hace la operacion xor
        for i in range(size):
            xored += '0' if x1[i] == xp[i] else '1'
        return xored

    def LCG(self,a, b, N):
        # a ≡ b(mod N)
        bitChain = '' 
        t = 16 # Binary concatenation cycle size
        k = 8 # Individual bitChain size
        size = 128992

        try:
            parse = list(map(int,[a, b, N])) # Parsing Verification
            a = parse[0]
            b = parse[1]
            N = parse[2]
        except:
            return "Something went wrong"
        
        x = random.randrange(200)%N # Randomized initial value

        for i in range(int(size/t)): 
            x = (a*x + b)%N 
            binary = bin(x).replace('b','').zfill(t)
            bitChain += binary

        return bitChain


