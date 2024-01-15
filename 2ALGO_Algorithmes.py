#################### DECLARATION VARIABLES ##########################

def filetomatrix():
    namefile = "tree.txt"
    file = open(namefile, "r")
    matrice = []
    for rows in file:
        rows = rows.strip()
        element = rows.split()
        for i in range(len(element)):
            element[i] = int(element[i])
        matrice.append(element)
    file.close()
    return matrice

T = filetomatrix()
n = len(T)
m = len(T[0]) 


#################### ALGORITHME GLOUTON ##########################


def planter_arbres_gloutons(n, m, T):
    E = [0] * n
    C = [0] * n

    for i in range(n):
        couts_possibles = [(T[i][j], j + 1) for j in range(m)]
        couts_possibles.sort()

        for j in range(i):
            if E[j] == couts_possibles[0][1] and (i - j) < 2:
                couts_possibles.pop(0)

        meilleure_essence = couts_possibles[0][1]
        E[i] = meilleure_essence
        C[i] = couts_possibles[0][0]

    return E, sum(C)


emplacements_plantes, cout_total = planter_arbres_gloutons(n, m, T)

print("Emplacements des essences plantées avec glouton :", emplacements_plantes)
print("Coût total de plantation avec glouton :", cout_total)


#################### ALGORITHME RECURSIF NAÏF ##########################


def planter_arbres_récursif_naïf(n, m, T, ligne=0, indice_exclu=-1, E=None, C=None):
    def trouver_essence_minimale(T, ligne, indice_exclu):
        m = len(T[0])
        min_cout = float('inf')
        meilleure_essence = -1

        for j in range(m):
            if j + 1 != indice_exclu and T[ligne][j] < min_cout:
                min_cout = T[ligne][j]
                meilleure_essence = j + 1

        return meilleure_essence, min_cout
    
    if E is None:
        E = [0] * n
    if C is None:
        C = [0] * n

    if ligne >= n:
        return E, sum(C)

    meilleure_essence, min_cout = trouver_essence_minimale(T, ligne, indice_exclu)
    E[ligne] = meilleure_essence
    C[ligne] = min_cout

    return planter_arbres_récursif_naïf(n, m, T, ligne + 1, meilleure_essence, E, C)


emplacements_plantes2, cout_min2 = planter_arbres_récursif_naïf(n,m,T)

print("Emplacements des essences plantées avec récursif naïf :", emplacements_plantes2)
print("Coût minimal de plantation avec récursif naïf :", cout_min2)


#################### ALGORITHME TOP DOWN ##########################


def planter_arbres_top_down(n, m, T):
    memo = {} 

    def trouver_essence_minimale(ligne, indice_exclu):
        if (ligne, indice_exclu) in memo:
            return memo[(ligne, indice_exclu)]

        min_cout = float('inf')
        meilleure_essence = -1

        for j in range(m):
            if j + 1 != indice_exclu and T[ligne][j] < min_cout:
                min_cout = T[ligne][j]
                meilleure_essence = j + 1

        memo[(ligne, indice_exclu)] = (meilleure_essence, min_cout)
        return meilleure_essence, min_cout

    def planter_arbres_recursif_top_down(ligne, indice_exclu, E, C):
        if ligne >= n:
            return E, sum(C)

        if (ligne, indice_exclu) in memo:
            return memo[(ligne, indice_exclu)]

        meilleure_essence, min_cout = trouver_essence_minimale(ligne, indice_exclu)
        E[ligne] = meilleure_essence
        C[ligne] = min_cout

        memo[(ligne, indice_exclu)] = planter_arbres_recursif_top_down(ligne + 1, meilleure_essence, E, C)
        return memo[(ligne, indice_exclu)]

    E = [0] * n  
    C = [0] * n  

    return planter_arbres_recursif_top_down(0, -1, E, C)


emplacements_plantes3, cout_min3 = planter_arbres_top_down(n,m,T)

print("Emplacements des essences plantées avec Top Down :", emplacements_plantes3)
print("Coût minimal de plantation avec top Down :", cout_min3)


#################### ALGORITHME BOTTOM UP ##########################


def planter_arbres_bottom_up(n, m, T):
    G = [[float('inf')] * m for _ in range(n)]
    E = [[0] * m for _ in range(n)]

    for j in range(m):
        G[0][j] = T[0][j]

    for i in range(1, n):
        for j in range(m):
            for k in range(m):
                if k != j:
                    cost = G[i-1][k] + T[i][j]
                    if cost < G[i][j]:
                        G[i][j] = cost
                        E[i][j] = k

    min_cost = float('inf')
    min_index = -1
    for j in range(m):
        if G[n-1][j] < min_cost:
            min_cost = G[n-1][j]
            min_index = j

    essences = [min_index + 1]
    for i in range(n-1, 0, -1):
        essences.append(E[i][essences[-1]])

    essences.reverse()

    return essences, min_cost


emplacements_plantes4, cout_min4 = planter_arbres_bottom_up(n,m,T)

print("Emplacements des essences plantées avec Bottom Up :", emplacements_plantes4)
print("Coût minimal de plantation avec Bottom Up :", cout_min4)

