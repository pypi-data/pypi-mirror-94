
import pathlib


from generallibrary import VerInfo, initBases, TreeDiagram, classproperty

from generalfile.errors import InvalidCharacterError
from generalfile.path_lock import Path_ContextManager
from generalfile.path_operations import Path_Operations
from generalfile.path_strings import Path_Strings
from generalfile.optional_dependencies.path_spreadsheet import Path_Spreadsheet
from generalfile.optional_dependencies.path_text import Path_Text
from generalfile.optional_dependencies.path_cfg import Path_Cfg


@initBases
class Path(TreeDiagram, Path_ContextManager, Path_Operations, Path_Strings, Path_Spreadsheet, Path_Text, Path_Cfg):
    """ Immutable cross-platform Path.
        Built on pathlib and TreeDiagram.
        Implements rules to ensure cross-platform compatability.
        Adds useful methods.
        Todo: Add a proper place for all variables, add working_dir, sys.executable and sys.prefix to it.
        Todo: Raise suppressable warning if space in Path. """
    verInfo = VerInfo()
    path_delimiter = verInfo.pathDelimiter
    _Path_cls = ...

    def __init__(self, path=None, parent=None):
        path = self._scrub(str_path="" if path is None else str(path))
        self.path = self.data_keys_add(key="path", value=path, unique=True)

        self._path = pathlib.Path(self.path)

    copy_to = NotImplemented  # Maybe something like this to disable certain methods

    @classproperty
    def Path(self):
        """ :rtype: Path """
        return self._Path_cls

    def get_parent(self, index=0):
        """ Override to generate all parents if direct parent is None.

            :rtype: Path or None """
        if self._parent is None:
            self._generate_parents()
        return TreeDiagram.get_parent(self=self, index=index)

    def _generate_parents(self):
        path = None
        for pathlib_path in reversed(self._path.parents):
            path = self.Path(path="" if str(pathlib_path) == "." else str(pathlib_path), parent=path)
        self.set_parent(path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.__str__()

    def __truediv__(self, other):
        """ :rtype: generalfile.Path """
        return self.Path(self._path / str(other))
    
    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __contains__(self, item):
        return self.path.__contains__(item)

    def _scrub(self, str_path):
        str_path = self._replace_delimiters(str_path=str_path)
        str_path = self._invalid_characters(str_path=str_path)
        str_path = self._trim(str_path=str_path)
        str_path = self._delimiter_suffix_if_root(str_path=str_path)
        return str_path

    def _delimiter_suffix_if_root(self, str_path):
        if len(str_path) == 2 and str_path[1] == ":":
            return f"{str_path}{self.path_delimiter}"
        return str_path

    def _replace_delimiters(self, str_path):
        str_path = str_path.replace("/", self.path_delimiter)
        str_path = str_path.replace("\\", self.path_delimiter)
        # str_path = str_path.replace(self.path_delimiter_alternative, self.path_delimiter)  # Don't remember why I commented this
        return str_path

    def _invalid_characters(self, str_path):
        # Simple invalid characters testing from Windows
        for character in '<>"|?*':
            if character in str_path:
                raise InvalidCharacterError(f"Invalid character '{character}' in '{str_path}'")
        if ":" in str_path:
            if not self.verInfo.pathRootHasColon:
                raise InvalidCharacterError(f"Path has a colon but '{self.verInfo.os}' doesn't use colon for path root: '{str_path}'")
            if str_path[1] != ":":
                raise InvalidCharacterError(f"Path has a colon but there's no colon at index 1: '{str_path}'")
            if len(str_path) >= 3 and str_path[2] != self.path_delimiter:
                raise InvalidCharacterError(f"Path has a colon but index 2 is not a delimiter: '{str_path}'")
            if ":" in str_path[2:]:
                raise InvalidCharacterError(f"Path has a colon that's not at index 1: '{str_path}'")
        if str_path.endswith("."):
            raise InvalidCharacterError(f"Path cannot end with a dot ('.').")
        return str_path

    def _trim(self, str_path):
        if not self.verInfo.pathRootIsDelimiter and str_path.startswith(self.path_delimiter):
            str_path = str_path[1:]
        if str_path.endswith(self.path_delimiter) and len(str_path) > 1:
            str_path = str_path[0:-1]
        return str_path

    def view(self, only_last_part=True, indent=1, relative=False, custom_repr=None, print_out=True):
        """ Override view to use default custom repr. """
        if not self.get_children():
            list(self.get_paths_recursive())

        if only_last_part and custom_repr is None:
            custom_repr = lambda path: path.parts()[-1]
        return TreeDiagram.view(self=self, indent=indent, relative=relative, custom_repr=custom_repr, print_out=print_out)

setattr(Path, "_Path_cls", Path)















































