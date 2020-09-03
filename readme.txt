In order to transfer MEG data to MRI images follow instructions below.

First of all conversion from subject coordinate system to MRI coordinate system have to be handled using function cs_convert in MatLab:

Pdest = cs_convert(sMri, 'scs', 'mri', Psrc);
sMri: MRI structure from the database: right-click on the MRI file > File > Export to Matlab > sMri  
'scs'/'mri': Source and destination coordinates systems
Psrc/Pdest: List of points in source and destination coordinates systems [Npoints x 3]
All the the coordinates have to be in meters (not millimeters).

Points in MRI coordinate system have to be exported from MatLab in .txt format.

Then we have to convert data points to sphere surfaces for further visualization in MRI images using following Python script.

import numpy as np
from mayavi import mlab

points = np.loadtxt('points.txt')
fig = mlab.figure('MEG data')
mlab.points3d(points[:,0], points[:,1], points[:,2], color = (1,0,0), scale_factor=4)
mlab.savefig('MEG_data' + '.x3d')

Obtained 3D model have to be converted to .xyz file format. 
To visualize data in MRI images we need xyz to ijk transition matrix that can be automatically computed in 3DSliser:

volumeNode= getNode('MRI')
mat = vtk.vtkMatrix4x4()
volumeNode.GetRASToIJKMatrix(mat)
print mat

Then data can be visualized in MRI images using Python script "data_to_mri.py".