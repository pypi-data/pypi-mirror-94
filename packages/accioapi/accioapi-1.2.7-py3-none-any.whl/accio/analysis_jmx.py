#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : analysis_jmx.py
@Time    : 2020/11/25 16:46
@Author  : Yu Tao
@Software: PyCharm
"""
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from accio import parse_tools
import sys


class Jxm(object):

    def source(self, jmx_content):
        """
        生成测试用例
        :param jmx_content:
        :return:
        """
        try:
            swagger_json, path_list = self.format_data(jmx_content=jmx_content)
            parse_tools.Parse.tmp(swagger_json, 'a')
            parse_tools.Parse.tmp_create_case()
            return path_list
        except Exception as ex:
            print('获取jmx文件数据失败！')
            print(ex)
            sys.exit()

    def format_data(self, jmx_content):
        """
        格式化数据，使其满足“用例生成”的调用要求
        :param jmx_content: 读出的jmx文件数据
        :return:
        """
        root = ET.fromstring(jmx_content)
        template_data = {"swagger": "2.0"}
        template_data.update({"basePath": ""})
        template_data.update({"paths": {}})
        path_list = []
        for HTTPSamplerProxy in root.iter("HTTPSamplerProxy"):
            consumes = []
            parameters = []
            for elementProp in HTTPSamplerProxy.iter("elementProp"):
                if elementProp.attrib.get("elementType") == "HTTPArgument":
                    name = elementProp.attrib.get("name")
                    parameters.append({"name": name, "in":"body"})
            for stringProp in HTTPSamplerProxy.iter("stringProp"):
                print(stringProp.tag, ":", stringProp.attrib)
                if stringProp.attrib['name'] == 'HTTPSampler.path' and stringProp.text is not None:
                    url = stringProp.text
                    path = urlparse(url).path
                    path_list.append(path)
                if stringProp.attrib['name'] == 'HTTPSampler.method' and stringProp.text is not None:
                    method = stringProp.text.lower()
            template_data["paths"].update({path: {}})
            template_data["paths"][path].update({method: {"parameters": parameters, "consumes": consumes}})
        return template_data, path_list


# if __name__ == '__main__':
#     with open('D:/yt/2message_api.jmx', 'r',encoding='utf-8') as f:
#         # print(f.read())
#         file_content = f.read()
#         Jxm().source(jmx_content=file_content)



