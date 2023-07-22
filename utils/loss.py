import torch


class InfoNCELossGrid():
    """
    InfoNCE Loss for 3DoF Grid
    
    It can be seen as a generalized version of triplet loss used in image retrieval in the case of multiple negative samples are presented at the same time.
    """
    
    def __init__(self, img_sizes, alfa):
        """
        Args:
            img_sizes (dict): dictionary with images sizes
                H (int) : height of (resized) ground image
                W (int) : width of (resized) ground image
                A (int) : height and width of (resized) aerial image
                H_original (int) : height of original ground image
                W_original (int) : width of original ground image
                A_original (int): height and width of original aerial image
            alfa (int) : scaling factor for number of negatives
        """
        
        super().__init__()
        
        # settings
        self._img_sizes = img_sizes
        self._alfa      = 4
        self._tau       = 0.1
        
        
    def get_loss(self, grd_descriptors, aer_descriptors, aer_descriptors_gt):
        """        
        Args:
            grd_descriptors (tensor) : ground descriptors with shape (B,N*C')
            aer_descriptors (tensor) : aerial descriptors with shape (B,T,N,N*C')
            aer_descriptors_gt (tensor) : aerial descriptors with shape (B,N*C')
            
        Returns:
            loss (float) : average loss
            
        B : batch size
        T : num_locs (number of locations in the grid)
        R : number of rotations for the slicing
        C' : feature channel size
        N : number of horizontal slices
        """
        
        B = grd_descriptors.shape[0]
        
        # determine similarities
        sims_pos = torch.einsum('ab,ab->a', grd_descriptors, aer_descriptors_gt)
        sims_neg = torch.einsum('abcd,abcd->abc', grd_sfs_norm.view(B,1,1,-1), aer_descriptors)
        
        # determine loss for each image pair
        loss_sum = 0
        for b in range(B):
            # ground view as anchor
            # 1 positive:    GT aerial pose
            # T*N negatives: aerial grid locations with each N orientations
            
            # positive similarity
            pos = sims_pos[b]                                                           # value
            
            # negative similarities
            neg = sims_neg[b].flatten()                                                 # (T*N)
            
            # determine exp(similarity/tau)
            expon_pos = torch.exp(pos/self._tau)                                        # value
            expon_neg = torch.exp(neg/self._tau).sum()                                  # value
            
            # add loss
            if self._alfa is None:
                expon_pos = torch.exp(pos/self._tau)                                    # value
                expon_neg = torch.exp(neg/self._tau).sum()                              # value
                loss_sum += -torch.log(expon_pos/(expon_neg+expon_pos))                 # value
            else:
                expon_pos = torch.exp(pos/self._tau)                                    # value
                expon_neg = torch.exp(neg/self._tau).mean()                             # value
                loss_sum += -torch.log(expon_pos/(self._alfa*expon_neg+expon_pos))      # value
                
        # loss
        loss = loss_sum/B                                                               # value
        
        return loss                                                                     # value
