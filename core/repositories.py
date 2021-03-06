import urllib.parse
import math
from abc import ABC
from flask import request
from core.models import Session


class BaseRepository(ABC):
    """Class representing the abstract base repository."""

    _session = Session()
    _model = None
    _schema = None
    _options = {}

    @classmethod
    def set_options(cls, options={}):
        """Set optional data, eg: to pagination."""
        cls._options.update(options)
        return cls

    @classmethod
    def paginate(cls, **expressions):
        """Retrieve all data by expressions paginated."""
        cls._page = cls._get_page()
        cls._limit = cls._get_limit()
        cls._count = cls.count(**expressions)
        cls._page_count = int(math.ceil(cls._count / cls._limit))

        query = cls.filter_by(**expressions).offset(cls._limit * (cls._page - 1)).limit(cls._limit)

        schema = cls.get_schema(many=True)

        response = {
            'data': schema.dump(query.all()),
            'meta': {
                'current_page': cls._page,
                'per_page': cls._limit,
                'total': cls._count,
            },
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
                ),
            },
        }

        return response

    @classmethod
    def filter_by(cls, **expressions):
        """Apply the given filtering criterion."""
        return cls._session.query(cls.get_model()).filter_by(**expressions)

    @classmethod
    def filter(cls, *criterion):
        """Apply the given filtering criterion using SQL expressions."""
        return cls._session.query(cls.get_model()).filter(*criterion)

    @classmethod
    def query(cls):
        """Return a query session."""
        return cls._session.query(cls.get_model())

    @classmethod
    def get(cls, **expressions):
        """Retrieve all data by expressions."""
        return cls.filter_by(**expressions).all()

    @classmethod
    def find(cls, pk):
        """Retrieve one data by pk."""
        data = cls._session.query(cls.get_model()).get(pk)
        cls._session.commit()
        return data

    @classmethod
    def count(cls, **expressions):
        """Count the number of registers by expressions."""
        query = cls.filter_by(**expressions)
        cls._session.commit()

        return query.count()

    @classmethod
    def update(cls, pk_or_model, payload={}):
        """Update a register by pk or model."""
        data = pk_or_model if isinstance(pk_or_model, cls.get_model()) else cls.find(pk_or_model)

        for column, value in payload.items():
            if hasattr(data, column):
                setattr(data, column, value)

        cls._session.commit()

        return data

    @classmethod
    def create(cls, payload):
        """Save a new register."""
        data = cls.make(**payload)

        cls._session.add(data)
        cls._session.commit()

        return data

    @classmethod
    def delete(cls, pk_or_model):
        """Delete a register by pk or model."""
        data = pk_or_model if isinstance(pk_or_model, cls.get_model()) else cls.find(pk_or_model)

        cls._session.delete(data)
        cls._session.commit()

        return data

    @classmethod
    def make(cls, **kwargs):
        """Make a instance of the model."""
        if cls._model is None:
            raise ValueError('Model is required, set _model')
        return cls._model(**kwargs)

    @classmethod
    def get_model(cls):
        """Get the model."""
        if cls._model is None:
            raise ValueError('Model is required, set _model')
        return cls._model

    @classmethod
    def get_schema(cls, **kwargs):
        """Get the schema."""
        if cls._schema is None:
            raise ValueError('Schema is required, set _schema')
        return cls._schema(**kwargs)

    @classmethod
    def _get_page(cls):
        """Get current page."""
        page = cls._options.get('page') if 'page' in cls._options else int(request.args.get('page', 1))
        return page if page > 0 else 1

    @classmethod
    def _get_limit(cls):
        """Get retrieve limit of registers."""
        limit = cls._options.get('limit') if 'limit' in cls._options else int(
            request.args.get('limit', cls.get_model().get_default_limit())
        )
        limit = limit if limit <= cls.get_model().get_max_limit() else cls.get_model().get_max_limit()
        return limit if limit > 0 else 1

    @classmethod
    def _validate_page(cls, page):
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
