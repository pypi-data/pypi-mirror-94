# pyra-pytorch


### This is a package supporting Pytorch datasets. This implementation is based on the augmentation method discussed in the paper "Pyramid-Focus-Augmentation: Medical Image Segmentation with Step-Wise Focus" ([PDF](https://arxiv.org/pdf/2012.07430v1.pdf)) and the original github repository: [PYRA](https://vlbthambawita.github.io/PYRA/).





```latex
@article{thambawita2020pyramid,
  title={Pyramid-Focus-Augmentation: Medical Image Segmentation with Step-Wise Focus},
  author={Thambawita, Vajira and Hicks, Steven and Halvorsen, P{\aa}l and Riegler, Michael A},
  journal={arXiv preprint arXiv:2012.07430},
  year={2020}
}
```

# How to use:

### Install the package,
```bash
pip install pyra-pytorch
```

### Creating a PYRA augmented dataset:

```python
from pyra_pytorch import PYRADataset

dataset = PYRADataset("./image_path", # image folder
                      "./masks_path", # mask folder - files´s names of this folder should have image names as prefix to find correct image and mask pairs.
                      img_size = 256,  # height and width of image to resize
                      grid_sizes=[2,4,8,16,32,64,128,256] , # Gird sizes to use as grid augmentation. Note that, the image size after resizing ()
                      transforms = None
                      )
'''
./image_path" --> image folder

./masks_path" --> mask folder - files´s names of this folder should have image names as prefix to find correct image and mask pairs.

img_size = 256 --> height and width of image to resize

grid_sizes=[2,4,8,16,32,64,128,256]  --> Gird sizes to use as grid augmentation. Note that, the image size after resizing (in this case, it is 256) shoud be divisible by these grid sizes.
                      
transforms = None --> Other type of transformations using in Pytorch. 

'''
```


### Creating a PYRA augmented dataset using path list files:

```python
from pyra_pytorch import PYRADataset

dataset = PYRADatasetFromPaths("path_to_the_file_with_image_paths", # file containing all image paths
                      "path_to_file_with_mask_paths", # file containing all mask paths - files´s names of this folder should have image names as prefix to find correct image and mask pairs.
                      img_size = 256,  # height and width of image to resize
                      grid_sizes=[2,4,8,16,32,64,128,256] , # Gird sizes to use as grid augmentation. Note that, the image size after resizing ()
                      transforms = None
                      )
'''
path_to_the_file_with_image_paths" --> A file with all paths of images. File should have one path (absolute path) per line. 

path_to_file_with_mask_paths" --> A file with all paths of masks. The file should have one path (absolute path) per line. Please use the image names as prefix for mask's names to find correct mask for correct image.

img_size = 256 --> height and width of image to resize

grid_sizes=[2,4,8,16,32,64,128,256]  --> Gird sizes to use as grid augmentation. Note that, the image size after resizing (in this case, it is 256) shoud be divisible by these grid sizes.
                      
transforms = None --> Other type of transformations using in Pytorch. 

'''
```

# Sample ipython notebook

[notebook](https://github.com/vlbthambawita/pyra-pytorch/blob/main/tutorial/load_data_with_PYRA.ipynb)


# Contact us:

vajira@simula.no | michael@simula.no
