import os

# to write K and D into configs folder
def writeIntriToFile(file_path,cmx,dist):
    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write("import numpy as np\n")
        
        f.write("cameraMatrix = np.float32("+str(cmx.tolist())+')')

        f.write("\ndistCoeff = np.float32("+str(dist.tolist())+')')

    print(f"file has been written to : {file_path}.")

# to remove files in a folder
def cleanFolder(folder):
    # delete the formal photos
    del_list = os.listdir(folder)
    for f in del_list:
        file_path = os.path.join(folder, f)
        if os.path.isfile(file_path):
            os.remove(file_path)