# -*- coding: utf-8 -*-
import os
import oss2
import pickle
import urllib.parse
from myimage.common import gen_img_key, LogFileHandler
from myimage.settings import DATA_DIR
from typing import List
# from multiprocessing import Pool
# import threading


class AliOss:
    def __init__(self, AK=None, SK=None, end_point=None, bucket_name=None):
        if AK:
            self._config(AK, SK, end_point, bucket_name)
        try:
            data = pickle.load(open(self._get_secret_path(), "rb"))
            self._AK = data["AK"]
            self._SK = data["SK"]
            self._end_point = data["END_POINT"]
            self._bucket_name = data["BUCKET_NAME"]
            self._auth = oss2.Auth(self._AK, self._SK)
            self.bucket = oss2.Bucket(self._auth, self._end_point, self._bucket_name)
        except (FileNotFoundError, KeyError):
            raise Exception("You need to use api `AliOss.config()` first to config your secret data!")
        self.log = LogFileHandler("ali_oss")

    def _get_secret_path(self) -> str:
        return os.path.join(DATA_DIR, ".ali_oss.pkl")

    def _config(self, AK, SK, end_point, bucket_name):
        data = {
            "AK": AK,
            "SK": SK,
            "END_POINT": end_point,
            "BUCKET_NAME": bucket_name
        }
        pickle.dump(data, open(self._get_secret_path(), "wb"))
        self.log.info("Successfully configured AliOss Secret Data!")

    def _gen_url(self, end_point: str, img_key: str) -> str:
        """
        https://mark-vue-oss.oss-cn-hangzhou.aliyuncs.com/20210211_160322_116264-%E5%8D%97%E5%AE%A1-%E5%A4%A7%E6%B4%BB-%E4%BF%AF%E7%9E%B0%E5%9B%BE.jpg
        :param end_point:
        :param img_key:
        :return:
        """
        return "https://" + self._bucket_name + "." + end_point + "/" + urllib.parse.quote_plus(img_key)

    def upload_img(self, img_path: str, _id=None) -> dict:
        img_path = img_path.strip('"')          # 去掉引号，typora support
        key = gen_img_key(img_path)
        result = self.bucket.put_object_from_file(key, img_path)
        img_data = {
            "path": img_path,
            "key": key,
            "url": self._gen_url(self._end_point, key),
            "id": result.request_id,
            "status": result.status
        }
        self.log.info({"uploaded": img_data})
        return img_data

    def upload_multi_imgs(self, img_paths: List[str]) -> List[dict]:
        return [self.upload_img(p) for p in img_paths]
