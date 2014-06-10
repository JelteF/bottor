"""base_model.py - Some things done to spare time.

Extra functionality that is used by all models. It extends db.Model with extra
functions.

"""
from app import db
from app.utils import serialize_sqla
from datetime import datetime
import dateutil.parser


class BaseEntity(object):
    __table_args__ = {'sqlite_autoincrement': True}

    # Only json items if explicitly defined, and just print id when not
    # defined.
    jsons = None
    json_relationships = None
    prints = ('id',)

    # Columns that every model needs.
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now,
                         onupdate=datetime.now)

    def __repr__(self):
        """Used by print to print a model at server side. It uses the prints
        attribute from the object to determine what values to print."""
        first = True
        string = '<%s(' % (type(self).__name__)

        for attr in self.prints:
            string += (', ' if not first else '') + '"%s"' % (getattr(self,
                                                                      attr))
            first = False

        string += ')>'

        return string

    # Function to
    def to_dict(self):
        """Convert a sqlalchemy object instance to a dictionary.

        This is needed for json serialization of an object. The jsons attribute
        is used to determine what values to serialize (password hashes and such
        should not in there).

        """
        attrs = {}
        set_jsons = False

        if not self.jsons:
            self.jsons = (column.name for column in self.__table__.columns)
            set_jsons = True

        for column in self.jsons:
            value = serialize_sqla(getattr(self, column))
            attrs[column] = value

        if self.json_relationships:
            for rel in self.json_relationships:
                attrs[rel] = serialize_sqla(getattr(self, rel).all())

        if set_jsons:
            self.jsons = None

        return attrs

    @classmethod
    def merge_dict(cls, obj, relationships={}):
        """Merge dictionary as object."""
        # Get the correct entry from the database.
        if 'id' in obj and obj['id']:
            entry = cls.by_id(obj['id'])
            if not entry:
                return None

        # If the dict doesn't contain id it means the entry does not exist yet.
        else:
            entry = cls()

        # Remove id, created and modified, since those are things you want to
        # automaticaly update.
        obj.pop('id', None)
        obj.pop('created', None)
        obj.pop('modified', None)

        column_names = tuple(column.name for column in cls.__table__.columns)

        # Update all values from the dict that exist as a column or a
        # relationship.
        for key, value in obj.items():
            if key in column_names:
                columntype = str(cls.__table__.columns[key].type)
                if columntype == 'DATE' and value is not None:
                    if isinstance(value, str):
                        value = dateutil.parser.parse(value)
                elif columntype == 'TIME' and value is not None:
                    if isinstance(value, str):
                        value = dateutil.parser.parse(value).time()

                setattr(entry, key, value)

            elif key in relationships:
                setattr(entry, key, relationships[key].by_ids(value))

        return entry

    # For future proofing use new_dict when creating new entries, so it could
    # become a separate function if needed.
    new_dict = merge_dict

    @classmethod
    def by_id(cls, _id):
        """Get entry by id."""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def by_ids(cls, ids):
        """Get entries by id list."""
        try:
            return db.session.query(cls).filter(cls.id.in_(ids)).all()
        except:
            return []
