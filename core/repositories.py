from abc import ABC
from flask_restful import Resource, marshal


class BaseRepository(ABC):
    """Class representing the abstract base repository."""

    _model = None

    @classmethod
    def paginate(cls, filters={}, options={}):
        """Retrieve all data by filters paginated."""

        query = cls.get(filters, options)

        response = {
            'data': [marshal(i, cls.get_model().get_resource()) for i in query],
            # 'links': {
            #     'first': cls._get_url(1),
            #     'last': cls._get_url(cls._page_count),
            #     'prev': (
            #         cls._get_url(cls._page - 1)
            #         if cls._validate_page(cls._page - 1) else None
            #     ),
            #     'next': (
            #         cls._get_url(cls._page + 1)
            #         if cls._validate_page(cls._page + 1) else None
            #     )
            # },
            # 'meta': {
            #     'current_page': cls._page,
            #     'last_page': cls._page_count,
            #     'per_page': cls._limit,
            #     'total': cls._count,
            # }
        }

        return response

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

    @classmethod
    def _get_page(cls, options):
        """Get current page."""
        page = int(options.get('page', 1))
        return page if page > 0 else 1

    @classmethod
    def _get_limit(cls, options):
        """Get limit of registers."""
        limit = int(options.get('limit', cls.get_model().get_limit()))
        return limit if limit <= cls.get_model().get_max_limit() else cls.get_model().get_max_limit()
