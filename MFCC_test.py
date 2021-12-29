import numpy as np
import scipy.signal as signal
from utils import *
import matplotlib.pyplot as plt

F1 = 100
F2 = 500
F3 = 1000
S1 = []
S2 = []
S3 = []
Somme = []
Fe = 16000 

for t in range(1000):
    S1.append(np.sin(2*np.pi*F1*(t/Fe)))
    S2.append(np.sin(2*np.pi*F2*(t/Fe)))
    S3.append(np.sin(2*np.pi*F3*(t/Fe)))

l = MFCC(S1,Fe)
   
print("f1 = ",l)
#print("f2 = "+str(MFCC(s2,fe)))
#print("f3 = "+str(MFCC(s3,fe)))