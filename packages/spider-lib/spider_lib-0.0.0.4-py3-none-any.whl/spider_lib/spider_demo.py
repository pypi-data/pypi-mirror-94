# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2021 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
基金爬虫示例

Authors: fubo
Date: 2021/02/03 00:00:00
"""

import logging
import time
from typing import List
from pydantic import BaseModel
from bs4 import BeautifulSoup
from spider import Spider, Message


class Fund(BaseModel):
    # 基金名称
    name: str = ""

    # 基金code
    code: str = ""

    # 基金页面
    url: str = ""

    # 基金类型
    fund_type: str = ""

    # 所属公司code
    fund_company_code: str = ""

    # 基金经理codes
    fund_managers_code: List[str] = []

    # 发行日期
    launch_date: str = ""

    # 资产规模
    capital_scale: str = ""

    # 份额规模
    share_scale: str = ""


class SpiderDemo(Spider):
    def __init__(self, max_coroutine_count: int = 200):
        super().__init__(max_coroutine_count=max_coroutine_count)

    async def phase_parse_fund(self, message: Message) -> List:
        """
        解析基金基础信息
        :param message:
        :return:
        """
        return eval(message.parse_page.split("=")[1].strip(" ").strip(";"))

    async def phase_parse_fund_detail(self, message: Message) -> Fund:
        """
        解析基金详细信息
        :param message:
        :return:
        """
        fund = Fund()
        if message.parse_page == "":
            return fund

        soup = BeautifulSoup(message.parse_page, features="html.parser")
        table = soup.select(".info")[0]
        for elem in table.find_all("tr"):
            if elem.th.text.strip(" ") == "发行日期":
                fund.launch_date = elem.td.text.strip(" ").replace("年", "-").replace("月", "-").strip("日")

            if elem.th.text.strip(" ") == "资产规模":
                fund.capital_scale = elem.td.text.strip(" ")
                fund.share_scale = elem.find_all("td")[-1].text.strip(" ")

            if elem.th.text.strip(" ") == "基金管理人":
                fund.fund_company_code = elem.td.a["href"].split("/")[-1].split(".")[0]

            if elem.th.text.strip(" ") == "基金经理人":
                fund.fund_managers_code = [a["href"].split("/")[-1].split(".")[0] for a in elem.td.find_all("a")]
        return fund

    def get_funds(self) -> List[Fund]:
        """
        1、获取基金基本信息
        2、获取基金详情
        :return:
        """
        # 执行基金基本信息
        logging.info("Get basic information of funds")
        results = self.run(
            messages=[
                Message(
                    message_id="funds_basic_" + str(time.time()),
                    request_delay_second=0.0,
                    request_method="phase_request_get", parse_method="phase_parse_fund",
                    request_url="http://fund.eastmoney.com/js/fundcode_search.js"
                )
            ]
        )

        # 获得基本信息
        # 构造基金详细信息message
        funds = []
        messages = []
        for elem in results[0]:
            fund = Fund()
            fund.code = elem[0]
            fund.name = elem[2]
            fund.fund_type = elem[3]
            fund.url = "http://fundf10.eastmoney.com/jbgk_%s.html" % fund.code
            funds.append(fund.copy())

            messages.append(
                Message(
                    message_id="funds_basic_" + str(time.time()),
                    request_delay_second=0.01,
                    request_method="phase_request_get", parse_method="phase_parse_fund_detail",
                    request_url=fund.url
                )
            )

        # 执行获取基金详细信息
        logging.info("Get information of funds")
        results = self.run(messages=messages)
        for index, elem in enumerate(results):
            elem.code = funds[index].code
            elem.name = funds[index].name
            elem.fund_type = funds[index].fund_type
            elem.url = funds[index].url
            funds[index] = elem.copy()

        return funds


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    )
    data_file = "funds.jsonl"
    spider_demo = SpiderDemo(max_coroutine_count=30)
    spider_demo.save_to_jsonl(spider_demo.get_funds(), data_file)


if __name__ == '__main__':
    main()