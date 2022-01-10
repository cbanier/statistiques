from function import *


# la méthode .reverse() ne marche pas sur la liste 'numbers'
def reverse(L):
    rev = []
    for elem in reversed(L):
        rev.append(elem)
    return rev


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

    # affiche l'écrart type
    print('Ecart-type : ', round(ecart_type(variance(numbers)), 4))

    # affiche l'histogramme de la série avec l'approximation de la loi normale
    # ou enregistre les histogrammes dans le dossier output/
    x, p = normal_approximation(numbers)

    numbers_rev = reverse(numbers)
    # affiche l'effectif observé de la série sur les intervalle de [i; i+1[
    observed = effectif_obs(numbers_rev, 6)
    print('eff observé = ', observed)

    # affiche l'effectif théorique pour chaque intervalle de [i; i+1[
    theoric = effectif_the(effectif_obs(x, 6), freq_theoric(x, p, 6), 6)
    print('eff théorique = ', theoric)

    # affiche la mesure du khi2
    d_root = mesure_khi2(observed, theoric)
    print('Mesure du khi2, d^2 = ', round(d_root, 3))

    # affiche le paramètre k pour la loi du khi2
    k = k_khi2('normale', len(theoric))
    print('k = ', k)

    # Résultat du test
    print("\n/-----------------------")
    print("Résultat: ")
    test_khi2(k, d_root, 0.05)
    print("-----------------------/")
