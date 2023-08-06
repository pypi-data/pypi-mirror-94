# About
This repository provides various functions useful for python and machine learning. The goal is to keep your code cleaner, keeping business logic out of your primary functions. For example, formatting paths is common, can often turn into many lines of code, and is done frequently throughout a script. Often people do the path formatting multiple times, mid-function, convoluting the code and distracting from the functions purpose. Further, paths aren't always formatted consistently and error handling is poor. Thus, I created the following function to format all paths consistently:

```python
def format_path(path):
  """ Format paths into a consistent format. Expand user paths.
      Relative paths are converted to full paths. Directories 
      should all end in forward slashes. Note this will format even if
      the paths don't actually exist yet.
  Args:
    path: Full or relative path of directory or file in question.
  Returns:
    Formatted full paths, relative to 
  """
  # If path is None (e.g. when no --arg from parser), default to same dir as the script
  if path is None:
    path = ""

  # Expand paths
  path = os.path.expanduser(path)

  # Handle relative paths
  path = os.path.abspath(path)

  # Check if path *could be* a valid file or dir 
  # Note, files like MAKE or LICENCE that don't actually exist
  # will be considered as dirs.
  is_dir = os.path.isdir(path) or is_dir_like(path) and not os.path.isfile(path)

  # Make sure dirs end with a slash
  if is_dir and not path.endswith('/'):
    path += "/"

  return path  
```

This function can take relative or full paths to files or directories. It ensures that empty paths and paths that are type None are handled, paths are expanded, and that directories end with a trailing slash. Using this function removes clutter from your other functions and ensures that paths are formatted consistently, resulting in cleaner, more robust code.

A common machine learning example is writing detections to a textfile. This often involves multiple loops of a nested list. With pymltools, this can conveniently be done in one, self-evident line `write_label(path, labels)` rather than having to include a business-logic heavy method:

```python
def write_label(path, labels, mode='w+', precision=6):
  """ Write the list to the file at specified full path.
      Create the file if it doesn't exist.
  Args:
    path: Full path to label file.
    bbox_list: List of yolo bboxes to be written in format:
               [class, center_x, center_y, width, height]
    mode: The mode of writing.
    precision: How many decimal places to keep for bbox.
  Return:
    True on completion.
  """
  file = open(path, mode)

  # Write all lines to file
  for label in labels:
    # Line to be written to file
    line = ""

    for item in label:
      line += str(round(item, precision)) + " "

    line = line.strip()
    file.write(f"{line}\n")

  file.close()
  return True
```

# How to Install
Install the package  
`pip install pymlutils`

For dev, make sure you install the dev requirements  
`pip install -r requirements_dev.txt`

# How to Use
In your script, import `pymlutils`. Some example usage:

```python
import pymlutils.pymlutils as pyml

formatted_path = pyml.format_path(path)
```

```python
from pymlutils.pymlutils import *

formatted_path = format_path(path)
```

```python
import pymlutils.yolo as yolo

label_list = yolo.read_label(path)
```

```python
from pymlutils.yolo import *

label_list = read_label(path)
```

# Documentation
The following functions can be found at [pymlutils/pymlutils.py](https://gitlab.com/baka-san/pymlutils/-/blob/master/pymlutils/pymlutils.py). The functions related to YOLO can be found at [pymlutils/yolo.py](https://gitlab.com/baka-san/pymlutils/-/blob/master/pymlutils/yolo.py).

### Path related functions
##### `check_path`
> *Ensure a file or directory exists. Kill the script if file or directory doesn't exist.*  
>
> **Arguments:**  
> `path`: Full path of file or directory in question.  
> 
> **Returns**  
> True if the path exists. Kills program if false.

##### `format_path`
> *Format paths into a consistent format. Expand user paths. Relative paths are converted to full paths. Directories should all end in forward slashes. Note this will format even if the paths don't actually exist yet. Typically this function should be called before running other functions to ensure the path is formatted correctly.*  
>
> **Arguments:**  
> `path`: Full or relative path of file or directory in question. 
> 
> **Returns**  
> A formatted full path (including forward slashes for directories).

### Directory related functions
##### `check_dir`
> *Ensure a directory exists. Kill the script if directory doesn't exist.*  
>
> **Arguments:**  
> `path`: Full path of the directory in question.  
> 
> **Returns**  
> True if the directory exists. Kills program if false.

##### `check_or_mkdir`
> *Create directories recursively in specified path if they don't exist.*  
>
> **Arguments:**  
> `path`: Full path of the directory in question.  
> 
> **Returns**  
> True if the directory exists and False if it doesn't (function had to create it).

##### `is_dir_like`
> *Check if the full path is "directory like," that is, it \*could\* be a valid directory based on format alone. The directory doesn't actually have to exist.*  
>
> **Arguments:**  
> `path`: Full path of a could-be directory.  
> 
> **Returns**  
> True for paths that are directory like and False for those that aren't.

### File related functions
##### `check_file`
> *Ensure the file exists. Kill the script if file doesn't exist.*  
>
> **Arguments:**  
> `path`: Full path of the file in question.  
> 
> **Returns**  
> True if the file exists. Kills program if false.

##### `convert_file_ext`
> *Convert file extension of the file provided path.*  
>
> **Arguments:**  
> `path`: Full path of the file in question.  
> `ext`: Extension to be converted to.  
> 
> **Returns**  
> Full path of the file with the new extension.

##### `convert_image_ext`
> *Convert the image format (png or jpg) of images in the provided image_location. The image_location can be a directory or a file containing full paths to the images.*  
>
> **Arguments:**  
>  `image_location`: Full path to directory or a file with a list of full paths to images.  
>  `should_remove`: Whether to delete the old images (default: False).  
>  `should_print`: Whether to print feedback (default: True).  
> 
> **Returns**  
> A list containing full paths of converted images.

##### `get_file_list_from_dir_or_file`
> *Get a list of full paths to all files in provided path of specified extension (e.g. all .txt files).*  
>
> **Arguments:**  
> `path`: Full path to directory or a file with a list of full paths to other files.  
> `file_format`: The format of the files (typically jpg, png, or txt).  
> `full_path`: Whether to return the full or relative paths of the files (default: True).  
> `should_print`: Whether to print feedback (default: True).  
> `is_empty_ok`: Whether to kill the program if no files are found (default: False).  
> 
> **Returns**  
> A  list of files of specified file_format (full paths by default).

##### `get_num_lines_from_file`
> *Get the number of lines in a file.*  
>
> **Arguments:**  
> `path`: Full path of the file in question.  
> 
> **Returns**  
> Integer number of lines in the file.

##### `is_file_like`
> *Check if path is "file like," that is, it \*could\* be a valid file path based on format alone. The file doesn't actually have to exist. Note: files with no extension and that don't actually exist will not be considered to be valid file names as there is no way to distiguist them from a directory (e.g. a LICENCE or MAKE file).*  
>
> **Arguments:**  
> `path`: Full path of could-be file.  
> 
> **Returns**  
> True for strings that are file-like and False for those that aren't.

##### `rm_file`
> *Delete the file if it exists.*  
>
> **Arguments:**  
> `path`: Full path of the file in question.  
> `should_print`: Whether to print feedback (default: True).  
> 
> **Returns**  
> True if deleted, False of not.

##### `rm_files`
> *Delete the files if they exist.*  
>
> **Arguments:**  
> `list_:` A list of full paths to files in question.  
> `should_print`: Whether to print feedback (default: True).  
> 
> **Returns**  
> A list of files which failed to delete. If all files were deleted, the list will be empty.

##### `to_png`
> *Convert jpg images to png images, optionally deleting the old images.*  
>
> **Arguments:**  
> `list_:` A list of full paths to images in question.  
> `should_remove`: Whether to delete the old images (default: False).  
> `should_print`: Whether to print feedback (default: True).  
> 
> **Returns**  
> A list of paths of converted images.

##### `to_jpg`
> *Convert png images to jpg images, optionally deleting the old images.*  
>
> **Arguments:**  
> `list_:` A list of full paths to images in question.  
> `should_remove`: Whether to delete the old images (default: False).  
> `should_print`: Whether to print feedback (default: True).  
> 
> **Returns**  
> A list of paths of converted images.

##### `write_list_to_file`
> *Write the list to the file at the specified full path. Create the file if it doesn't exist.*  
>
> **Arguments:**  
> `path`: Full path of the file in question.  
> `list`: The list to be written item by item.  
> `mode`: The mode of writing (default: w+).  
> 
> **Returns**  
> True on completion.

### JSON file related functions
##### `remove_comments`
> *Removes C-style comments (i.e. // or /*...*/) from a json-like string and returns the result. See `get_args_from_json_config`.*  
>
> **Arguments:**  
> `json_like`: A json-like string to be parsed. 
> 
> **Returns**  
> A json-like string without comments.

##### `remove_trailing_commas`
> *Removes (accidental) trailing commas from a json-like string. See `get_args_from_json_config`.*  
>
> **Arguments:**  
> `json_like`: A json-like string to be parsed. 
> 
> **Returns**  
> A json-like string without comments.

### JSON config files
##### `check_json_config`
> *Get the full, formatted path of the json config file.*  
>
> **Arguments:**  
> `path`: Full or relative path to the json config file. Defaults to the [script directory]/config.json.
> 
> **Returns**  
> The formatted, full path to the json config file. Program kills if the config file doesn't exist.

##### `get_args_from_json_config`
> *Read the json config file, converting all arguments into a python dict. Any C-style comments (i.e. // or /*...*/) or accidental trailing commas will automatically be removed.*  
>
> **Arguments:**  
> `path`: Full path to the json config file.
> 
> **Returns**  
> A python dict containing all config arguments.

### General Python functions
##### `camelize`
> *Convert a string, dict, or list of dicts to camelcase.*  
>
> **Arguments:**  
> `str_or_iter`: A string or iterable.
> 
> **Returns**  
> A camelized string, dictionary, or list of dictionaries.

##### `pascalize`
> *Convert a string, dict, or list of dicts to pascalcase.*  
>
> **Arguments:**  
> `str_or_iter`: A string or iterable.
> 
> **Returns**  
> A pascalized string, dictionary, or list of dictionaries.

### YOLO related functions
##### `get_classes_from_label`
> *Get all classes from a yolo label file.*  
>
> **Arguments:**  
> `path`: Full path to the image or label.  
> 
> **Returns**  
> A list containing all ids (as ints) of classes.

##### `get_bboxes_from_label`
> *Get all bboxes from a yolo label file. Note, the class name (id) is not included. See read_label if class names are needed.*  
>
> **Arguments:**  
> `path`: Full path to the image or label.  
> 
> **Returns**  
> A nested list of bboxes in the format: [[center_x, center_y, width, height], ...], all as floats.

##### `read_label`
> *Get all detections from a yolo label file. Note, the class name (id) is included. See get_bboxes_from_label if class names are not needed.*  
>
> **Arguments:**  
> `path`: Full path to the image or label.  
> 
> **Returns**  
> A nested list of detections in the format: [[class/id, center_x, center_y, width, height], ...], all as floats.

##### `write_label`
> *Write a list to the file at specified full path. Create the file if it doesn't exist.*  
>
> **Arguments:**  
> `path`: Full path to label file.  
> `bbox_list`: List of yolo bboxes to be written in the format: [class/id, center_x, center_y, width, height]  
> `mode`: The mode of writing (default: w+).  
> `precision`: How many decimal places to keep for bbox (default: 6).  
> 
> **Returns**  
> True on completion.

##### `check_bbox`
> *Check if bounding boxes extend beyond the image bounds.*  
>
> **Arguments:**  
> `bbox`: A list containing a bbox in Yolo format [center_x, center_y, width, height]. Recall that in yolo coords, the origin is the upper left, not the upper right, so the y-axis is inverted.  
> 
> **Returns**  
> A value of True if valid and false if invalid.

##### `x_y_to_yolo`
> *Convert [x_min, y_min, x_max, y_max] to yolo's format [x_center, y_center, width, height]. Assumesthat the x-y coords are NOT normalized. Do not pass labels.*  
>
> **Arguments:**  
> `bbox`: A list containing a bbox in Yolo format [center_x, center_y, width, height]. Recall that in yolo coords, the origin is the upper left, not the upper right, so the y-axis is inverted.  
> `image_path`: Full path to the image (used to get w & h in normalization).
> 
> **Returns**  
> A list containing the bbox in yolo format.

