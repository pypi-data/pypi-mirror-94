import re


class String(object):

    @staticmethod
    def is_number(num):
        """
        Check whether it is a number.
        >>> String.is_number(num='13569')
        True
        >>> String.is_number(num='126B1')
        False
        """
        pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+$')
        result = pattern.match(num)
        if result:
            return True
        else:
            return False

    @staticmethod
    def get_lines_from_text(text):
        """
        Text segmentation based on standard.
        >>> String.get_lines_from_text('1。2！3？')
        ['1', '2', '3', '']
        """
        return re.split(r'。|\?|!|？|！', text)
