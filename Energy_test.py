
from utils import *

#test que des valeurs positive ou nulle 
SignalA = [0, 1, 2, 3, 4, 5]
if (signalenergy(SignalA)==55):
    print("Good")
else: print("Error")

#test avec des valeurs négatives et les floats
SignalB = [0, -1, -2, -3, 4.2, -5]
if (signalenergy(SignalB)==56.64):
    print("Good")
else: print("Error")

#test avec que des valeurs nulles 
SignalC = [0, 0, 0, 0, 0]
if (signalenergy(SignalC)==0):
    print("Good")
else: print("Error")


Signal = [0, -1, -2, -3, -4, -5, 6, 7, 8]
energysignal= signalenergy(Signal)

def testenergy(energysignal):
    
    for value in range(energysignal):
        if(value<0):
            return "Error"
            break
    return "Tout est bon"

print(testenergy(energysignal))