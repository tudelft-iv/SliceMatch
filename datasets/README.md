# Datasets Instructions



<p align="justify">
The VIGOR and KITTI folders are empty. Please download the ([VIGOR](https://github.com/Jeff-Zilence/VIGOR) and [KITTI](https://github.com/shiyujiao/HighlyAccurate) datasets, and put the VIGOR and KITTI datasets in the VIGOR and KITTI folders, respectively. After that, please run the Jupyter Notebook [VIGOR_Resize_Images](./VIGOR_resize/VIGOR_Resize_Images.ipynb) to resize the VIGOR images. Finally, replace the original VIGOR labels with our corrected labels. The corrected labels can be found [here](../VIGOR_corrected_labels).
</p>



<p align="justify">
The [VIGOR_masks](./VIGOR_masks) and [KITTI_masks](./KITTI_masks) folders are used for storing the slice masks of the GT pose of each image pair to accelerate the training of SliceMatch. The [VIGOR_oriens](./VIGOR_oriens) folder contains text files with the used training and testing orientations for all VIGOR image pairs. Lastly, the [VIGOR_resize](./VIGOR_resize) folder contains the Jupyter Notebook for resizing the VIGOR images.
</p>
