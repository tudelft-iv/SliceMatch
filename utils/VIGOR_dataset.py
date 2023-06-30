import cv2
import numpy as np
import os
import torch


class VIGORDataset(torch.utils.data.Dataset):
    """ The VIGOR dataset class for pose estimation (and localization only). """
    
    def __init__(self, directories, img_sizes, transforms=None, oriens={}, ids=[], do_pose_estimation=True):
        """
        Args:
            directories (dict) : dictionary with dataset directories
                root (str) : root directory
                datasets (str) : directory to datasets folder
                vigor (str) : directory to VIGOR dataset
                vigor_masks (str) : directory to slice masks 
                cities (list) : list with the names of the used cities
                grd_folder_name (str) : name of folder with ground images
                aer_folder_name (str) : name of folder with aerial images
                pair_folder_name (str) : name of folder with pair and splits information
                file_name (str) : name of (text) document with pair information
            img_sizes (dict): dictionary with images sizes
                H (int) : height of (resized) ground image
                W (int) : width of (resized) ground image
                A (int) : height and width of (resized) aerial image
                A_original (int): height and width of original aerial image
            transforms (obj) : instance of Compose class that contains the transformations
            oriens (dict) : dictionary with orientations (if empty use random orientations)
            ids (list) : list with all indices that should be picked from the file with pair information
            do_pose_estimation (bool) : do pose estimation, otherwise do localization only
        """
        
        self.directories        = directories
        self.img_sizes          = img_sizes
        self.scale_factor       = img_sizes['A']/img_sizes['A_original']
        self.transforms         = transforms
        self.oriens             = oriens
        self.ids                = ids
        self.do_pose_estimation = do_pose_estimation
        
        # get pairs
        self.pairs  = []                                                                # (ground, aerial) pairs
        self.annots = []                                                                # deltas (aerial locations)
        self.get_pairs(directories, ids)


    def get_pairs(self, directories, ids):
        """
        Get ground and aerial image pairs with their corresponding annotations.
        
        Args:
            directories (dict) : dictionary with dataset directories
                root (str) : directory to dataset
                cities (list) : list with the names of the used cities
                grd_folder_name (str) : name of folder with ground images
                aer_folder_name (str) : name of folder with aerial images
                pair_folder_name (str) : name of folder with pair and splits information
                file_name (str) : name of (text) document with pair information
            ids (list) : list with all indices that should be picked from the file with pair information
        """

        cnt = -1
        for city_name in directories['cities']:
            file_dir = os.path.join(directories['vigor'], directories['pair_folder_name'], city_name, directories['file_name'])
            with open(file_dir, 'r') as file:
                for line in file.readlines():
                    cnt += 1
                    if cnt in ids or len(ids)==0:
                        data = line.split(' ')
                        grd_img_subdir = os.path.join(city_name, directories['grd_folder_name'], data[0])
                        aer_img_subdir = os.path.join(city_name, directories['aer_folder_name'], data[3*0+1])
                        delta = (float(data[3*0+2]), float(data[3*0+3]))
                        if abs(delta[0])<=self.img_sizes['A_original']//2 and abs(delta[1])<=self.img_sizes['A_original']//2:
                            self.pairs.append((grd_img_subdir, aer_img_subdir))
                            self.annots.append((self.img_sizes['A']//2+self.scale_factor*delta[0], self.img_sizes['A']//2-self.scale_factor*delta[1]))


    def __getitem__(self, idx):
        """
        Args:
            idx (int) : index of sample

        Returns:
            imgs (list) : list with ground and aerial image (both tensors)
            target (dict) : dictionary with index of sample and annotation (GT pose) 
        """

        grd_img_dir = os.path.join(self.directories['vigor'], self.pairs[idx][0])
        aer_img_dir = os.path.join(self.directories['vigor'], self.pairs[idx][1])

        grd_img = cv2.imread(grd_img_dir)[:,:,::-1]
        aer_img = cv2.imread(aer_img_dir)[:,:,::-1]
        imgs    = [grd_img, aer_img]

        # rotate ground image (orientation is angle from North direction clockwise to center line of the ground image)
        if self.do_pose_estimation:
            file_name = self.pairs[idx][0]
            orien     = self.oriens[file_name] if len(self.oriens)>0 else 360*np.random.rand()
            pixels    = np.round(self.img_sizes['W']*orien/360).astype(int)
            imgs[0]   = np.concatenate((grd_img[:,pixels:,:], grd_img[:,:pixels,:]), axis=1)
        else:
            orien = 0

        # mask dir
        mask_dir = os.path.join(self.directories['vigor_masks'], f'{os.path.basename(self.pairs[idx][1])[:-4]}__Mask_Nx_Orien{str(int(orien+1e-6)).zfill(3)}.pt')

        # create targets
        target             = {}                                                         # target
        target['img_id']   = torch.tensor([idx])                                        # image id (equal to index)
        target['grd_id']   = self.pairs[idx][0]                                         # subdir of ground image
        target['aer_id']   = self.pairs[idx][1]                                         # subdir of aerial image
        target['loc']      = torch.tensor([*self.annots[idx]])                          # location (h,w)
        target['orien']    = torch.tensor([orien])                                      # orientation
        target['mask_dir'] = mask_dir                                                   # mask directory

        # apply transformations
        if self.transforms is not None:
            imgs, target = self.transforms(imgs, target)

        return imgs, target


    def __len__(self):       
        return len(self.pairs)
