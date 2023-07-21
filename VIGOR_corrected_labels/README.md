# VIGOR Dataset: Corrected Labels
<p align="justify">
The <a href="https://github.com/Jeff-Zilence/VIGOR">VIGOR</a> dataset has been published in CVPR2021 (see <a href="https://openaccess.thecvf.com/content/CVPR2021/papers/Zhu_VIGOR_Cross-View_Image_Geo-Localization_Beyond_One-to-One_Retrieval_CVPR_2021_paper.pdf">paper</a>). The original labels were based on an incorrect ground resolution for the aerial images. We corrected the labels of this dataset and the details can be found in Section A of the supplementary material of our paper (see <a href="https://openaccess.thecvf.com/content/CVPR2023/supplemental/Lentsch_SliceMatch_Geometry-Guided_Aggregation_CVPR_2023_supplemental.pdf">supp</a>).
</p>



## Data Structure
<p align="justify">
The folder <a href="./splits__corrected">splits__corrected</a> ontains our corrected labels. After downloading the VIGOR dataset, the original <code>splits</code> folder should be replaced by our <code>splits__corrected</code> folder. The data should be organized as:
</p>



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
<p align="justify">
The Jupyter notebook <a href="Visualize_Corrected_Labels.ipynb">Visualize_Corrected_Labels</a> can be used to visualize the corrected labels. The notebook assumes that the VIGOR dataset is placed in the datasets folder, i.e., the directory of the dataset should be <code>DIR_TO_SLICEMATCH/SliceMatch/datasets/VIGOR</code>.
</p>
