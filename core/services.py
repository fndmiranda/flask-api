from abc import ABC
from flask import abort
from playhouse.flask_utils import get_object_or_404
from playhouse.shortcuts import update_model_from_dict
from peewee import Model


class BaseService(ABC):
    """Class representing the abstract base service."""

    _repository = None

    def paginate(self, expressions=None, options={}):
        """Retrieve all data by filters paginated."""
        return self.get_repository().paginate(expressions, options)

    def get(self, filters={}, options={}):
        """Retrieve all data by filters."""
        return self.get_repository().get()

    def find(self, pk):
        """Retrieve one data by pk."""
        return self.get_repository().find(pk)

    def find_by(self, expressions={}):
        """Retrieve one data by expressions."""
        return self.get_repository().find_by(expressions)

    def find_or_404(self, pk):
        """Retrieve one data by pk or abort with http status code 404."""
        data = self.find(pk)
        return data if data else abort(404)

    def create(self, payload):
        """Save a new register."""
        return self.get_repository().create(payload)

    def update(self, pk_or_model, payload):
        """Update data by pk or model."""
        if isinstance(pk_or_model, Model):
            update_model_from_dict(pk_or_model, payload).save()
            return pk_or_model

        return self.get_repository().update(pk_or_model, payload)

    def update_or_404(self, pk, payload):
        """Update data by pk or abort with http status code 404."""
        return self.update(self.find_or_404(pk), payload)

    def delete(self, pk_or_model):
        """Delete data by pk or model."""
        if isinstance(pk_or_model, Model):
            return pk_or_model.delete_instance()

        return self.find(pk_or_model).delete_instance()

    def delete_or_404(self, pk):
        """Delete data by pk or abort with http status code 404."""
        return self.delete(self.find_or_404(pk))

    def get_repository(self):
        """Get repository."""
        if self._repository is None:
            raise ValueError('Repository is required, set _repository')
        return self._repository

    def get_model(self):
        """Get the model."""
        return self.get_repository().get_model()
