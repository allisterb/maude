import json
import string

from numpy import float32
from maude_global import DEBUG

interactive_console = False
         
def _json_default(o):
    if isinstance(o, float32): 
        return str(o)
    else:
        try:
            return o.toJSON()
        except:
            return o.__dict__

def serialize_to_json_str(obj):
    return json.dumps(obj, default=_json_default, indent=2)

def serialize_to_json_bytes(obj):
    return serialize_to_json_str(obj).encode('utf-8')

class PluralFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        if format_spec.startswith('plural,'):
            words = format_spec.split(',')
            if value == 1:
                return words[1]
            else:
                return words[2]
        else:
            return super().format_field(value, format_spec)