import numpy as np

x = np.random.randint(135, size=100)
cena = np.random.randint(1000, size=100)

z = np.zeros(x.size)
z_cena = np.zeros(cena.size)

for i in range(x.size):
    zi = (x[i] - min(x)) / (max(x) - min(x))
    z[i] = round(zi, 1)*10
    z_cenai = (x[i] - min(x)) / (max(x) - min(x))
    z_cena[i] = round(z_cenai, 1) * 10
    z_cena[i] = 10 - z_cena[i]

#for i in range(x.size):
#    print('wartość:', x[i], 'punkty:', str(int(z[i]))+"/10", 'cena:', cena[i], 'punkty_cenowe:', str(int(z_cena[i]))+"/10")


def normalizacja(lista):

    znormalizowana_lista = []
    for i in range(len(lista)):
        znormalizowana_wartosc = (lista[i] - min(lista)) / (max(lista) - min(lista))
        znormalizowana_lista.append(round(znormalizowana_wartosc, 1)*10)

    return znormalizowana_lista

x = [523,107,296,34,57]
nowe_x = normalizacja(x)

for i in range(len(x)):
    print('wartość:', x[i], 'punkty:', str(int(nowe_x[i]))+"/10")
