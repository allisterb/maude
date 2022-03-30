import sys
import json
from logging import error
from maude_global import DEBUG

interactive_console = False
         
def serialize_to_json(obj):
    json.dumps(obj, default=_json_dumper, indent=2)

def _json_dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__
