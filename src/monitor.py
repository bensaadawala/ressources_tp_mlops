
import os
import json
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetDriftMetric


def run_drift_analysis(
    reference_path="data/credit_scoring.csv",
    current_path="data/production_requests.csv",
    output_html="reports/data_drift_report.html"
):
    # 1. Charger les données
    ref_df = pd.read_csv(reference_path).drop(
        columns=["default_risk"], errors="ignore"
    )
    cur_df = pd.read_csv(current_path).drop(
        columns=["default_risk"], errors="ignore"
    )

    # 2. Générer le rapport détaillé
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_df, current_data=cur_df)

    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    report.save_html(output_html)

    # 3. Calculer le Data Drift global
    drift_metric = Report(
        metrics=[DatasetDriftMetric(drift_share=0.30)]
    )
    drift_metric.run(reference_data=ref_df, current_data=cur_df)

    result = drift_metric.as_dict()["metrics"][0]["result"]

    total_variables = result["number_of_columns"]
    drifted_variables = result["number_of_drifted_columns"]
    drift_percentage = result["share_of_drifted_columns"] * 100

    # 4. Afficher les résultats
    print(f"Nombre de variables surveillées : {total_variables}")
    print(f"Nombre de variables avec Drift : {drifted_variables}")
    print(f"Pourcentage de Drift : {drift_percentage:.2f} %")
    print("Seuil autorisé : 30 %")

    # 5. Déterminer si le seuil est dépassé
    drift_detected = drift_percentage > 30

    if drift_detected:
        print("ALERTE : le seuil de Drift est dépassé !")
    else:
        print("Aucune alerte : le seuil de Drift n'est pas dépassé.")

    # 6. Enregistrer le résultat pour l'automatisation
    os.makedirs("reports", exist_ok=True)

    status = {
        "total_variables": total_variables,
        "drifted_variables": drifted_variables,
        "drift_percentage": drift_percentage,
        "threshold": 30,
        "drift_detected": drift_detected
    }

    with open("reports/drift_status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, indent=4)

    print(f"Rapport HTML généré : {output_html}")
    print("Statut enregistré : reports/drift_status.json")


if __name__ == "__main__":
    run_drift_analysis()
