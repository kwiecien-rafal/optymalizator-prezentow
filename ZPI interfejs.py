from tkinter import *
from tkinter.font import Font
import numpy as np
import itertools as itr
import csv
import ograniczenia as ogr
import ZPI_f_celu as fcl

root_menu = Tk()
root_menu.wm_title("Optymalizator prezentów świątecznych")
root_menu.iconbitmap('Optymalizator prezentów.ico')
windowWidth_g = 475
windowHeight_g = 550
positionRight = int(root_menu.winfo_screenwidth()/2 - windowWidth_g/2)
positionDown = int(root_menu.winfo_screenheight()/2 - windowHeight_g/2)


frame_l = Frame(root_menu)
frame_l.grid(row = 0, column = 0, sticky = 'n', padx= (5, 10), pady = (11, 0))

frame_p = Frame(root_menu)
frame_p.grid(row = 0, column = 1, sticky = 'n', padx= (35, 10), pady = (40, 0))

frame_d = Frame(root_menu)
frame_d.grid(row = 1, column = 1, sticky = 'n', pady = (50, 0))

osoby = []
przedmioty = []

ahpo = {}
koszykid = 0
koszykidc = 0
x = 0
#####################

def dodaj_osoby():
    global windowWidth_g
    
    root_osob = Toplevel()
    root_osob.wm_title("dodaj osobe")
    

    windowWidth = 200
    windowHeight = 150

    l_nazwa = Label(root_osob, text = 'Nazwa profilu')
    l_nazwa.grid(row = 1, column = 0)
    e_nazwa = Entry(root_osob, width=15, bg='white')
    e_nazwa.grid(row = 1, column = 1)

    l_plec = Label(root_osob, text = 'Plec')
    l_plec.grid(row = 2, column = 0)
    e_plec = Spinbox(root_osob, width = 7, values=('k', 'm'))
    e_plec.grid(row = 2, column = 1, sticky = 'w')

    l_wiek = Label(root_osob, text = 'Wiek')
    l_wiek.grid(row = 3, column = 0)
    e_wiek = Spinbox(root_osob, width = 7, from_= 0, to = 100)
    e_wiek.grid(row = 3, column = 1, sticky = 'w')

    
    def dodos():

        nz = e_nazwa.get()
        if len(nz) < 1:
            nz = 'bezimienny'

        pl = e_plec.get()
        if pl not in ['k', 'm']:
            pl = 'k'

        wk = int(e_wiek.get())
        if wk <=0:
            wk = 1
        o = {'nazwa': nz, 'plec': pl, 'wiek': wk, 'waga': 1 , 'przedmioty':[], 'ahpkryt':{'kategorie': 1, 'popularność': 1, 'cena': 1}, 'ahpkat':{}}
        osoby.append(o)
        up_lb_osoby()


    b_dodaj = Button(root_osob, text = 'dodaj', command = dodos, width = 10)
    b_dodaj.grid(row = 10, column = 0, columnspan = 2, pady = (10 ,0))

    b_ok = Button(root_osob, text = 'ok', command=root_osob.destroy, width = 10)
    b_ok.grid(row = 11, column = 0, columnspan = 2, sticky = 'n')


    root_osob.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight-windowWidth, positionDown))

def usun_osoby():

    del osoby[lb_osoby.curselection()[0]]
    lb_osoby.delete(lb_osoby.curselection(),lb_osoby.curselection())
    lb_przed.delete(0, END)

def up_lb_osoby():
    lb_osoby.delete(0, END)

    for i in range(len(osoby)):
        lb_osoby.insert(END, osoby[i]['nazwa'])

 
def dodaj_przedmioty(zazn):
    
    if lb_osoby.curselection() == ():
        return 

    root_przedm = Toplevel()
    root_przedm.wm_title("dodaj przedmioty dla "+str(osoby[zazn]['nazwa']))
    windowWidth = 450
    windowHeight = 500
    positionRight = int(root_przedm.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root_przedm.winfo_screenheight()/2 - windowHeight/2)
    
    frame0 = Frame(root_przedm)
    frame0.grid(row = 0, column = 0, sticky = 'n', padx= (10,10), pady = (10,0))

    with open('baza_wszystkich_produktow.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        baza_produktow = list(reader)

    osoba = osoby[zazn] 

    budzet = int(e_budz.get())
    plec = osoba['plec']
    wiek = int(osoba['wiek'])


    baza_produktow = ogr.ograniczenia_plec(baza_produktow, plec)
    baza_produktow = ogr.ograniczenia_wiek(baza_produktow, wiek)
    baza_produktow = ogr.ograniczenie_budzet(baza_produktow, budzet)


    tagi = {}

    for i in baza_produktow:
        if i[0] not in tagi:
            tagi[i[0]] = {}
        if i[1] not in tagi[i[0]]:
            tagi[i[0]][i[1]] = []
        if i[2] not in tagi[i[0]][i[1]]:
            tagi[i[0]][i[1]].append(i[2])
    tagi0 = list(tagi)
    tagi1 = list(tagi[tagi0[0]])
    tagi2 = list(tagi[tagi0[0]][tagi1[0]])


    var0 = StringVar(frame0)
    var0.set(tagi0[0]) 
    var1 = StringVar(frame0)
    var1.set(tagi1[0]) 
    var2 = StringVar(frame0)
    var2.set(tagi2[0]) 

    def akt():
        lb_przedmioty.delete(0, END)
        for i in baza_produktow:
            if i[0] == var0.get():
                if i[1] == var1.get():
                    if i[2] == var2.get():
                        lb_przedmioty.insert(END, i[3])


    def dd0(x):
        nonlocal o_kat1, o_kat2

        o_kat1.destroy()
        o_kat2.destroy()
        tagi1 = list(tagi[x])
        tagi2 = list(tagi[x][tagi1[0]])

        var1.set(tagi1[0]) 
        var2.set(tagi2[0])
        o_kat1 = OptionMenu(frame0, var1, *tagi1, command = dd1)
        o_kat1.grid(row = 1, column = 0, sticky = 'nesw', columnspan = 2)
        o_kat1.config(width = 30)
        o_kat2 = OptionMenu(frame0, var2, *tagi2, command = dd2)
        o_kat2.grid(row = 2, column = 0, sticky = 'nesw', columnspan = 2)
        o_kat2.config(width = 30)
        akt()

    def dd1(x):
        nonlocal o_kat2
        o_kat2.destroy()
        tagi2 = list(tagi[var0.get()][x])
        var2.set(tagi2[0])

        o_kat2 = OptionMenu(frame0, var2, *tagi2, command = dd2)
        o_kat2.grid(row = 2, column = 0, sticky = 'nesw', columnspan = 2)
        o_kat2.config(width = 30)
        akt()

    def dd2(x):
        akt()

    def dodaj():
        nonlocal osoba

        for i in baza_produktow:
            if i[3] == lb_przedmioty.get(ACTIVE):
                nazwa = i[3]
                kategoria = i[1]
                cena = i[5]
                popularnosc = i[7]
                score = 1
        osoba['przedmioty'].append([nazwa, kategoria, cena, popularnosc, score])
                
        
        up_lb_przedmioty(zazn)

    o_kat0 = OptionMenu(frame0, var0, *tagi0, command = dd0)
    o_kat0.grid(row = 0, column = 0, sticky = 'nesw', columnspan = 2)

    o_kat1 = OptionMenu(frame0, var1, *tagi1, command = dd1)
    o_kat1.config(width = 30)
    o_kat1.grid(row = 1, column = 0, sticky = 'nesw', columnspan = 2)

    o_kat2 = OptionMenu(frame0, var2, *tagi2, command = dd2)
    o_kat2.grid(row = 2, column = 0, sticky = 'nesw', columnspan = 2)

    lb_przedmioty = Listbox(frame0, height = 10, width = 70)
    lb_przedmioty.grid(row = 3, column = 0, sticky = 'n', columnspan = 2)

    b_dodaj = Button(frame0, text = 'dodaj', command = dodaj)
    b_dodaj.grid(row = 4, column = 0, sticky = 'nesw')
    b_ok = Button(frame0, text = 'ok', command=root_przedm.destroy)
    b_ok.grid(row = 4, column = 1, sticky = 'nesw')

    akt()

    root_przedm.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, (positionRight-windowWidth-15), positionDown- 25))
  

def usun_przedmioty(zazn):
    osoba = osoby[zazn]
    del osoba['przedmioty'][lb_przed.curselection()[0]]
        
    lb_przed.delete(lb_przed.curselection(),lb_przed.curselection())

def up_lb_przedmioty(zazn):
    lb_przed.delete(0, END)
    for i in osoby[zazn]['przedmioty']:
        lb_przed.insert(0, i[0])


def ahp(kryt, osob, tryb):
    global x

    if len(kryt)<1:
        return 

    kryteria = list(kryt.keys())

    windowWidth = 550
    windowHeight = 550


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
    root_ahp = Toplevel()
    root_ahp.wm_title("ahp do tkintera")
    
    root_ahp.minsize(700, 550)

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

        if n == 1:
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


            for i in range(len(kryteria)):
                #kryteria_d[kryteria[i]] = "%.3f" % weights[i]
                kryteria_d[kryteria[i]] = round((weights[i]),2)


        else:
            listbox2.delete(0,END)
            listbox2.insert(END, 'macierz NIE jest spójna: ')
            listbox2.insert(END, '{0:.3g}'.format(ConsistencyRatio)+ ' > '+ str(cri))
            listbox2.config(bg = '#ff7a7a')
            b_ok.config(relief=SUNKEN)
            b_ok.config(state=DISABLED)
        

    def wyswietl_wynik(): 
        # wyswietl słownik w boxie
        listbox.delete(0,END)
        for i in kryteria_d:
            listbox.insert(END, i+': '+str(kryteria_d[i]))


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
        # nowy label widget
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
        scale = Scale(frame_p, from_=0, to= 16, orient= HORIZONTAL, showvalue = 0, command = sval)
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


    def ok():
        global x, root_menu, ahpo
        
        x+= 1

        if tryb == 'ahposoby':
            ahpo = kryteria_d.copy()

        else:
            osoby[osob][tryb] = kryteria_d.copy()

        if x>=(len(osoby)*2)+1:
            wyniki()
            x = 0
            root_ahp.destroy()

        root_ahp.destroy()

    if tryb == 'ahposoby':
        wiadomosc = 'wybranych osob'
    else:
        wiadomosc = osoby[osob]['nazwa']

    label = Label(frame_g, text = ('Określ preferencje dla: '+wiadomosc)).grid(row=0, column=0, pady=7, padx = 4)

    listbox = Listbox(frame_l, width=35, height= 7)
    listbox.grid(columnspan = 2, row=0, column=0, pady=4, padx = 4)
    listbox2 = Listbox(frame_l, width=35, height=2)
    listbox2.grid(columnspan = 2, row=1, column=0, pady=4, padx = 4)

    for i in kryteria_d:
            listbox.insert(END, i+': '+kryteria_d[i])

    for i in range(len(kryteriaKomb)):
        lkat(i, kryteriaKomb[i])

    b_ok = Button(frame_l, text = 'ok', command=ok)
    b_ok.grid(row = 4, column = 0, sticky = 'nwes', columnspan = 2, pady =(0,4), padx = 4)

    b_m = Button(frame_l, text = 'oblicz wagi', command= bt)
    b_m.grid(row = 3, column = 0, sticky = 'nwes', columnspan = 2, padx = 4)

    b_r = Button(frame_l, text = 'reset', command= reset)
    b_r.grid(row = 5, column = 0, sticky = 'nwes', columnspan = 2, pady = (8,0), padx = 4)
   
    root_ahp.geometry("+{}+{}".format(positionRight, positionDown))  
    root_ahp.attributes("-topmost", True)

def ahpw():
    global x, ahpo

    x = 0

    for i in osoby:
        for j in i['przedmioty']:
            if j[1] not in list(i['ahpkat'].keys()):
                i['ahpkat'][j[1]] = 1
    ahposoby = {}
    for i in range(len(osoby)):

        ahp(osoby[i]['ahpkryt'], i, 'ahpkryt')
        ahp(osoby[i]['ahpkat'], i, 'ahpkat')
        ahposoby[osoby[i]['nazwa']] = 1

    ahp(ahposoby, 0, 'ahposoby')



def wyniki():

    def normalizacja(lista):

        znormalizowana_lista = []
        for i in range(len(lista)):
            znormalizowana_wartosc = (lista[i] - min(lista)) / (max(lista) - min(lista))
            znormalizowana_lista.append(round(znormalizowana_wartosc, 1)*10)

        return znormalizowana_lista


    lista_przedmiotow_osob = []
    for i in range(len(osoby)):
        ahp_1 = osoby[i]['ahpkat']
        ahp_2 = osoby[i]['ahpkryt']
        ahp_2_lista_wartosci = list(map(float, ahp_2.values()))
        for h in range(len(ahp_2_lista_wartosci)):
            ahp_2_lista_wartosci[h] = round(ahp_2_lista_wartosci[h], 2)
        
        wskaznik_ceny = []
        cena = []
        for produkt in osoby[i]['przedmioty']:
            cena.append(int(produkt[2]))
        wskaznik_ceny = normalizacja(cena)

        nazwa_produktu = []
        wsk_podkategorii = []
        wsk_popularnosc_prod = []
        wsk_cena_prod = []
        for j in range(len(osoby[i]['przedmioty'])):
            nazwa_produktu.append(osoby[i]['przedmioty'][j][0])
            wsk_podkategorii.append(float(ahp_1[osoby[i]['przedmioty'][j][1]]))
            wsk_popularnosc_prod.append(float(osoby[i]['przedmioty'][j][3]))
            wsk_cena_prod.append(wskaznik_ceny[j])
            
        wynik = fcl.f_celu(wsk_podkategorii, nazwa_produktu, wsk_popularnosc_prod, wskaznik_ceny, ahp_2_lista_wartosci)
        wynik = fcl.sortowanie(wynik)

        lista_przedmiotow_osob.append(wynik)


    budzet = int(e_budz.get())
    ahp_3 = {}

    for k, v in ahpo.items():
        ahp_3[k] = round(float(v), 2)

    zz = fcl.optymalizacja(ahp_3, lista_przedmiotow_osob, budzet)


    root_wyniki = Toplevel()
    root_wyniki.wm_title("Wyniki")
    windowWidth = 550
    windowHeight = 550

    osobyw = []
    for i in osoby:
        osobyw.append(i['nazwa'])
    wyniki = zz
    miejsce = 0
    score = wyniki[miejsce][0]

    lb_osobyw = Listbox(root_wyniki, height = len(osoby)+1, width = 10)
    lb_osobyw.grid(row = 1, column = 0, columnspan = 1, padx=(20, 0))

    lb_przedw = Listbox(root_wyniki, height = len(osoby)+1, width = 70)
    lb_przedw.grid(row = 1, column = 1, columnspan = 3, pady=(0, 0))

    for i in osobyw:
        lb_osobyw.insert(END, i)


    def lewo():
        nonlocal miejsce, score
        if miejsce >0:
            miejsce-= 1
        score = round(wyniki[miejsce][0],3)
        wyn()
        upl()

    def prawo():
        nonlocal miejsce, score
        if miejsce <len(wyniki)-1:
            miejsce+= 1
        score = round(wyniki[miejsce][0],3)
        wyn()
        upl()

    def wyn():
        with open('baza_wszystkich_produktow.csv', newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            baza_produktow_wyn = list(reader)

        cen = 0
        lb_przedw.delete(0, END)
        for i in wyniki[miejsce][1]:
            lb_przedw.insert(END, i[0])
            pass

    def upl():
        m_wynik.configure(text = 'miejsce: '+str(miejsce+1)+'\nscore: '+str(score))



    b_lewo = Button(root_wyniki, text = '<', width = 10, command= lewo)
    b_lewo.grid(row = 0, column = 1, columnspan = 1, sticky = 'nsw')

    m_wynik = Message(root_wyniki, text = 'miejsce: '+str(miejsce+1)+'\nscore: '+str(score), width = 300)
    m_wynik.grid(row = 0, column = 2, columnspan = 1)

    b_prawo = Button(root_wyniki, text = '>', width = 10, command= prawo)
    b_prawo.grid(row = 0, column = 3, columnspan = 1, sticky = 'nse')

    wyn()
    print(zz)

    root_wyniki.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))


fb = frame_p
fl = frame_l


l_budz = Label(fb, text = 'Budżet')
l_budz.grid(row = 2, column = 0, sticky = 'nesw', pady=(0, 0))
e_budz = Entry(fb,width = 5)
e_budz.insert(0,100)
e_budz.grid(row = 2, column = 1, sticky = 'nesw', pady=(0, 0))

rob = 0
rol = 1
rpb = 2
rpl = 3

def onselect(evt):
    global koszykidc, zazn
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    zazn = int(w.curselection()[0])
    up_lb_przedmioty(zazn)



b_plso = Button(fl, text = '+', font=Font(family='default', weight = 'bold'), command = dodaj_osoby)
b_plso.grid(row = rob, column = 0, sticky = 'nesw')
l_osoby = Label(fl, text = 'Osoby', relief = RIDGE)
l_osoby.grid(row = rob, column = 1, sticky = 'nesw')
b_mnso = Button(fl, text = '-', font=Font(family='default', weight = 'bold'), command = usun_osoby )
b_mnso.grid(row = rob, column = 2, sticky = 'nesw')
lb_osoby = Listbox(fl, height = 5, width = 50)
lb_osoby.grid(row = rol, column = 0, columnspan = 3, pady=(0, 20))

lb_osoby.bind('<<ListboxSelect>>', onselect)

b_plsp = Button(fl, text = '+', font=Font(family='default', weight = 'bold'), command = lambda:dodaj_przedmioty(zazn))
b_plsp.grid(row = rpb, column = 0, sticky = 'nesw')
l_przed = Label(fl, text = 'Przedmioty', relief = RIDGE)
l_przed.grid(row = rpb, column = 1, sticky = 'nesw')
b_mnsp = Button(fl, text = '-', font=Font(family='default', weight = 'bold'), command = lambda:usun_przedmioty(zazn))
b_mnsp.grid(row = rpb, column = 2, sticky = 'nesw')
lb_przed = Listbox(fl, height = 14, width = 50)
lb_przed.grid(row = rpl, column = 0, columnspan = 3)

b_mnsp = Button(fb, text = 'optymalizuj', height = 2, command = ahpw)
b_mnsp.grid(row = 7, column = 0, sticky = 's', pady=(25,0), columnspan = 2)


root_menu.geometry("{}x{}+{}+{}".format(windowWidth_g, windowHeight_g, positionRight, positionDown))
root_menu.mainloop()