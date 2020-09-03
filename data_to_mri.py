import pydicom
import dicom_numpy
from os import listdir
import numpy as np
import math
from copy import deepcopy

# load data
path='path_to_mri_folder'
matrix = np.loadtxt('path_to xyz_to_ijk_matrix')
spikes = np.loadtxt('path_to_meg_data')
slices = [pydicom.read_file(path + '/' + s) for s in listdir(path)]
slices.sort(key = lambda x: int(x.InstanceNumber))
voxel_ndarray, _ = dicom_numpy.combine_slices(slices)


# you have to check that the orientation of slices and voxel_ndarray are the same
# sometimes you have to inverse z orientation
# voxel_ndarray = voxel_ndarray.T[::-1]
# plt.imshow(voxel_ndarray[-67], cmap=plt.cm.bone)
# plt.show()
# plt.imshow(slices[-67].pixel_array, cmap=plt.cm.bone)
# plt.show()

# switch to ijk space
spikes_in_ijk = np.dot(matrix, np.c_[spikes, np.ones(len(spikes))].T).T[:,:-1]*[1,1,1]
voxel_ind = spikes_in_ijk.astype(int)

# increase the intensity of the required voxels
# indices are specified depending on the orientation of the original volume, 
# so that the coordinate system of the displayed data coincides 
# with the coordinate system of the original MRI
for i in voxel_ind:
    slices[i[2]].pixel_array[i[1],i[0]] = 10000

# save data
for i in range(len(slices)):
    slices[i][0x8,0x103e].value = 'MEG data'
    slices[i].PixelData = slices[i].pixel_array.tobytes()
    slices[i].save_as('path_to_output_folder/%s.dcm' %i)
