#
# Autori: Chirus Mina-Sebastian, Popescu Pavel-Yanis
#
#sectiune pentru LA
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
        setam direct in variabilele globale
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
                        #adaugam actiunea in lista. totul este ok
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
        iteratie = 0
        lista = []
        if self.sectiune_alfabet and self.sectiune_stari and self.sectiune_actiuni:
            #incepem cu starea initiala
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
                    if mesaj.startswith(c):
                        mesaj = mesaj.removeprefix(c)
                        schimbare = True
                        if stare != None:
                            actiuni = self.sectiune_actiuni.getActiuni(stare, c)
                            if not len(actiuni):
                                # print("EROARE: Nu a fost gasita o actiune pentru", stare, "la inputul", c)
                                # exit()
                                return False
                            actiuneAleasa: Actiune|None = None
                            for actiune in actiuni:
                                if '!' in actiune.inLista:
                                    if actiune.inLista.replace('!','') not in lista:
                                        actiuneAleasa = actiune
                                        break
                                else:
                                    if actiune.inLista in lista or actiune.inLista == self.string_epsilon:
                                        actiuneAleasa = actiune
                                        break
                            if actiuneAleasa:
                                stare = actiuneAleasa.stare_urmatoare
                                if actiuneAleasa.scoate in lista and actiuneAleasa.scoate != self.string_epsilon:
                                    lista.remove(actiuneAleasa.scoate)
                                if  actiuneAleasa.introdu != self.string_epsilon:
                                    lista.append(actiuneAleasa.introdu)
                            else:
                                print("Nu a fost o actiune aleasa")
                                return False

                        else:
                            # print("EROARE: Nu a fost gasita o actiune pentru", stare, "la inputul", c)
                            # exit()
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
                    # print("Eroare: Unul sau mai multe caractere nu au fost gasite in alfabet: >" + mesaj)
                    # exit()
                    return False
                iteratie += 1
            if self.debug:
                if stare:
                    print("FINAL:", stare)
                else:
                    print("FINAL:", "Nu este nicio stare")
            if stare:
                return stare.final_state
            return False


import random

#Codul de la gramatica scrisa la laborator
class SectiuneG:
    """
    Clasa memoreaza o sectiune in formatul specific
    """
    def __init__(self, nume: str, continut: list[str], gram) -> None:
        self.nume = nume
        self.continut = continut
        self.gram = gram
    
    def checkNSet(self):
        """
        Pentru a evita cautarea specifica a unei sectiuni,
        setam direct in obiectul CFG
        """
        if self.nume == self.gram.string_var:
            self.gram.sectiune_var = self
        if self.nume == self.gram.string_sigma:
            self.gram.sectiune_sigma = self
        if self.nume == self.gram.string_rules:
            self.gram.sectiune_rules = self

    @staticmethod
    def loadSectiuni(fisier: str, gram):
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
                    if linie.startswith('#') and len(linie) > 1:
                        linie = f.readline()
                        continue
                    #vedem daca incepe o noua sectiune
                    if linie.startswith("[") and linie.endswith("]"):
                        if currentSec:
                            currentSec.checkNSet()
                            sectiuni.append(currentSec)
                        
                        linie = linie.replace("[","").replace("]","")
                        if linie == gram.string_var:
                            currentSec = SectiuneG_Variables(gram, [])
                        elif linie == gram.string_sigma:
                            currentSec = SectiuneG_Sigma(gram, [])
                        elif linie == gram.string_rules:
                            currentSec = SectiuneG_Rules(gram, [])
                        else:
                            currentSec = SectiuneG(linie, [], gram)
                    else:
                        if currentSec:
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
        except Exception as ex:
            print(ex)
            print("Eroare: Fisierul nu exista!")
            exit()
            return None

class SectiuneG_Variables(SectiuneG):
    def __init__(self, gram, continut: list[str] = []) -> None:
        super().__init__(gram.string_var, continut, gram)
        self.verificat = False
    
    def variabilaValida(self, variabila: str) -> bool:
        "Functia se asigura ca argumentul apartine listei de variabile"
        for var in variabila.split(" "):
            if not var in self.continut and not var == self.gram.string_epsilon:
                return False
        return True

    def loadVariables(self) -> list[str]:
        "Functia verifica sa nu fie ambiguitate la citirea variabilelor"
        if self.verificat:
            return self.continut
        else:
            for x in self.continut:
                if x.isalpha() and not x.isupper():
                    print("Eroare: Caracterul", x ,"din variabile trebuie sa fie cu litere mari")
                    exit()
                    return []
                for y in self.continut:
                    if x != y:
                        if y.startswith(x):
                            print("Eroare: O variabila din lista de variabile o contine pe alta: " + y + " si " + x)
                            exit()
                            return [] 
            self.verificat = True
            return self.continut


class SectiuneG_Sigma(SectiuneG):
    def __init__(self, gram, continut: list[str] = []) -> None:
        super().__init__(gram.string_sigma, continut, gram)
        self.verificat = False
    
    def caracterValid(self, caracter: str) -> bool:
        "Functia se asigura ca argumentul apartine listei de caractere"
        return (caracter in self.continut) or (caracter == self.gram.string_epsilon)

    def loadSigma(self) -> list[str]:
        "Functia verifica sa nu fie ambiguitate la citirea de la sigma"
        if self.verificat:
            return self.continut
        else:
            for x in self.continut:
                for y in self.continut:
                    if x != y:
                        if y.startswith(x):
                            print("Eroare: O variabila din sigma o contine pe alta: " + y + " si " + x)
                            exit()
                            return [] 
            self.verificat = True
            return self.continut

class Strin:
    def __init__(self, strin: str, gram) -> None:
        self.strin = strin
        self.gram = gram
    
    def isVariable(self):
        return self.gram.sectiune_var.variabilaValida(self.strin)

    def isCharacter(self):
        return self.gram.sectiune_sigma.caracterValid(self.strin)

    def __str__(self):
        return self.strin
    def __repr__(self):
        return self.strin

class Rule:
    def __init__(self, strin_initial: Strin, strin_urmator: Strin) -> None:
        self.strin_initial = strin_initial
        self.strin_urmator = strin_urmator
    def __str__(self):
        return "["+str(self.strin_initial)+" -> "+str(self.strin_urmator)+"]"
    def __repr__(self):
        return "["+str(self.strin_initial)+" -> "+str(self.strin_urmator)+"]"

class SectiuneG_Rules(SectiuneG):
    def __init__(self, gram, continut: list[str] = []) -> None:
        super().__init__(gram.string_rules, continut, gram)
        self.rules: list[Rule] = []

    def isDone(self, strin: str) -> bool:
        """
        Functia verifica daca nu mai sunt variabile de inlocuit
        """
        for var in self.gram.sectiune_var.continut:
            if var in strin:
                return False
        return True

    def getRandomNext(self, banda: str) -> Rule:
        """
        Functia gaseste o regula aleatorie pentru o variabila
        """
        if self.rules:
            reguli = []
            for regula in self.rules:
                if regula.strin_initial.strin in banda:
                    reguli.append(regula)
            if not len(reguli): return None # type: ignore
            return random.choice(reguli)
        return None # type: ignore

    def isTerminal(self, terminal):
        """
        Functia verifica daca parametrul este un terminal
        """
        for variabila in self.gram.sectiune_var.continut:
            if variabila in terminal:
                return False
        return True

    def getRegulaTerminal(self, banda: str):
        """
        Functia intoarce o regula aleatoare care are un terminal
        """
        if self.rules:
            reguli = []
            for regula in self.rules:
                if regula.strin_initial.strin in banda and self.isTerminal(regula.strin_urmator.strin):
                    reguli.append(regula)
            if not len(reguli): return None
            return random.choice(reguli)
        return None
    
    def valideazaRegula(self, parte2Regula: str) -> bool:
        """
        Functia valideaza o regula
        """
        for vari in self.gram.sectiune_var.continut:
            for var in vari.split(" "):
                while var in parte2Regula:
                    parte2Regula = parte2Regula.replace(var, "")
        for caractere in self.gram.sectiune_sigma.continut:
            for caracter in caractere.split(" "):
                while caracter in parte2Regula:
                    parte2Regula = parte2Regula.replace(caracter, "")
        return not parte2Regula.strip().replace(self.gram.string_epsilon,"")

    def loadRules(self) -> list[Rule]:
        """
        Functia verifica si incarca regulile
        """
        if not self.rules:
            if not self.gram.sectiune_var or not self.gram.sectiune_sigma:
                print("Eroare: Sigma sau Variabilele nu sunt initializate si se incearca incarcarea Regulilor")
                return []
            for rule_str in self.continut:
                rule = rule_str.split("->")
                if len(rule) == 2:
                    strin_initial, strin_final = rule
                    for term in strin_final.split('|'):
                        if self.gram.sectiune_var.variabilaValida(strin_initial) and self.valideazaRegula(term):
                            initial = Strin(strin_initial, self.gram)
                            final = Strin(term, self.gram)
                            self.rules.append(Rule(initial, final))
                        elif not self.gram.sectiune_var.variabilaValida(strin_initial):
                            print("Eroare: Variabila '" + strin_initial + "' nu este valida")
                            exit()
                            return []
                        else:
                            print("Eroare: Partea a doua a regulii '" + term + "' nu este valida")
                            exit()
                            return []
                else:
                    if not rule_str.replace(" ",""):
                        print("Eroare: Configuratia nu accepta linii goale")
                    else:
                        print("Eroare: Configuratia '" + rule_str + "' nu este corecta")
                    exit()
                    return []

        return self.rules


class CFG:
    def __init__(self, nume_fisier: str, debug: bool = False) -> None:
        #declaram variabilele pentru headerele din configuratie
        #[Variables]
        self.string_var = "Variables"
        #[Sigma]
        self.string_sigma = "Sigma"
        #[Rules]
        self.string_rules = "Rules"
        self.string_epsilon = "*"

        self.debug = debug

        #typehinting la sectiuni
        self.sectiune_var: SectiuneG_Variables
        self.sectiune_sigma: SectiuneG_Sigma
        self.sectiune_rules: SectiuneG_Rules

        if self.debug:
            print("------SE INCARCA------")
            print("FISIER", nume_fisier)
        
        # Metoda de mai jos returneaza toate sectiunile din configuratie
        # + instantiaza obiectele corespunzatoare variabilelor, alfabetului si
        # a regulilor
        self.sectiuni = SectiuneG.loadSectiuni(nume_fisier, self)
        # Daca apare o eroare, pentru siguranta programului,
        # acesta se va inchide
        # iar mesajul cu eroarea este afisat in consola

        # ne asiguram ca toate sectiunile sunt ok
        # si incarcam configuratiile in obiecte
        try:
            if self.sectiune_var:
                if self.debug:
                    print("VARIABILE", self.sectiune_var.loadVariables())
                else:
                    self.sectiune_var.loadVariables()
        except:
            print("EROARE: SectiuneGa cu headerul","["+self.string_var+"]","nu a fost gasita in configuratie")
            exit()
        
        try:
            if self.sectiune_sigma:
                if self.debug:
                    print("SIGMA", self.sectiune_sigma.loadSigma())
                else:
                    self.sectiune_sigma.loadSigma()
        except:
            print("EROARE: SectiuneGa cu headerul","["+self.string_sigma+"]","nu a fost gasita in configuratie")
            exit()

        try:
            if self.sectiune_rules:
                if self.debug:
                    print("REGULI", self.sectiune_rules.loadRules())
                else:
                    self.sectiune_rules.loadRules()
        except:
            print("EROARE: SectiuneGa cu headerul","["+self.string_rules+"]","nu a fost gasita in configuratie")
            exit()
        if self.debug: print("------INCARCAT------")
        
    def genereaza(self, lim_max=4000)->str:
        """
        Functia genereaza o singura propozitie.
        "lim_max" obliga programul dupa iteratia cu numarul "lim_max"
        sa aplice terminali oriunde poate
        """
        if not self.sectiune_var or not self.sectiune_rules or not self.sectiune_sigma:
            print("EROARE: Obiectele nu sunt instantiate")
            exit()
        banda = self.sectiune_rules.rules[0].strin_urmator.strin
        nrGenerari = 0
        while not self.sectiune_rules.isDone(banda):
            reg = None
            if nrGenerari > lim_max:
                reg = self.sectiune_rules.getRegulaTerminal(banda)
            if not reg:
                regula = self.sectiune_rules.getRandomNext(banda)
            else:
                regula = reg
            if regula:
                banda = banda.replace(regula.strin_initial.strin, regula.strin_urmator.strin, 1).replace(self.string_epsilon,"")
            nrGenerari+=1
        while "  " in banda:
            banda = banda.replace("  ", " ")
        return banda.strip()
    
    
    def genereazaNr(self, nr: int, lim_max: int = 4000):
        """
        Functia genereaza un numar "nr" de proprozitii.
        "lim_max" obliga programul dupa iteratia cu numarul "lim_max"
        sa aplice terminali oriunde poate
        """
        rez = []
        for _ in range(nr):
            generat = self.genereaza(lim_max)
            rez.append(generat)
            if self.debug:
                print("---------------------------")
                print("GENERAT", generat)
        return rez


#codul de la PDA de la laborator
class SectiuneP:
    """
    Clasa memoreaza o sectiune in formatul specific
    """
    def __init__(self, nume: str, continut: list[str], pda) -> None:
        self.pda = pda
        self.nume = nume
        self.continut = continut
    
    def checkNSet(self):
        """
        Pentru a evita cautarea specifica a unei sectiuni,
        setam direct in obiect
        """
        if self.nume == self.pda.string_alfabet:
            self.pda.sectiune_alfabet = self
        if self.nume == self.pda.string_gama:
            self.pda.sectiune_gama = self
        if self.nume == self.pda.string_stari:
            self.pda.sectiune_stari = self
        if self.nume == self.pda.string_actiuni:
            self.pda.sectiune_actiuni = self
    

    @staticmethod
    def loadSectiuni(fisier: str, pda) -> list:
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
                        if linie == pda.string_alfabet:
                            currentSec = SectiuneP_Alfabet(pda, [])
                        elif linie == pda.string_stari:
                            currentSec = SectiuneP_Stari(pda, [])
                        elif linie == pda.string_actiuni:
                            currentSec = SectiuneP_Actiuni(pda, [])
                        elif linie == pda.string_gama:
                            currentSec = SectiuneP_Gama(pda, [])
                        else:
                            currentSec = SectiuneP(linie, [], pda)
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
        except Exception as e:
            print(e)
            print("Eroare: Fisierul nu exista!")
            exit()
            # SectiuneP.delAll()
            return None

class SectiuneP_Alfabet(SectiuneP):
    def __init__(self, pda, continut: list[str] = []) -> None:
        super().__init__(pda.string_alfabet, continut, pda)
        self.verificat = False
    
    def cuvantValid(self, cuvant: str) -> bool:
        "Functia se asigura ca argumentul apartine alfabetului"
        return (cuvant in self.continut) or (cuvant == self.pda.string_epsilon)

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
                            # self.delAll()
                            exit()
                            return [] 
            self.verificat = True
            return self.continut

class SectiuneP_Gama(SectiuneP):
    def __init__(self, pda, continut: list[str] = []) -> None:
        super().__init__(pda.string_gama, continut, pda)
        self.verificat = False
    
    def cuvantValid(self, cuvant: str) -> bool:
        "Functia se asigura ca argumentul apartine multimii gama"
        return (cuvant in self.continut) or (cuvant == self.pda.string_epsilon)

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

class StareP:
    "Obiectul corespunzator unei stari care poate prelua si o stiva de la alte stari"
    def __init__(self, stare_str: str, initial_state: bool = False, final_state: bool = False, stack: list[str] = []) -> None:
        self.stare_str = stare_str
        self.initial_state = initial_state
        self.final_state = final_state
        self.stack = stack

    "Intstructiunile de mai jos ne ajuta sa dam print() direct"
    "la ce ne intereseaza cand incercam sa vedem obiectul"
    def __str__(self):
        statusStareP = ""
        if self.initial_state: statusStareP+=" INIT"
        if self.final_state: statusStareP+=" FIN"
        return "["+self.stare_str+":"+statusStareP+" - "+str(self.stack)+"]"
    def __repr__(self):
        statusStareP = ""
        if self.initial_state: statusStareP+=" INIT"
        if self.final_state: statusStareP+=" FIN"
        return "["+self.stare_str+":"+statusStareP+" - "+str(self.stack)+"]"



class SectiuneP_Stari(SectiuneP):
    "SectiuneP speciala care incarca si retine starile"
    def __init__(self, pda, continut: list[str] = []) -> None:
        super().__init__(pda.string_stari, continut, pda)
        self.stari = []
        self.initState = None
        self.stari_dict = {}

    def getStareP(self, stare_str: str) -> StareP | None:
        """
        Functia gaseste starea cu un nume dat
        """
        if stare_str in self.stari_dict.keys():
            return self.stari_dict[stare_str]
        else:
            return None
    def getStarePInitiala(self) -> StareP:
        """
        Functia returneaza starea de inceput
        """
        if not self.initState:
            self.stari = [self.stari_dict[x] for x in self.stari_dict.keys()]
            for stare in self.stari:
                if stare.initial_state:
                    self.initState = stare
                    break
        return self.initState # type: ignore

    def loadStari(self) -> list[StareP]:
        """
        Functia verifica si incarca toate starile
        """
        if not len(self.stari_dict.keys()):
            for stare_str in self.continut:
                if ',' in stare_str:
                    state, info = stare_str.split(",", 1)
                    if self.getStareP(state):
                        print("Eroare: StarePa "+state+" a fost definita de 2 ori!")
                        # self.delAll()
                        exit()
                        return []
                    info = info.lower()
                    if 's' in info:
                        if not self.initState:
                            final_state = 'f' in info
                            self.initState = StareP(state, initial_state=True, final_state=final_state)
                            self.stari_dict[state] = self.initState
                        else:
                            print("Eroare: S-au gasit mai multe stari initiale")
                            # self.delAll()
                            exit()
                            return []
                    elif 'f' in info:
                        self.stari_dict[state] = StareP(state, final_state=True)
                    else:
                        print("Eroare: O stare poate fi simpla, finala(f) sau initiala(s). StarePa '"+info+"' nu exista")
                        # self.delAll()
                        exit()
                        return []
                else:
                    if self.getStareP(stare_str):
                        print("Eroare: StarePa "+stare_str+" a fost definita de 2 ori!")
                        # self.delAll()
                        exit()
                        return []
                    self.stari_dict[stare_str] = StareP(stare_str)
            if not self.initState:
                print("Eroare: Nu exista o stare initiala")
                # self.delAll()
                exit()
                return []
        self.stari = [self.stari_dict[x] for x in self.stari_dict.keys()]
        return self.stari

class ActiuneP:
    """
    Clasa ne ajuta sa tinem cont de toate tranzitiile mai usor
    """
    def __init__(self, stare_initiala: StareP, conditie_stare: str, scoate_stiva: str, introdu_stiva: str, stare_urmatoare: StareP) -> None:
        self.stare_initiala = stare_initiala
        self.conditie_stare = conditie_stare
        self.scoate_stiva = scoate_stiva
        self.introdu_stiva = introdu_stiva
        self.stare_urmatoare = stare_urmatoare
    
    "Intstructiunile de mai jos ne ajuta sa dam print() direct"
    "la ce ne intereseaza cand incercam sa vedem obiectul"
    def __str__(self):
     return "["+self.stare_initiala.stare_str+" -> "+self.conditie_stare+", "+self.scoate_stiva+", "+self.introdu_stiva+" -> "+self.stare_urmatoare.stare_str+"]"
    def __repr__(self):
        return "["+self.stare_initiala.stare_str+" -> "+self.conditie_stare+", "+self.scoate_stiva+", "+self.introdu_stiva+" -> "+self.stare_urmatoare.stare_str+"]"
class SectiuneP_Actiuni(SectiuneP):
    def __init__(self, pda, continut: list[str] = []) -> None:
        super().__init__(pda.string_actiuni, continut, pda)
        self.actiuni: list[ActiuneP] = []

    def getActiuni(self, stare_initiala: StareP, conditie_stare: str) -> list[ActiuneP]:
        """
        Functia gaseste o multime de actiuni pentru o anumita stare si o conditie data
        """
        if self.actiuni:
            ret_actiuni = []
            for actiune_pos in self.actiuni:
                if actiune_pos.stare_initiala.stare_str == stare_initiala.stare_str and actiune_pos.conditie_stare == conditie_stare:
                    if actiune_pos.scoate_stiva == self.pda.string_epsilon or (len(stare_initiala.stack) > 0 and stare_initiala.stack[-1] == actiune_pos.scoate_stiva):
                        ret_actiuni.append(actiune_pos)
            return ret_actiuni
        return []

    def loadActiuni(self) -> list[ActiuneP]:
        """
        Functia verifica si incarca delta
        """
        if not self.actiuni:
            if not self.pda.sectiune_alfabet or not self.pda.sectiune_stari:
                print("Eroare: Alfabetul sau Starile nu sunt initializate si se incearca incarcarea Actiunilor")
                # self.delAll()
                exit()
                return []
            for actiune_str in self.continut:
                actiune = actiune_str.split(",")
                if len(actiune) == 5:
                    fr_s, cond, scoate, introd, to_s = actiune
                    fr = self.pda.sectiune_stari.getStareP(fr_s)
                    to = self.pda.sectiune_stari.getStareP(to_s)
                    if to and self.pda.sectiune_alfabet.cuvantValid(cond) and fr:
                        if (self.pda.sectiune_alfabet.cuvantValid(scoate) or self.pda.sectiune_gama.cuvantValid(scoate)) and (self.pda.sectiune_alfabet.cuvantValid(introd) or self.pda.sectiune_gama.cuvantValid(introd)):
                            self.actiuni.append(ActiuneP(fr, cond, scoate, introd, to))
                        else:
                            print("Eroare: Un caracter din delta nu se gaseste in dictionare:",scoate, introd)
                            # self.delAll()
                            exit()
                            return []
                    elif not fr:
                        print("Eroare: StarePa '" + fr_s + "' nu este valida")
                        # self.delAll()
                        exit()
                        return []
                    elif not self.pda.sectiune_alfabet.cuvantValid(cond):
                        print("Eroare: Caracterul '" + cond + "' nu este in dictionar")
                        # self.delAll()
                        exit()
                        return []
                    elif not to:
                        print("Eroare: StarePa '" + to_s + "' nu este valida")
                        # self.delAll()
                        exit()
                        return []
                else:
                    print("Eroare: Configuratia '" + actiune_str + "' nu este corecta")
                    # self.delAll()
                    exit()
                    return []

        return self.actiuni


class PDA:
    def __init__(self, sigma: list[str], gama: list[str], stari: list[StareP], actiuni: list[ActiuneP], debug: bool = False) -> None:
        self.string_alfabet = "Sigma"
        self.string_stari = "States"
        self.string_actiuni = "Actions"
        self.string_gama = "Gama"
        self.string_epsilon = "*"

        self.debug = debug

        self.sectiune_alfabet: SectiuneP_Alfabet = SectiuneP_Alfabet(self, sigma)
        self.sectiune_gama: SectiuneP_Gama = SectiuneP_Gama(self, gama)
        self.sectiune_stari: SectiuneP_Stari = SectiuneP_Stari(self, [])
        self.sectiune_actiuni: SectiuneP_Actiuni = SectiuneP_Actiuni(self, [])

        if self.debug:
            print("------SE INCARCA------")
        
        #initializam starile si actiunile primite de la gramatica
        for st in stari:
            self.sectiune_stari.stari_dict[st.stare_str] = st
        
        self.sectiune_stari.getStarePInitiala()
        self.sectiune_actiuni.actiuni = actiuni

        if self.debug:
            print("STARI:")
            for st in self.sectiune_stari.stari:
                print(st)

            print("ACTIUNI:")
            for ac in self.sectiune_actiuni.actiuni:
                print(ac)

            print("------INCARCAT------")
        
    def cloneazaStareP(self, parinte: StareP, scoateStiva: str, puneStiva: str, fiu: StareP):
        """
        Functia face un nou obiect de tip StareP si face
        operatiile necesare pe stiva
        """
        stivaFin = list(parinte.stack)
        if scoateStiva != self.string_epsilon and len(stivaFin) > 0:
            stivaFin.pop(-1)
        if puneStiva != self.string_epsilon:
            stivaFin.append(puneStiva)
        
        return StareP(fiu.stare_str, fiu.initial_state, fiu.final_state, stivaFin)
    
    def getStariDinStariCuEpsilon(self, stari_init: list[StareP]) -> list[StareP]:
        """
        Functia aduna toate starile care sunt legate prin epsilon
        din lista de stari "stari_init"
        """
        stari: list[StareP] = []
        for stare in stari_init:
            
            for epsi_act in self.sectiune_actiuni.getActiuni(stare, self.string_epsilon):
                    stari.append(
                        self.cloneazaStareP(stare, epsi_act.scoate_stiva, epsi_act.introdu_stiva, epsi_act.stare_urmatoare)
                    )
            
        if len(stari) > 0:
            try:
                stari_aditionale = self.getStariDinStariCuEpsilon(stari)
                while len(stari_aditionale) > 0:
                    stari.extend(stari_aditionale)
                    stari_aditionale = self.getStariDinStariCuEpsilon(stari_aditionale)
            except RecursionError as err:
                print("EROARE: Ciclu epsilon infinit!")
                exit()
        return stari

    def valideaza(self, mesaj: str)->bool:
        """
        Functia valideaza/invalideaza un string
        """
        iteratie = 0
        if self.sectiune_alfabet and self.sectiune_stari and self.sectiune_actiuni:
            stari = [self.sectiune_stari.getStarePInitiala()]
            while mesaj:
                iteratie += 1
                schimbare = False
                schimbareGasita = ""
                #facem tranzitiile epsilon fara sa citim
                sce = self.getStariDinStariCuEpsilon(stari)
                stari.extend(sce)
                if self.debug:
                    print("---------","Iteratie", iteratie, "---------")
                    if stari:
                        for stare in stari:
                            print(stare)
                    else:
                        print("Nu sunt stari")
                    print("---------","Iteratie", iteratie, "---------")
                for c in self.sectiune_alfabet.continut:
                    if mesaj.startswith(c):
                        schimbare = True
                        schimbareGasita = c
                        stariNoi = []
                        for stare in stari:
                            actiuni = self.sectiune_actiuni.getActiuni(stare, c)
                            for actiune in actiuni:
                                stariNoi.append(
                                    self.cloneazaStareP(stare, actiune.scoate_stiva, actiune.introdu_stiva, actiune.stare_urmatoare)
                                )
                        stari = stariNoi
                        if self.debug:
                            print("---------","Iteratie", iteratie, "final", "---------")
                            if stari:
                                for stare in stari:
                                    print(stare)
                            else:
                                print("Nu sunt stari")
                            print("---------","Iteratie", iteratie, "final", "---------")
                        break
                if not schimbare:
                    # print("Eroare: Unul sau mai multe caractere nu au fost gasite in alfabet: >" + mesaj)
                    # exit()
                    return False
                else:
                    mesaj = mesaj.removeprefix(schimbareGasita)
            sce = self.getStariDinStariCuEpsilon(stari)
            stari.extend(sce)
            if self.debug: print("Final", stari)
            return True in [x.final_state for x in stari]
        else:
            print("EROARE: Obiectele nu sunt instantiate")
            exit()


class ConvertorInPDA:
    def __init__(self, cfg: CFG, debug: bool) -> None:
        self.cfg = cfg
        self.debug = debug
    def pushString(self, stareInit: StareP, cond: str, scoate: str, deAdaugat: list[str], stareFinal: StareP):
        """
        Aceasta functie introduce intre stareInit si stareFinal stari si actiuni noi
        pentru a putea da push pe stiva la mai multe
        cuvinte din gama
        """
        #introducem in ordine inversa
        deAdaugat.reverse()
        rezStari: list[StareP] = []
        #facem starile mai intai
        for i, adaug in enumerate(deAdaugat):
            if i < len(deAdaugat)-1:
                p = StareP("q"+"".join(deAdaugat)+str(i), False, False, [])
                rezStari.append(p)
        #facem actiunile pentru fiecare pereche de stari
        rezActiuni: list[ActiuneP] = []
        #prima actiune
        rezActiuni.append(ActiuneP(stareInit, cond, scoate, deAdaugat[0], rezStari[0]))
        for i, adaug in enumerate(deAdaugat):
            if i < len(deAdaugat)-2:
                rezActiuni.append(ActiuneP(rezStari[i], '*', '*', deAdaugat[i+1], rezStari[i+1]))
            else: break
        #ultima actiune
        rezActiuni.append(ActiuneP(rezStari[-1], '*', '*', deAdaugat[-1], stareFinal))
        return rezStari, rezActiuni

    def getRulesArray(self, strin: str):
        """
        Aceasta functie descompune un string in cuvintele din gama si sigma
        """
        rez = []
        schimbare = True
        while schimbare:
            schimbare = False
            for var in self.cfg.sectiune_var.continut:
                if strin.startswith(var):
                    rez.append(var)
                    strin = strin.removeprefix(var)
                    schimbare = True
            for term in self.cfg.sectiune_sigma.continut:
                if strin.startswith(term):
                    rez.append(term)
                    strin = strin.removeprefix(term)
                    schimbare = True
        return rez
            

    def convToPDA(self) -> PDA:
        new_sigma = []
        #pregatim un nou sigma
        for term in self.cfg.sectiune_rules.rules:
            if self.cfg.sectiune_rules.isTerminal(term.strin_urmator.strin):
                new_sigma.append(term.strin_urmator.strin)
        new_sigma = list(dict.fromkeys(new_sigma))
        #pregatim un nou gama
        new_gama = []
        for term in self.cfg.sectiune_rules.rules:
            if not self.cfg.sectiune_rules.isTerminal(term.strin_urmator.strin):
                new_gama.extend(self.getRulesArray(term.strin_urmator.strin))
        new_gama = list(dict.fromkeys(new_gama))

        #initializam cele 3 stari
        sInit = StareP("qinit", True, False, [])
        sLoop = StareP("qloop", False,False,[])
        sFin = StareP("qfin", False, True, [])
        lista_stari = [sInit, sLoop, sFin]

        actiuni = []
        # dam push pe stiva la prima variabila din gramatica si la simbolul $
        # intre sInit si sLoop
        newStates, newActions = self.pushString(sInit, '*', '*', [self.cfg.sectiune_rules.rules[0].strin_initial.strin,"$"], sLoop)
        lista_stari.extend(newStates)
        actiuni.extend(newActions)

        for regula in self.cfg.sectiune_rules.rules:
            # daca sunt variabile, ne asiguram ca sunt inlocuite
            # de regulile care le substituie
            if not self.cfg.sectiune_rules.isTerminal(regula.strin_urmator.strin):
                newStates, newActions = self.pushString(sLoop, '*', regula.strin_initial.strin, self.getRulesArray(regula.strin_urmator.strin), sLoop)
                lista_stari.extend(newStates)
                actiuni.extend(newActions)
            else:
                #daca sunt terminali, ne asiguram ca vor inlocui variabila
                actiuni.append(ActiuneP(sLoop, '*', regula.strin_initial.strin, regula.strin_urmator.strin, sLoop))
        for t in new_sigma:
            #asiguram sa nu fie ciclu infinit de epsilon
            if t != self.cfg.string_epsilon:
                #ne asiguram ca un terminal citit nu mai este pe stiva
                actiuni.append(ActiuneP(sLoop, t, t, '*', sLoop))
        
        #adaugam tranzitia dintre sLoop si sFin
        actiuni.append(ActiuneP(sLoop, '*', '$', '*', sFin))
        return PDA(new_sigma, new_gama, lista_stari, actiuni, self.debug)

###########################
#     Inceput program     #
###########################

"""
Programul foloseste LA-ul pentru a valida miscarea jucatorului(go),
pentru a valida camerele adiacente(look) dar si camera de final.
Am scris mai multe tipuri de tranzitii in configuratie:
s[Camera] - pentru setarea camerei, indiferent de pozitia in care se afla
l[Camera] - pentru validarea camerelor adiacente
fSecret Exit - pentru validarea camerei de final

comanda go:
    programul valideaza daca se poate ajunge in camera dorita
    tinand cont de inventar apoi seteaza camera curenta iar
    apoi adauga camera in care se vrea sa se ajunga. Acolo se valideaza/invalideaza
    tinand cont de toate informatiile de mai sus.
    Acest lucru se executa la fiecare comanda.
comanda look:
    se itereaza prin toate camerele posibile
    si se valideaza fiecare in parte.
comanda take:
    se verifica daca se poate lua obiectul respectiv
    din camera.

Textul jucatorului este verificat de un PDA rezultat dinamic dintr-un CFG.
"""

def main():
    nume_fisier = "lfa/la-castel.txt"
    la = LA(nume_fisier, False)
    nume_fisier_gramatica = "lfa/la-cfg.txt"
    gram = CFG(nume_fisier_gramatica, False)
    conv = ConvertorInPDA(gram, False)
    pdaco = conv.convToPDA()

    locatii = {
        "Entrance Hall": ["key"],
        "Dining Room": ["invitation", "chef's hat"],
        "Kitchen": ["spoon"],
        "Armoury": ["sword","crown"],
        "Treasury": ["ancient coin"],
        "Library": ["spell book"],
        "Pantry": [],
        "Throne Room": [],
        "Wizard's Study": ["magic wand"],
        "Secret Exit": [],
    }
    
    inventar = []
    print("Welcome adventurer! Select an action to begin!")
    print("go [room name]")
    print("look")
    print("inventory")
    print("take [item]")
    print("drop [item]")
    camere = ["Dining Room"]
    while True:
        alegere = input("Enter your choice: ")
        if not pdaco.valideaza(alegere.replace(" ","", 1)):
            print("The PDA does not recognize this command.")
            continue
        if alegere.lower().startswith('go '):
            #extragem camera din comanda
            room = alegere.split(" ", 1)[1]
            #setam toate itemele + camera curenta si adaugam camera urmatoare
            #pentru a vedea daca se valideaza
            if la.valideaza("".join(inventar)+"s"+camere[-1]+room):
                camere.append(room)
                print("You enter in", room)
                if la.valideaza("s"+camere[-1]+"f"+room):
                    print("The magic was broken. Your need for knowledge made you to see the world as it is.")
                    exit()
            else:
                print("You cannot go there!")
        elif alegere.lower() == "look":
            for item in locatii[camere[-1]]:
                print("Item on floor: "+item)
            # pentru fiecare camera validam comanda l[Camera]
            # pentru a vedea daca sunt adiacente camerei curente
            for lCamera in locatii.keys():
                if la.valideaza("s"+camere[-1]+"l"+lCamera):
                    print("Door to: "+lCamera)
        elif alegere.lower() == "inventory":
            print("You look in your infinite bag and see:")
            if inventar:
                for item in inventar:
                    print("- "+item)
            else:
                print("Nothing")
        elif alegere.lower().startswith('take '):
            item = alegere.split(" ", 1)[1]
            if item in locatii[camere[-1]]:
                #validam daca se poate lua obiectul respectiv din camera
                if la.valideaza("".join(inventar)+"s"+camere[-1]+item):
                    inventar.append(item)
                    locatii[camere[-1]].remove(item)
                    print("You took a", item)
                else:
                    print("That item was not found in the", camere[-1])
            else:
                print("That item was not found in the", camere[-1])
        elif alegere.lower().startswith('drop '):
            item = alegere.split(" ", 1)[1]
            if item in inventar:
                locatii[camere[-1]].append(item)
                inventar.remove(item)
                print("You dropped", item, "in", camere[-1])
            else:
                print("You don't have", item)
            
        else:
            print("Invalid choice. Please try again.")



main()




