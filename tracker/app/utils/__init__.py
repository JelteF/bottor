"""__init__.py - Various utilities to use throughout the system."""


def serialize_sqla(data):
    """Serialiation function to serialize any dicts or lists containing
    sqlalchemy objects. This is needed for conversion to JSON format."""
    # If has to_dict this is asumed working and it is used.
    if hasattr(data, 'to_dict'):
        return data.to_dict()

    if hasattr(data, '__dict__'):
        return data.__dict__

    # DateTime objects should be returned as isoformat.
    if hasattr(data, 'isoformat'):
        return str(data.isoformat())

    # Items in lists are iterated over and get serialized separetly.
    if isinstance(data, (list, tuple, set)):
        return [serialize_sqla(item) for item in data]

    # Dictionaries get iterated over.
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = serialize_sqla(value)

        return result

    # Just hope it works.
    return data


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d
