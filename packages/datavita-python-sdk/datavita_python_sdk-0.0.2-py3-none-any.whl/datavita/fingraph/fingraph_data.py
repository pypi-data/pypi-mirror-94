#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : fingraph_data.py
    @desc :
"""
import typing

import pandas as pd

from datavita.core.auth import Auth
from datavita.core.common import contants
from datavita.core.transport.comrequests import CommonRequests
from datavita.core.transport.http import Request
from datavita.core.utils import log
from datavita.core.utils.middleware import Middleware
from datavita.fingraph.fingraph_apis import fingraph_apis_dict


class FingraphData:
    """
        中台数据
        初始化固定参数 auth 超时 最大重试次数
    """

    def __init__(
            self,
            auth: typing.Optional[Auth] = None,
            base_url: str = contants.BASE_URL,
            timeout: int = contants.SESSION_PERIOD_TIMEOUT,
            max_retries: int = contants.MAX_RETRIES,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.auth = auth
        middleware = Middleware()
        self._middleware = middleware
        self.logger = log.default_logger

    def _send(self, api_name, action, api, params, max_retries, timeout):
        try:
            req = self._build_http_request(api_name, action, api, params=params)
            resp = CommonRequests(auth=self.auth, max_retries=max_retries, timeout=timeout).send(req=req)
        except Exception as e:
            return pd.DataFrame()
            raise e
        return self._middleware.logged_response_df_handler(self.auth, resp, resp.request.request_name)

    def _build_http_request(self, api_name, action, api, params) -> Request:
        headers = {
            'Authorization': '{}'.format(self.auth.make_authorization()),
            'content-type': 'application/json'
        }
        return Request(
            request_name=api_name,
            url=api,
            method=action.upper(),
            data=params,
            headers=headers
        )

    def get_fingraph_data_by_group_id(self, group_id: str) -> pd.DataFrame:
        """
            根据图谱组获取datacode数据 get_fingraph_data_by_group_id()
        :param group_id: 图谱组代码
        :return:
        """
        url = fingraph_apis_dict.get('get_fingraph_data_by_group_id').format(base_url=self.base_url,
                                                                             group_id=str(group_id))
        return self._send(api_name="根据图谱组获取数据", action='get', api=url, params=None, max_retries=self.max_retries,
                          timeout=self.timeout)
