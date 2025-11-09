# -*- coding: utf-8 -*-
import json

import allure
import pytest
import requests
from common.recordlog import logs
from requests import cookies
from common.readyaml import ReadYamlData

class SendRequests(object):
    def __init__(self):
        self.read = ReadYamlData()

    #封装请求的方法
    def send_request(self,**kwargs):
        cookie = {}
        session = requests.session()
        result = None
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                #写入cookie到extract文件
                self.read.write_yaml_data(cookie)
                logs.info(f'cookie:{cookie}')
            logs.info(f'接口的实际返回信息:{result.text}')
        except requests.exceptions.ConnectionError:
            logs.error("接口连接服务器异常")
            pytest.fail("接口连接服务器异常")
        except requests.exceptions.HTTPError:
            logs.error("http异常")
            pytest.fail("http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("e")
        return result

    #组合封装   调用的主方法
    def run_main(self,name,url,case_name,headers,method,cookies=None,file=None,**kwargs):
        logs.info(f'接口名称：{name}')
        logs.info(f'接口请求地址：{url}')
        logs.info(f'请求方法：{method}')
        logs.info(f'测试用例名称：{case_name}')
        logs.info(f'请求头：{headers}')
        logs.info(f'Cookies：{cookies}')
        #print(kwargs)
        req_params = json.dumps(kwargs,ensure_ascii=False)
        #print(req_params)   #req_params 是请求参数，是一个动态变量
        try:
            if 'data' in kwargs.keys():
                #print(kwargs)
                logs.info("请求参数：%s" % kwargs)
                allure.attach(str(req_params), f'请求头：{req_params}', attachment_type=allure.attachment_type.TEXT)
            elif 'json' in kwargs.keys():
                #print(kwargs)
                logs.info(f"请求参数：{kwargs}")
                allure.attach(str(req_params), f'请求头：{req_params}', attachment_type=allure.attachment_type.TEXT)
            elif 'params' in kwargs.keys():
                logs.info(f"请求参数：{kwargs}")
                allure.attach(str(req_params), f'请求头：{req_params}', attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            logs.info(e)
        response = self.send_request(method=method,url=url,headers=headers,cookies=cookies,files=file,
                                     verify=False,**kwargs)
        return response

if __name__ == "__main__":
    url = "http://127.0.0.1:8787/dar/user/login"
    data = {'user_name': 'test01', 'passwd': 'admin123'}
    header = None
    method = "post"
    send = SendRequests()
    res = send.run_main(url=url,data=data,method=method,headers=header)
    print(res)