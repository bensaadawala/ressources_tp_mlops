
import os
import json
import pandas as pd
import subprocess
import sys


def run_continuous_training():
    # 1. Lire le statut du Data Drift
    with open("reports/drift_status.json", "r", encoding="utf-8") as f:
        status = json.load(f)

    print("=== CONTINUOUS TRAINING ===")
    print(f"Pourcentage de Drift : {status['drift_percentage']} %")

    # 2. Vérifier si le seuil est dépassé
    if not status["drift_detected"]:
        print("Aucun réentraînement nécessaire.")
        return

    print("ALERTE : seuil de Drift dépassé !")

    # 3. Vérifier la disponibilité des données étiquetées
    labeled_path = "data/production_labeled.csv"

    if not os.path.exists(labeled_path):
        print("Réentraînement en attente : fichier production_labeled.csv absent.")
        print("En attente des véritables labels default_risk.")
        return

    # 4. Vérifier les labels
    df = pd.read_csv(labeled_path)

    if "default_risk" not in df.columns:
        print("ERREUR : colonne default_risk absente.")
        return

    if df["default_risk"].isna().any():
        print("ERREUR : certains labels sont manquants.")
        return

    if not df["default_risk"].isin([0, 1]).all():
        print("ERREUR : les labels doivent être 0 ou 1.")
        return

    # 5. Déclencher le réentraînement
    print("Données étiquetées validées.")
    print("Déclenchement du réentraînement...")

    subprocess.run(
        [sys.executable, "-m", "src.train"],
        check=True
    )


if __name__ == "__main__":
    run_continuous_training()
