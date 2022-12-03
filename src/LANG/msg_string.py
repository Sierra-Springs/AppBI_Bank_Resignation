import importlib
import inspect

module_base = "LANG."

LANG_MSG_SOURCE = 'LANG_MSG_FRA'
LANG_MSG_SOURCE_ROLLBACK = 'LANG_MSG_ANG'

try:
    STRINGS_MSG = importlib.import_module(module_base + LANG_MSG_SOURCE).STRINGS_MSG
except:
    STRINGS_MSG = importlib.import_module(module_base + LANG_MSG_SOURCE_ROLLBACK).STRINGS_MSG

STRING_MSG_ROLLBACK = importlib.import_module(module_base + LANG_MSG_SOURCE_ROLLBACK).STRINGS_MSG


def launch_msg_lang(lang_source):
    global LANG_MSG_SOURCE, STRINGS_MSG
    LANG_MSG_SOURCE = lang_source
    STRINGS_MSG = importlib.import_module(module_base + lang_source).STRINGS_MSG


def get_lang_msg_source():
    return LANG_MSG_SOURCE


def construct_string(*kwargs):
    try:
        return STRINGS_MSG[inspect.stack()[1][3]].format(*kwargs)
    except:
        return STRING_MSG_ROLLBACK[inspect.stack()[1][3]].format(*kwargs)


def MSG_MISSING_KEY(key_name, example):
    return construct_string(key_name, inspect.stack()[1][3], example)


def MSG_MODEL_LOADED_SUCCESSFULLY(model_name):
    return construct_string(model_name)


def MSG_MODEL_LOAD_ERROR(model_name):
    return construct_string(model_name)


def MSG_PREDICTION_ATTEMPT_ON_NONE_MODEL():
    return construct_string()


def MSG_LOG_LANG_CHANGED_SUCCESSFULLY(lang_name):
    return construct_string(lang_name)


def MSG_LOG_LANG_CHANGE_ERROR(lang_name):
    return construct_string(lang_name)


def MSG_MSG_LANG_CHANGED_SUCCESSFULLY(lang_name):
    return construct_string(lang_name)


def MSG_MSG_LANG_CHANGE_ERROR(lang_name):
    return construct_string(lang_name)


def MSG_MSG_LOCAL_LANG_CHANGE_ERROR(lang_name):
    return construct_string(lang_name)


def MSG_NO_NEW_DATA_AVAILABLE():
    return construct_string()


def MSG_NEW_DATA_DOWNLOADED(last_game_time):
    return construct_string(last_game_time)


def MSG_PREDICTION_RECEIVED():
    return construct_string()


def MSG_PREDICTION_IMPOSSIBLE(model_name):
    return construct_string(model_name)


def MSG_GAME_TIME_RESET():
    return construct_string()


def MSG_NO_NEW_PREDICTION():
    return construct_string()


def MSG_LAST_GAME_TIME_IS(last_game_time):
    return construct_string(last_game_time)


def MSG_WAIT_FOR_THE_DOWNLOAD(wait_time_with_unit):
    return construct_string(wait_time_with_unit)

def W_MODEL_IS():
    return construct_string()

def W_WORKSPACE_IS():
    return construct_string()

def W_VALUES_ARE():
    return construct_string()

def W_CLICK_ME():
    return construct_string()

def W_LANG():
    return construct_string()

def W_DOWNLOAD_MODEL():
    return construct_string()

def W_PREDICT():
    return construct_string()

def W_LOAD_DATA():
    return construct_string()

def W_RESET():
    return construct_string()

def W_CHANGE_LANG():
    return construct_string()