import pickle
import joblib
import time
from pathlib import Path
from collections.abc import MutableMapping
import os
import numpy as np

from comet_ml import Experiment
from comet_ml import API


from Utils.logger import StyleLogger
from LANG.log_string import *



module_path = Path(os.path.dirname(__file__))
default_model_dataBase = module_path / "models"


class CometMLManager:
    def __init__(self,
                 workspace="appbi-bank-resignation",
                 project_name="development",
                 model_database=default_model_dataBase):
        os.makedirs(model_database, exist_ok=True)
        self.logger = StyleLogger()
        self.workspace = workspace
        self.project_name = project_name
        self.model_database = model_database
        if "COMET_API_KEY" in os.environ:
            self.API_KEY = os.environ["COMET_API_KEY"]
            self.api = API(api_key=self.API_KEY)
        else:
            self.API_KEY = None
            self.api = None
            self.logger.log_err(LOG_ENV_VAR_NOT_SET("COMET_API_KEY"))
            # raise Exception("COMET_API_KEY environment variable must be set")
        self.experience_name = None
        self.experiment = None

    def start_experiment(self, experiment_name):
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return
        self.experience_name = experiment_name
        self.experiment = Experiment(api_key=self.API_KEY,  # don’t hardcode!!
                                     project_name=self.project_name,
                                     workspace=self.workspace,
                                     )
        self.experiment.set_name(self.experience_name)

    def end_experiment(self):
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return
        self.experiment.end()

    def get_model_path(self, model_name, extension='joblib'):
        """
        retourne le chemin vers le fichier où le model model_name devrait être enregistré
        """
        return self.model_database / f"{model_name}.{extension}"

    def save_model_to_file(self, model, model_name):
        """
        Enregistre le model sklearn sous le nom model_name + ".joblib" dans le dossier self.model_database
        """
        file_path = self.get_model_path(model_name)
        joblib.dump(model, file_path)

        return file_path

    def load_model_from_file(self, model_name):
        """
        Retourne le model sklearn enregistré dans le fichier self.model_database + model_name + ".joblib"
        En cas d'échec, tente de charger le modèle enregistré avec l'extension .pkl
        """
        try:
            return joblib.load(self.get_model_path(model_name))
        except:
            with open(self.get_model_path(model_name, extension='pkl'), "rb") as file_handle:
                return pickle.load(file_handle)

    def log_model(self, _model_name, _model_path=None):
        """
        Enregistre le model dans les expériences Comet_ml
        Lorsque l'on veut garder une trace d'un modèle sans savoir si on le réutilisera vraiment plus tard
        """
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return
        _model_path = str(self.get_model_path(_model_name)) if _model_path is None else _model_path
        self.experiment.log_model(name=_model_name, file_or_folder=_model_path)

    def register_model(self, model_name, registry_name=None):
        """
        Enregistre le model dans Model Registry sur Comet ML.
        Pour des modèles "intéresants" dont on se servira plus tard
        """
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return
        registry_name = model_name if registry_name is None else registry_name
        self.experiment.register_model(model_name=model_name, registry_name=registry_name)

    def log_and_register_model(self, model_name, model_path=None):
        """
        Enregistre le model dans les expériences Comet_ml
        puis enregistre le model dans Model Registry sur Comet ML.
        Lorsque l'on est sûr que le modèle est intéressant
        """
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return
        # log the model
        self.log_model(model_name=model_name, _model_path=model_path)

        # register the model for future use
        self.register_model(model_name)

    def download_model(self, model_name, workspace="appbi-bank-resignation", force=False):
        """
        Télécharge un modèle de Model Registry sur Comet ML
        """
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return
        if force or not (os.path.exists(self.get_model_path(model_name)) or os.path.exists(self.get_model_path(model_name, extension=".pkl"))):
            if force:
                self.logger.log(LOG_ATTEMPT_TO_FORCE_DOWNLOAD_MODEL(model_name))
            else:
                self.logger.log(LOG_ATTEMPT_TO_DOWNLOAD_MODEL(model_name))
            self.api.download_registry_model(workspace=workspace,
                                             registry_name=model_name,
                                             output_path=self.model_database,
                                             expand=True)
        else:
            self.logger.log(LOG_MODEL_ALREADY_DOWNLOADED(model_name))
        return self.load_model_from_file(model_name=model_name)

    def download_model_from_experiment(self, model_name, experiment_name=None, force=False):
        """
        Télécharge un modèle depuis les expériences sur Comet ML
        """
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return
        if force or not os.path.exists(self.get_model_path(model_name)):
            if experiment_name is not None:
                experiment = self.api.get(self.workspace, self.project_name, experiment_name)
                experiment.download_model(model_name, output_path=self.model_database, expand=True)
            else:
                self.experiment.download_model(model_name, output_path=self.model_database, expand=True)

        return self.load_model_from_file(model_name=model_name)

    def log_metrics(self, metrics, prefix=None, step=None, epoch=None):
        """
        Enregistre les metrics dans l'experiment Comet_ml
        """
        if self.API_KEY is None:
            self.logger.log_warn(LOG_IGNORE_API_KEY_NOT_SET())
            return

        def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.') -> MutableMapping:
            """source : https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/"""
            items = []
            for k, v in d.items():
                new_key = parent_key + sep + k if parent_key else k
                if isinstance(v, MutableMapping):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                else:
                    if isinstance(v, np.ndarray):
                        items.append((new_key, v.tolist()))
                    else:
                        items.append((new_key, v))
            return dict(items)

        flatten_metrics = flatten_dict(metrics)

        self.experiment.log_metrics(flatten_metrics, prefix=prefix, step=step, epoch=epoch)


if __name__ == "__main__":
    if "COMET_API_KEY" in os.environ:
        API_KEY = os.environ["COMET_API_KEY"]
        print(API_KEY)

    cmm = CometMLManager(project_name='milestone-3')
    #cometMLManager.register_model("log-reg-distance-angle")
    #cometMLManager.log_model("MLPClassifier")

    #cometMLManager.log_model("mlp-classifier")
    #cometMLManager.register_model("mlp-classifier")
    #print(type(model))
    #cometMLManager.sklearn_model_to_file(model, model_name="log-reg-distance-angle")

    model = cmm.download_model("mlp-classifier")
    print(type(model))


