import re
import json
import jsonpointer
from . import error


class Resolver:
    _VARIABLE_PATTERN = re.compile(r'(?P<variable>\$\((?P<pointer>/[\w]+(/[\w]+)*)\))')

    def _replace(self, dct: dict, value: str, depth: int) -> str:
        if 0 >= depth:
            raise error.CircularReferenceError(value)

        match = Resolver._VARIABLE_PATTERN.search(value)
        if not match:
            return value

        variable = match.group('variable')
        pointer = match.group('pointer')
        try:
            resolved = jsonpointer.resolve_pointer(dct, pointer)
        except jsonpointer.JsonPointerException as e:
            raise error.NotFoundError(value, pointer)

        if not isinstance(resolved, str):
            raise error.NotStringValueError(value, pointer, resolved)

        return self._replace(dct, value.replace(variable, resolved), depth - 1)

    def _resolve(self, root: dict, current: dict, maxdepth: int):
        for key, value in current.items():
            if isinstance(value, str):
                current[key] = self._replace(root, value, maxdepth)                
            elif isinstance(value, dict):
                self._resolve(root, value, maxdepth)

    def resolve(self, dct: dict, maxdepth=3):
        self._resolve(dct, dct, maxdepth)
