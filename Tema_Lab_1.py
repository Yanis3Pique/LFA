fisier = input("Dati numele fisierului: ") # Aici scriem in consola numele fisierului pe care vrem sa-l folosim
sectiuni = {}

def load(fisier):
    try:
        with open(fisier) as f:
            global sectiuni
            currentName = ""
            linie = f.readline()
            while linie:
                linie = linie.strip()
                # ignoram comentariile
                if linie.startswith('#') or linie == 'End':
                    linie = f.readline()
                    continue
                # vedem daca incepe o noua sectiune
                if linie.startswith("[") and linie.endswith("]"):
                    linie = linie.replace("[", "").replace("]", "")
                    currentName = linie
                    sectiuni[currentName] = []
                else:
                    if linie:
                        sectiuni[currentName].append(linie)
                    else:
                        print("Eroare: Formatul fisierului este incorect la linia " + linie)
                        return None
                # citim o linie noua
                linie = f.readline()
            return sectiuni
    except:
        return "Nu exista acest fisier!"

print(load(fisier))

def validate_alfabet(sectiuni):
    first_key = list(sectiuni.keys())[0]
    first_value = sectiuni[first_key]
    if first_value == []:
        print("Nu exista alfabet!")
    else:
        return True

def validate_stari(sectiuni):
    are_s = 0
    are_f = 0
    second_key = list(sectiuni.keys())[1]
    second_value = sectiuni[second_key]
    for x in second_value:
        if 's' in x:
            are_s = 1
        if 'f' in x:
            are_f = 1
    if are_s == 0 and are_f == 0:
        print("Nu exista stare de inceput si nici de final")
    elif are_s == 0:
        print("Nu exista stare de inceput")
    elif are_f == 0:
        print("Nu exista stare de inceput")
    else:
        return True

def validate_actiuni(sectiuni):
    third_key = list(sectiuni.keys())[2]
    third_value = sectiuni[third_key]
    if third_value == []:
        print("Nu exista actiuni")
    else:
        return True

def validate():
    try:
        if validate_alfabet(sectiuni) and validate_stari(sectiuni) and validate_actiuni(sectiuni):
            print("Validat <3")
    except:
        pass
validate()

def validate_input(input_string, sectiuni):
    sigma = sectiuni['Sigma']
    states = sectiuni['States']
    actions = sectiuni['Actions']
    start_state = [s for s in states if ',s' in s][0].replace(',s', '') # gaseste starea initiala
    current_state = start_state
    for c in input_string.strip():
        if c == sigma[0]: # daca cifra de input e 0
            pass # ramai in starea curenta
        elif c == sigma[1]: # daca cifra de input e 1
            next_state = current_state # aflam starea urmatoare
            for a in actions: # pentru fiecare actiune
                if a.startswith(current_state + ',' + sigma[1] + ','): # cautam actiunea care arata sub forma 'current_state,digit in input,'
                    next_state = a.split(',')[2]
                    break
            current_state = next_state
    condition = False
    for c in states:
        if ',f' in c and c.split(',')[0] == current_state:
            condition = True
    if condition == True: # starea curenta e stare finala
        return current_state + ', corect'
    else:
        return current_state + ', gresit'

print()
input_string = input("Dati un sir de comenzi: ")
print()

def verification_input(input_string):
    for x in input_string:
        if x not in sectiuni[list(sectiuni.keys())[0]]:
            return False
    return True

if verification_input(input_string):
    print(validate_input(input_string, sectiuni))
else:
    print("Input invalid!")