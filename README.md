git created on 2023/5/12

此项目为2023年秋同济大学CV课程作业，用于实现行人和减速带检测以及距离解算。 opencv  version：4.7.0.22 (原先用的3.x，但是yolov7需要4.0+)

# 一、相机标定（拍照+标定+去畸变）

​		相机标定在calibration.py里实现。目前不足：鱼眼相机去畸变有点问题，其他均正常。

​		使用方法：运行calibration.py，按照提示运行即可。**请注意，本程序capture时会自动清空标定板图片文件夹**。先capture拍照，拍照数目可以在程序里预设；然后calibrate标定，不同类型相机的结果会自动写入不同config里。然后可以undistort去畸变。

​		标定板相关请参考：[openCV踩坑汇总 | 雨白的博客小屋 (ameshiro77.cn)](https://www.ameshiro77.cn/posts/4e9580a4.html) 的目录2，**本程序使用的标定板是x方向奇数11个、y方向偶数8个、角点间距1cm的标定板**，在程序里为calibration.py的：

```python
board = Board(11,8,10) #col row width(mm)
```

​		如果您的标定板与之不同，请务必记得修改。



2023/5/14 更新：

​		把部分函数放入到了utils/calibrate下，供其他程序使用。**新增了鸟瞰图**，运行birdeye.py即可。

​		PS：鸟瞰图转换中，标定板平面坐标系的原点以左上角为基础，向左上平移了200mm。

2023/5/23 更新：

        下载了yolov7代码，能够检测视频中人物但是非常卡。



# 二、单应矩阵标定



# 三、目标检测

2023/5/29更新：

初步试了下用自己的数据集训练。建立了datasets文件夹，标注工具为labelimg。数据处理过程为：

1.将要标注的图片放到data/images里。

2.用labelimg标注，标注结果放到data/labels里。

3.运行yolo文件夹下的data_process.py来划分数据，生成训练集等路径。参考博客：[Yolov7训练自己的数据集（超详细） - 玻璃公主 - 博客园 (cnblogs.com)](https://www.cnblogs.com/boligongzhu/p/16718242.html)

**github不传图片，请自己拍摄**~

踩了以下坑，作个汇总。

1.train.py的config我更改过。之前当使用预训练时，会报keyerror:"assets"的错误。(**据我观察，这基本就是.pt文件路径不对的问题，请检查自己参数里的路径是否写对了**)。

2.train.txt等等里面的路径最好还是写绝对路径，用os.getcwd和join拼接即可。

3.如果要用cpu训练，把utils/loss.py里面的780多行那几个device gpu：0务必改成cpu：0.