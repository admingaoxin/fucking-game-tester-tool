"""
@Filename:   commons/session
@Author:      北凡
@Time:        2023/5/12 22:11
@Describe:    ...
"""
import logging

import requests
from commons import settings

logger = logging.getLogger("session")


class BeifanSession(requests.Session):
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> requests.Response:
        # 记录请求

        if not url.startswith("http"):
            logger.warning("使用的不是绝对URL地址，需要补全base_url")
            url = settings.base_url + url

        logger.info(f"请求方法: {method}")
        logger.info(f"接口地址: {url}")
        logger.info(f"params: {params or self.params}")
        logger.info(f"请求头: {headers}")
        logger.info(f"cookies: {cookies or self.cookies}")
        logger.info("请求正文:")
        logger.info(f"json: {json}")
        logger.info(f"data: {data}")
        logger.info(f"files: {files}")

        if files:
            for k, v in files.items():
                files[k] = open(v, "rb")

        resp = super().request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )

        # 记录响应

        logger.info(f"状态码：{resp.status_code}")
        logger.info(f"响应头：{resp.headers}")
        logger.info(f"响应正文：{resp.text}")

        # 返回接口响应结果

        return resp
