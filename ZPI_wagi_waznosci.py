import numpy as np
import matplotlib.pyplot as plt

ilosc_osob = 5

w_max = [1, 1.5]
w_min = [ilosc_osob, 0.5]

a = (w_min[1]-w_max[1])/(w_min[0]-w_max[0])

b = 1.5 - a

wagi = np.zeros(ilosc_osob)
wagi[0] = 1.5
wagi[-1] = 0.5

for i in range(2, ilosc_osob):
    wagi[i-1] = round(((a*i)+b), 2)

for i in wagi:
    print(i)
