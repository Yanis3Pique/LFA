fisier = input("Dati numele fisierului: ")
alfabet = [] #Aici salvam elementele alfabetului
stare = [] #Aici salvam elementele starilor prin care putem trece (de unde plecam, pe unde trecem si unde putem ajunge)
actiune = [] #Aici salvam posibilitatile de a actiona la fiecare pas
nr = 0 #Variabila nr salveaza pe parcursul programului la a cata sectiune am ajuns, iar la finalul programului ne spune cate sectiuni avem
are_s = 0 #Cu aceasta variabila verificam daca exista stare de start pentru automata nedefinita
are_f = 0 #Cu aceasta variabila verificam daca exista stare de final pentru automata nedefinita
try:
    with open(fisier) as f:
        for linie in f:
            linie = linie.strip() # remove whitespace at the beginning and end of the line
            if linie.startswith('#') or linie == 'End': # skip lines with comments or 'End'
                continue
            for x in linie.split():
                if x.startswith('['):
                    nr += 1
                else:
                    if nr == 1:
                        alfabet.append(int(x))
                    elif nr == 2:
                        temp = 1
                        if 'f' in x:
                            are_f = 1
                            stare.append((x.strip(',f'), "stare finala"))   #stare.append(x.strip(',f'))
                            temp = 0
                        if 's' in x:
                            are_s = 1
                            stare.append((x.strip(',s'), "stare initiala"))   #stare.append(x.strip(',s'))
                            temp = 0
                        if temp == 1:
                            stare.append(x)
                    elif nr == 3:
                        temp = [x.strip('\n') for x in linie.split(',')]
                        actiune.append(temp)
        if alfabet == []: print("Nu exista alfabet!")
        else: print("Alfabet:", alfabet)
        if are_s == 0: print("Nu avem stare initiala!")
        if are_f == 0: print("Nu avem cel putin o stare finala!")
        if stare == []: print("Nu exista stari!")
        else: print("Stare:", stare)
        if actiune == []: print("Nu exista actiuni!")
        else: print("Actiuni:", actiune)
except:
    print("Nu exista numele fisierului!")

#NE TREBUIE 4 FUNCTII: UNA PENTRU SIGMA/ALFABET, UNA PENTRU STARE, UNA PENTRU ACTIUNI, UNA PENTRU PROGRAMUL COMPLET CARE LE FOLOSESTE PE PRECEDENTELE 3

'''
alfabet = [] # Aici salvam elementele alfabetului
stare = [] # Aici salvam elementele starilor prin care putem trece (de unde plecam, pe unde trecem si unde putem ajunge)
actiune = [] # Aici salvam posibilitatile de a actiona la fiecare pas

def Alfabet(fisier, alfabet, nr):
    with open(fisier) as f: # Deschidem fisierul selectat
        for linie in f: # Pentru fiecare linie din fisier
            linie = linie.strip()  # Eliminam spatiile albe de la inceputul si sfarsitul liniei, daca acestea exista
            if linie.startswith('#') or linie == 'End':  # Sarim peste liniile care contin comentarii sau "End"
                continue
            for x in linie.split(): # Luam fiecare element din linie
                if x.startswith('['): # Daca gasim un cuvant care incepe cu '[', inseamna ca incepe o noua sectiune
                    nr += 1 # Deci, crestem nr, pentru a sti la a cate sectiune ne aflam
                else:
                    if nr == 1: # Daca acel cuvant nu incepe cu '[', inseamna ca este, in cazul in care nr e 1, un element al alfabetului
                        if x.isnumeric(): # Daca elementul curent e numar
                            alfabet.append(int(x)) # Adaugam elementul curent in alfabet
                        else: # Daca elementul curent nu este numar
                            alfabet.append((x)) # Adaugam elementul curent in alfabet
    if alfabet == []: # Daca lista alfabetului este goala, inseamna ca nu exista alfabet
        return "Nu exista alfabet!" # Afisam un mesaj corespunzator
    else: # Daca, totusi, exista un alfabet
        return alfabet # Returnam alfabetul construit
def Stare(fisier, stare, nr):
    are_s = 0  # Cu aceasta variabila verificam daca exista stare de start pentru automata nedefinita
    are_f = 0  # Cu aceasta variabila verificam daca exista stare de final pentru automata nedefinita
    with open(fisier) as f: # Deschidem fisierul selectat
        for linie in f: # Pentru fiecare linie din fisier
            linie = linie.strip()  # Eliminam spatiile albe de la inceputul si sfarsitul liniei, daca acestea exista
            if linie.startswith('#') or linie == 'End':  # Sarim peste liniile care contin comentarii sau "End"
                continue
            for x in linie.split(): # Luam fiecare element din linie
                if x.startswith('['): # Daca gasim un cuvant care incepe cu '[', inseamna ca incepe o noua sectiune
                    nr += 1 # Deci, crestem nr, pentru a sti la a cate sectiune ne aflam
                else:
                    if nr == 2: # Daca acel cuvant nu incepe cu '[', inseamna ca este, in cazul in care nr e 2, un element al starii
                        temp = 1 # Cu temp vedem daca suntem la o stare finala/initiala sau nu
                        if 'f' in x: # Daca am gasit o stare finala in fisier
                            are_f = 1 # O contorizam ca gasita
                            stare.append((x.strip(',f'), "stare finala"))  # stare.append(x.strip(',f')) # O adaugam sub forma de tuplu in lista de stari
                            temp = 0 # Facem temp 0, ca sa nu ne adauge starea de doua ori in lista, la linia (*)
                        if 's' in x: # Daca am gasit o stare initiala in fisier
                            are_s = 1 # O contorizam ca gasita
                            stare.append((x.strip(',s'), "stare initiala"))  # stare.append(x.strip(',s')) # O adaugam sub forma de tuplu in lista de stari
                            temp = 0 # Facem temp 0, ca sa nu ne adauge starea de doua ori in lista, la linia (*)
                        if temp == 1: # Daca temp a ramas 1, adica starea curenta nu e nici finala, nici initiala, ci este oarecare, atunci    (*)
                            stare.append(x) # Adaugam starea orarecare in lista de stari
    if are_s == 0 and are_f == 0: return "Nu avem nici stare initiala, nici finala!" # Daca nu exista stare initiala si nici finala, afisam un mesaj corespunzator
    elif are_s == 0: return "Nu avem stare initiala!" # Daca nu exista stare initiala, afisam un mesaj corespunzator
    elif are_f == 0: return "Nu avem cel putin o stare finala!" # Daca nu exista stare finala, afisam un mesaj corespunzator
    elif stare == []: return "Nu exista stari!" # Daca nu exista stari, afisam un mesaj corespunzator
    else: return stare # Daca exista stari valide, le returnam
def Actiune(fisier, actiune, nr):
    with open(fisier) as f: # Deschidem fisierul selectat
        for linie in f: # Pentru fiecare linie din fisier
            linie = linie.strip()  # Eliminam spatiile albe de la inceputul si sfarsitul liniei, daca acestea exista
            if linie.startswith('#') or linie == 'End':  # Sarim peste liniile care contin comentarii sau "End"
                continue
            for x in linie.split(): # Luam fiecare element din linie
                if x.startswith('['): # Daca gasim un cuvant care incepe cu '[', inseamna ca incepe o noua sectiune
                    nr += 1 # Deci, crestem nr, pentru a sti la a cate sectiune ne aflam
                else:
                    if nr == 3: # Daca acel cuvant nu incepe cu '[', inseamna ca este, in cazul in care nr e 3, un element al actiunii
                        temp = [x.strip('\n') for x in linie.split(',')] # Adaugam actiunea sub forma de lista cu 3 elemente, in lista mare de actiuni
                        actiune.append(temp) # Adaugam actiunea curenta in lista de actiuni
    if actiune == []: # Daca nu exista actiuni
        return "Nu exista actiuni!" # Afisam un mesaj corespunzator
    else: # Daca, totusi, exista actiuni valide
        return actiune # Returnam actiunile gasite
def main():
    try:
        print(Alfabet(fisier, alfabet, nr))
        print(Stare(fisier, stare, nr))
        print(Actiune(fisier, actiune, nr))
    except:
        print("Nu exista fisierul selectat!")
main()
'''