import os
import pickle


class Storage(object):
    """
    Lightweight object storage.
    """

    @staticmethod
    def save_objects(objects, save_path):
        """
        Save objects.
        >>> Storage.save_objects(objects=[0,1,2],save_path='__cases/obj.pk')
        True
        """
        if os.path.exists(save_path):
            os.remove(save_path)

        with open(save_path, 'wb') as file:
            pickle.dump(objects, file, pickle.HIGHEST_PROTOCOL)
        return True

    @staticmethod
    def load_objects(saved_path):
        """
        load objects.
        >>> Storage.load_objects(saved_path='__cases/obj.pk')
        [0, 1, 2]
        """
        objects = None
        if os.path.exists(saved_path):
            with open(saved_path, 'rb') as file:
                objects = pickle.load(file)
        return objects
