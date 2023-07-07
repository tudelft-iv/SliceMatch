# Conda Environment Install Instructions



```
conda create --name SliceMatch_env python=3.8
conda activate SliceMatch_env
conda install pytorch=2.0 torchvision=0.15 torchaudio=2.0 pytorch-cuda=11.8 -c pytorch -c nvidia
conda install -c conda-forge shapely=2.0
conda install -c anaconda jupyter=1.0
conda install -c conda-forge matplotlib=3.7
pip install opencv-python==4.7.0.72
```
