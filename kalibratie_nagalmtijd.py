# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 08:16:24 2023

@author: dhira
"""

import sounddevice as sd
import numpy as np
import math
import matplotlib.pyplot as plt

# opnemen, 48000 meetwaarden per seconden
duration = 3  # seconds
myrecording = sd.rec(int(duration * 48000), samplerate=48000, channels=2)
sd.wait()

# maak alle meetwaarden positief
record = np.absolute(myrecording)

# omrekenen van meetwaarden naar dB
dB_lijst = []
for i in record[:,0]:
    dB = 10 * math.log10(math.exp(18.937*i)*(1e-9)/1e-12)
    dB_lijst.append(dB)
    
# Gemiddelde van elke 100 meetwaarden
arr = np.array(dB_lijst)
dB_Gem = np.mean(arr.reshape(-1, 100), axis=1)
#print("Result:\n",dB_Gem)
    
# plot
x = [ i for i in range(len(dB_Gem)) ]
y = dB_Gem
plt.plot(x,y)
plt.show()
print("Gemiddelde geluidniveau:",np.average(dB_Gem))
print("Maximum waarde:", np.max(dB_Gem))

## Nagalmtijd
# bepaal de maximun en minimum
dB_Gem_revers = dB_Gem[::-1]
max_start = np.mean(dB_Gem[20:200]) 
mini_achtergrond = np.mean(dB_Gem[-100:-1])
print("Gemiddelde Maximum:",max_start)
print("Achtergrond geluid",mini_achtergrond)
max_gem = list(filter(lambda i: i > max_start, dB_Gem_revers))[0]
index_max = len(dB_Gem_revers) - np.where(dB_Gem_revers==max_gem)[0][0] - 1
verschil_mimax = max_start - mini_achtergrond
from_the_top = np.array(dB_Gem[index_max::])



# bereken nagalmtijd
if verschil_mimax > 60:
    rt60 = dB_Gem[index_max] - 60
    find_rt60 = min(from_the_top, key=lambda x:abs(x-rt60))
    rt60_index = np.where(from_the_top==find_rt60)[0][0] + 1
    nagalmtijd = (rt60_index/480)
    print(index_max)
    print(rt60_index)
    print("Nagalmtijd in seconden:",nagalmtijd)

elif verschil_mimax <= 60 and verschil_mimax > 30:
    rt30 = dB_Gem[index_max] - 30
    find_rt30 = min(from_the_top, key=lambda x:abs(x-rt30))
    rt30_index = np.where(from_the_top==find_rt30)[0][0] + 1 
    nagalmtijd = (rt30_index/480) * 2
    print(index_max)
    print(rt30_index)
    print("Nagalmtijd in seconden:",nagalmtijd)
    
elif verschil_mimax <= 30 and verschil_mimax > 20:
    rt20 = dB_Gem[index_max] - 20
    find_rt20 = min(from_the_top, key=lambda x:abs(x-rt20))
    rt20_index = np.where(from_the_top==find_rt20)[0][0] + 1
    nagalmtijd = (rt20_index/480) * 3
    print(index_max)
    print(rt20_index)
    print("Nagalmtijd in seconden:",nagalmtijd)
    
else:
    print("te zacht")





 