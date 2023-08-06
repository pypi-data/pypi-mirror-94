import numpy as np


class Similar(object):
    """
    Similarity calculation.
    """

    def __init__(self):
        pass

    @staticmethod
    def cosine(vector_a,
               vector_b):
        """
        Cosine similarity calculation of two vectors.
        :param vector_a: Vector a.
        :param vector_b: Vector b.
        :return: Returns a value between 0 and 1, the larger value means more similar.
        >>> Similar.cosine(vector_a=[0.5,0.4],vector_b=[0.6,0.7])
        0.9912432621534781
        """
        if vector_a is None or vector_b is None:
            return -1
        if len(vector_a) != len(vector_b):
            return 0
        vector_a = np.mat(vector_a)
        vector_b = np.mat(vector_b)
        num = float(vector_a * vector_b.T)
        cos = num / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
        similar_value = 0.5 + 0.5 * cos
        return similar_value
