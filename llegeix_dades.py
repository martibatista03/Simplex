def llegeix_dades(direccio_dades):
    # Definim el problema a resoldre
    numero_estudiant = 27
    numero_problema = 3
    llegint_problema = False

    llegint_costos = False
    llegint_constriccions = False
    llegint_b = False
    comptador_constriccions = 0

    vector_costos = []
    matriu_constriccions = []
    vector_b = []

    with open(direccio_dades, "r") as dades:
        lectura_numero_estudiant = ""
        if (numero_estudiant >= 10):
            lectura_numero_estudiant = "dades "
        else:
            lectura_numero_estudiant = "dades  "

        for dada in dades.readlines():
            if ((lectura_numero_estudiant + str(numero_estudiant) in dada) and ("problema PL " + str(numero_problema) in dada)):
                llegint_problema = True
            
            elif (llegint_problema):
                if ("c=" in dada):
                    llegint_costos = True
                
                elif ("A=" in dada):
                    llegint_constriccions = True
                
                elif ("b=" in dada):
                    llegint_b = True

                elif(llegint_costos == True):
                    vector_costos = list(int(x) for x in dada.split())
                    llegint_costos = False

                elif (llegint_constriccions == True):
                    constriccio = list(int(x) for x in dada.split())
                    matriu_constriccions.append(constriccio)
                    comptador_constriccions += 1

                    if (comptador_constriccions > 9):
                        llegint_constriccions = False
                
                elif (llegint_b == True):
                    vector_b = list(int(x) for x in dada.split())
                    llegint_b = False
                    llegint_problema = False
                    break

        return vector_costos, matriu_constriccions, vector_b