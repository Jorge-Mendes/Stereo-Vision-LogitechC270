# Stereo-Vision-LogitechC270: 3D reconstruction from stereo images captured through two Logitech C270 HD cameras #

Stereo-Vision-LogitechC270 provides scripts that allow to obtain a 3D reconstruction from stereo images captured through two Logitech C270 HD cameras.

## System description ##

(soon)

## Dependencies ##
- [OpenCV](https://opencv.org/) (>=2.4.8)
- Python packages:
	- [numpy](https://www.numpy.org/) (>=1.14.0)
	- [matplotlib](https://matplotlib.org/) (>=2.1.1)

## Scripts ##
- [capture_images.py](https://github.com/Jorge-Mendes/Stereo-Vision-LogitechC270/blob/master/capture_images.py) (Allows to capture stereo images through the Logitech C270 HD cameras)
- [images_to_pointcloud.py](https://github.com/Jorge-Mendes/Stereo-Vision-LogitechC270/blob/master/images_to_pointcloud.py) (Allows to obtain the 3D reconstruction from the captured images)

## Installation ##

```
git clone https://github.com/Jorge-Mendes/Stereo-Vision-LogitechC270.git
```

## Use ##
### Capture images ###

```
python capture_images.py 1 2 --out_folder output/ --show_frames 1
```
In this case, the right camera is the **/dev/video1** (```1```), the left camera is the **/dev/video2** (```2```), the captured images will be saved in the **output/** directory (```--out_folder output/```) and they will be shown in the end (```--show_frames 1```).
### Obtain de 3D reconstruction ###

```
python images_to_pointcloud.py input/image_right_01.jpg input/image_left_01.jpg output/
```
In this case, the input right image is the **image_right_01.jpg** (```input/image_right_01.jpg```), the input left image is the **image_left_01.jpg** (```input/image_left_01.jpg```) and the output pointcloud and disparity image will be saved in the **output/** directory (```output/```).


---

If you find a bug or would like to request a feature, please [report it with the issue tracker](https://github.com/Jorge-Mendes/Stereo-Vision-LogitechC270/issues). If you'd like to contribute to StereoVision, feel free to [fork it on GitHub](https://github.com/Jorge-Mendes/Stereo-Vision-LogitechC270).

Author: [Jorge Mendes](https://github.com/Jorge-Mendes)

