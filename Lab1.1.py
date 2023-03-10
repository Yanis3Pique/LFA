fisier = input("Dati numele fisierului: ")
def functie(fisier):
    d = {}
    nr = 0
    try:
        with open(fisier) as f:
            for linie in f:
                for x in linie.split('\n'):
                    if linie.startswith('#') == False:
                        if x.startswith('['):
                            nume_sectiune = x.strip('[]')
                            d[nume_sectiune]=[]
                            nr += 1
                        else:
                            if x!='':
                                    d[nume_sectiune].append(x)
        #print(d, nr, sep='\n')
        for cheie in d:
            print(cheie)
            for element in d[cheie]:
                print(element, end=' ')
            print('\n')
        print("Avem", nr, "sectiuni.")
    except:
        print("Nu exista fisierul!")
functie(fisier)