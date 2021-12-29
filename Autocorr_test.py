
from utils import *


F1 = 100
F2 = 200
F3 = 300
S1 = []
S2 = []
S3 = []
Fe = 16000 
somme = []

for t in range(800):
    S1.append(np.sin(2*np.pi*F1*(t/Fe)))
    S2.append(np.sin(2*np.pi*F2*(t/Fe)))
    S3.append(np.sin(2*np.pi*F3*(t/Fe)))
   
print("F1 = "+str(Autocorr(S1,Fe,100)))
print("F2 = "+str(Autocorr(S2,Fe,100)))
print("F3 = "+str(Autocorr(S3,Fe,100)))
