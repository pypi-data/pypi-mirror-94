import glob
import gzip
import os
import pickle
from typing import Any, Dict, Generator, List, Tuple


def _check_key(key: Any) -> None:
    if not isinstance(key, str):
        raise TypeError('key must be str.')


def load_pickle(path: str) -> Any:
    with open(path, 'rb') as f:
        return pickle.loads(gzip.decompress(f.read()))


def dump_pickle(path: str, val: Any) -> None:
    with open(path, 'wb') as f:
        f.write(gzip.compress(pickle.dumps(val)))


class PyKVS:

    def __init__(self, root: str) -> None:
        self.root: str = root
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        self.cache: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        _check_key(key)

        path: str = f'{self.root}/{key}.gz'
        if not os.path.exists(path):
            return default

        if key in self.cache:
            return self.cache[key]
        return load_pickle(path)

    def set(self, key: str, val: Any, cache: bool = False) -> None:
        _check_key(key)
        if cache:
            self.cache[key] = val

        path: str = f'{self.root}/{key}.gz'
        dump_pickle(path, val)

    def keys(self) -> List[str]:
        keys: List[str] = []
        for path in glob.glob(f'{self.root}/*.gz'):
            key, _ = os.path.splitext(os.path.basename(path))
            keys.append(key)
        return keys

    def values(self) -> Generator[Any, None, None]:
        for path in glob.glob(f'{self.root}/*.gz'):
            key, _ = os.path.splitext(os.path.basename(path))
            yield self.get(key)

    def items(self) -> Generator[Tuple[str, Any], None, None]:
        for path in glob.glob(f'{self.root}/*.gz'):
            key, _ = os.path.splitext(os.path.basename(path))
            yield (key, self.get(key))

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, val: Any) -> None:
        return self.set(key, val)

    def __delitem__(self, key: str) -> None:
        _check_key(key)
        path: str = f'{self.root}/{key}.gz'
        os.remove(path)
