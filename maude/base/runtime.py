import sys
import json
import numpy
from logging import error
from maude_global import DEBUG

interactive_console = False
         
def serialize_to_json(obj):
    return json.dumps(obj, default=_json_default, indent=2)

def _json_default(o):
    if isinstance(o, numpy.float32): 
        return str(o)
    else:
        try:
            return o.toJSON()
        except:
            return o.__dict__

