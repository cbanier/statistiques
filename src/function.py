import os
import csv
import numpy as np
from scipy.stats import norm, chi2
import matplotlib.pyplot as plt
from statistics import geometric_mean
from math import sqrt
from typing import List, Tuple


path = os.getcwd()


# parse les valeurs dans une liste de tuple(classement, moyenne_10_km)
def convert_all_data_to_list(file: str):
    data: List[tuple] = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((row['Classement moins de 22 ANS'], float(row['Vitesse moyenne sur 10 kilomètres'])))
    return data


# parse les valeurs dans une liste
def get_data(data: List[Tuple[str, int]]):
    numbers: List[int] = []
    for number in data:
        numbers.append(number[1])
    return numbers


# moyenne arithmétique
def mean_arith(data: List[int]):
    return np.mean(data)


# moyenne géométrique
def mean_geo(data):
    return geometric_mean(data)


# médiane de la série
def median(data: List[int]):
    return np.median(data)


# Q1 représente 25% des valeurs
def q1(data):
    return np.percentile(data, 25)


# Q3 représente 75% des valeurs
def q3(data):
    return np.percentile(data, 75)


# Calcule de la variance
def variance(data):
    return np.var(data)


# Calcule l'écart_type
def ecart_type(var):
    return sqrt(var)


# Vérifie si le dossier output/ existe, le créer sinon
def check_output_dir():
    if not os.path.exists(path + '/output'):
        os.makedirs(path + '/output')


# Dessine l'histogramme correspond aux valeurs de data
# Et l'approximation de la loi normale associée
def normal_approximation(data):
    fig, ax = plt.subplots()

    # affiche l'histogramme des données
    bins: List[float] = [i for i in range(int(data[-1]), int(data[0]) + 1)]
    ax.hist(data, bins=bins, density=True, alpha=0.6, color='green', edgecolor='k', label='histogramme')
    check_output_dir()
    fig.savefig(path + '/output/histogramme.png')

    # tracé de la densité
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, len(data))
    mean = mean_arith(data)
    std = sqrt(variance(data))
    # approximation loi normale
    p = norm.pdf(x, mean, std)
    ax.plot(x, p, color='black', label='densité_loi_normale')
    ax.legend()
    fig.suptitle(f'Allure des résultats: N(moyenne = {round(mean, 3)} , écart-type = {round(std, 3)})')
    #plt.show()

    check_output_dir()
    fig.savefig(path + '/output/approximation.png')
    return x, p


# Détermine l'effectif observé ce trouvant sur l'intervalle : [interval; interval + 1[
def effectif_obs(x, interval):
    eff: List = []
    cpt: int = 0
    i = 0
    while i < len(x):
        if interval <= x[i] < interval + 1:
            cpt += 1
        else:
            eff.append(cpt)
            interval += 1
            cpt = 1
        i += 1
    eff.append(cpt)
    return eff


# Détermine la fréquence de chaque valeur de x dans l'intervalle : [interval; interval +1[
def freq_theoric(x, p, interval):
    freq: List = []
    cpt: int = 0
    i = 0
    while i < len(x):
        if interval <= x[i] < interval + 1:
            cpt += p[i]
        else:
            freq.append(cpt)
            interval += 1
            cpt = p[i]
        i += 1
    freq.append(cpt)
    return freq


# Détermine la fréquence théorique de la loi normale
def effectif_the(x, freq, interval):
    for i in range(len(x)):
        x[i] *= freq[i]
    return x


# Calcule la mesure du khi2
def mesure_khi2(effectif_observe, effectif_theorique):
    res: int = 0
    for i in range(len(effectif_theorique)):
        res += ((effectif_observe[i] - effectif_theorique[i]) ** 2) / effectif_theorique[i]
    return res


# Détermine k pour la loi du khi2
def k_khi2(loi, nb_cases):
    if loi == 'normale':
        return nb_cases - 3
    else:
        pass


# Effectue le test du khi2
def test_khi2(k, d_root, error):
    val = chi2.ppf(1-error, k)
    if d_root > val:
        print("H0 est rejeté")
        print("X ne suit pas une loi normale")
    else:
        print("H0 est accepté")
        print("X suit une loi normale")


# Dessine l'histogramme correspond aux valeurs de data
# Et l'approximation de la loi du khi2 associée
def khi2_approximation(data):
    fig, ax = plt.subplots()

    # affiche l'histogramme des données
    bins: List[float] = [i for i in range(int(data[-1]) - 1, int(data[0]) + 2)]
    ax.hist(data, bins=bins, density=True, alpha=0.6, color='green', edgecolor='k', label='histogramme')

    # tracé de la densité
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, len(data))
    mean = mean_arith(data)
    std = sqrt(variance(data))
    # approximation loi khi2
    p = chi2.pdf(x, df=30)
    ax.plot(x, p, color='black', label='densité_loi_khi2')
    ax.legend()
    fig.suptitle(f'Allure des résultats: N(moyenne = {round(mean, 3)} , écart-type = {round(std, 3)})')
    plt.show()
