import numpy as np

def conv(img2d, f, fil):
    # conv() is 2D convolution function.
    # img2d is 2D image, f is filter size and fil is convolution filter.
    # conv() returns convolution of img_gary with fil along with zero padding.
    
    r, c = img2d.shape # r = rows of image; c = columns of image
    
    # Padding of img2d
    pad = int((f-1) * 0.5) # calculate padding using filter size
    img_pad = np.zeros((r + pad, c + pad)) # create a padded image with all entries zero
    for m in range(r): # iterate through all row pixels
        for n in range(c): # iterate through all column pixels
            img_pad[m+pad,n+pad] = img2d[m,n] # store values of img2d in img_pad to get final padded image
    
    # Convolution of img_pad with fil
    out_img = np.zeros((r,c)) # create an output array with all alues zero 
    for i in range(r): # iterate through all row pixels
        for j in range(c): # iterate through all column pixels
            if i < r-pad and j < c-pad: # Check for indexing of img_pad
                out_img[i,j] = np.sum(np.multiply(img_pad[i:i+f,j:j+f], fil)) # Convolution operation
            elif i < r-pad and j >= c-pad: # Check for indexing of img_pad
                out_img[i,j] = np.sum(np.multiply(img_pad[i:i+f,j-pad:j+pad+1], fil)) # Convolution operation
            elif i >= r-pad and j < c-pad: # Check for indexing of img_pad
                out_img[i,j] = np.sum(np.multiply(img_pad[i-pad:i+pad+1,j:j+f], fil)) # Convolution operation
            elif i >= r-pad and j >= c-pad: # Check for indexing of img_pad
                out_img[i,j] = np.sum(np.multiply(img_pad[i-pad:i+pad+1,j-pad:j+pad+1], fil)) # Convolution operation

    return out_img
