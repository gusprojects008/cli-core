import time
import json
from pathlib import Path

def new_file_path(fullpath: str | Path = None, fallback="output"):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    p = Path(fullpath if fullpath else fallback)
    return p.with_name(f"{p.stem}-{timestamp}{p.suffix}")

def iter_json_objects(path: str | Path):
    is_jsonl = str(path).lower().endswith(".jsonl")

    with open(path, "r", encoding="utf-8") as file:
        if is_jsonl:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Error decoding JSONL at line {line_num}: {error}")
        else:
            content = file.read()
            try:
                yield json.loads(content)
            except json.JSONDecodeError:
                decoder = json.JSONDecoder()
                idx = 0
                length = len(content)

                while idx < length:
                    while idx < length and content[idx].isspace():
                        idx += 1
                    if idx >= length:
                        break

                    try:
                        obj, idx = decoder.raw_decode(content, idx)
                        yield obj
                    except json.JSONDecodeError:
                        break

def walk_json(data, extractor: callable):
    if isinstance(data, dict):
        yield from extractor(data)
        for value in data.values():
            yield from walk_json(value, extractor)

    elif isinstance(data, list):
        for item in data:
            yield from walk_json(item, extractor)

def iter_from_json(
    path: str | Path,
    extractor: callable
):
    try:
        for obj in iter_json_objects(path):
            yield from walk_json(obj, extractor)
    except Exception as error:
        raise RuntimeError(f"Could not process file {path}: {error}")
