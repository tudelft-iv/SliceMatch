# Datasets Instructions



<p align="justify">
The VIGOR and KITTI folders are empty. Please download the <a href="https://github.com/Jeff-Zilence/VIGOR">VIGOR</a> and <a href="https://github.com/shiyujiao/HighlyAccurate">KITTI</a> datasets, and put the VIGOR and KITTI datasets in the VIGOR and KITTI folders, respectively. After that, please run the Jupyter Notebook <a href="./VIGOR_resize/VIGOR_Resize_Images.ipynb">VIGOR_Resize_Images</a> to resize the VIGOR images. Finally, replace the original VIGOR labels with our corrected labels. The corrected labels can be found <a href="../VIGOR_corrected_labels">here</a>.
</p>



<p align="justify">
The <a href="./VIGOR_masks">VIGOR_masks</a> and <a href="./KITTI_masks">KITTI_masks</a> folders are used for storing the slice masks of the GT pose of each image pair to accelerate the training of SliceMatch. The <a href="./VIGOR_oriens">VIGOR_oriens</a> folder contains text files with the used training and testing orientations for all VIGOR image pairs. Lastly, the <a href="./VIGOR_resize">VIGOR_resize</a> folder contains the Jupyter Notebook for resizing the VIGOR images.
</p>
