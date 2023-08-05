# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2021 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
定向爬虫

Authors: fubo
Date: 2021/02/03 00:00:00
"""

import json
import time
import random
import logging
from typing import Dict, Any, List
from pydantic import BaseModel
import requests_async as requests
import asyncio
import tqdm


class Message(BaseModel):
    # message ID
    message_id: str = ""

    # 页面请求处理的函数名称
    request_method: str = "phase_request_get"

    # url
    request_url: str = ""

    # url请求时等待时间
    request_delay_second: float = 0.02

    # url请求重试的等待事件
    request_retry_delay_seconds: float = 60

    # url请求重试的次数
    request_retry_times: int = 3

    # params
    request_params: Dict = {}

    # headers
    request_headers: Dict = {}

    # data
    request_data: str = ""

    # parse等待时间
    parse_delay_second: float = 0.0

    # parse重试的等待事件
    parse_retry_delay_seconds: float = 60

    # parse重试的次数
    parse_retry_times: int = 3

    # 页面解析函数名称
    parse_method: str = ""

    # 页面解析page
    parse_page: str = ""


class ProcessFunc(BaseModel):
    # URL页面请求函数
    request_func: Any = None

    # 页面解析函数
    parse_func: Any = None


class Spider(object):
    def __init__(self, max_coroutine_count: int = 200):
        self.sem = asyncio.Semaphore(max_coroutine_count)

    def random_sleep_time(self, standard_sleep_time: float = 0.02):
        """

        :param stard_sleep_time:
        :return:
        """
        second = standard_sleep_time + (random.random() - 0.5) * 0.01
        return second if second > 0 else 0.01

    def random_user_agents(self) -> str:
        """
        随机获取一个user agent
        :return:
        """
        return random.choice(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 7.0; wv) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/10.3 "
                "SearchCraft/2.6.2 (Baidu; P1 7.0)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 "
                "(KHTML, like Gecko) Version/12.0 Safari/605.1.15",
                "Mozilla/5.0 (Linux; Android 10; SEA-AL10 Build/HUAWEISEA-AL10; wv) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 "
                "Mobile Safari/537.36 T7/11.22 SP-engine/2.18.0 baiduboxapp/11.22.5.10 (Baidu; P1 10)",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 "
                "(KHTML, like Gecko) Mobile/12H321 MicroMessenger/6.3.9 NetType/WIFI Language/zh_CN",
                "Mozilla/5.0 (Linux; Android 5.1; m2 note Build/LMY47D) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.2 TBS/036215 Safari/537.36 "
                "MicroMessenger/6.3.18.800 NetType/WIFI Language/zh_CN",
                "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 "
                "(KHTML, like Gecko) CriOS/31.0.1650.18 Mobile/11B554a Safari/8536.25",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 "
                "(KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4",
                "Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; M351 Build/KTU84P) "
                "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
                "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
                "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
                "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
                "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
                "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
                "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
                "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
                "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
                "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
                "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]
        )

    async def __request_get_url_status_code(self, index: int, info: Message) -> (int, int):
        """
        测试url的status_code
        :param info:
        :return:
        """
        request_headers = {
            'User-Agent': self.random_user_agents()
        }
        request_params = {}

        if info.request_headers is not None:
            request_headers.update(info.request_headers)

        if info.request_params is not None:
            request_params.update(info.request_params)

        async with self.sem:
            count = info.request_retry_times
            while count > 0:
                try:
                    time.sleep(self.random_sleep_time(info.request_delay_second))
                    response = await requests.get(url=info.request_url, params=request_params, headers=request_headers)
                    response.encoding = "utf-8"
                    if count < info.request_retry_times:
                        logging.info("Got data at times %d from url %s" % (count, info.request_url))
                    return index, int(response.status_code)
                except Exception as exp:
                    logging.warning(
                        "Failed to request url at times=%d [%s] wait for %f seconds" % (
                            count, exp, info.request_retry_delay_seconds
                        )
                    )
                    count = count - 1
                    time.sleep(info.request_retry_delay_seconds)

            raise ConnectionError("Failed to request url %s" % info.request_url)

    async def phase_request_get(self, info: Message) -> str:
        """
        HTTP GET请求
        :param info: URL
        :return:
        """
        request_headers = {
            'User-Agent': self.random_user_agents()
        }
        request_params = {}

        if info.request_headers is not None:
            request_headers.update(info.request_headers)

        if info.request_params is not None:
            request_params.update(info.request_params)
        try:
            response = await requests.get(url=info.request_url, params=request_params, headers=request_headers)
            response.encoding = "utf-8"
            if response.status_code != 200:
                raise IOError("Status code error %d" % response.status_code)
        except Exception as exp:
            raise ConnectionAbortedError("Failed to crawl url %s [%s]" % (info.request_url, exp))

        return response.text

    async def phase_parse_empty(self, info: Message) -> Dict:
        """
        解析页面(示例)
        """
        return {"page": info.parse_page}

    async def __select_strategy(self, message: Message) -> ProcessFunc:
        """
        选择策略
        """
        request_strategies = set(
            filter(
                lambda fun_name: "phase_request_" in fun_name and fun_name.index("phase_request_") == 0, dir(self)
            )
        )
        parse_strategies = set(
            filter(
                lambda fun_name: "phase_parse_" in fun_name and fun_name.index("phase_parse_") == 0, dir(self)
            )
        )
        funcs = ProcessFunc()
        if message.request_method in request_strategies:
            funcs.request_func = eval("self." + message.request_method)

        if message.parse_method in parse_strategies:
            funcs.parse_func = eval("self." + message.parse_method)

        return funcs

    async def __run_request(self, funcs: ProcessFunc, message: Message) -> Message:
        """
        执行request操作
        :param funcs:
        :param message:
        :return:
        """
        logging.debug(
            "Run request message_id=%s url=%s method=%s headers=%s, params=%s data=%s" % (
                message.message_id, message.request_url, message.request_method,
                message.request_headers, message.request_params, message.request_data
            )
        )
        if funcs.request_func is None:
            return message

        count = message.request_retry_times
        while count > 0:
            try:
                message.parse_page = await funcs.request_func(message)
                if count < message.request_retry_times:
                    logging.info("Got data at times %d from url %s" % (count, message.request_url))
                return message
            except Exception as exp:
                logging.warning(
                    "Failed to request url at times=%d [%s] wait for %f seconds" % (
                        count, exp, message.request_retry_delay_seconds
                    )
                )
                time.sleep(message.request_retry_delay_seconds)
            count = count - 1

        raise ConnectionError("Failed to request url %s" % message.request_url)

    async def __run_parse(self, funcs: ProcessFunc, message: Message) -> Any:
        """
        执行request操作
        :param funcs:
        :param message:
        :return:
        """
        logging.debug(
            "Run parse message_id=%s data=[\"%s...\" ] method=%s" % (
                message.message_id, message.parse_page[:100], message.parse_method
            )
        )
        if funcs.parse_func is None:
            return {}
        count = message.parse_retry_times
        while count > 0:
            try:
                output = await funcs.parse_func(message)
                if count < message.request_retry_times:
                    logging.info("Parsed data at times %d in %s" % (count, message.parse_page))
                return output
            except Exception as exp:
                logging.warning(
                    "Failed to parse at times=%d [%s] wait for %f seconds" % (
                        count, exp, message.parse_retry_delay_seconds
                    )
                )
                time.sleep(message.parse_retry_delay_seconds)
            count = count - 1

        raise ValueError("Failed to parse message %s" % message.parse_page)

    async def __run_message(self, index: int, message: Message) -> Any:
        """
        1、选择处理策略
        1、获取页面数据，
        2、解析页面数据，抽取变量
        """
        async with self.sem:
            logging.debug("[S1] Select strategies by input message message_id=%s" % message.message_id)
            funcs = await self.__select_strategy(message=message)

            logging.debug("[S2] Run request step message_id=%s" % message.message_id)
            time.sleep(self.random_sleep_time(message.request_delay_second))
            message = await self.__run_request(funcs=funcs, message=message)

            logging.debug("[S3] Run parse step message_id=%s" % message.message_id)
            time.sleep(self.random_sleep_time(message.parse_delay_second))
            data = await self.__run_parse(funcs=funcs, message=message)

        return index, data

    async def __equip_messages_progress_bar(self, messages: List[Message]) -> List[Any]:
        """
        messages请求添加progress bar
        :param messages:
        :return:
        """
        results = []
        output = [0] * len(messages)
        tasks = [self.__run_message(index=index, message=message) for index, message in enumerate(messages)]
        for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            results.append(await task)

        for result in results:
            output[result[0]] = result[1]
        return output

    async def __equip_urls_status_code_progress_bar(self, messages: List[Message]) -> List[Any]:
        """
        url状态码获取添加progress bar
        :param messages:
        :return:
        """
        results = []
        output = [0] * len(messages)
        tasks = [
            self.__request_get_url_status_code(index=index, info=message) for index, message in enumerate(messages)
        ]
        for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            results.append(await task)

        for result in results:
            output[result[0]] = result[1]
        return output

    def run(self, messages: List[Message]) -> List[Any]:
        """
        批量执行message
        :param messages:
        :return:
        """
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__equip_messages_progress_bar(messages=messages))
        loop.run_until_complete(task)
        return task.result()

    def run_without_progress_bar(self, messages: List[Message]) -> List[Any]:
        """
        批量执行message 不需要进度条
        :param messages:
        :return:
        """
        loop = asyncio.get_event_loop()
        tasks = [
            asyncio.ensure_future(
                self.__run_message(index=index, message=message)
            ) for index, message in enumerate(messages)
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        return [task.result()[1] for task in tasks]

    def run_urls_status_code(self, messages: List[Message]) -> List[int]:
        """
        获取status_code
        :param messages:
        :return:
        """
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__equip_urls_status_code_progress_bar(messages=messages))
        loop.run_until_complete(task)
        return task.result()

    def save_to_jsonl(self, data: List[BaseModel], file_name: str):
        with open(file_name, "w") as fp:
            fp.write("\n".join([json.dumps(d.dict(), ensure_ascii=False) for d in data]))
