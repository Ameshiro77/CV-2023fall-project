import sys
sys.path.append('../')  # 添加上级目录到sys.path中
import numpy as np
from configs.homography2 import homographyMatrix

def getDistance(u,v)-> float:
        point=np.array([u,v,1])
        world_coordinate = np.dot(homographyMatrix,point)
        coeff =  1 / world_coordinate[2]
        world_coordinate = world_coordinate * coeff
        return (np.sqrt(world_coordinate[0]**2+world_coordinate[1]**2) / 1000 ) # mm -> m