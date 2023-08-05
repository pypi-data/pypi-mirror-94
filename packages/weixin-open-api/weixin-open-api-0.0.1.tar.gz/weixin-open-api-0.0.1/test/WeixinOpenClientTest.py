# -*- coding: utf-8 -*-
import unittest
from pprint import pprint

from weixin_open_api.weixin_open_client import WeixinOpenClient
import logging

weixin_open_api_logger = logging.getLogger("weixin-open-api")
weixin_open_api_logger.setLevel(logging.DEBUG)
weixin_open_api_logger.addHandler(logging.StreamHandler())


class CustomWeixinOpenClient(WeixinOpenClient):
    appid = 'wxf58226346ab662bf'
    secret = '2a3a0f2d13d42ed79e616f9d0a6da284'


class WeixinOpenClientTest(unittest.TestCase):

    def testSign(self):
        client = CustomWeixinOpenClient()
        ret = client.get_share_params(url='https://www.pjw.cn/download/app')
        pprint(ret)
