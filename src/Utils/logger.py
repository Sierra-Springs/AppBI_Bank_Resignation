from colorama import Fore, Style
import logging
import inspect
import os


class Logger:
    def __init__(self, log_func=None):
        self.log_func = log_func

    def log(self, *kwargs):
        self.log_func(*kwargs)

    def log_warn(self, *kwargs):
        pass

    def log_err(self, *kwargs):
        pass


class LoggingLogger(Logger):
    def __init__(self):
        super().__init__(log_func=logging.log)
        self.modulesToIgnore = []

    def get_caller_info(self):
        """
        :return: dictionnaire des infos de la fonction depuis laquelle l'appel au logger est fait
        exemple :
        ##% exe(self.calling_func_locals: [])
        pass
        ##%
        def foo(arg1, arg2):
            MSRH.foo()
            pass

        -> calling_func_args retourne : {'arg1': valArg1, 'arg2': valArg2}
        """
        pos = 1
        caller_file = inspect.getmodule(inspect.stack()[pos][0]).__file__
        while caller_file == os.path.realpath(__file__) or os.path.basename(caller_file) in self.modulesToIgnore:
            pos += 1
            caller_file = inspect.getmodule(inspect.stack()[pos][0]).__file__

        caller_func = inspect.stack()[pos][3]

        return {'caller_file': caller_file, 'caller_func': caller_func}

    def log(self, msg, level=logging.INFO, transmission=None):
        caller_info = self.get_caller_info()
        extra = {'transmission': repr(transmission)}
        extra.update(caller_info)
        self.log_func(msg=repr(msg), level=level, extra=extra)

    def log_warn(self, msg, transmission=None):
        self.log(msg, level=logging.WARN, transmission=transmission)

    def log_err(self, msg, transmission=None):
        self.log(msg, level=logging.ERROR, transmission=transmission)




class StyleLogger(Logger):
    def __init__(self, log_func=print):
        self.log_func = log_func
        self.colors = Fore
        self.reset_all = Style.RESET_ALL

    def log(self, *kwargs):
        self.log_func(*kwargs, f"{self.reset_all}")

    def log_warn(self, *kwargs):
        if len(kwargs) > 1:
            self.log_func(self.colors.YELLOW + kwargs[0], end='')
            self.log_func('', *kwargs[1:], f"{self.reset_all}")
        else:
            self.log_func(self.colors.YELLOW + kwargs[0], f"{self.reset_all}")


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__(log_func=print)


if __name__ == "__main__":
    lg = ConsoleLogger()
    lg.log(f"{lg.colors.CYAN}hello", "hi")
    lg.log_warn("hello")
    lg.log_warn("my", "dear")
    print("my", "dear")

    lg.log("hello" + "1")