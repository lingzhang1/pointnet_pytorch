
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
        self.neighbors = []
        for x in lines:
            l = x.split('\t')
            coords = array([float(l[0]),float(l[1]),float(l[2])] )
            self.image.append(coords)
        # for x in lines:
        #     l = x.split(' ')
        #     coords = array([float(l[0]),float(l[1]),float(l[2])] )
        #     self.image.append(coords)

        self.image = array(self.image)

    def get_k_neighborhood(self, k, points):
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='kd_tree').fit(self.image)
        distances, indices = nbrs.kneighbors(self.image)
        neighbors = []
        for ind in indices:
            tmp = []
            for i in ind:
                tmp.append(self.image[i])
            neighbors.append(tmp)
        return array(neighbors)


#===============================================================================

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
        # k neighborhood points
        k = int(len(lines) * 0.7)
        # neighbors for each point and get normal
        I.neighbors = I.get_k_neighborhood(k)

        #   output points to file
        out_lines = []
        line = ""

        for l in I.neighbors:
            line = " ".join([str(x) for x in l])
            out_lines.append(line)


        ofname = mypath + "/" + "neighbors_" + filename
        with open(ofname, mode='w') as fo:
                for l in out_lines:
                    fo.write(str(l)+'\n')
        print("file number: ", num)
        num += 1
