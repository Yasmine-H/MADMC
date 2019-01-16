***Projet MADMC : Décision multicritère interactive***

Lancer part1.py pour tester le programme comportant la partie "Décision multicritère sur ensemble d'alternatives défini de manière explicite". La fonction interaction est celle qui récupère les réponses du décideur et qui génère les solutions appropriées. Elle a entre autres recours à get_pareto, get_ideal, get_nadir et tchebytcheff_augmente. Une partie des fonctions utilisées se trouvent dans utils.py.

Lancer part2.py pour tester le code portant sur la partie "Décision multicritère par élicitation incrémentale sur ensemble d'alternatives
défini de manière explicite" (implémentation de l'article).
Le programme comporte interactive_elicitation qui procède à l'intéraction et au calcul des résultats de manière itérative. 
automatic_elicitation prend en entrée une fonction de préférences dont il tente de se rapprocher.
pairwise_max_regret, max_regret et minimax_regret correspondent au fonctions PMR, MR et MMR respectivement décrites dans l'article.

La 3ème partie du projet a été entamée mais pas achevée. part3.py comporte les deux fonctions suivantes : 
generate_knapsack_instance : génère une instance du sac-à-dos multicritère.
knapsack_plmo : définition du programme linéaire multiobjectif
Elle utilise également des fonctions de utils.py notamment pour calculer le point idéal et le point nadir.