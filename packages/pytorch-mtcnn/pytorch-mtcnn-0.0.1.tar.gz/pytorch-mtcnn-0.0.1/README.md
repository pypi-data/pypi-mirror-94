This project is belongs to the original creator (https://github.com/khrlimam/mtcnn-pytorch). I just fixed some problems that may have been caused by newer version of PyTorch. Also this project is available to install from pypi: `pip install torch-mtcnn`


## How to install
Install the package with pip: `pip install torch-mtcnn`


## How to use
```python
from torch_mtcnn import detect_faces
from PIL import Image

image = Image.open('image.jpg')
bounding_boxes, landmarks = detect_faces(image)
```

You can use the `bounding_boxes` to crop the image (assuming there is only 1 face):
```python
bounding_boxes = list(map(int, bounding_boxes[0]))
img_1 = cv2.imread(path)
img_1[ bounding_boxes[1] : bounding_boxes[3], bounding_boxes[0] : bounding_boxes[2]]
```

## Autocrop
I have included a utility function `get_faces`. This function gets the image path and returns all of the faces in the image:
```python
from torch_mtcnn import get_faces

faces = get_faces('img.jpg')
```

## Requirements
Please see the `requirements.txt`

## Credit
The original project belongs to https://github.com/khrlimam/mtcnn-pytorch.