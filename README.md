# SliceMatch: Geometry-guided Aggregation for Cross-View Pose Estimation [CVPR'23]



[[`Paper`](https://openaccess.thecvf.com/content/CVPR2023/html/Lentsch_SliceMatch_Geometry-Guided_Aggregation_for_Cross-View_Pose_Estimation_CVPR_2023_paper.html)] [[`ArXiv`](https://arxiv.org/abs/2211.14651)] [[`Video`](https://www.youtube.com/watch?v=gql1dkQQNrA)] [[`BibTeX`](#citation-information)]



![](README_data/poster.png)



### Abstract
This work addresses cross-view camera pose estimation, i.e., determining the 3-Degrees-of-Freedom camera pose of a given ground-level image w.r.t. an aerial image of the local area. We propose SliceMatch, which consists of ground and aerial feature extractors, feature aggregators, and a pose predictor. The feature extractors extract dense features from the ground and aerial images. Given a set of candidate camera poses, the feature aggregators construct a single ground descriptor and a set of pose-dependent aerial descriptors. Notably, our novel aerial feature aggregator has a cross-view attention module for ground-view guided aerial feature selection and utilizes the geometric projection of the ground camera’s viewing frustum on the aerial image to pool features. The efficient construction of aerial descriptors is achieved using precomputed masks. SliceMatch is trained using contrastive learning and pose estimation is formulated as a similarity comparison between the ground descriptor and the aerial descriptors. Compared to the state-of-the-art, SliceMatch achieves a 19% lower median localization error on the VIGOR benchmark using the same VGG16 backbone at 150 frames per second, and a 50% lower error when using a ResNet50 backbone.



### Installation Instructions
Soon to be updated!



### Training SliceMatch
Soon to be updated!



### Testing SliceMatch
Soon to be updated!



### Compare to Our Results
Soon to be updated!



### VIGOR Dataset: Corrected Labels
The corrected labels of the VIGOR dataset can be found [here](./VIGOR_corrected_labels).



### Citation Information
If SliceMatch or the corrected labels of the VIGOR dataset are useful to your research, please kindly recognize our contributions by citing our CVPR paper:

```
@InProceedings{Lentsch_2023_CVPR,
    author    = {Lentsch, Ted and Xia, Zimin and Caesar, Holger and Kooij, Julian F. P.},
    title     = {SliceMatch: Geometry-Guided Aggregation for Cross-View Pose Estimation},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2023},
    pages     = {17225-17234}
}
```
