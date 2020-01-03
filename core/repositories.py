from abc import ABC


class BaseRepository(ABC):
    """Class representing the abstract base repository."""

    _model = None

    @classmethod
    def get(cls, filters={}, options={}):
        """Retrieve all data by filters."""
        return cls.get_model().select()

    @classmethod
    def find(cls, pk):
        return cls.get_model().get_by_id(pk)

    @classmethod
    def create(cls, payload):
        """Save a new register."""
        return cls.get_model().create(**payload)

    @classmethod
    def update(cls, pk, payload):
        """Update data by pk."""
        return cls.get_model().update(**payload).where(cls.get_model().id == pk).execute()
    #
    # @classmethod
    # async def delete(cls, payload):
    #   """Delete data by filters."""
    #   collection = cls.get_model().get_collection_name()
    #   doc = await get_connection()[collection].delete_one(payload)
    #   return doc

    @classmethod
    def get_model(cls):
        """Get the model."""
        if cls._model is None:
            raise ValueError('Model is required, set _model')
        return cls._model
