
import string, sys
from numpy import *
from numpy.linalg import *
from sklearn.neighbors import NearestNeighbors
from os import listdir
from os.path import isfile, join


class Image:

    def __init__(self, lines):

        # open file
        # lines = open(filename, "r").readlines()

        self.image = []
        self.normals = []
        self.coords_normal = []
        for x in lines:
            l = x.split(' ')
            coords = array([float(l[0]),float(l[1]),float(l[2])] )
            self.image.append(coords)

        self.image = array(self.image)

    def get_kxk_neighborhood(self, k):
        # return all k by k neighborhood points
        nbrs = NearestNeighbors(n_neighbors=k*k, algorithm='kd_tree').fit(self.image)
        distances, indices = nbrs.kneighbors(self.image)
        neighbors = []
        for ind in indices:
            tmp = []
            for i in ind:
                tmp.append(self.image[i])
            neighbors.append(tmp)
        return array(neighbors)

def get_normal(P):

    k = len(P[0])
    centroid = array([0.,0.,0.])
    for i in range(0,k):
        for j in range(0,k):
            centroid = centroid + P[i][j]
    # centroid of the k by k matrix
    centroid = centroid/(k*k)
    # covariance matrix
    A = array([[0,0,0],[0,0,0],[0,0,0]])
    for i in range(0,k):
        for j in range(0,k):
            [p1,p2,p3] = P[i][j] - centroid
            # A = A + ([p1,p2,p3]^T times [p1,p2,p3])
            A = A + array([[p1],[p2],[p3]]) * array([p1,p2,p3])

    #Eigenvalues and corresponding eigenvectors of A.
    eigs = eigh(A)
    eigenvalues = eigs[0]
    eigenvectors = eigs[1]
    # smallest eigenvalue index
    min_eval_index = argmin(eigenvalues)
    # smallest eigenvalue
    min_eigenval = eigenvalues[min_eval_index]
    #The eigenvector associated with the smallest eigenvalue
    normal = eigenvectors[min_eval_index]
    return array(normal)
    #if the eigenvalue is small than threshold, then these points are coplanar so return True.
    # if(min_eigenval <= p_thresh): return True
    # else: return False

#===============================================================================

# 3 by 3 neighborhood points
k = 3
# read data
mainpath = "shapenetcore_partanno_segmentation_benchmark_v0"
lines = open(mainpath + "/synsetoffset2category.txt", "r").readlines()
categories = []
for x in lines:
    l = x.split('\t')
    # ['Airplane', '02691156\n']
    categories.append(l[1][0:len(l) - 3])
num = 1;
for cat in categories:
    # read all files under each categories
    mypath = mainpath + "/" + cat + "/points"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for filename in files:
        lines = open(mypath + "/" + filename, "r").readlines()
        I = Image(lines)

        # neighbors for each point and get normal
        neighbors = I.get_kxk_neighborhood(k)
        for i in range(len(neighbors)):
            normal = get_normal(neighbors[i])
            I.normals.append(normal)
            # print(normal)
            I.coords_normal.append(concatenate((I.image[i], normal), axis=None))

        #   output points to file
        out_lines = []
        line = ""
        out_normals = []
        for l in I.normals:
            line = " ".join([str(x) for x in l])
            out_normals.append(line)

        for l in I.coords_normal:
            line = " ".join([str(x) for x in l])
            out_lines.append(line)


        ofname = mypath + "/" + filename
        with open(ofname, mode='w') as fo:
                for l in out_lines:
                    fo.write(str(l)+'\n')
        ofname = mypath + "/" + "normals_" + filename
        with open(ofname, mode='w') as fo:
                for l in out_normals:
                    fo.write(str(l)+'\n')
        print("file number: ", num)
        num += 1
