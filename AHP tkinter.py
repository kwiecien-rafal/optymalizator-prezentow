from tkinter import *
from tkinter.font import Font
import numpy as np
import itertools as itr
import os

kryteria = ['rowery', 'telewizory', 'książki', 'telefony', 'drukarki']
#kryteria = ['rowery', 'telewizory', 'telefony']

kryteria_d = { i : "%.2f" % (1/len(kryteria)) for i in kryteria}
kryteriaKomb =list(itr.combinations(range(len(kryteria)),2))
kryteriaKomb_d = { i : 1 for i in kryteriaKomb }

label_list = []
label_list2 = []
button_list = []
spinbox_list = []
scale_list = []
skala = ['1/9', '1/8', '1/7', '1/6', '1/5', '1/4', '1/3', '1/2', '1', '2', '3', '4', '5', '6', '7', '8', '9']

##################### 'ramki' w okienku
root_ahp = Tk()
root_ahp.wm_title("AHP tkinter")

frame_g = Frame(root_ahp)
frame_g.grid(row = 0, column = 0, sticky = 'n', columnspan = 2, padx = 10, pady = 10)
frame_l = Frame(root_ahp)
frame_l.grid(row = 1, column = 0, sticky = 'n')
frame_p = Frame(root_ahp)
frame_p.grid(row = 1, column = 1, sticky = 'n')
frame_d = Frame(root_ahp)
frame_d.grid(row = 2, column = 0, columnspan = 2 ,sticky = 'n', padx = 10, pady = 10)

##################### funkcje
def aktd(): 
    # zapisz skale z przycisku do słownika
    for i in range(len(kryteriaKomb_d)):
        kryteriaKomb_d[kryteriaKomb[i]] = label_list[(i*4)+1].cget('text')

def wagi():
    # AHP
    RandomIndex = [0.01, 0.01, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]  
    cri = 0.20
    n = len(kryteria)
    k_matrix = np.ones((n, n))
    
    for i in range(n):
        for j in range(n):
            if i == j :
                k_matrix[i][j] = 1
            if i < j:
                k_matrix[i][j] = eval(str(kryteriaKomb_d[(i,j)]))
                k_matrix[j][i] = k_matrix[i][j]**(-1)
    weights = np.true_divide(k_matrix, np.sum(k_matrix, axis=0))
    weights = np.sum(weights, axis=1)
    weights = weights / weights.shape[0]

    cons_vector = np.multiply(k_matrix, weights)  
    weightedsum = np.sum(cons_vector, axis=1)
    ratio = weightedsum / weights
    lambdamax = np.sum(ratio, axis = 0) / n 
    if n - 1 == 0:
        ConsistencyIndex = (lambdamax - n) / 1                     
    else:
        ConsistencyIndex = (lambdamax - n) / (n - 1)  
    ConsistencyRatio = ConsistencyIndex / RandomIndex[n-1]    

    if ConsistencyRatio <= cri:
        listbox2.delete(0,END)
        listbox2.insert(END,'macierz jest spójna:')
        listbox2.insert(END, '{0:.3g}'.format(ConsistencyRatio)+ ' < '+ str(cri))
        listbox2.config(bg = '#b2ffa8')
        b_ok.config(relief=RAISED)
        b_ok.config(state=NORMAL)
    else:
        listbox2.delete(0,END)
        listbox2.insert(END, 'macierz NIE jest spójna: ')
        listbox2.insert(END, '{0:.3g}'.format(ConsistencyRatio)+ ' > '+ str(cri))
        listbox2.config(bg = '#ff7a7a')
        b_ok.config(relief=SUNKEN)
        b_ok.config(state=DISABLED)

    for i in range(len(kryteria)):
        kryteria_d[kryteria[i]] = "%.3f" % weights[i]

def wyswietl_wynik(): 
    # wyswietl słownik w boxie
    listbox.delete(0,END)
    for i in kryteria_d:
        listbox.insert(END, (i, kryteria_d[i]))

def sval(r):
    for i in range(len(scale_list)):
        label_list[(i*4)+1].config(text = skala[-int(scale_list[i].get())-1])
        label_list[(i*4)+2].config(text = skala[int(scale_list[i].get())])
    b_ok.config(relief = SUNKEN)
    b_ok.config(state = DISABLED)
    
def bt(): 
    # funkcja zbiorcza dla przycisku
    aktd()
    wagi()
    wyswietl_wynik()
    
def nLabel(r, c, tx): 
    # nowy label widget
    label = Label(frame_p, text = tx)
    label_list.append(label)
    label.grid(row=r, column=c, pady=1, padx = 4)

def nLabel2(r, c, tx):
    # nowy label widget 2
    label = Label(frame_p, text = tx, width = 3, relief = GROOVE)
    label_list.append(label)
    label.grid(row=r, column=c, pady=1, padx = 4)

def nSpinbox(r, c):
    # nowy spinbox widget
    spinbox = Spinbox(frame_p, values=skala, width = 3, font=Font(family='default', size=12),
                      command = lambda: bt(spinbox, spinbox.grid_info()['row']))
    spinbox_list.append(spinbox)
    spinbox.grid(row=r, column=c, pady=1, padx=4)
    spinbox.delete(0,"end")
    spinbox.insert(0,1)

def nScale(r, c):
    # nowy scale widget
    scale = Scale(frame_p, from_=0, to= 16, orient= HORIZONTAL, showvalue = 0, command = sval, length = 150)
    scale_list.append(scale)
    scale.set(8)
    scale.grid(row =r, column= c, pady = 1, padx = 4)

def lkat(r, x): 
    # jeden rząd do porównania
    nLabel(r,0, kryteria[int(x[0])])
    nLabel2(r,1, '--')
    nScale(r,2)
    nLabel2(r,3, '--')
    nLabel(r,4, kryteria[int(x[1])])

def reset():
    # resetuje wagi 
    for i in range(len(kryteriaKomb_d)):
        scale_list[i].set(8)
        kryteriaKomb_d[kryteriaKomb[i]] = 1
    wagi()
    wyswietl_wynik()   
    b_ok.config(relief=RAISED)
    b_ok.config(state=NORMAL)


listbox = Listbox(frame_l, width=21, height=len(kryteria)+1)
listbox.grid(columnspan = 2, row=0, column=0, pady=4, padx = 4)
listbox2 = Listbox(frame_l, width=21, height=2)
listbox2.grid(columnspan = 2, row=1, column=0, pady=4, padx = 4)

for i in kryteria_d:
    listbox.insert(END, (i, kryteria_d[i]))

for i in range(len(kryteriaKomb)):
    lkat(i, kryteriaKomb[i])

b_ok = Button(frame_l, text = 'ok', command=root_ahp.destroy)
b_ok.grid(row = 4, column = 0, sticky = 'nwes', columnspan = 2, pady =(0,4), padx = 4)

b_m = Button(frame_l, text = 'oblicz wagi', command= bt)
b_m.grid(row = 3, column = 0, sticky = 'nwes', columnspan = 2, padx = 4)

b_r = Button(frame_l, text = 'reset', command= reset)
b_r.grid(row = 5, column = 0, sticky = 'nwes', columnspan = 2, pady = (8,0), padx = 4)



root_ahp.mainloop()


