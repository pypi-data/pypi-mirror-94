<<<<<<< HEAD
# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/3/10 1:48
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

import os
import requests


def check_local_exist(func):
	def wrapper(self, img_path, *args, **kwargs):
		assert os.path.exists(img_path), "本地不存在该图片！请核实: {}".format(img_path)
		return func(self, img_path, *args, **kwargs)
	return wrapper


def check_target_exist(target_path: str):
	return requests.head(target_path).status_code == 200
=======
# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/3/10 1:48
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
import logging
from myimage.settings import LOG_DIR

import os
import datetime
import requests


def check_local_exist(func):
	def wrapper(self, img_path, *args, **kwargs):
		assert os.path.exists(img_path), "本地不存在该图片！请核实: {}".format(img_path)
		return func(self, img_path, *args, **kwargs)
	return wrapper


def check_target_exist(target_path: str):
	return requests.head(target_path).status_code == 200


def gen_img_key(img_path: str) -> str:
	key = os.path.basename(img_path)
	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
	return timestamp + "-" + key


class LogFileHandler(logging.Logger):
	def __init__(self, name: str, *args, **kwargs):
		super().__init__(name)
		log_formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s")
		log_file_handler = logging.FileHandler(os.path.join(LOG_DIR, "ali_oss.log"))
		log_file_handler.setLevel(logging.DEBUG)
		log_file_handler.setFormatter(log_formatter)
		self.addHandler(log_file_handler)
>>>>>>> firwst
