from scikit_talkbox_lpc import lpc_ref
from xcorr import *
from filterbanks import *
import scipy.signal as signal
import matplotlib.pyplot as plt


# ************************ PRE PROCESSING ************************
#1.1
# l'objectif de la normalisation est de réduire le vecteur signal pour que chaque donnée soit représenté comme un pourcentage
# de la plus grande(petite) valeur (pour ca qu'on aura un vecteur entre -1 et 1)
#voir dans la fonction main le test

def normalisation(signal):

   # on met tous les éléments du tableau en valeur absolue pour avoir plus facilement accès à la valeur la plus grande
   abs_signal = np.abs(signal)


   #on trouve la valeur la plus grande
   max = np.max(abs_signal)

   #on divise chaque valeur par le max (pour ainsi avoir un pourcentage)
   normalized_signal = signal/max

   return normalized_signal

#1.2
#def split(width,step,Fe,signal):

#return 0


def split(Signal, Fe, Tss, Tw):
   # Ici, on commence par poser les conditions qui permettront d'éviter les cas "illogiques"
   if (Tw == 0):

      print("la largeur de la fenêtre est : 0")
      return 0

   elif (Tw == Tss == 0):

      print("la largeur de la fenêtre est : 0 et le saut est : 0")
      return 0

      # Ici, on spécifie le cas du chevauchement
   elif (Tw > Tss):

      print(" On risque d'avoir un recouvrement ")
      return 0

   if (Fe == 0):
      print("la fréquence d'échantillonage est inexistante")
      return 0

   # (On passe au domaine discret)
   Fe = int(Fe / 1000)
   Nss = Tss * Fe  # Pour les steps
   Nw = Tw * Fe  # Pour les frames

   Frameslist = []  # Liste pour les différentes frames
   SamplesFrames = []  # Liste d'échantillons d'une frame à la fois

   SampleDiff = Nss - Nw  # Nombre d'échantillons séparant une frame et sa suivante
   i = 0  # Indice de l'échantillon
   temp = Nw  # Valeur tampon pour ne pas modifier Nw

   while i < len(Signal):  # On parcoure tous les échantillons du signal

      # Chaque loop crée une fenêtre

      if (
              i != 0 and i % temp == 0):  # Echantillon différent du premier et échantillon correspond au dernier d'une fenêtre
         Frameslist.append(SamplesFrames)  # On rajoute une nouvelle fenêtre à la liste
         SamplesFrames = []  # On vide la liste d'échantillons pour commencer une nouvelle fenêtre
         i += SampleDiff  # On décale (pour prendre en compte le step)

         # Vérifie que le step ne sorte pas du signal

         if (temp + Nss <= len(Signal)):
            temp += Nss  # On décale la fin de la nouvelle fenêtre (pour prendre en compte le step)
         else:  # Si le step dépasse les échantillons
            return Frameslist

      # On remplit petit à petit tant qu'on reste dans la même frame
      SamplesFrames.append(Signal[i])

      i += 1

   # Ce dernier "échantillon frame" ne remplit pas les conditions de la boucle mais il faut quand même l'ajouter
   Frameslist.append(SamplesFrames)

   return Frameslist

#2.1
def signalenergy(signal):

   energy = 0
   for i in range(len(signal)):
      energy = energy + signal[i]**2

   return energy


def FrameEnergy(Frameslist):
   A = len(Frameslist)  # on définit la longueur du nombre de frames qu'on a


   E = np.zeros(A)  # on utilise numpy pour avoir un "tableau" (liste) de 0
   # de même longueur que le nombre de frames
   for frame in range(A):
      # on calcule l'énergie des frames
      E[frame] = signalenergy(Frameslist[frame])

   return E

#2.2.1
def Autocorr(Signal, Fe, Es):
   # initialisation
   Pitchlist = []

   Signal = split(Signal,Fe,2,2)
   Energy = FrameEnergy(Signal)

   B = len(Signal)

   i = 0  # on crée une boucle afin de tout parcourir
   while i < B:

      if (Energy[i - 1] > Es):  # on définit un seuil minimum
         SignalArr = np.array(Signal[i - 1])  # Passer en "array/list" facilite les calculs
         lags, c = xcorr(SignalArr, maxlags=int(Fe / 50), y = None)  # on utilise la fonction donner sur moodle
         # plt.plot(c)
         # on cherche les maxima
         maxima, value = signal.find_peaks(c, height=0,
                                        distance=45)  # on utilise la fonction"find peaks" de la librairie "scipy", la distance permet d'éviter des erreurs
         Mvalue = value['peak_heights']  # L'affichage contient {'peak_heights':array([... ])}, on veut que "array"
         # "maxima" = localisation des pics (selon x)
         maxima = maxima.tolist()  # "value" = hauteur des pics
         # on utilise la fonction "tolist()" pour convertir maxima en une "list"
         Mvalue, maxima = zip(*sorted(zip(Mvalue, maxima)))  # triage croissant
         D = len(maxima)
         Dist = np.abs(maxima[D - 1] - maxima[
            D - 2])  # on calcule la distance (selon x) séparant les 2 plus grand maxima (en valeur absolue)
         Ffdmtl = Fe / Dist  # on calcul la frequence fondamentale
         Pitchlist.append(Ffdmtl)  # on l'ajoute à la liste

      else:
         Ffdmtl = 0  # Si on est en dessous du seuil, on considère que c'est nulle
         Pitchlist.append(Ffdmtl)
      i = i + 1

   PitchArr = np.array(Pitchlist)  # Encore une fois, passer en "array/list" facilite les calculs
   PitchArrMoy = abs(np.mean(PitchArr))  # Calcul la moyenne

   return Pitchlist


#2.2.2
def Compute_cepstrum(Signal, Frqsample):

   Framesize = Signal.size
   Signalw = np.hamming(Framesize) * Signal  # on utilise le filtre de hamming
   Dt = 1 / Frqsample
   Frqvector = np.fft.rfftfreq(Framesize,
                               D=Dt)  # on utilise la fonction issue de numpy pour avoir la Transfo. de Fourier discr.
   F = np.fft.rfft(Signalw)
   logF = np.log(np.abs(F))  # il est conseillé de passer en log
   # plt.plot(frqvector, D=Dt)
   # plt.show()
   Cepstrum = np.fft.rfft(logF)
   Df = Frqvector[1] - Frqvector[0]
   qfrvect = np.fft.rfftfreq(logF.size, Df)
   # plt.plot(qfrvector, np.abs(Cepstrum))
   # plt.xlabel('quefrency (s)')
   # plt.show()
   return qfrvect, Cepstrum


def Cepstrum_frqfond(Signal, Frqsample, Fmax=500, Fmin=60):
   qfrvect, Cepstrum = Compute_cepstrum(Signal, Frqsample)
   Domainevalide = (qfrvect > 1 / Fmax) & (qfrvect <= 1 / Fmin)  # on définit la région où on prend le maxima
   Maxqfr = np.argmax(np.abs(Cepstrum)[Domainevalide])
   F0 = 1 / qfrvect[Domainevalide][Maxqfr]  # on trouve la fréquence fondamentale
   return F0


def Cepstrum(Signal, Fe, threshold):  # threshold = seuil
   Cepstrumlist = []
   Energy = FrameEnergy(Signal)

   G = len(Signal)

   i = 0  # on crée une boucle afin de tout parcourir
   while i < G:

      if Energy[i - 1] > threshold:

         SignalArr = np.array(Signal[i - 1])

         Ffdmtl = Cepstrum_frqfond(SignalArr, Fe)

         Cepstrumlist.append(Ffdmtl)

      else:

         Ffdmtl = 0
         Cepstrumlist.append(Ffdmtl)

         i = i + 1

   CepstrumArr = np.array(Cepstrumlist)
   CepstrumMoy = abs(np.mean(CepstrumArr))
   return Cepstrumlist

#2.3
def formant(Signal, Fe):
   f = []


   HPfilter = np.array(signal.lfilter([1., -0.67], 1, Signal))

   # 3
   frame_hamm = HPfilter * signal.hamming(len(HPfilter))

   # 4
   lpc_coeff = lpc_ref(frame_hamm, (2 + int(Fe / 1000)))

   # 5
   complex = np.roots(lpc_coeff)

   complex = [r for r in complex if np.imag(r) > 0]

   angles = np.array(np.angle(complex))

   f = np.array(np.unique(abs(angles * (Fe / (2 * np.pi)))))

   return f

#2.4
def MFCC(Signal, Fe):
    Signal = np.asarray(Signal)
    
        
    Signal_emp = np.array(Signal.lfilter([1., -0.97], 1, Signal))
    Signal_emp.tolist()
    
    # 2
    frameslist = split(Signal_emp, Fe, 15, 30)
    frameslist = np.array(frameslist)
    
    # 3
    for i in range(len(frameslist)):
      frame_hamm = signal.hamming(len(frameslist[i]))
      frameslist[i] *= frame_hamm

    # 4
    NFFT = 512
    P = []
    P= [(np.abs(Signal.fft(frameslist[i]))**2)/NFFT for i in range(len(frameslist))]


    # 5
    Temp=(len(frameslist[0])*2)-1
    Filterbanks = filter_banks(P, Fe, nfilt = 40, NFFT = Temp) 
    
    # 6
    MFCCVect = signal.dct(Filterbanks,type=2,axis=1,norm ='ortho')
    # 7
    LastMFCC = MFCCVect[:, 0:12]
    plt.plot(MFCCVect)
    return LastMFCC    
