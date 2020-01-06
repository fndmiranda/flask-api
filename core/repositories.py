from abc import ABC
from flask import request
from peewee import Model
import urllib.parse
import math


class BaseRepository(ABC):
    """Class representing the abstract base repository."""

    _model = None

    @classmethod
    def paginate(cls, expressions=None, options={}):
        """Retrieve all data by expressions paginated."""

        query = cls.get(expressions, options).paginate(cls._get_page(options), cls._get_limit(options))

        response = {
            'data': query,
            'links': {
                'first': cls._get_url(1),
                'last': cls._get_url(cls._page_count),
                'prev': (
                    cls._get_url(cls._page - 1)
                    if cls._validate_page(cls._page - 1) else None
                ),
                'next': (
                    cls._get_url(cls._page + 1)
                    if cls._validate_page(cls._page + 1) else None
                )
            },
            'meta': {
                'current_page': cls._page,
                'last_page': cls._page_count,
                'per_page': cls._limit,
                'total': cls._count,
            }
        }

        return response

    @classmethod
    def get(cls, expressions=None, options={}):
        """Retrieve all data by expressions."""

        cls._limit = cls._get_limit(options)
        cls._page = cls._get_page(options)
        cls._count = cls.count(expressions)
        cls._page_count = int(math.ceil(cls._count / cls._limit))

        return cls.get_model().select().where(expressions)

    @classmethod
    def find(cls, pk):
        """Retrieve one data by pk."""
        return cls.get_model().get_by_id(pk)

    @classmethod
    def create(cls, payload):
        """Save a new register."""
        return cls.get_model().create(**payload)

    @classmethod
    def update(cls, pk, payload):
        """Update data by pk."""
        return cls.get_model().update(**payload).where(cls.get_model().id == pk).execute()

    @classmethod
    def count(cls, expressions):
        """Count the number of registers by expressions."""
        return cls.get_model().select().where(expressions).count()

    @classmethod
    def get_model(cls):
        """
        Get the model.

        :rtype: Model
        """
        if cls._model is None:
            raise ValueError('Model is required, set _model')
        return cls._model

    @classmethod
    def _validate_page(cls, page):
        """Check if page is valid."""
        if cls._count > 0:
            if page > cls._page_count or page < 1:
                return None

            return page

        return False

    @classmethod
    def _get_url(cls, page):
        """"Get current URL with page query string."""
        url_parts = list(urllib.parse.urlparse(request.url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update({'page': page})
        url_parts[4] = urllib.parse.urlencode(query)

        return urllib.parse.urlunparse(url_parts)

    @classmethod
    def _get_page(cls, options={}):
        """Get current page."""
        page = int(options.get('page', 1))
        return page if page > 0 else 1

    @classmethod
    def _get_limit(cls, options={}):
        """Get limit of registers."""
        limit = cls.get_model().get_limit() if options.get('limit') is None else int(options.get('limit'))

        return limit if limit <= cls.get_model().get_max_limit() else cls.get_model().get_max_limit()
