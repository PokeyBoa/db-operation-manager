# -*- coding: UTF-8 -*-
import json
from decimal import Decimal
from datetime import datetime

# The Python "TypeError: Object of type set is not JSON serializable"
# occurs when we try to convert a set object to a JSON string.


class AdvancedEncoder(json.JSONEncoder):

    """
    Supports the following objects and types by default:

    +-------------------+---------------+
    | Python            | JSON          |
    +===================+===============+
    | dict              | object        |
    +-------------------+---------------+
    | list, tuple       | array         |
    +-------------------+---------------+
    | str               | string        |
    +-------------------+---------------+
    | int, float        | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | None              | null          |
    +-------------------+---------------+

    To extend this to recognize other objects, subclass and implement a
    ``.default()`` method with another method that returns a serializable
    object for ``o`` if possible, otherwise it should call the superclass
    implementation (to raise ``TypeError``).
    """

    def default(self, o):
        # Support set type
        if isinstance(o, set):
            return sorted(list(o))

        # Support byte type
        elif isinstance(o, bytes):
            return o.decode("utf-8")

        # Support exact decimals type
        elif isinstance(o, Decimal):
            return str(o)

        # Support time type
        elif isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        # Let the base class default method raise the TypeError
        # return json.JSONEncoder.default(self, o)
        return super().default(o)


def _advjson_dump(data):
    """
    Extensible example:
    data = {
        "bytes": b'abc',
        "decimal": Decimal("256.99999999999999"),
        "set": {'A', 'B', 'C'},
        "time": datetime.now()
    }
    """
    result = json.dumps(
        data,
        cls=AdvancedEncoder,
        ensure_ascii=False
    )
    return result


