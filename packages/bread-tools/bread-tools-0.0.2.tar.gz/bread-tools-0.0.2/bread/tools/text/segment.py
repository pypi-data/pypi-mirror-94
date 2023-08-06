import threading
import jieba


class Segment(object):
    """
    Split sentence to words.
    >>> seg = Segment.instance()
    >>> seg.split('China ABC')
    ['China', ' ', 'ABC']
    """
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls,
                 *args,
                 **kwargs):
        with Segment._instance_lock:
            if not hasattr(Segment, "_instance"):
                Segment._instance = Segment(*args, **kwargs)
        return Segment._instance

    def split(self,
              sentence):
        """
        Split sentence.
        :param sentence: The sentence to be split.
        :return: words as list.
        """
        return jieba.lcut(sentence)
