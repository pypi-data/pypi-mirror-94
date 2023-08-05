# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals

import logging
from pprint import pprint

from weixin_open_api import WeixinOpenClient

weixin_open_api_logger = logging.getLogger("weixin-open-api")
# weixin_open_api_logger.setLevel(logging.DEBUG)
weixin_open_api_logger.addHandler(logging.StreamHandler())


class CustomWeixinOpenClient(WeixinOpenClient):
    appid = 'wxf58226346ab662bf'
    secret = '2a3a0f2d13d42ed79e616f9d0a6da284'


# class WeixinOpenClientTest(unittest.TestCase):
#
#     def testSign(self):
#         pass


if __name__ == '__main__':
    client = CustomWeixinOpenClient()
    ret = client.get_share_params(url='https://www.pjw.cn/download/app')
    pprint(ret)
