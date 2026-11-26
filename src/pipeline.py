
import subprocess
import sys


def run_pipeline():
    print("\n========== ETAPE 1 : DETECTION DU DATA DRIFT ==========\n")

    subprocess.run(
        [sys.executable, "-m", "src.monitor"],
        check=True
    )

    print("\n========== ETAPE 2 : CONTINUOUS TRAINING ==========\n")

    subprocess.run(
        [sys.executable, "-m", "src.continuous_training"],
        check=True
    )

    print("\n========== PIPELINE TERMINE ==========\n")


if __name__ == "__main__":
    run_pipeline()
