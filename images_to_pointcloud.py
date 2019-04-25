#!/usr/bin/env python

'''
Simple example of stereo image matching and point cloud generation.
Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
'''

import numpy as np
import cv2

import matplotlib



import argparse
import os

parser = argparse.ArgumentParser(description="===> OBTAIN THE 3D RECONSTRUCTION FROM THE CAPTURED IMAGES <===")
parser.add_argument("in_images", nargs=2, help="Input images path that should be indicated in order: (right_image, left_image)")
parser.add_argument("out_folder", help="Folder to write output pointcloud and disparity image")
args = parser.parse_args()



ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'w') as f:
        f.write(ply_header % dict(vert_num=len(verts)))
        np.savetxt(f, verts, '%f %f %f %d %d %d')


if __name__ == '__main__':
    print 'loading images...'
    imgL = cv2.pyrDown( cv2.imread(args.in_images[1]) )  # downscale images for faster processing
    imgR = cv2.pyrDown( cv2.imread(args.in_images[0]) )


    #imgL = cv2.resize(imgL, (529, 397)) 
    #imgR = cv2.resize(imgR, (529, 397)) 

    # disparity range is tuned for 'aloe' image pair
    window_size = 3
    min_disp = 16
    #jm#num_disp = 112-min_disp
    num_disp = 224-min_disp
    stereo = cv2.StereoSGBM(minDisparity = min_disp,
        numDisparities = num_disp,
        SADWindowSize = window_size,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32,
        disp12MaxDiff = 1,		# talvez com um valor grande, tipo 1000, isto pareca melhor
        P1 = 8*3*window_size**2,
        P2 = 64*3*window_size**2,
        fullDP = False
    )

    print 'computing disparity...'
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    disp_img = (disp-min_disp)/num_disp

## DISP_IMG era so DISP

    ##disp[disp < 0.20] = 0	#0.3 para a imagem grande
    ###disp[disp < 0.60] = 0	#0.3 para a imagem grande
				#0.35 para a imagem pequena
    ##disp[disp > 0.4] = 0
    ###disp[disp > 0.8] = 0

    #disp_img[disp_img < 0.3] = 0
    #disp_img[disp_img > 0.6] = 0
    #disp[disp < 78] = 0
    #disp[disp > 141] = 0

    print 'generating 3d point cloud...',
    h, w = imgL.shape[:2]
    f = 0.8*w                          # guess for focal length
    #f = 0.304*w                          # guess for focal length
    Q = np.float32([[1, 0, 0, -0.5*w],
                    [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                    [0, 0, 0,     -f], # so that y-axis looks up
                    [0, 0, 1,      0]])

    #Q = np.float32([[1, 0, 0, -0.5*w],
    #                [0, 0, 0,     -f],
    #                [0,-1, 0,  0.5*h],
    #                [0, 0, 1,      0]])

    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]

    filename_pc = "pointcloud.ply"
    output_pc_path = os.path.join(args.out_folder, filename_pc)
    write_ply(output_pc_path, out_points, out_colors)
    print '%s saved' % 'out.ply'

    filename_img = "disparity.jpg"
    output_img_path = os.path.join(args.out_folder, filename_img)
    cv2.imwrite(output_img_path, disp_img*255)	# Before converting pic to uint8, we need to multiply it by 255 to get the correct range.

    cv2.imshow('Image_Left', imgL)
    #cv2.imshow('Image_Disparity', disp_img)
    cv2.imshow('Image_Disparity', (disp-min_disp)/num_disp)
    cv2.waitKey()
cv2.destroyAllWindows()

