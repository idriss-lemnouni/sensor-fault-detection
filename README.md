# Détection d’anomalies de température

Comparaison d’une règle de saut entre deux mesures et d’un seuil robuste fondé sur la médiane et l’écart absolu médian des 24 mesures précédentes. Les deux méthodes traitent les mesures dans l’ordre, sans connaître le futur. Le script compte les alertes à l’intérieur et à l’extérieur des fenêtres annotées.

Télécharger [le CSV NAB](https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/machine_temperature_system_failure.csv), puis lancer `python detect.py machine_temperature_system_failure.csv`. Python 3 suffit.

Les fenêtres sont reprises des [annotations du Numenta Anomaly Benchmark](https://raw.githubusercontent.com/numenta/NAB/master/labels/combined_windows.json). Il s’agit d’une série industrielle réelle. Les scores sont calculés par point et ne représentent pas le score événementiel officiel de NAB. Les seuils sont exprimés dans l’unité brute du fichier. L’exécution locale a été vérifiée sur un extrait de 335 mesures autour de la première fenêtre. Le fichier complet permet d’étendre la comparaison aux quatre fenêtres.
