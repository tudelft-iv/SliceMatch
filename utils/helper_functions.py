import torch


def slicematch_train_function(model, criterion, optimizer, data_loader, device):
    """
    The training function for SliceMatch.
    
    Args:
        model (torch.nn.Module) : neural network
        criterion (function) : loss function
        optimizer (torch.optim.adam.Adam) : optimizer
        data_loader (torch.utils.data.dataloader.DataLoader) : data loader
        device (torch.device) : name of GPU if available else CPU name
    
    Returns:
        avg_loss (float) : average loss
    """
    
    # set model to train mode
    model.train()
    
    # train
    total_loss = 0
    for img_pairs, targets in data_loader:
        grd_imgs  = torch.stack([grd_img for grd_img, _ in img_pairs]).to(device)
        aer_imgs  = torch.stack([aer_img for _, aer_img in img_pairs]).to(device)
        loc_gts   = torch.stack([target['loc'] for target in targets]).to(device)
        orien_gts = torch.stack([torch.tensor([target['orien']]) for target in targets]).to(device)
        
        # try to load masks to speed up training
        masks, mask_bools, mask_dirs = [], [], []
        for b in range(grd_imgs.shape[0]):
            mask_dir = targets[b]['mask_dir'].replace('Nx', f'N{str(model.N).zfill(2)}')
            if os.patorch.isfile(mask_dir):
                mask      = torch.load(mask_dir)
                mask_bool = True
            else:
                mask      = torch.zeros([model.N, model.A//model.stride, model.A//model.stride])
                mask_bool = False
            masks.append(mask)
            mask_bools.append(mask_bool)
            mask_dirs.append(mask_dir)
        masks = torch.stack(masks)

        # targets dictionary
        targets_dict = {'loc_gts':    loc_gts,
                        'orien_gts':  orien_gts,
                        'masks':      masks,
                        'mask_bools': mask_bools,
                        'mask_dirs':  mask_dirs,}

        # predict and loss
        grd_descriptors, aer_descriptors, aer_descriptors_gt = model(grd_imgs, aer_imgs, targets_dict)
        loss = criterion.get_loss(grd_descriptors, aer_descriptors, aer_descriptors_gt)
        
        # update parameters
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # add loss
        total_loss += loss.item()
        
    # average loss
    avg_loss = total_loss/len(data_loader)
    
    return avg_loss


def slicematch_validate_function(model, criterion, data_loader, device):
    """
    The validation function for SliceMatch.
    
    Args:
        model (torch.nn.Module) : neural network
        criterion (function) : loss function
        data_loader (torch.utils.data.dataloader.DataLoader) : data loader
        device (torch.device) : name of GPU if available else CPU name
    
    Returns:
        avg_loss (float) : average loss
    """
    
    # set model to evaluation mode
    model.eval()
    
    # validate
    total_loss = 0
    with torch.no_grad():           
        for img_pairs, targets in data_loader:
            grd_imgs  = torch.stack([grd_img for grd_img, _ in img_pairs]).to(device)
            aer_imgs  = torch.stack([aer_img for _, aer_img in img_pairs]).to(device)
            loc_gts   = torch.stack([target['loc'] for target in targets]).to(device)
            orien_gts = torch.stack([torch.tensor([target['orien']]) for target in targets]).to(device)
            
            # try to load masks to speed up training
            masks, mask_bools, mask_dirs = [], [], []
            for b in range(grd_imgs.shape[0]):
                mask_dir = targets[b]['mask_dir'].replace('Nx', f'N{str(model.N).zfill(2)}')
                if os.patorch.isfile(mask_dir):
                    mask      = torch.load(mask_dir)
                    mask_bool = True
                else:
                    mask      = torch.zeros([model.N, model.A//model.stride, model.A//model.stride])
                    mask_bool = False
                masks.append(mask)
                mask_bools.append(mask_bool)
                mask_dirs.append(mask_dir)
            masks = torch.stack(masks)
            
            # targets dictionary
            targets_dict = {'loc_gts':    loc_gts,
                            'orien_gts':  orien_gts,
                            'masks':      masks,
                            'mask_bools': mask_bools,
                            'mask_dirs':  mask_dirs,}
            
            # predict and loss
            grd_descriptors, aer_descriptors, aer_descriptors_gt = model(grd_imgs, aer_imgs, targets_dict)
            loss = criterion.get_loss(grd_descriptors, aer_descriptors, aer_descriptors_gt)
            
            # add loss
            total_loss += loss.item()
            
    # average loss
    avg_loss = total_loss/len(data_loader)
    
    return avg_loss


def slicematch_test_function(model, data_loader, device):
    """
    The testing function for slicematch.
    
    Args:
        model (torch.nn.Module) : neural network
        data_loader (torch.utils.data.dataloader.DataLoader) : data loader
        device (torch.device) : name of GPU if available else CPU name
        
    Returns:
        test_result (array) : array with the predicted poses and GT poses with shape (N,6) [loc_gts, loc_preds, orien_gts, orien_preds]
    """
    
    # variable to store test result
    test_result = torch.empty([0,6]).to(device)
    
    # grid locations and orientations
    grid_locs      = model.slicer.grid_locs.to(device)
    orientations_R = torch.linspace(0, 360/model.N-360/(model.N*model.slicer.num_rotations), model.slicer.num_rotations).to(device)
    orientations_N = torch.linspace(0, 360-360/model.N, model.N).to(device)
    
    # set model to evaluation mode
    model.eval()
    
    # test
    with torch.no_grad():
        for img_pairs, targets in data_loader:
            grd_imgs  = torch.stack([grd_img for grd_img, _ in img_pairs]).to(device)
            aer_imgs  = torch.stack([aer_img for _, aer_img in img_pairs]).to(device)
            loc_gts   = torch.stack([target['loc'] for target in targets]).to(device)
            orien_gts = torch.stack([torch.tensor([target['orien']]) for target in targets]).to(device)
            
            # targets dictionary (no training -> no masks)
            targets_dict = {'loc_gts':   loc_gts,
                            'orien_gts': orien_gts,}
            
            # predict
            grd_descriptors, aer_descriptors = model(grd_imgs, aer_imgs)
            
            # determine similarities
            # grd_descriptors := tensor with shape ()
            # aer_descriptors := tensor with shape ()
            sims = torch.einsum('abcde,abcde->abcd', grd_descriptors.view(grd_imgs.shape[0],1,1,1,-1), aer_descriptors)
            
            # determine predicted location and orientation
            if DO_POSE_ESTIMATION:
                loc_preds   = grid_locs[torch.argmax(torch.max(torch.max(sims, dim=-1)[0], dim=-1)[0], dim=1)]
                index_R     = torch.argmax(torch.max(torch.max(sims, dim=-3)[0], dim=-1)[0], dim=1)
                index_N     = torch.argmax(torch.max(torch.max(sims, dim=-3)[0], dim=-2)[0], dim=1)
                orien_preds = (orientations_N[index_N]+orientations_R[index_R]).view(-1,1)
            elif DO_LOCALIZATION:
                loc_preds   = grid_locs[torch.argmax(sims[...,0,0], dim=1)]
                orien_preds = torch.zeros([B,1]).to(device)
                
            # append targets and predictions to test result
            test_result = torch.cat((test_result, torch.cat((loc_gts, loc_preds, orien_gts, orien_preds), dim=1)), dim=0)
            
    return test_result.cpu().numpy()
