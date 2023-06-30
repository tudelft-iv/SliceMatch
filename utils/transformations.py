import torch
import torchvision


class ToTensor():
    """ Convert all images in the list to tensors with type float. """
    
    def __call__(self, imgs, target):
        imgs = [torchvision.transforms.functional.to_tensor(img.copy()).type(torch.float) for img in imgs]
        
        return imgs, target


class NormalizeTensor():
    """ Normalize tensors by using PyTorch ImageNet mean and std. """
    
    def __init__(self):
        self.mean = [0.485, 0.456, 0.406]
        self.std  = [0.229, 0.224, 0.225]
        
    def __call__(self, imgs, target):
        imgs = [torchvision.transforms.functional.normalize(img, self.mean, self.std) for img in imgs]
        
        return imgs, target


class Compose():
    """ Apply all transformations. """
    
    def __init__(self, transforms):
        self.transforms = transforms
        
    def __call__(self, imgs, target):
        for transform in self.transforms:
            imgs, target = transform(imgs, target)
            
        return imgs, target


def get_transform():
    """ Combine all transformations into a single transformation. """
    
    transforms = []
    
    # NumPy array to tensor (this scales element values from 0-255 to 0-1)
    transforms.append(ToTensor())
    
    # normalize tensor (using ImageNet mean and std)
    transforms.append(NormalizeTensor())
    
    return Compose(transforms)
