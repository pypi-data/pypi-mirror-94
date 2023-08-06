from pathlib import Path
from os import environ
from itertools import chain
from dataclasses import dataclass, InitVar, field
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from asyncio import get_running_loop
from shutil import copyfileobj
from enum import Enum
from tempfile import mkdtemp
from warnings import warn

from ruamel.yaml import YAML
from more_itertools import unique_everseen

from .file_locking import lock_file

executor = ThreadPoolExecutor(max_workers=5)


__all__ = (
    'File',
    'FileType',
    'ProgramFiles',
)


class FileType(Enum):
    config = 'config'
    program = 'program'
    data = 'data'
    runtime = 'runtime'
    cache = 'cache'


def set_attr(self, key, value):
    object.__setattr__(self, key, value)


@dataclass(frozen=True)
class File:
    name: str
    write_dir: InitVar[Path]
    search_dirs: InitVar[Sequence[Path]]
    type: FileType
    path: Path = field(init=False)
    search_files: tuple[Path] = field(init=False)

    yaml = YAML(pure=True)
    yaml.default_flow_style = False

    def __post_init__(self, write_dir, search_dirs):
        set_attr(self, 'path', write_dir / self.name)
        set_attr(self, 'search_files', tuple(
            path / self.name
            for path in search_dirs
        ))

    def merge(self, data_mappings):
        new = {}
        for mapping in data_mappings:
            new.update(mapping)

        return new

    def get_data_sync(self):
        data_mappings = (
            self.read_file(file)
            for file in reversed(self.search_files)
        )

        return self.merge(
            filter(
                lambda mapping: mapping is not None,
                data_mappings,
            ),
        )

    def read_file(self, path):
        try:
            with lock_file(path, 'r') as file_obj:
                return self.yaml.load(file_obj)
        except FileNotFoundError:
            return None

    async def get_data(self):
        return await executor.submit(self.get_data_sync)

    def write_file_sync(self, new_data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with lock_file(self.path, 'w', exclusive=True) as file_obj:
            self.yaml.dump(new_data, file_obj)

    async def write_file(self, new_data):
        return await get_running_loop().run_in_executor(
            executor,
            self.write_file_sync,
            new_data,
        )

    def copy_file_sync(self, new_stream, *, mode='w'):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with lock_file(self.path, mode=mode) as file_obj:
            copyfileobj(new_stream, file_obj)


class DirList(tuple):
    def __new__(cls, write_path, path_iter, /):
        instance = super().__new__(cls, chain((write_path,), path_iter))
        instance.write_path = write_path
        return instance


RUNTIME_VAR = 'XDG_RUNTIME_DIR'
CACHE_VAR = 'XDG_CACHE_HOME'
DATA_VAR = 'XDG_DATA_HOME'
DATA_SEARCH = 'XDG_DATA_DIRS'
CONFIG_VAR = 'XDG_CONFIG_HOME'
CONFIG_SEARCH = 'XDG_CONFIG_DIRS'


default_eager_files = object()


class ProgramFiles:
    def __init__(
            self,
            name,
            *,
            file_cls=File,
            eager_files=default_eager_files,
    ):
        self.name = name
        self.__file_cls = file_cls

        self.__data_dirs = self.__get_paths(
            DATA_VAR,
            fallback=Path.home() / '.local/share',
            search_paths_var=DATA_SEARCH,
            search_fallback=(Path(' /usr/local/share/'), Path('/usr/share'))
        )

        self.__config_dirs = self.__get_paths(
            CONFIG_VAR,
            fallback=Path.home() / '.config',
            search_paths_var=CONFIG_SEARCH,
            search_fallback=(Path('/etc/xdg'), ),
        )

        runtime_dir_set = RUNTIME_VAR in environ
        if runtime_dir_set and Path(environ[RUNTIME_VAR]).is_absolute():
            self.__runtime_dir = Path(environ[RUNTIME_VAR])
        else:
            self.__runtime_dir = None

        if CACHE_VAR in environ and Path(environ[CACHE_VAR]).is_absolute():
            self.__cache_dir = Path(environ[CACHE_VAR])
        else:
            self.__cache_dir = Path.home()/'.cache'/self.name

        if eager_files:
            if eager_files is default_eager_files:
                eager_files = {
                    'config': (name, )
                }

            for type, files in eager_files.items():
                for file in files:
                    self.get(FileType(type), file)

    def get_config_file(self, name, *args, **kwargs):
        file = self.__file_cls(
            self.get_file_name(name, *args, **kwargs),
            self.__config_dirs.write_path,
            self.__config_dirs,
            FileType.config,
            *args,
            **kwargs,
        )

        return file

    def get_data_file(self, name, *args, **kwargs):
        file = self.__file_cls(
            self.get_file_name(name, *args, **kwargs),
            self.__data_dirs.write_path,
            self.__data_dirs,
            FileType.data,
            *args,
            **kwargs,
        )

        return file

    def get_runtime_file(self, name, *args, **kwargs):
        if self.__runtime_dir is None:
            warn(
                '$XDG_RUNTIME_DIR not set in env defaulting to temp dir',
                ResourceWarning,
            )
            self.__runtime_dir = Path(mkdtemp())

        file = self.__file_cls(
            self.get_file_name(name, *args, **kwargs),
            self.__runtime_dir,
            (self.__runtime_dir, ),
            FileType.runtime,
            *args,
            **kwargs,
        )

        return file

    def get_cache_file(self, name, *args, **kwargs):
        file = self.__file_cls(
            self.get_file_name(name, *args, **kwargs),
            self.__cache_dir,
            (self.__cache_dir, ),
            FileType.cache,
            *args,
            **kwargs,
        )

        return file

    def get(self, type, name, *args, **kwargs):
        if type is FileType.cache:
            return self.get_cache_file(name, *args, **kwargs)
        elif type is FileType.config:
            return self.get_config_file(name, *args, **kwargs)
        elif type is FileType.runtime:
            return self.get_runtime_file(name, *args, **kwargs)
        elif type is FileType.data:
            return self.get_data_file(name, *args, **kwargs)

    def get_file_name(self, name):
        return f'{name}.yaml'

    def __get_paths(
        self,
        env_var,
        *,
        fallback,
        search_paths_var,
        search_fallback,
    ):
        user_path = fallback
        if env_var in environ:
            path = Path(environ[env_var])
            if path.is_absolute():
                user_path = path

        paths = search_fallback
        if search_paths_var in environ and environ[search_paths_var]:
            env_str = environ[search_paths_var]
            str_paths = env_str.split(':')
            search_paths = tuple(
                Path(path)
                for path in str_paths
                if Path(path).is_absolute()
            )

            if search_paths:
                paths = search_paths

        if user_path in paths:
            index = paths.index(user_path)
            start = paths[:index]
            end = paths[index + 1:]
            paths = start + end

        return DirList(
            user_path / self.name,
            unique_everseen(
                path / self.name
                for path in paths
            )
        )
