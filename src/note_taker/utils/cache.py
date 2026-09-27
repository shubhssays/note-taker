import json
from pathlib import Path
from typing import Any

file_path = "cache.json"

def create_cache_path():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("{}", encoding="utf-8")
    return path

def set_cache(key:str, value:Any)-> None:
    path = create_cache_path()
    with open(path, "r", encoding="utf-8") as file:
        cache = json.load(file)

    cache[key] = value

    with open(path, "w", encoding="utf-8") as file:
       json.dump(cache, file, indent=4)

def get_cache(key: str)-> Any | None:
    path = create_cache_path()
    with open(path, "r", encoding="utf-8") as f:
        cache = json.load(f)
        return cache.get(key)

