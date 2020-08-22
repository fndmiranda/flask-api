from app.schema import ma
from user.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'is_admin', 'created_at', 'updated_at', '_links')
        ordered = True

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('api.userdetail', user_id='<id>'), 'collection': ma.URLFor('api.userlist')}
    )
