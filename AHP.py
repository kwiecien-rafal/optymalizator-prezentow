import numpy as np

# kryteria = ['cena', 'popularność', 'telefony', 'agd', 'książki']


def ahp(kryteria):
    RandomIndex = [0.00, 0.00, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]  # RandomIndex dla roznych ilosci kryteriow
    cri = 0.15                                                                  # prog spojnosci
    
    n = len(kryteria)
    k_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i == j :
                k_matrix[i][j] = 1
            if i < j:
                k_matrix[i][j] = eval(input(kryteria[i]+' do '+kryteria[j]+': '))
                k_matrix[j][i] = k_matrix[i][j]**(-1)
    
                                                                    ### wagi
    weights = np.true_divide(k_matrix, np.sum(k_matrix, axis=0))    # podziel elementy macierzy porównań przez sumę jej kolumny
    weights = np.sum(weights, axis=1)                               # zsumuj rzedy
    weights = weights / weights.shape[0]                            # podziel elementy przez liczbe kryteriow

                                                                    ### spojnosc
    cons_vector = np.multiply(k_matrix, weights)                    # pomnoz macierz porownan przez wektor wag
    weightedsum = np.sum(cons_vector, axis=1)                       # zsumuj rzedy
    ratio = weightedsum / weights                                   # podziel przez wektor wag
    lambdamax = np.sum(ratio, axis = 0) / n                         # srednia z poprzedniego wyniku
    ConsistencyIndex = (lambdamax - n) / (n - 1)                    # wskaznik spojnosci
    ConsistencyRatio = ConsistencyIndex / RandomIndex[n-1]          # wspolczynnik spojnosci 

    print('-'*20)                                                   ### porownanie z progiem spojnosci
    if ConsistencyRatio <= cri:
        print('macierz jest spójna: ', ConsistencyRatio, '<', cri)
    else:
        print('macierz NIE jest spójna: ', ConsistencyRatio, '>', cri)

    kryteria_dict = {}
    for i in range(k_matrix.shape[0]):
        kryteria_dict[kryteria[i]] = round((weights[i]),2)

    return kryteria_dict


'''print('- określ preferencje jednej kategorii względem drugiej w skali (1/9, 1/8, ... 1/2, 1, 2, ...9) - ')
wynik = ahp(kryteria)
print('-'*20)
for i in wynik:
    print(i,':',wynik[i])'''

