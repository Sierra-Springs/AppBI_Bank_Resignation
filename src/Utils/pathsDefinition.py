from pathlib import Path
import os


modelSavePath = Path(os.path.dirname(__file__)).parent.parent
figPath = modelSavePath / "Rapport/fig"

if __name__ == "__main__":
    print(modelSavePath)
    print(modelSavePath/"hello"/"hi")
