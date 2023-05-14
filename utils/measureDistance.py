import sys
sys.path.append('../')  # 添加上级目录到sys.path中
import numpy as np
from configs.Intrinsic_fisheye import homographyMatrix
class distance:
    def __init__(self) -> None:
        pass
    """
    the pic
    parameters:
        u,v represent the coordinate of the center-point
    return: the real distance of the point    
    """
    def getDistance(self,u:int,v:int)-> float:
        point=np.array([u,v,1])
        world_coordinate=np.dot(homographyMatrix,point)
        return np.sqrt(world_coordinate[0]**2+world_coordinate[1]**2)

        