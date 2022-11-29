from pathlib import Path
import os


projectPath = Path(os.path.dirname(__file__)).parent.parent
figPath = projectPath / "Rapport" / "fig"
textPartsPath = projectPath / "Rapport" / "texParts"
srcPath = projectPath / "src"
modelsPaths = srcPath / "Models" / "models"

table1Path = "Data/donnees_banque/table1.csv"
table2Path = "Data/donnees_banque/table2.csv"

if __name__ == "__main__":
    print(projectPath)
    print(projectPath / "hello" / "hi")
