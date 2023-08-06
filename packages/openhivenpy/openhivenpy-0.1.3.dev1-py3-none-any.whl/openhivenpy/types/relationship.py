import logging
import sys
from marshmallow import Schema, fields, post_load, ValidationError, RAISE

from . import HivenObject
from . import user
from .. import utils
from ..exceptions import exception as errs

logger = logging.getLogger(__name__)

__all__ = ['Relationship']


class RelationshipSchema(Schema):
    user_id = fields.Int(required=True)
    user = fields.Raw(required=True)
    type = fields.Int(required=True)
    id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)


# Creating a Global Schema for reuse-purposes
GLOBAL_SCHEMA = RelationshipSchema()


class Relationship(HivenObject):
    """
    Represents a user-relationship with another user or bot

    ---

    Possible Types:
    
    0 - No Relationship
    
    1 - Outgoing Friend Request
    
    2 - Incoming Friend Request
    
    3 - Friend
    
    4 - Restricted User
    
    5 - Blocked User
    """
    def __init__(self, data: dict, http):
        try:
            user_data = data.get('user')
            # user_id does not always exist
            self._user_id = utils.convert_value(int, data.get('user_id'))
            self._user = user.User.from_dict(user_data, http)
            self._type = data.get('type')
            self._id = utils.convert_value(int, data.get('id'))
            self._recipient_id = utils.convert_value(int, data.get('recipient_id'))
            self._http = http
        
        except Exception as e:
            utils.log_traceback(msg="[RELATIONSHIP] Traceback:",
                                suffix="Failed to initialize the Relationship object; \n"
                                       f"{sys.exc_info()[0].__name__}: {e} >> Data: {data}")
            raise errs.FaultyInitialization(f"Failed to initialize Relationship object! "
                                            f"> {sys.exc_info()[0].__name__}: {e}")

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        info = [
            ('id', self.id),
            ('recipient_id', self.recipient_id),
            ('user_id', self.user_id),
            ('user', repr(self.user)),
            ('type', self.type)
        ]
        return '<Relationship {}>'.format(' '.join('%s=%s' % t for t in info))

    @property
    def user(self) -> user.User:
        return self._user

    @property
    def type(self) -> int:
        return self._type

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def recipient_id(self) -> int:
        return self._recipient_id

    @property
    def id(self) -> int:
        return self._id
