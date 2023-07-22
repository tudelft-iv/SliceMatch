import torch
import torch.nn as nn


class ImageMLP(nn.Module):
    """
    Image multilayer perceptron := stacking 1x1 convolution layers including activation functions
    """
    
    def __init__(self, input_dim, hidden_dims, output_dim):
        """
        Args:
            input_dim (int) : number of channels in the input image (C_in)
            hidden_dims (list) : number of channels in the intermediate representations
            output_dim (int) : number of channels in the output attention map (C_out)
        """
        
        super().__init__()
        
        # sizes
        sizes = [input_dim, *hidden_dims, output_dim]
        
        # layers        
        layers = []
        for idx in range(len(sizes)-1):
            layers.append(nn.Conv2d(in_channels=sizes[idx], out_channels=sizes[idx+1], kernel_size=1, stride=1, bias=True))
            if idx!=len(sizes)-2:
                layers.append(nn.ReLU())
            else:
                layers.append(nn.Sigmoid())
        self.layers = nn.Sequential(*layers)
        
    def forward(self, img):
        """
        Args:
            img (tensor) : image with shape (B,C_in,H,W)
            
        Returns:
            att_map (tensor) : attention map with shape (B,C_out,H,W)
            
        B : batch size
        C_in : number of channels in the input image
        C_out : number of channels in the output attention map
        H : spatial height of image
        W : spatial width of image
        """

        att_map = self.layers(img)
        
        return att_map
