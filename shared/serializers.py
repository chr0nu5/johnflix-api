from datetime import date
from datetime import datetime


def json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type %s not serializable" % type(obj))
