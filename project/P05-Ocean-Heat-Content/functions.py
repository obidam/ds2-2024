import numpy as np

R = 6371e3 # Earth radius

def volume_voxel(lat, height):
    radius_circle = R*np.cos(np.deg2rad(lat))
    circunf_circle = 2*np.pi*radius_circle
    length_1deg = circunf_circle/360
    
    area = length_1deg**2
    vol = area * height
    
    return vol

def total_vol_by_depth(depth):
    '''
    Receives the depth (must be the depth of the voxels that will be calulated)
    i.e. the difference between two adjacents depths in the dataset, to represent
    the height of the volume being calculated.
    '''
    
    total_vol = 0
    
    for lat in range(-180,181):
        single_voxel = volume_voxel(lat,depth)
        total_volume_for_lat = single_voxel*360
        
        total_vol += total_volume_for_lat
        
    return total_vol
