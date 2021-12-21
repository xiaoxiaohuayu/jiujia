# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12
# @Author  : MashiroF
# @File    : HT_config.py
# @Software: PyCharm

#################################### 以下配置可更改 #########################################
## 云函数/青龙面板 环境变量优先级  >  配置文件 `HT_config` 变量优先级
# 通知黑名单
# 环境变量名:notifyBlack,多个以`&`隔开
# notifyBlackList = ['TimingCash','']

###########################################################################################




####################################### 以下配置不要动 #######################################
# 导入系统内置包
# import os
# import sys
import logging


# 读取通知黑名单以及转盘抽奖环境变量
# if "Lottery" in os.environ:
#     Lottery = os.environ["Lottery"]
# if "notifyBlack" in os.environ:
#     notifyBlack = os.environ["notifyBlack"]

# 日志模块
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(message)s")

# 日志输出流
stream = logging.StreamHandler()
stream.setFormatter(logFormat)
logger.addHandler(stream)

###########################################################################################
