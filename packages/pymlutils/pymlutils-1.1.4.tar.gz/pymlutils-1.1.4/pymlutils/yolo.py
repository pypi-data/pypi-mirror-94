import os
from .pymlutils import *

### YOLO ###
def get_classes_from_label(path):
  """ Get all classes from a yolo label file.
  Args:
    path: Full path to the image or label.
  Returns:
    A list containing all ids (as ints) of classes.
  """
  # Change file extension to .txt
  path = convert_file_ext(path, '.txt')

  # Read classes to list
  classes = []

  with open(path) as file:
    for line in file:
      class_ = line.split()[0]
      classes.append(class_)
  return classes

def get_bboxes_from_label(path):
  """ Get all bboxes from a yolo label file. Note, 
  the class name (id) is not included. See 
  read_label if class names are needed.
  Args:
    path: Full path to the image or label.
  Returns:
    A nested list of bboxes in the format: 
    [[center_x, center_y, width, height], ...], 
    all as floats.
  """
  # Change file extension to .txt
  path = convert_file_ext(path, '.txt')

  # Read bboxes to list
  bboxes = []

  with open(path) as file:
    for line in file:
      bbox = line.strip().split()[1:]

      # Convert strings to floats
      for i, coord in enumerate(bbox):
        bbox[i] = float(coord)

      bboxes.append(bbox)
  return bboxes

def read_label(path):
  """ Get all detections from a yolo label file. Note, 
      the class name is included. See 
      get_bboxes_from_label if class nanmes are not needed.
  Args:
    path: Full path to the image or label.
  Returns:
    A nested list of detections in the format: 
    [class, center_x, center_y, width, height].
  """
  # Change file extension to .txt
  path = convert_file_ext(path, '.txt')

  # Read labels to list
  detections = []

  with open(path) as file:
    for line in file:
      # Add the class as an int
      list_ = [int(line.split()[0])]

      # Convert bbox to floats
      for coord in line.strip().split()[1:]:
        list_.append(float(coord))

      detections.append(list_)
  return detections  

def write_label(path, labels, mode='w+', precision=6):
  """ Write a list to the file at specified full path.
      Create the file if it doesn't exist.
  Args:
    path: Full path to label file.
    bbox_list: List of yolo bboxes to be written in the format: 
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

def check_bbox(bbox):
  """ Check if bounding boxes extend beyond the image bounds.
  Args:
    bbox: A list containing a bbox in Yolo format 
         [center_x, center_y, width, height]. Recall that 
         in Yolo coords, the origin is the upper left,
         not the upper right, so the y-axis is inverted.
  Return:
    A boolean value of True if valid and false if invalid.
  """
  x_min = bbox[0] - bbox[2]/2
  x_max = bbox[0] + bbox[2]/2
  y_max = bbox[1] + bbox[3]/2
  y_min = bbox[1] - bbox[3]/2

  if((x_min < 0.0) or (x_max > 1.0) or (y_min < 0.0) or (y_max > 1.0)):
    print(f"The following bbox is out of bounds:")
    print(f"bbox = {bbox}")
    return False
  else:
    return True

def x_y_to_yolo(bbox, image_path):
  """ Convert [x_min, y_min, x_max, y_max] to yolo's 
      format [x_center, y_center, width, height]. Assumes
      that the x-y coords are NOT normalized. Do not pass labels.
  Args:
    bbox: A list containing a bbox formatted as
         [center_x, center_y, width, height]. Recall that 
         in Yolo coords, the origin is the upper left,
         not the upper right, so the y-axis is inverted.
    image_path: Path to the image (used to get w & h 
      in normalization).
  Return:
    A list containing the bbox in yolo format.
  """

  # Get image dimensions
  image = Image.open(image_path)
  width, height = image.size
  image.close()

  # Convenience variables
  x_min, y_min, x_max, y_max = bbox

  # Convert to Yolo format
  x = (x_min + x_max)/2.0
  y = (y_min + y_max)/2.0
  w = x_max - x_min
  # The origin is the upper left, not the upper right, 
  # so the y-axis is inverted.
  h = abs(y_min - y_max)

  # Normalize
  x = x/width
  w = w/width
  y = y/height
  h = h/height

  return [x,y,w,h]
