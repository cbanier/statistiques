from function import *

if __name__ == "__main__":
    data = convert_all_data_to_list('moyenne10km.csv')
    numbers = get_data(data)
    # affiche la moyenne arithmétique
    print('Moyenne arithmétique : ', round(mean_arith(numbers), 4))

    # affiche la moyenne géométrique
    print('Moyenne géométrique: ', round(mean_geo(numbers), 4))

    # affiche la médiane
    print('Médiane : ', round(median(numbers), 4))

    # affiche Q1
    print('Q1 : ', round(q1(numbers), 4))

    # affiche Q3
    print('Q3 : ', round(q3(numbers), 4))

    # affiche la variance
    print('Variance : ', round(variance(numbers), 4))

    # affiche l'histogramme de la série avec l'approximation de la loi normale
    normal_approximation(numbers)

    # affiche l'histogramme de la série avec l'approximation de la loi du khi2
    # khi2_approximation(numbers)
