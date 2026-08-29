from pathlib import Path
from machine_edition_devkit.research.me_res_001.analysis import perform_statistical_analysis

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent.parent.parent
    perform_statistical_analysis(root)
    print("ME-RES-001 statistical analysis executed successfully.")
