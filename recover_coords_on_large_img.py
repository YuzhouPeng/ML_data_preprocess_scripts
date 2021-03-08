import os
cropped_coords = []
cropped_filesnames = []

cropsize = 1000
def recover_coords_on_origin_img(cropped_coords,cropped_filesnames):
    newcoords = []
    for coord,filename in zip(cropped_coords, cropped_filesnames):
        ele = filename.split("_")
        h,w = int(ele[0]),int(ele[1])
        for point in coord:
            x = w*cropsize+x
            y = h*cropsize+y
            newcoords.append([x,y])
    return newcoords

