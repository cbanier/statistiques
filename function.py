import os
import csv
import numpy as np
from scipy.stats import norm, chi2
import matplotlib.pyplot as plt
from statistics import geometric_mean
from math import sqrt
from typing import List, Tuple


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


# Vérifie si le dossier output/ existe, le créer sinon
def check_output_dir():
    if not os.path.exists('output/'):
        os.makedirs('output/')


# Dessine l'histogramme correspond aux valeurs de data
# Et l'approximation de la loi normale associée
def normal_approximation(data):
    fig, ax = plt.subplots()

    # affiche l'histogramme des données
    bins: List[float] = [i for i in range(int(data[-1]) - 1, int(data[0]) + 2)]
    ax.hist(data, bins=bins, density=True, alpha=0.6, color='green', edgecolor='k', label='histogramme')
    check_output_dir()
    fig.savefig('output/histogramme.png')

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
    fig.savefig('output/approximation.png')


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
