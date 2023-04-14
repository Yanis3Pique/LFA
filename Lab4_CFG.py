fisier = input("Dati numele fisierului: ") # Aici scriem in consola numele fisierului pe care vrem sa-l folosim
sectiuni = {} # Aici initilizam multimea starilor(care e defapt un dictionar) cu o multime goala
valid_file_name = True # Presupunem pentru moment ca acest contor nr 1 este valid

def load(fisier): # Definim functia de incarcare a datelor din fisier
    try: # Se incearca deschiderea fisierului
        with open(fisier) as f: # Deschidem fisierul f
            global sectiuni # Folosim multimea sectiunilor declarata global
            currentName = "" # Numele curent al sectiunii este gol
            linie = f.readline() # Citim prima linie din fisier
            while linie: # Cat timp avem ce linie sa citim
                linie = linie.strip() # Eliminam spatiile laterale inutile de pe fiecare linie
                # ignoram comentariile
                if (linie.startswith('#') and len(linie) > 1) or linie == 'End':
                    linie = f.readline()  # Adica sarim peste linia curenta
                    continue
                # vedem daca incepe o noua sectiune
                if linie.startswith("[") and linie.endswith("]"): # Daca linia e de forma [nume], atunci am dat peste o noua sectiune
                    linie = linie.replace("[", "").replace("]", "") # Formatam linia curenta pentru a salva doar ce este in interiorul "[]"
                    currentName = linie # Numele sectiunii curente devine linia formatata anterior
                    sectiuni[currentName] = [] # Initializam o lista vida pentru sectiunea curenta
                else: # Daca inia NU e de forma [nume], atunci aici se afla date pentru sectiunea curenta
                    if linie: # Daca linia nu e goala
                        if '->' in linie:
                            sublista_stanga = linie.split('->')[0]  # In sublista stanga se afla un singur element(simbol din var), de la care plecam
                            sublista_dreapta = linie.split('->')[1]  # In sublista dreapta se afla elementul(simbolul/simbolurile) care va inlocui sublista stanga
                            vector_dreapta = sublista_dreapta.split('|')
                            for element in vector_dreapta:  # Luam fiecare element din sublista dreapta
                                sectiuni[currentName].append(str(sublista_stanga + '->' + element)) # Adaugam linia(datele) la lista sectiunii curente
                        else:
                            sectiuni[currentName].append(linie)  # Adaugam linia(datele) la lista sectiunii curente
                    else: # Daca linia e goala
                        print("Eroare: Formatul fisierului este incorect la linia " + linie) # Evident mesajul
                        return None
                # citim o linie noua
                linie = f.readline()
            return sectiuni # La final returnam toate sectiunile
    except: # Daca nu exista numele fisierului returnam mesajul corespunzator
        global valid_file_name
        valid_file_name = False
        return "Nu exista acest fisier!"

print(load(fisier)) # Vedem ce a facut functia noastra loader
var = sectiuni[list(sectiuni.keys())[0]] # Preluam lista cu variabilele
sigma = sectiuni[list(sectiuni.keys())[1]] # Preluam lista cu sigma
rules = sectiuni[list(sectiuni.keys())[2]] # Preluam lista cu regulile
start_state = var[0].split(',')[0]

def validate_var(): # Validam variabilele
    are_s = 0 # Momentan presupunem ca nu avem variabila de start
    for element in var: # Luam fiecare element din lista
        if '*' in element: # Daca gasim un '*'
            are_s = 1 # Inseamna ca exista variabila de start
        for character in element:
            if (character < 'A' or character > 'Z') and (character != ',' and character != '*'):  # Daca variabilele sunt scrise cu litere mici
                return False  # Evident mesajul
    if are_s == 0: # Daca nu exista variabila de start
        print("Nu exista stare de inceput") # Evident mesajul
        return False # Evident mesajul
    if var == []: # Daca nu exista variabile
        return False # Evident mesajul
    else: # Daca nu se intampla nimic pana acum, nu avem probleme
        return True # Si atunci avem variabile valide

def validate_sigma(): # Validam sigma
    if sigma == []: # Daca nu gasim nimic
        print("Nu exista sigma!") # Evident mesajul
        return False # Evident mesajul
    for simbol in sigma: # Luam fiecare simbol din sigma
        if simbol.isupper(): # Verificam sa nu fie litere mari
            return False # Evident mesajul
    else: # Daca gasim totusi ceva
        return True # Atunci avem sigma

def validate_rules(): # Validam regulile
    for element in rules: # Luam fiecare element din lista
        if len(element.split('->')) != 2: # Daca fiecare element(sublista) din lista are mai putin/mai mult de 2 elemente
            return False # Invalid
        else: # Daca totusi elementul are fix 2 elemente, impartim elementul in doua subliste
            sublista_stanga = element.split('->')[0] # In sublista stanga se afla un singur element(simbol din var), de la care plecam
            sublista_dreapta = element.split('->')[1] # In sublista dreapta se afla elementul(simbolul/simbolurile) care va inlocui sublista stanga
            if (sublista_stanga not in var) and ((sublista_stanga + ',*') not in var): # Daca elementul(sublista stanga)
                return False # Invalid
            vector_dreapta = sublista_dreapta.split('|')
            for posibile_transformari_dreapta in vector_dreapta:
                for element in posibile_transformari_dreapta.split(','): # Luam fiecare element din sublista dreapta
                    # Daca elementul nu se regaseste nici in var nici in sigma
                    if (element not in var) and ((element + ',*') not in var) and (element not in sigma) and (element not in sigma):
                        return False # Invalid
    if rules == []: # Daca lista e goala
        print("Nu exista reguli!") # Evident mesajul
    else: # Daca totul e bine pana acum
        return True # Atunci avem reguli valide

def validate(): # Validam intreg fisierul
    try: # Incercam sa apelam functia
        if validate_var() and validate_sigma() and validate_rules(): # Daca cele 3 functii anterioare sunt validate
            print("Validat <3") # Evident mesajul <3
        else: # Daca nu sunt validate toate cele 3 functii anterioare
            global valid_file_name # Folsim contorul nr 1 global de mai sus
            valid_file_name = False # Atunci contorul nr 1 nostru devine fals
            print("Invalidat!") # Evident mesajul
    except: # Daca nu putem sa utilizam functia
        pass # Trecem peste
validate() # Acum validam fisierul de intrare cu totul

import random

def generate_word(rules):
    word = var[0].split(',')[0] # Initialize the word
    rule_applied = True # Flag to keep track of whether we've applied a rule
    while rule_applied:
        # Filter rules that can be applied to the word
        applicable_rules = [rule.replace(',', '') for rule in rules if rule[0] in word]
        if applicable_rules:
            rule_index = random.randint(0, len(applicable_rules)-1) # Choose a random applicable rule
            rule = applicable_rules[rule_index] # Get the chosen rule
            if "->" in rule: # If the rule has a "->" symbol, it's a replacement rule
                lhs, rhs = rule.split("->")
                if rhs=='~': rhs=''
                word = word.replace(lhs, rhs)
                print(word)
            elif "->~" in rule: # If the rule has a "->~" symbol, it's a terminal rule
                pass
        else:
            rule_applied = False # No more applicable rules
    return word

i = 0
numar_executii = int(input("Dati de cate ori sa se execute functia/generarea de cuvinte: "))
while i < numar_executii:
    print(i+1,":")
    generate_word(rules)
    print('\n')
    i += 1
