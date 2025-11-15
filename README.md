# **Projet de Compilation : Générateur et Testeur de Code**

Ce projet a pour but de créer et tester le compilateur. Il comprend deux étapes principales :

1. **Génération de code** : Un script Python (main.py) génère le code binaire des tests(test.txt) et de la bibliothèque (lib.txt)
2. **Compilation et exécution** : Le code généré est ensuite compilé et exécuté par une machine externe (msm.exe).

Le script run_tests.py automatise l'ensemble de ce processus.

## **Composants du Projet**

- **main.py**: Le script qui génère le code binaire final. Il assemble les fonctions de la bibliothèque et les cas de test en un seul fichier prêt à être exécuté.
- **run_tests.py**: Le script principal pour lancer l'ensemble de la suite de tests.
- **lib.txt**: Une bibliothèque de fonctions standard mises à disposition pour les tests. Elle inclut actuellement des fonctions utiles comme print, println, malloc et power.
- **Les fichiers de test**: Le projet inclut une batterie de tests, où chaque test valide une fonctionnalité spécifique du langage.

## **Prérequis**

Avant de lancer les tests, assurez-vous d'avoir les éléments suivants installés et accessibles sur votre machine :

- **Python 3**
- **Compilateur msm.exe**

**Configuration**

Pour que le script de test fonctionne correctement, vous devez **impérativement** mettre à jour les chemins d'accès aux fichiers dans le script run_tests.py.

Ouvrez le fichier run_tests.py et modifiez les variables suivantes pour qu'elles correspondent à votre configuration locale :

1. **PYTHON_EXE_PATH** : Le chemin absolu vers votre exécutable Python.  

2. **CODE_GENERATOR_SCRIPT** : Le chemin absolu vers le script principal de génération de code **main.py.**(si la structure du projet a été conservé pas besoin de le changer car on se moment on a le chemin relatif)
3. **MSM_DIRECTORY** : Le chemin absolu vers le dossier contenant le compilateur msm.exe.

   ## **Exécution des tests**

Une fois la configuration terminée, vous pouvez lancer la suite de tests en exécutant le script **run_test.py**

## **Fonctionnement du script**

Le script run_tests.py exécute les étapes suivantes :

1. **Lancement du générateur de code** : Il exécute main.py à l'aide de l'interpréteur Python spécifié.
2. **Capture de la sortie** : Le code source généré par main.py est capturé.
3. **Exécution du compilateur** : Le script lance msm.exe et lui transmet le code généré en entrée (similaire à un "pipe" | en ligne de commande).
4. **Comparaison des résultats** : La sortie du compilateur est comparée à un résultat attendu prédéfini dans la variable EXPECTED_OUTPUT.

   ## **Interprétation des résultats**

À la fin de l'exécution, le script affichera l'un des messages suivants :

- **TESTS RÉUSSIS \!** : Si la sortie obtenue correspond exactement à la sortie attendue.
- **TESTS ÉCHOUÉS \!** : Si la sortie obtenue est différente de celle attendue. Dans ce cas, le script affichera les deux versions pour faciliter le débogage.
- **ERREUR CRITIQUE** : Si un fichier est introuvable (vérifiez vos chemins dans la section **Configuration**) ou si l'un des processus (génération ou compilation) se termine avec une erreur.
