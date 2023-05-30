# 将图片和标注数据按比例切分为 训练集和测试集
# 请务必在yolo文件夹运行
import shutil
import random
import os

dataset_name = "SpeedBumpDataset"
dataset_name = "InstantNoodlesDataset"

cur_path = os.getcwd()  # 用绝对路径好一些
print(cur_path)
# 原始路径
image_original_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/data/images/")
label_original_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/data/labels/")

# 训练集路径
train_image_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/images/train/")
train_label_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/labels/train/")

# 验证集路径
val_image_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/images/val/")
val_label_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/labels/val/")

# 测试集路径
test_image_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/images/test/")
test_label_path = os.path.join(
    cur_path, "datasets/"+dataset_name+"/labels/test/")

# 数据集对应划分的txt,是运行之后生成的
list_train = os.path.join(cur_path, "datasets/"+dataset_name+"/train.txt")
list_val = os.path.join(cur_path, "datasets/"+dataset_name+"/val.txt")
list_test = os.path.join(cur_path, "datasets/"+dataset_name+"/test.txt")

train_percent = 0.6
val_percent = 0.2
test_percent = 0.2


def del_file(path):
    for i in os.listdir(path):
        file_data = path + "\\" + i
        os.remove(file_data)


def mkdir():
    if not os.path.exists(train_image_path):
        os.makedirs(train_image_path)
    else:
        del_file(train_image_path)
    if not os.path.exists(train_label_path):
        os.makedirs(train_label_path)
    else:
        del_file(train_label_path)

    if not os.path.exists(val_image_path):
        os.makedirs(val_image_path)
    else:
        del_file(val_image_path)
    if not os.path.exists(val_label_path):
        os.makedirs(val_label_path)
    else:
        del_file(val_label_path)

    if not os.path.exists(test_image_path):
        os.makedirs(test_image_path)
    else:
        del_file(test_image_path)
    if not os.path.exists(test_label_path):
        os.makedirs(test_label_path)
    else:
        del_file(test_label_path)


def clearfile():
    if os.path.exists(list_train):
        os.remove(list_train)
    if os.path.exists(list_val):
        os.remove(list_val)
    if os.path.exists(list_test):
        os.remove(list_test)


def main():
    mkdir()
    clearfile()

    file_train = open(list_train, 'w')
    file_val = open(list_val, 'w')
    file_test = open(list_test, 'w')

    total_txt = os.listdir(label_original_path)
    print("total_txt:", total_txt)
    num_txt = len(total_txt) - 1  # 不要管那个classed.txt
    list_all_txt = range(num_txt)

    num_train = int(num_txt * train_percent)  # 训练集样本个数
    num_val = int(num_txt * val_percent)  # 验证集
    num_test = num_txt - num_train - num_val  # 测试集

    train = random.sample(list_all_txt, num_train)
    # train从list_all_txt取出num_train个元素
    # 所以list_all_txt列表只剩下了这些元素
    val_test = [i for i in list_all_txt if not i in train]
    # 再从val_test取出num_val个元素，val_test剩下的元素就是test
    val = random.sample(val_test, num_val)

    print("训练集数目：{}, 验证集数目：{}, 测试集数目：{}".format(
        len(train), len(val), len(val_test) - len(val)))
    for i in list_all_txt:
        name = total_txt[i][:-4]

        srcImage = image_original_path + name + '.png'
        srcLabel = label_original_path + name + ".txt"

        if i in train:
            dst_train_Image = train_image_path + name + '.png'
            dst_train_Label = train_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_train_Image)
            shutil.copyfile(srcLabel, dst_train_Label)
            file_train.write(dst_train_Image + '\n')
        elif i in val:
            dst_val_Image = val_image_path + name + '.png'
            dst_val_Label = val_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_val_Image)
            shutil.copyfile(srcLabel, dst_val_Label)
            file_val.write(dst_val_Image + '\n')
        else:
            dst_test_Image = test_image_path + name + '.png'
            dst_test_Label = test_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_test_Image)
            shutil.copyfile(srcLabel, dst_test_Label)
            file_test.write(dst_test_Image + '\n')

    file_train.close()
    file_val.close()
    file_test.close()


if __name__ == "__main__":
    main()
