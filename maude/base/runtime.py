import sys
import json

from maude_global import DEBUG

interactive_console = False

def exception_handler(exc_type, exc, tb):
    from rich.console import Console
    from rich.traceback import Traceback
    console = Console(file=sys.stderr)
    console.print(
            Traceback.from_exception(
                exc_type,
                exc,
                tb,
                width=100,
                extra_lines=3,
                theme=None,
                word_wrap=False,
                show_locals=True if DEBUG else False,
                indent_guides=True,
                suppress=(),
                max_frames=100,
            )
        )

def serialize_to_json(obj):
    json.dumps(obj, default=_json_dumper, indent=2)

def _json_dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__
