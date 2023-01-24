import numpy as np
from numpy.linalg import det, inv

def optim (vector_costos, matriu_constriccions, indexs_basics, inversa_B, A_n, indexs_no_basics, x_b, z, n_it, n_fase, B):
    # Definim vector de costos no bàsics
    costos_no_basics = np.empty((0, len(indexs_no_basics)), int)
    for i in indexs_no_basics:
        costos_no_basics = np.append(costos_no_basics, vector_costos[i - 1])

    # Definim vector de costos bàsics
    costos_basics = np.empty((0, len(indexs_basics)), int)
    for i in indexs_basics:
        costos_basics = np.append(costos_basics, vector_costos[i - 1])
    
    # Fem la matriu transposta dels costos
    costos_no_basics_transposats = costos_no_basics.transpose()
    costos_basics_transposats = costos_basics.transpose()

    # Calculem els costos reduïts aplicant la definició
    producte_inversa_B_A_n = inversa_B.dot(A_n)
    producte_C_b_B_A_n = costos_basics_transposats.dot(producte_inversa_B_A_n)
    costos_reduits = costos_no_basics_transposats - producte_C_b_B_A_n

    # Definim q com a None, per tal de, en cas que els costos reduïts siguin positius, parar i retornar la solució
    q = None

    # Definim l'índex de q dins de les variables no bàsiques
    index_z = None

    # Apliquem regla de Bland, busquem l'índex més petit amb costos reduïts negatius
    for i in range(len(costos_reduits)):
        if (costos_reduits[i] < 0):
            q = indexs_no_basics[i]
            index_z = i
            break

    # Tenim costos reduïts positius, per tant comprovem a quina fase estem i, en funció d'això, fem print d'un missatge o un altre. En ambdós casos retornem allò que ens interessa de la solució
    if (q == None):
        if (n_fase == 1 and round(z, 4) > 0):
            return ["Problema Infactible"]
        if (n_fase == 1):
            print("[ASP1] Iteració ", n_it, ": Solució bàsica factible trobada.")
        else: 
            print("[ASP1] Iteració ", n_it, ": Solució òptima trobada.")
        return [indexs_basics, x_b, indexs_no_basics, inversa_B, A_n, z, costos_reduits, n_it, B]
    
    # Determinem la matriu columna A_q (columna q de la matriu constriccions)
    A_q = np.empty((0, len(matriu_constriccions)), int)
    for i in range(len(matriu_constriccions)):
        A_q = np.append(A_q, matriu_constriccions[i][q - 1])

   # Calculem la direcció bàsica associada a la variable d'entrada q
    direccio_basica = -(inversa_B.dot(A_q))

    # Analitzem si el problema és il·limitat
    problema_ilimitat = True

    for i in range(len(direccio_basica)):
        if (direccio_basica[i] < 0):
            problema_ilimitat = False
    
    if (problema_ilimitat):
        return (["Problema Il·limitat"])
    
    # Calculem la longitud de pas, que calcularem buscant el mínim de les diverses variables amb costos reduïts negatius
    longitud_pas = None
    primera_iteracio = True
    p = None

    for i in range(len(direccio_basica)):
        if (direccio_basica[i] < 0):
            longitud_pas_temporal = -(x_b[i] / direccio_basica[i])
            if (primera_iteracio):
                longitud_pas = longitud_pas_temporal
                primera_iteracio = False
                p = indexs_basics[i]
            elif (longitud_pas_temporal < longitud_pas):
                longitud_pas = longitud_pas_temporal
                p = indexs_basics[i]

    # Actualitzem els índexs bàsics, eliminant p i afegint q
    posicio_p_indexs_basics = indexs_basics.index(p)
    del indexs_basics[posicio_p_indexs_basics]
    indexs_basics.insert(posicio_p_indexs_basics, q)

    # Actualitzem els índexs no bàsics, eliminant q i afegint p
    posicio_q_indexs_no_basics = indexs_no_basics.index(q)
    del indexs_no_basics[posicio_q_indexs_no_basics]
    indexs_no_basics.insert(posicio_q_indexs_no_basics, p)

    # Actualitzem x_b
    x_b = x_b + longitud_pas * direccio_basica
    x_b =  np.delete(x_b, posicio_p_indexs_basics)
    x_b = np.insert(x_b, posicio_p_indexs_basics, longitud_pas, axis=None)
    
    # Definim la matriu H, que ens servirà per actualitzar la inversa de B
    H = np.identity(len(matriu_constriccions))
    for i in range(len(H)):
        if (i != posicio_p_indexs_basics):
            H[i][posicio_p_indexs_basics] = -(direccio_basica[i] / direccio_basica[posicio_p_indexs_basics])
        else:
            H[i][posicio_p_indexs_basics] = -(1 / direccio_basica[posicio_p_indexs_basics])
    
    # Actualitzem la inversa de B, multiplicant H per la inversa de B de la base anterior
    inversa_B = H.dot(inversa_B)

    # Actualitzem el valor de la funció de cost
    z = 0
    c = 0

    for i in indexs_basics:
        z += x_b[c] * vector_costos[i - 1]
        c += 1
    
    # Actualitzem B, per tal de poder comprovar que la matriu inversa es calcula correctament
    B = np.delete(B, posicio_p_indexs_basics, 1)
    B = np.insert(B, posicio_p_indexs_basics, matriu_constriccions[ : , q - 1], axis=1)

    # Comprovem que la inversa s'ha calculat bé
    if (round(det(B), 4) != 0):
        inversa_B_python = inv(B)
        diferencia_inversa_B = abs(inversa_B - inversa_B_python)

        if (diferencia_inversa_B.all() > 10 ** -12):
            inversa_B = inversa_B_python

    # Actualitzem A_n, eliminant la columna associada a q i afegint la columna p de la matriu constriccions
    A_n = np.delete(A_n, posicio_q_indexs_no_basics, 1)
    A_n = np.insert(A_n, posicio_q_indexs_no_basics, matriu_constriccions[ : , p - 1], axis=1)

    print("[ASP1]     Iteració", n_it, ": q =",  q,", rq = ", np.round(costos_reduits[posicio_q_indexs_no_basics], 3), ", B(p) = ", p, ", theta*= ",  np.round(longitud_pas, 3), ", z = ", np.round(z, 3))
    n_it += 1

    # fem crida recursiva de l'algorisme
    return optim (vector_costos, matriu_constriccions, indexs_basics, inversa_B, A_n, indexs_no_basics, x_b, z, n_it, n_fase, B)