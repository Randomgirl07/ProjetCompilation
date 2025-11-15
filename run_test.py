import subprocess
import os
import sys  
PYTHON_EXE_PATH = sys.executable 


CODE_GENERATOR_SCRIPT = r".\main.py"
MSM_DIRECTORY = r".\msm"
MSM_EXE = os.path.join(MSM_DIRECTORY, "msm.exe") # Façon plus propre de construire le chemin

EXPECTED_OUTPUT = """1
1
1
1
1
1
1
1"""

def run_test_suite():


    try:
        print(f"1. Exécution de '{os.path.basename(CODE_GENERATOR_SCRIPT)}' pour générer le code...")

        generation_process = subprocess.run(
            [PYTHON_EXE_PATH, CODE_GENERATOR_SCRIPT],
            capture_output=True,
            text=True, 
            check=True,
     
        )
        
        generated_code = generation_process.stdout
        print("   Code source généré avec succès.")
        
   
        print(f"2. Exécution de '{os.path.basename(MSM_EXE)}' avec le code source généré...")

        compilation_process = subprocess.run(
            [MSM_EXE],
            input=generated_code, 
            capture_output=True,
            text=True,
            check=True,
           
        )
        
        actual_output = compilation_process.stdout
        cleaned_actual = actual_output.strip()
        cleaned_expected = EXPECTED_OUTPUT.strip()

        if cleaned_actual == cleaned_expected:
            print("\n====================")
            print("  TESTS RÉUSSIS !")
            print("====================")
        else:
            print("\n!!!!!!!!!!!!!!!!!!!!")
            print("  TESTS ÉCHOUÉS !")
            print("!!!!!!!!!!!!!!!!!!!!")
            print("\n--- RÉSULTAT ATTENDU ---")
            print(cleaned_expected)
            print("\n--- RÉSULTAT OBTENU ---")
            print(cleaned_actual)
            print("\n-------------------------")

    except FileNotFoundError as e:
        print(f"\nERREUR CRITIQUE : Fichier ou programme introuvable.")
        print(f"Assurez-vous que '{e.filename}' existe et est accessible.")
        print(f"Détails : {e}")
        
    except subprocess.CalledProcessError as e:
        print(f"\nERREUR CRITIQUE : Une commande a échoué.")
        print(f"Commande : '{' '.join(e.cmd)}'")
        # Affiche la sortie d'erreur du processus qui a échoué, ce qui est très utile pour le débogage
        print(f"Erreur retournée :\n{e.stderr}")

# Point d'entrée du script
if __name__ == "__main__":
    run_test_suite()