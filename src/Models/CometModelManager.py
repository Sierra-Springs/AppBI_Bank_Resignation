import pickle

from comet_ml import Experiment
from comet_ml import API
import joblib
import time
import os

from Utils.logger import StyleLogger
from LANG.log_string import *



module_path = os.path.dirname(__file__) + '/'
default_model_dataBase = os.path.dirname(__file__) + "/models/"


class CometModelManager:
    def __init__(self, workspace="appbi-bank-resignation",
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
            #raise Exception("COMET_API_KEY environment variable must be set")


    def get_model_path(self, model_name, extension='.joblib'):
        """
        retourne le chemin vers le fichier où le model model_name devrait être enregistré
        """
        return self.model_database + model_name + extension

    def sklearn_model_to_file(self, sklearn_model, model_name):
        """
        Enregistre le model sklearn sous le nom model_name + ".joblib" dans le dossier self.model_database
        """
        file_path = self.get_model_path(model_name)
        joblib.dump(sklearn_model, file_path)

        return file_path

    def file_to_sklear_model(self, model_name):
        """
        Retourne le model sklearn enregistré dans le fichier self.model_database + model_name + ".joblib"
        En cas d'échec, tente de charger le modèle enregistré avec l'extension .pkl
        """
        try:
            return joblib.load(self.get_model_path(model_name))
        except:
            with open(self.get_model_path(model_name, extension='.pkl'), "rb") as file_handle:
                return pickle.load(file_handle)

    def log_model(self, _model_name, _experience_name=None, _model_path=None):
        """
        Enregistre le model dans les expériences Comet_ml
        Lorsque l'on veut garder une trace d'un modèle sans savoir si on le réutilisera vraiment plus tard
        """
        exp = Experiment(api_key=self.API_KEY,  # don’t hardcode!!
                         project_name=self.project_name,
                         workspace=self.workspace,
                         )
        exp.set_name(_model_name if _experience_name is None else _experience_name)

        _model_path = self.get_model_path(_model_name) if _model_path is None else _model_path
        exp.log_model(name=_model_name, file_or_folder=_model_path)

    def register_model(self, model_name):
        """
        Enregistre le model dans Model Registry sur Comet ML.
        Pour des modèles "intéresants" dont on se servira plus tard
        """
        experiment = self.api.get(self.workspace, self.project_name, model_name)
        print(self.workspace, self.project_name, model_name)
        print(experiment)
        experiment.register_model(model_name=model_name, registry_name=model_name)

    def log_and_register_model(self, model_name, experience_name=None, model_path=None, n_attempts=10, sleep_time=0.5):
        """
        Enregistre le model dans les expériences Comet_ml
        puis enregistre le model dans Model Registry sur Comet ML.
        Lorsque l'on est sûr que le modèle est intéressant
        """
        # log the model
        self.log_model(self, _model_name=model_name, _experience_name=experience_name, _model_path=model_path)

        # give some time to the model to be availaible on Comet_ML
        experiment = self.api.get(self.workspace, self.project_name, model_name)
        for i in range(n_attempts):
            if experiment is None:
                experiment = self.api.get(self.workspace, self.project_name, model_name)
            else:
                continue
            time.sleep(0.5)

        # register the model for future use
        self.register_model(model_name)

    def download_model(self, model_name, workspace="appbi-bank-resignation", force=False):
        """
        Télécharge un modèle de Model Registry sur Comet ML
        """
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
        return self.file_to_sklear_model(model_name=model_name)

    def download_model_from_experiment(self, model_name, force=False):
        """
        Télécharge un modèle depuis les éxpériences sur Comet ML
        """
        if force or not os.path.exists(self.get_model_path(model_name)):
            experiment = self.api.get(self.workspace, self.project_name, model_name)
            experiment.download_model(model_name, output_path=self.model_database, expand=True)
        return self.file_to_sklear_model(model_name=model_name)


if __name__ == "__main__":
    if "COMET_API_KEY" in os.environ:
        API_KEY = os.environ["COMET_API_KEY"]
        print(API_KEY)

    cmm = CometModelManager(project_name='milestone-3')
    #cmm.register_model("log-reg-distance-angle")
    #cmm.log_model("MLPClassifier")

    #cmm.log_model("mlp-classifier")
    #cmm.register_model("mlp-classifier")
    #print(type(model))
    #cmm.sklearn_model_to_file(model, model_name="log-reg-distance-angle")

    model = cmm.download_model("mlp-classifier")
    print(type(model))


