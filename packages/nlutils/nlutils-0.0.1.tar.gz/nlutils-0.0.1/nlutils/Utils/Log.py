import time
import os
from datetime import datetime
from ..CommonDefine import LogLevel

# DIS
# from .CommonDefine import LogLevel



def get_local_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Logger(object):

    def __init__(self, level=LogLevel.INFO, write_to_file=False, log_path='/tmp/log-{}'.format(get_local_time())):
        self.write_to_file = write_to_file
        if write_to_file:
            if not log_path:
                raise ValueError("Argument [log_path] cannot be None when write_to_file is True")
            else:
                self.log_path = log_path
        self.level = level

    @staticmethod
    def instance():
        return Logger()

    def set_log_path(self, log_path):
        self.log_path = log_path

    def set_level(self, level):
        self.level = level

    def log_fatal(self, message):
        if self.level.value>= LogLevel.FATAL.value:
            log_content = "\033[1;36m{}\033[0m \033[1;35mFATAL: {}\033[0m".format(get_local_time(), message)
            print(log_content)
            if self.write_to_file and os.path.isfile(self.log_path):
                with open(self.log_path, 'a') as f:
                    f.writelines([log_content])
    
    def log_error(self, message):
        if self.level.value >= LogLevel.ERROR.value:
            log_content = "\033[1;36m{}\033[0m \033[1;31mERROR: {}\033[0m".format(get_local_time(), message)
            print(log_content)
            if self.write_to_file and os.path.isfile(self.log_path):
                with open(self.log_path, 'a') as f:
                    f.writelines([log_content])

    def log_warning(self, message):
        if self.level.value >= LogLevel.WARNING.value:
            log_content = "\033[1;36m{}\033[0m \033[1;33mWARNING: {}\033[0m".format(get_local_time(), message)
            print(log_content)
            if self.write_to_file and os.path.isfile(self.log_path):
                with open(self.log_path, 'a') as f:
                    f.writelines([log_content])
    
    def log_info(self, message):
        if self.level.value >= LogLevel.INFO.value:
            log_content = "\033[1;36m{}\033[0m \033[1;32mINFO: {}\033[0m".format(get_local_time(), message)
            print(log_content)
            if self.write_to_file and os.path.isfile(self.log_path):
                with open(self.log_path, 'a') as f:
                    f.writelines([log_content])
    
    def log_debug(self, message):
        if self.level.value >= LogLevel.DEBUG.value:
            log_content = "\033[1;36m{}\033[0m \033[1;37mDEBUG: {}\033[0m".format(get_local_time(), message)
            print(log_content)
            if self.write_to_file and os.path.isfile(self.log_path):
                with open(self.log_path, 'a') as f:
                    f.writelines([log_content])
    
    @staticmethod
    def log_performance(func):
        def wrapper():
            start = time.time()
            func()
            end = time.time()
            print("\033[1;36m{}\033[0m \033[1;34mPERFORMANCE: {} consumes {} seconds\033[0m".format(get_local_time(), func.__name__, end -start))
        return wrapper        

if __name__ == '__main__':
    calculate_time()
    Logger.instance().log_warning("This is a test warning.")
    Logger.instance().log_error("This is a test error.")
    Logger.instance().log_fatal("This is a test fatal.")
    Logger.instance().log_info("This is a test info.")
    Logger.instance().log_debug("This is a test debug.")