from abc import ABC
from playhouse.flask_utils import get_object_or_404
from playhouse.shortcuts import update_model_from_dict
from peewee import Model


class BaseService(ABC):
    """Class representing the abstract base service."""

    _repository = None

    @classmethod
    def get(cls, filters={}, options={}):
        """Retrieve all data by filters."""
        return cls.get_repository().get()

    @classmethod
    def find(cls, pk):
        """Get one data by pk."""
        return cls.get_repository().find(pk)

    @classmethod
    def get_or_404(cls, pk):
        """Get one data by pk or abort with http status code 404."""
        return get_object_or_404(cls.get_model(), cls.get_model().id == pk)

    @classmethod
    def create(cls, payload):
        """Save a new register."""
        return cls.get_repository().create(payload)

    @classmethod
    def update(cls, pk_or_model, payload):
        """Update data by pk or model."""
        if isinstance(pk_or_model, Model):
            update_model_from_dict(pk_or_model, payload).save()
            return pk_or_model

        return cls.get_repository().update(pk_or_model, payload)

    @classmethod
    def update_or_404(cls, pk, payload):
        """Update data by pk or abort with http status code 404."""
        return cls.update(cls.get_or_404(pk), payload)

    @classmethod
    def delete(cls, pk_or_model):
        """Delete data by pk or model."""
        if isinstance(pk_or_model, Model):
            return pk_or_model.delete_instance()

        return cls.find(pk_or_model).delete_instance()

    @classmethod
    def delete_or_404(cls, pk):
        """Delete data by pk or abort with http status code 404."""
        return cls.delete(cls.get_or_404(pk))

    @classmethod
    def get_repository(cls):
        """Get repository."""
        if cls._repository is None:
            raise ValueError('Repository is required, set _repository')
        return cls._repository

    @classmethod
    def get_model(cls):
        """Get the model."""
        return cls.get_repository().get_model()
