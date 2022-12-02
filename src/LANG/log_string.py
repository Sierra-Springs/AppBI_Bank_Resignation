import importlib
import inspect

module_base = "LANG."

LANG_LOG_SOURCE = 'LANG_LOG_FRA'
LANG_LOG_SOURCE_ROLLBACK = 'LANG_LOG_ANG'


try:
    STRINGS_LOG = importlib.import_module(module_base + LANG_LOG_SOURCE).STRINGS_LOG
except:
    STRINGS_LOG = importlib.import_module(module_base + LANG_LOG_SOURCE_ROLLBACK).STRINGS_LOG

STRING_LOG_ROLLBACK = importlib.import_module(module_base + LANG_LOG_SOURCE_ROLLBACK).STRINGS_LOG


def launch_log_lang(lang_source):
    global LANG_LOG_SOURCE, STRINGS_LOG
    LANG_LOG_SOURCE = lang_source
    STRINGS_LOG = importlib.import_module(module_base + lang_source).STRINGS_LOG


def get_lang_log_source():
    return LANG_LOG_SOURCE


def construct_string(*kwargs):
    try:
        return STRINGS_LOG[inspect.stack()[1][3]].format(*kwargs)
    except:
        return STRING_LOG_ROLLBACK[inspect.stack()[1][3]].format(*kwargs)


def LOG_MISSING_KEY(key_Name):
    return construct_string(key_Name)


def LOG_ENV_VAR_NOT_SET(env_var_name):
    return construct_string(env_var_name)


def LOG_LOGGER_INITIALIZED():
    return construct_string()


def LOG_SENDING_LOGS_TO_CLIENT():
    return construct_string()


def LOG_SENDING_RESPONSE_TO_CLIENT():
    return construct_string()


def LOG_REQUEST_RECEIVED():
    return construct_string(inspect.stack()[1][3])


def LOG_ATTEMPT_TO_FORCE_DOWNLOAD_MODEL(model_name):
    return construct_string(model_name)


def LOG_ATTEMPT_TO_DOWNLOAD_MODEL(model_name):
    return construct_string(model_name)


def LOG_MODEL_ALREADY_DOWNLOADED(model_name):
    return construct_string(model_name)


def LOG_MODEL_LOADED_SUCCESSFULLY(model_name):
    return construct_string(model_name)


def LOG_MODEL_LOAD_ERROR(model_name):
    return construct_string(model_name)


def LOG_PREDICTION_SENT_TO_CLIENT():
    return construct_string()


def LOG_PREDICTION_ATTEMPT_ON_NONE_MODEL():
    return construct_string()


def LOG_LOG_LANG_CHANGED_SUCCESSFULLY(lang_name):
    return construct_string(lang_name)


def LOG_LOG_LANG_CHANGE_ERROR(lang_name):
    return construct_string(lang_name)


def LOG_MSG_LANG_CHANGED_SUCCESSFULLY(lang_name):
    return construct_string(lang_name)


def LOG_MSG_LANG_CHANGE_ERROR(lang_name):
    return construct_string(lang_name)

def LOG_NO_NEW_DATA_AVAILABLE(last_game_time):
    return construct_string(last_game_time)

def LOG_NEW_DATA_SENT(last_game_time):
    return construct_string(last_game_time)

def LOG_PREDICTION_IMPOSSIBLE(model_name):
    return construct_string(model_name)