import threading
from configparser import ConfigParser


class Configuration(object):
    """
    Read Configuration and Cache them.
    >>> config = Configuration.instance(config_file='__cases/config.ini')
    >>> config.get('example','name')
    "'Joe'"
    >>> config.get_int('example','age')
    41
    >>> config.get_float('example','height')
    163.5
    >>> config.get_boolean('example','is_fat')
    False
    """

    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls,
                 *args,
                 **kwargs):
        with Configuration._instance_lock:
            if not hasattr(Configuration, "_instance"):
                Configuration._instance = Configuration(*args, **kwargs)
        return Configuration._instance

    def __init__(self,
                 config_file):
        """
        Load configuration.
        :param config_file: Configuration file path.
        """
        self.__parser = ConfigParser()
        self.__parser.read(config_file, encoding='UTF-8')

    def get(self,
            section,
            option):
        """
        Get value by section and option.
        :param section: The section to be selected.
        :param option:  The option to be selected.
        :return: The value of the result.
        """
        return self.__parser.get(section=section, option=option)

    def get_int(self,
                section,
                option):
        """
        Get value by section and option.
        :param section: The section to be selected.
        :param option:  The option to be selected.
        :return: The value of the result.
        """
        return self.__parser.getint(section=section, option=option)

    def get_float(self,
                  section,
                  option):
        """
        Get value by section and option.
        :param section: The section to be selected.
        :param option:  The option to be selected.
        :return: The value of the result.
        """
        return self.__parser.getfloat(section=section, option=option)

    def get_boolean(self,
                    section,
                    option):
        """
        Get value by section and option.
        :param section: The section to be selected.
        :param option:  The option to be selected.
        :return: The value of the result.
        """
        return self.__parser.getboolean(section=section, option=option)
