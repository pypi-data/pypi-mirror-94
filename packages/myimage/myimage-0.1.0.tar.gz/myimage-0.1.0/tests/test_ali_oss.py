# -*- coding: utf-8 -*-
import oss2
from myimage.common import gen_img_key

AK = "LTAI4G8kArj75ch3irL8mUUJ"
SK = "A6HV7Bjypq1J788FhSu3n6zKduwpIs"
END_POINT = "oss-cn-hangzhou.aliyuncs.com"
BUCKET_NAME = "mark-vue-oss"

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
auth = oss2.Auth(AK, SK)
# Endpoint以杭州为例，其它Region请按实际情况填写。
endpoint = END_POINT
bucket_name = BUCKET_NAME

bucket = oss2.Bucket(auth, endpoint, bucket_name)


def gen_url(end_point: str, img_key: str) -> str:
    """
    https://mark-vue-oss.oss-cn-hangzhou.aliyuncs.com/20210211_160322_116264-%E5%8D%97%E5%AE%A1-%E5%A4%A7%E6%B4%BB-%E4%BF%AF%E7%9E%B0%E5%9B%BE.jpg
    :param end_point:
    :param img_key:
    :return:
    """
    return "https://" + bucket_name + "." + end_point + "/" + img_key


def upload_img(img_path: str) -> str:
    key = gen_img_key(img_path)
    result = bucket.put_object_from_file(key, img_path)
    print({"path": img_path, "key": key, "url": gen_url(endpoint, key)})
    return result


if __name__ == '__main__':
    upload_img("/Users/mark/Pictures/南审-大活-俯瞰图.jpg")
