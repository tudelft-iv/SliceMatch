# VIGOR Dataset: Corrected Labels

The [VIGOR](https://github.com/Jeff-Zilence/VIGOR) dataset has been published in CVPR2021 (see [paper](https://openaccess.thecvf.com/content/CVPR2021/papers/Zhu_VIGOR_Cross-View_Image_Geo-Localization_Beyond_One-to-One_Retrieval_CVPR_2021_paper.pdf)). The original labels were based on an incorrect ground resolution for the aerial images. We corrected the labels of this dataset and the details can be found in Section A of the supplementary material of our paper (see [supp](https://openaccess.thecvf.com/content/CVPR2023/supplemental/Lentsch_SliceMatch_Geometry-Guided_Aggregation_CVPR_2023_supplemental.pdf)).


## Data Structure

The folder [splits__corrected](./splits__corrected) contains our corrected labels. After downloading the VIGOR dataset, the original ``splits`` folder should be replaced by our ``splits__corrected`` folder. The data should be organized as:


```
VIGOR
|_ Chicago
| |_ panorama
|    |_ [prefix,latitude,longitude,].jpg
|    |_ ...
| |_ satellite
|    |_ [satelitte_latitude_longitude].jpg
|    |_ ...
|_ NewYork
| |_ panorama
|    |_ [prefix,latitude,longitude,].jpg
|    |_ ...
| |_ satellite
|    |_ [satelitte_latitude_longitude].jpg
|    |_ ...
|_ SanFrancisco
| |_ panorama
|    |_ [prefix,latitude,longitude,].jpg
|    |_ ...
| |_ satellite
|    |_ [satelitte_latitude_longitude].jpg
|    |_ ...
|_ Seattle
| |_ panorama
|    |_ [prefix,latitude,longitude,].jpg
|    |_ ...
| |_ satellite
|    |_ [satelitte_latitude_longitude].jpg
|    |_ ...
|_ splits__corrected
```


## Visualize Corrected Labels

The Jupyter notebook [Visualize_Corrected_Labels](Visualize_Corrected_Labels.ipynb) can be used to visualize the corrected labels. The notebook should be placed in the folder of the VIGOR dataset, i.e., the directory should be ``DIR_TO_VIGOR_DATASET/VIGOR/Visualize_Corrected_Labels.ipynb``.
