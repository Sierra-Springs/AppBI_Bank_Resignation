from pathlib import Path
import os


projectPath = Path(os.path.dirname(__file__)).parent.parent
figPath = projectPath / "Rapport/fig"
textPartsPath = projectPath / "Rapport" / "texParts"


if __name__ == "__main__":
    print(projectPath)
    print(projectPath / "hello" / "hi")
