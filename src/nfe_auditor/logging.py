import json
from typing import Any


def emit_event(event: str, **data: Any) -> None:
    print(json.dumps({"event": event, **data}, ensure_ascii=False, sort_keys=True))
