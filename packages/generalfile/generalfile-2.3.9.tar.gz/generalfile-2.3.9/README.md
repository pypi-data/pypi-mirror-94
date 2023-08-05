# generalfile
Easily manage files cross platform.

This package and 3 other make up [ManderaGeneral](https://github.com/Mandera).

## Information
| Package                                                      | Version                                        | Latest Release       | Python                                                                                                                   | Platform        | Todos                                                    |   Hierarchy |
|:-------------------------------------------------------------|:-----------------------------------------------|:---------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------|:---------------------------------------------------------|------------:|
| [generalfile](https://github.com/ManderaGeneral/generalfile) | [2.3.9](https://pypi.org/project/generalfile/) | 2021-02-04 17:13 CET | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) | Windows, Ubuntu | [10](https://github.com/ManderaGeneral/generalfile#Todo) |           1 |

## Contents
<pre>
<a href='#generalfile'>generalfile</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Contents'>Contents</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Installation
| Command                                | <a href='https://pypi.org/project/generallibrary'>generallibrary</a>   | <a href='https://pypi.org/project/send2trash'>send2trash</a>   | <a href='https://pypi.org/project/appdirs'>appdirs</a>   | <a href='https://pypi.org/project/pandas'>pandas</a>   |
|:---------------------------------------|:-----------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|
| `pip install generalfile`              | Yes                                                                    | Yes                                                            | Yes                                                      | No                                                     |
| `pip install generalfile[spreadsheet]` | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    |
| `pip install generalfile[full]`        | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/__init__.py#L1'>Module: generalfile</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/errors.py#L4'>Class: CaseSensitivityError</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/errors.py#L5'>Class: InvalidCharacterError</a>
└─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path.py#L17'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path.py#L17'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L59'>Method: absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_lock.py#L124'>Method: as_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: copy</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L218'>Method: copy_to_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L328'>Method: create_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L35'>Method: delete</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L35'>Method: delete_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L265'>Method: encode</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L102'>Method: endswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L246'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L32'>Method: get_alternative_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L345'>Method: get_cache_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: get_differing_files</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L353'>Method: get_lock_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L42'>Method: get_lock_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path.py#L41'>Method: get_parent</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L48'>Method: get_path_from_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: get_paths_in_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: get_paths_recursive</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L22'>Method: get_replaced_alternative_characters</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L361'>Method: get_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L82'>Method: is_absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L234'>Method: is_file</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L240'>Method: is_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L459'>Method: is_identical</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L88'>Method: is_relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_lock.py#L115'>Method: lock</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L252'>Method: match</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L226'>Method: move</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L157'>Method: name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L338'>Method: open_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L94'>Method: open_operation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L150'>Method: parts</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L120'>Method: read</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L70'>Method: relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L126'>Method: remove_end</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L110'>Method: remove_start</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: rename</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L142'>Method: same_destination</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: seconds_since_creation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: seconds_since_modified</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L381'>Method: set_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L11'>Method: size</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L94'>Method: startswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L171'>Method: stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L199'>Method: suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L238'>Method: suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L35'>Method: trash</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L35'>Method: trash_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L185'>Method: true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path.py#L117'>Method: view</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L163'>Method: with_name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L177'>Method: with_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L205'>Method: with_suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L244'>Method: with_suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_strings.py#L191'>Method: with_true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L266'>Method: without_file</a>
   └─ <a href='https://github.com/ManderaGeneral/generalfile/blob/4ce1626/generalfile/path_operations.py#L108'>Method: write</a>
</pre>

## Todo
| Module                                                                                                                                               | Message                                                                                                                                                                                                    |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_lock.py#L1'>path\_lock.py</a>                                     | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_lock.py#L16'>other\_paths</a>                                                                                           |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/decorators.py#L1'>decorators.py</a>                                   | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/decorators.py#L2'>Put this in library</a>                                                                                   |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L22'>Add a proper place for all variables, add working\_dir, sys.executable and sys.prefix to it.</a>                |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L23'>Raise suppressable warning if space in Path.</a>                                                               |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L1'>path\_operations.py</a>                         | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L138'>Can we not just change signature to rename(self, new\_path, overwrite=False) ?</a>                  |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L1'>path\_operations.py</a>                         | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L290'>Filter for Path.get\_paths\_* like we have in ObjInfo.</a>                                           |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L1'>path\_operations.py</a>                         | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L391'>Add this error parameter for more methods</a>                                                      |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L1'>path\_operations.py</a>                         | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path\_operations.py#L484'>Tests for get\_differing\_files.</a>                                                                 |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional\_dependencies/path\_spreadsheet.py#L1'>path\_spreadsheet.py</a> | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional\_dependencies/path\_spreadsheet.py#L35'>Make it order columns if there are any so that they line up with append.</a> |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional\_dependencies/path\_spreadsheet.py#L1'>path\_spreadsheet.py</a> | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional\_dependencies/path\_spreadsheet.py#L115'>Should probably support DataFrame and Series as well.</a>                   |

<sup>
Generated 2021-02-05 18:47 CET for commit <a href='https://github.com/ManderaGeneral/generalfile/commit/4ce1626'>4ce1626</a>.
</sup>
