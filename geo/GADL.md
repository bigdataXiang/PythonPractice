# gadl

## 官网
 https://pypi.python.org/pypi/GDAL/

## other

这里使用 ubuntugis提供的gdal进行安装。
首先更新一下ubuntugis的源：

sudo add-apt-repository ppa:ubuntugis && sudo apt-get update

或者

sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable && sudo apt-get update

这里科普一下PPA（摘自百度百科）：
Personal Package Archives（个人软件包档案）是Ubuntu Launchpad网站提供的一项服务，允许个人用户上传软件源代码，通过Launchpad进行编译并发布为2进制软件包，作为apt/新立得源供其他用户下载和更新。在Launchpad网站上的每一个用户和团队都可以拥有一个或多个PPA。

然后安装C++版本的GDAL：

sudo apt-get install gdal-bin

然后安装GDAL的Python Wrapper包：

sudo pip install gdal

在Ubuntu下使用Eclipse+PyDev进行开发。
参见一个小程序：

from osgeo import gdal

file_path = '/home/theone/Data/GreatKhingan/DEM/Slope_GreatKhingan_500m.tif'
dataset = gdal.Open(file_path)
print(type(dataset))

metadata = dataset.GetMetadata()
print(metadata)

projection = dataset.GetProjection()


运行结果：

<class 'osgeo.gdal.Dataset'>
{'TIFFTAG_XRESOLUTION': '1', 'TIFFTAG_YRESOLUTION': '1', 'AREA_OR_POINT': 'Area'}
<type 'str'>
GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]