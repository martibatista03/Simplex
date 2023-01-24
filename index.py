from llegeix_dades import llegeix_dades
from optim import optim
import numpy as np
np.set_printoptions(suppress=True)

# Llegim les dades del problema i definim les següents variables
vector_costos = np.array(llegeix_dades("pm21_pràctica_ASP1_dades.txt")[0])
matriu_constriccions = np.array(llegeix_dades("pm21_pràctica_ASP1_dades.txt")[1])
vector_b = np.array(llegeix_dades("pm21_pràctica_ASP1_dades.txt")[2])
n = len(vector_costos)

# Definim els paràmetres per a la Fase I
vector_costos_I = np.zeros(n)
matriu_constriccions_I = np.empty((0, n + len(matriu_constriccions)), int)
indexs_base = []

# Afegim tantes variables artificials com constriccions
for i in range(len(matriu_constriccions)):
    # Vector de costos compost per les variables artificials
    vector_costos_I = np.append(vector_costos_I, 1)

    # Vector compost pels índexs de la base de fase I inicial, els de les variables artificials
    indexs_base.append(n + i + 1)

    # A cada constricció li afegim la seva corresponent variable artificial
    vector_constriccions = np.array(matriu_constriccions[i])
    for j in range(len(matriu_constriccions)):
        if (j == i): vector_constriccions = np.append(vector_constriccions, 1)
        else: vector_constriccions = np.append(vector_constriccions, 0)
    row = np.array(vector_constriccions)
    matriu_constriccions_I = np.append(matriu_constriccions_I, [row], axis=0)

# Definim la resta de paràmetres inicials per a la fase I

# La matriu inversa de B serà la matriu identitat de dimensió m a l'inici de la fase I, degut a les variables artificials. B serà evidentment igual.
inversa_B = np.identity(len(matriu_constriccions))
B = np.identity(len(matriu_constriccions))

# Definim la matriu A_n com les columnes de A restants (la matriu de constriccions original)
A_n = matriu_constriccions

# Definim els índexs no bàsics, que seran els índexs de totes les variables no artificials
indexs_no_basics = []

for i in range(n):
    indexs_no_basics.append(i + 1)

# Definim el vector x_b, que serà el vector_b degut a les variables artificials
x_b_I = vector_b

# Calculem el valor de la funció de cost inicial
z = sum(vector_b)

# Definim una variable que anirà comptant quantes iteracions fem al llarg del ASP1
n_it = 1

# Definim una variable que ens indiqui a quina fase estem, per diferenciar entre SBF (final de la fase I) i SBF òptima (final de la fase II)
n_fase = 1

print ("[ASP1] Inici ASP1 amb regla de Bland.")
print ("[ASP1]   Fase I")

# Apliquem la fase I de l'ASP1
optim_fase_I = optim (vector_costos_I, matriu_constriccions_I, indexs_base, inversa_B, A_n, indexs_no_basics, x_b_I, z, n_it, n_fase, B)

# Analitzem els resultats obtinguts de la fase I
if (optim_fase_I[0] != "Problema Infactible"):
    # Índexs bàsics per la fase II
    indexs_basics_fase_II = optim_fase_I[0]

    # Solució òptima de fase I
    x_b_II = optim_fase_I[1]

    # Definim la matriu que conté els índexs no bàsics de la fase II. Això ho fem eliminant els índexs de les variables artificials d'entre les no bàsiques del final de la fase I 
    indexs_no_basics_artificials = optim_fase_I[2]
    indexs_no_basics_fase_II = []

    for i in range(len(indexs_no_basics_artificials)):
        if (indexs_no_basics_artificials[i] <= n):
            indexs_no_basics_fase_II.append(indexs_no_basics_artificials[i])

    # Actualitzem A_n per a la fase II. Això ho fem agafant la última A_n de la fase I i eliminant les columnes associades a variables artificials
    A_n_fase_II = optim_fase_I[4]
    c = 0

    for i in indexs_no_basics_artificials:
        if (i > n):
            A_n_fase_II = np.delete(A_n_fase_II, c, axis=1)
        else:
            c += 1

    # Definim la inversa de B inicial per a la fase II, la qual coincideix amb la última inversa de B en la fase I. Igualment succeeix amb la matriu B.
    inversa_B_fase_II = optim_fase_I[3]
    B_fase_II = optim_fase_I[8]

    # Calculem el valor de la funció de cost inicial per a la fase II
    z_fase_II = 0
    c = 0

    for i in indexs_basics_fase_II:
        z_fase_II += x_b_II[c] * vector_costos[i - 1]
        c += 1

    # Actualitzem la variable que ens indica a quina iteració estem
    n_it = optim_fase_I[7]

    # Actualitzem la variable que ens indica a quina fase estem
    n_fase = 2

    print ("[ASP1]   Fase II")

    # Apliquem la fase II de l'ASP1
    optim_fase_II = optim (vector_costos, matriu_constriccions, indexs_basics_fase_II, inversa_B_fase_II, A_n_fase_II, indexs_no_basics_fase_II, x_b_II, z_fase_II, n_it, n_fase, B_fase_II)

    print ("[ASP1] Fi ASP1")
    print ("\n")

    # Analitzem el resultat obtingut de la fase II
    if (optim_fase_II[0] != "Problema Il·limitat"):
        print ("VB*=", "\n", optim_fase_II[0], "\n")
        print ("xb*=", "\n", np.round(optim_fase_II[1], 4), "\n")
        print ("VNB*=", "\n", optim_fase_II[2], "\n")
        print ("r*=", "\n", np.round(optim_fase_II [6], 4), "\n")
        print ("z*=", "\n", round(optim_fase_II [5], 4))
    else:
        print (optim_fase_II[0])

else:
    print ("\n", optim_fase_I[0])
