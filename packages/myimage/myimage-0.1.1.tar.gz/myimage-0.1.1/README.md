# 我的图床

## 需求来源
使用Typora写完的Markdown文章在发布到其他平台（比如公众号、知乎等），
需要考虑将文章内的图片引用转成在线外链。

本项目灵感来自于PicGo这款软件，但它存在一些问题，
比如多图片上传的bug等，基于此开发了替代版本。

## 使用说明
### 使用阿里云OSS服务
#### 初始化
1. 初始化会需要输入AK、SK、EndPoint和BucketName四个信息，
这些都可以在你的阿里云服务上找到，具体可以访问：
https://oss.console.aliyun.com/overview

2. 运行后将自动存储这些信息为二进制文件，之后便可以不用输入这些信息，
防止你的秘钥泄露

```python    
AK = "XXXX"
SK = "XXXX"
END_POINT = "oss-cn-hangzhou.aliyuncs.com"
BUCKET_NAME = "XXXX"
ali_oss = AliOss(AK, SK, END_POINT, BUCKET_NAME)
```

#### 程序使用
```python
from myimage.upload.ali_oss import AliOss
ali_oss = AliOss()

# upload single image
ali_oss.upload_img("/Users/mark/Pictures/xxxx.jpg")

# upload multi images
ali_oss.upload_multi_imgs([
    "/Users/mark/Pictures/xxxx.jpg",
    "/Users/mark/Pictures/image-20201015195312768.png"
])
```
#### 命令行使用
在typora中可以配置自己的命令行，方便上传图片。
我已经写了一个`ali_oss_cmd.py`，可以使用它去上传一张或多张图片。

以我的typora为例，配置为：
```shell script
/Users/mark/PycharmProjects/mark_scripts/venv/bin/python /Users/mark/PycharmProjects/mark_scripts/myimage/upload/ali_oss_cmd.py
```
注意，如果你不是使用的默认`python`，则要指定`python`的具体位置。

否则，可以直接使用下面的简短版本：
```shell script
python /Users/mark/PycharmProjects/mark_scripts/myimage/upload/ali_oss_cmd.py
```

注意，要修改自己本地的文件路径。

### 使用SM.MS图床（SM.MS是2020年开发的，不保证2021年目前的可用性）
该图床可无需注册使用，即随手上传图片，并获得一个外链。

```python
import myimage
img_path = r'xxxx'
img_path_online = myimage.upload_img(img_path)
```

### 使用七牛云（七牛云是2020年开发的，不保证2021年目前的可用性）
需要配置您键信息，支持两种方式，具体可以参考官方说明：https://portal.qiniu.com/kodo/bucket

#### 1. （推荐）配置settings文件启动
在`myimage/myimage`下新建`settings.py`文件，填写一下键信息：
```python
DOMAIN = xxx
BUCKET = xxx
AK = xxx
SK = xxx
```

接着就可以使用以下代码上传图片了：
```python
import myimage
q = myimage.IMG_Qiniuyun()

img_path = r'xxx'
img_path_online = q.upload_img(img_path)
```
#### 2. 直接通过参数输入启动
```python
import myimage
q = myimage.IMG_Qiniuyun()
q.init_from_params(domain='xx', bucket='xx', ak='xx', sk='xx')

img_path = r'xxx'
img_path_online = q.upload_img(img_path)
```

## update log
- [x] 已完成阿里云的支持  

## TODO
- [ ] 支持腾讯云、Github等其他图床平台
- [ ] 完善markdown的转换
- [ ] 其他一些功能欢迎issue

## Others
### project Init
```shell script
git remote add origin git@github.com:MarkShawn2020/myimage.git
git branch -M main
git push -u origin main
```
