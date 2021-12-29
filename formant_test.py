from utils import *
import matplotlib.pyplot as plt

Signal = []



F1 = 100
F2 = 200
F3 = 1000
S1 = []
S2 = []
S3 = []
Fe = 16000
somme = []

for t in range(1000):
    S1.append(np.sin(2 * np.pi * F1 * (t / Fe)))
    S2.append(np.sin(2 * np.pi * F2 * (t / Fe)))
    S3.append(np.sin(2 * np.pi * F3 * (t / Fe)))

print("f1 = " + str(formant(S1, Fe)))
print("f2 = " + str(formant(S2, Fe)))
print("f3 = " + str(formant(S3, Fe)))


plt.plot(formant(S1, Fe), "o")
plt.show()
plt.plot(formant(S2, Fe),"o")
plt.show()
plt.plot(formant(S3, Fe),"o")
plt.show()