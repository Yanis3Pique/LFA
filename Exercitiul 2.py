#
# Autori: Chirus Mina-Sebastian, Popescu Pavel-Yanis
#
class Sectiune:
    """
    Clasa memoreaza o sectiune in formatul specific
    """
    def __init__(self, nume: str, continut: list[str], la) -> None:
        self.nume = nume
        self.continut = continut
        self.la = la
    
    def checkNSet(self):
        """
        Pentru a evita cautarea specifica a unei sectiuni,
        setam direct in variabile
        """
        if self.nume == self.la.string_alfabet:
            self.la.sectiune_alfabet = self
        if self.nume == self.la.string_gama:
            self.la.sectiune_gama = self
        if self.nume == self.la.string_stari:
            self.la.sectiune_stari = self
        if self.nume == self.la.string_actiuni:
            self.la.sectiune_actiuni = self

    @staticmethod
    def loadSectiuni(fisier: str, la):
        """
        Functia ia ca parametru adresa unui fisier
        si parsează sectiunile in obiecte
        pe care le returneaza
        """
        try:
            with open(fisier) as f:
                sectiuni = []
                currentSec = None
                linie = f.readline()
                while linie:
                    linie = linie.strip()
                    #ignoram comentariile
                    if linie.startswith('#'):
                        linie = f.readline()
                        continue
                    #vedem daca incepe o noua sectiune
                    if linie.startswith("[") and linie.endswith("]"):
                        if currentSec:
                            currentSec.checkNSet()
                            sectiuni.append(currentSec)
                        
                        linie = linie.replace("[","").replace("]","")
                        #setam in functie de header obiectele
                        if linie == la.string_alfabet:
                            currentSec = Sectiune_Alfabet(la, [])
                        elif linie == la.string_gama:
                            currentSec = Sectiune_Gama(la, [])
                        elif linie == la.string_stari:
                            currentSec = Sectiune_Stari(la, [])
                        elif linie == la.string_actiuni:
                            currentSec = Sectiune_Actiuni(la, [])
                        else:
                            currentSec = Sectiune(linie, [], la)
                    else:
                        if currentSec:
                            if not linie.replace(" ", ""):
                                print("Eroare: Configuratia nu accepta linii goale")
                                exit()
                                return None
                            currentSec.continut.append(linie)
                        else:
                            print("Eroare: Formatul fisierului este incorect la linia " + linie)
                            exit()
                            return None
                    #citim o linie noua
                    linie = f.readline()
                currentSec.checkNSet() # type: ignore
                sectiuni.append(currentSec)
                return sectiuni
        except:
            print("Eroare: Fisierul nu exista!")
            exit()
            return None

class Sectiune_Alfabet(Sectiune):
    def __init__(self, la, continut: list[str] = []) -> None:
        super().__init__(la.string_alfabet, continut, la)
        self.verificat = False
    
    def cuvantValid(self, cuvant: str) -> bool:
        "Functia se asigura ca argumentul apartine alfabetului"
        return cuvant in self.continut

    def loadAlfabet(self) -> list[str]:
        "Functia verifica sa nu fie ambiguitate la citirea caracterelor din cuvant"
        if self.verificat:
            return self.continut
        else:
            for x in self.continut:
                for y in self.continut:
                    if x != y:
                        if y.startswith(x):
                            print("Eroare: Un caracter din alfabet il contine pe altul: " + y + " si " + x)
                            exit()
                            return [] 
            self.verificat = True
            return self.continut

class Sectiune_Gama(Sectiune):
    def __init__(self, la, continut: list[str] = []) -> None:
        super().__init__(la.string_gama, continut, la)
        self.verificat = False
    
    def cuvantValid(self, cuvant: str) -> bool:
        "Functia se asigura ca argumentul apartine multimii gama"
        return (cuvant in self.continut) or (cuvant == self.la.string_epsilon)

    def loadAlfabet(self) -> list[str]:
        "Functia verifica sa nu fie ambiguitate la citirea caracterelor din cuvant"
        if self.verificat:
            return self.continut
        else:
            for x in self.continut:
                for y in self.continut:
                    if x != y:
                        if y.startswith(x):
                            print("Eroare: Un caracter din gama il contine pe altul: " + y + " si " + x)
                            # self.delAll()
                            exit()
                            return [] 
            self.verificat = True
            return self.continut

class Stare:
    "Obiectul corespunzator unei stari"
    def __init__(self, stare_str: str, initial_state: bool = False, final_state: bool = False) -> None:
        self.stare_str = stare_str
        self.initial_state = initial_state
        self.final_state = final_state
    
    def __str__(self):
        statusStare = ""
        if self.initial_state: statusStare+=" INIT"
        if self.final_state: statusStare+=" FIN"
        return "["+self.stare_str+":"+statusStare+"]"
    def __repr__(self):
        statusStare = ""
        if self.initial_state: statusStare+=" INIT"
        if self.final_state: statusStare+=" FIN"
        return "["+self.stare_str+":"+statusStare+"]"

class Sectiune_Stari(Sectiune):
    "Sectiune speciala care incarca si retine starile"
    def __init__(self, la, continut: list[str] = []) -> None:
        super().__init__(la.string_stari, continut, la)
        self.stari = []
        self.initState = None
        self.stari_dict = {}

    def getStare(self, stare_str: str) -> Stare | None:
        """
        Functia gaseste starea cu un nume dat
        """
        if stare_str in self.stari_dict.keys():
            return self.stari_dict[stare_str]
        else:
            return None
    def getStareInitiala(self) -> Stare | None:
        """
        Functia returneaza starea de inceput
        """
        return self.initState

    def loadStari(self) -> list[Stare]:
        """
        Functia verifica si incarca toate starile
        """
        if not len(self.stari_dict.keys()):
            for stare_str in self.continut:
                if ',' in stare_str:
                    state, info = stare_str.split(",", 1)
                    if self.getStare(state):
                        print("Eroare: Starea "+state+" a fost definita de 2 ori!")
                        exit()
                        return []
                    info = info.lower()
                    if 's' in info:
                        if not self.initState:
                            final_state = 'f' in info
                            self.initState = Stare(state, initial_state=True, final_state=final_state)
                            self.stari_dict[state] = self.initState
                        else:
                            print("Eroare: S-au gasit mai multe stari initiale")
                            exit()
                            return []
                    elif 'f' in info:
                        self.stari_dict[state] = Stare(state, final_state=True)
                    else:
                        print("Eroare: O stare poate fi doar simpla, finala(f) sau initiala(s). Starea '"+info+"' nu exista")
                        exit()
                        return []
                else:
                    if self.getStare(stare_str):
                        print("Eroare: Starea "+stare_str+" a fost definita de 2 ori!")
                        exit()
                        return []
                    self.stari_dict[stare_str] = Stare(stare_str)
            if not self.initState:
                print("Eroare: Nu exista o stare initiala")
                exit()
                return []
        self.stari = [self.stari_dict[x] for x in self.stari_dict.keys()]
        return self.stari

class Actiune:
    def __init__(self, stare_initiala: Stare, conditie_stare: str, inLista: str, scoate: str, introdu: str, stare_urmatoare: Stare) -> None:
        self.stare_initiala = stare_initiala
        self.conditie_stare = conditie_stare
        self.inLista = inLista
        self.scoate = scoate
        self.introdu = introdu
        self.stare_urmatoare = stare_urmatoare
    "Intstructiunile de mai jos ne ajuta sa dam print() direct"
    "la ce ne intereseaza cand incercam sa vedem obiectul"
    def __str__(self):
        return "["+self.stare_initiala.stare_str+", "+self.conditie_stare+", "+self.inLista+" -> "+self.stare_urmatoare.stare_str+", "+self.scoate+", "+self.introdu+"]"
    def __repr__(self):
        return "["+self.stare_initiala.stare_str+", "+self.conditie_stare+", "+self.inLista+" -> "+self.stare_urmatoare.stare_str+", "+self.scoate+", "+self.introdu+"]"

class Sectiune_Actiuni(Sectiune):
    def __init__(self, da, continut: list[str] = []) -> None:
        super().__init__(da.string_actiuni, continut, da)
        self.actiuni: list[Actiune] = []

    def getActiuni(self, stare_initiala: Stare, conditie_stare: str) -> list[Actiune]:
        """
        Functia gaseste o multime de actiuni pentru o anumita stare si o conditie data
        """
        rez = []
        if self.actiuni:
            for actiune_pos in self.actiuni:
                if actiune_pos.stare_initiala.stare_str == stare_initiala.stare_str and actiune_pos.conditie_stare == conditie_stare:
                    rez.append(actiune_pos)
        return rez

    def loadActiuni(self) -> list[Actiune]:
        if not self.actiuni:
            if not self.la.sectiune_alfabet or not self.la.sectiune_stari:
                print("Eroare: Alfabetul sau Starile nu sunt initializate si se incearca incarcarea Actiunilor")
                exit()
                return []
            for actiune_str in self.continut:
                actiune = actiune_str.split(",")
                if len(actiune) == 6:
                    #stare,input,inLista,stareUrmatoare,sterge,introdu
                    fr_s, cond, inLista, to_s, sterge, introdu = actiune
                    fr = self.la.sectiune_stari.getStare(fr_s)
                    to = self.la.sectiune_stari.getStare(to_s)

                    if not self.la.sectiune_gama.cuvantValid(inLista.replace("!","")):
                        print("Eroare: Caracterul '" + inLista + "' nu este in Gama")
                        exit()
                        return []
                    if not self.la.sectiune_gama.cuvantValid(sterge):
                        print("Eroare: Caracterul '" + sterge + "' nu este in Gama")
                        exit()
                        return []
                    if not self.la.sectiune_gama.cuvantValid(introdu):
                        print("Eroare: Caracterul '" + introdu + "' nu este in Gama")
                        exit()
                        return []
                    
                    if to and self.la.sectiune_alfabet.cuvantValid(cond) and fr:
                        self.actiuni.append(Actiune(fr, cond, inLista, sterge, introdu, to))
                    elif not fr:
                        print("Eroare: Starea '" + fr_s + "' nu este valida")
                        exit()
                        return []
                    elif not self.la.sectiune_alfabet.cuvantValid(cond):
                        print("Eroare: Caracterul '" + cond + "' nu este in dictionar")
                        exit()
                        return []
                    elif not to:
                        print("Eroare: Starea '" + to_s + "' nu este valida")
                        exit()
                        return []
                else:
                    print("Eroare: Configuratia '" + actiune_str + "' nu este corecta")
                    exit()
                    return []

        return self.actiuni


class LA:
    def __init__(self, nume_fisier: str, debug: bool = False) -> None:
        self.string_alfabet = "Sigma"
        self.string_stari = "States"
        self.string_actiuni = "Actions"
        self.string_gama = "Gama"
        self.string_epsilon = "*"

        self.debug = debug

        self.sectiune_alfabet: Sectiune_Alfabet
        self.sectiune_gama: Sectiune_Gama
        self.sectiune_stari: Sectiune_Stari
        self.sectiune_actiuni: Sectiune_Actiuni

        if self.debug:
            print("------SE INCARCA------")
            print("FISIER", nume_fisier)
        
        # Metoda de mai jos returneaza toate sectiunile din configuratie
        # + instantiaza obiectele corespunzatoare alfabetului, starilor si
        # al actiunilor
        self.sectiuni = Sectiune.loadSectiuni(nume_fisier, self)

        # ne asiguram ca pana acum sectiunile sunt ok

        # la incarcarea alfabetului se verifica cuvintele
        # pentru ambiguitate
        #sigma
        try:
            if self.sectiune_alfabet:
                if self.debug:
                    print("ALFABET", self.sectiune_alfabet.loadAlfabet())
                else:
                    self.sectiune_alfabet.loadAlfabet()
        except:
            print("EROARE: Sectiunea cu headerul","["+self.string_alfabet+"]","nu a fost gasita in configuratie")
            exit()

        #gama
        try:
            if self.sectiune_gama:
                if self.debug:
                    print("GAMA", self.sectiune_gama.loadAlfabet())
                else:
                    self.sectiune_gama.loadAlfabet()
        except:
            print("EROARE: Sectiunea cu headerul","["+self.string_gama+"]","nu a fost gasita in configuratie")
            exit()

        #stari
        try:
            if self.sectiune_stari:
                if self.debug:
                    print("STARI", self.sectiune_stari.loadStari())
                else:
                    self.sectiune_stari.loadStari()
        except:
            print("EROARE: Sectiunea cu headerul","["+self.string_stari+"]","nu a fost gasita in configuratie")
            exit()

        #actiuni
        try:
            if self.sectiune_actiuni:
                if self.debug:
                    print("ACTIUNI", self.sectiune_actiuni.loadActiuni())
                else:
                    self.sectiune_actiuni.loadActiuni()
        except:
            print("EROARE: Sectiunea cu headerul","["+self.string_actiuni+"]","nu a fost gasita in configuratie")
            exit()
        if self.debug: print("------INCARCAT------")
    
    def valideaza(self, mesaj: str):
    # se face o ultima verificare pentru toate cele 3 obiecte
        iteratie = 0
        lista = []
        if self.sectiune_alfabet and self.sectiune_stari and self.sectiune_actiuni:
            stare = self.sectiune_stari.getStareInitiala()
            while mesaj:
                schimbare = False
                if self.debug:
                    print("---------","Iteratie", iteratie, "---------")
                    if stare:
                        print(stare)
                        print(lista)
                    else:
                        print("Nu este nicio stare")
                    print("---------","Iteratie", iteratie, "---------")
                for c in self.sectiune_alfabet.continut:
                    #cautam un caracterul cu care incepe cuvantul
                    if mesaj.startswith(c):
                        mesaj = mesaj.removeprefix(c)
                        schimbare = True
                        if stare != None:
                            actiuni = self.sectiune_actiuni.getActiuni(stare, c)
                            if not len(actiuni):
                                # print("EROARE: Nu a fost gasita o actiune pentru", stare, "la inputul", c)
                                # exit()
                                if self.debug: print("Nu s-au gasit actiuni")
                                return False
                            actiuneAleasa: Actiune|None = None
                            for actiune in actiuni:
                                # conform definitiei de la exercitiul 1,
                                # trebuie sa fie doua functii pentru
                                # cazurile in care este/nu este caracterul in lista
                                if '!' in actiune.inLista:
                                    if actiune.inLista.replace('!','') not in lista:
                                        actiuneAleasa = actiune
                                        break
                                else:
                                    if actiune.inLista in lista or actiune.inLista == self.string_epsilon:
                                        actiuneAleasa = actiune
                                        break
                            #s-a gasit o actiune
                            if actiuneAleasa:
                                stare = actiuneAleasa.stare_urmatoare
                                if actiuneAleasa.scoate in lista and actiuneAleasa.scoate != self.string_epsilon:
                                    lista.remove(actiuneAleasa.scoate)
                                if  actiuneAleasa.introdu != self.string_epsilon:
                                    lista.append(actiuneAleasa.introdu)
                            else:
                                if self.debug: print("Nu s-a gasit o actiune")
                                return False

                        else:
                            # print("EROARE: Nu a fost gasita o actiune pentru", stare, "la inputul", c)
                            # exit()
                            if self.debug: print("Nu a fost gasita o stare")
                            return False
                        if self.debug:
                            print("---------","Iteratie final", iteratie, "---------")
                            if stare:
                                print(stare)
                                print(lista)
                            else:
                                print("Nu este nicio stare")
                            print("---------","Iteratie final", iteratie, "---------")
                if not schimbare:
                    print("Eroare: Unul sau mai multe caractere nu au fost gasite in alfabet: >" + mesaj)
                    exit()
                    break
                iteratie += 1
            if self.debug:
                if stare:
                    print("FINAL:", stare)
                else:
                    print("FINAL:", "Nu este nicio stare")
            if stare:
                return stare.final_state
            return False

###########################
#     Inceput program     #
###########################
"""
Pentru configuratia LA-ului, actiunile trebuie sa fie de forma:
#stare,input,inLista,stareUrmatoare,sterge,introdu
-stare = starea din care se verifica
-input = simbol citit de pe banda
-inLista = simbol care este sau nu in lista
--inLista poate avea semnul "!" inaintea caracterului pentru
a defini actiunea cand elementul nu se afla in lista
-stareUrmatoare = starea in care se trece
-sterge = elementul care se sterge din lista daca exista
-introdu = elementul care va fi introdus in lista
"""
nume_fisier = "lfa/la.txt"
#al doilea argument al obiectului specifica daca
#logurile sa fie afisate
la = LA(nume_fisier, True)
while True:
    if la.valideaza(input("string:")):
        print("ACCEPTAT")
    else:
        print("RESPINS")




