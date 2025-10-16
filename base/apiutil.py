import json
import re
from tokenize import cookie_re
from json.decoder import JSONDecodeError
import jsonpath
from common.recordlog import logs
import allure

from common.debugtalk import DebugTalk
from common.readyaml import ReadYamlData,get_testcase_yaml
from conf.operationConfig import OperationConfig
from common.sendrequests import SendRequests
from common.assertions import Assertions

assert_res = Assertions()
class BaseRequest:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()
        self.send = SendRequests()

    def replace_load(self,data):
        """
        yaml文件解析带有${}格式的数据
        :return:
        """
        str_data = data
        #print(str_data)
        if not isinstance(data,str):  # 如果不是字符串类型，则转换字符串类型
            str_data = json.dumps(data,ensure_ascii=False)

        for i in range(str_data.count("${")):
            if "${" in str_data and "}" in str_data:
                #获取字段前后坐标，截取数据
                start_index = str_data.index("$")
                end_index = str_data.index("}",start_index)
                #print(start_index,end_index)
                #截取字段
                ref_all_params = str_data[start_index:end_index+1]
                #获取函数名
                func_name = ref_all_params[2:ref_all_params.index("(")]
                print(func_name)
                #获取参数
                parmas = ref_all_params[ref_all_params.index("(")+1:ref_all_params.index(")")]
                # print(func_name)
                # print(parmas)
                print("解析前数据:",str_data)
                # 在DebugTalk中的function_name的函数，填入parmas参数
                extract_data = getattr(DebugTalk(),func_name)(*parmas.split(',') if parmas else "")
                str_data = str_data.replace(ref_all_params,str(extract_data))
                print("解析后数据:",str_data)

        #还原数据类型（dict or list)
        if data and isinstance(data,dict):
            data = json.loads(str_data)
        else:
            data = str_data
        # print(data)
        # print(type(data))
        return data

    def specification_yaml(self,base_info,test_case):

        """
        规范yaml接口测试数据的写法
        :param case_info: 用例的信息
        :return:
        """
        res = None
        cookie = None
        params_type = ['params','data','json']
        try:
            base_url = self.conf.get_envi('host')
            #print(base_url)
            url = base_url + base_info['url']
            allure.attach(url+f'接口地址:{url}')
            api_name = base_info['api_name']
            allure.attach(api_name,f'接口名称：{api_name}')
            method = base_info['method']
            allure.attach(method, f'接口方法：{method}')
            # 某些yaml文件中headers可能需要提取数据，（例如login.yaml)
            headers = self.replace_load(base_info['header'])
            allure.attach(str(headers), f'请求头：{headers}',attachment_type=allure.attachment_type.TEXT)
            # try:
            #     cookie = self.replace_load(case_info['baseInfo']['cookies'])
            # except:
            #     pass
            #print(headers)

            # 处理cookie,如果yaml文件中有cookies关键字，尝试解析
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_load(base_info['cookies']))

            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)

            #提取断言（如果需要则要解析）
            val = self.replace_load(test_case.get("validation"))
            test_case['validation'] = val
            validation = eval(test_case.pop('validation'))
            #处理参数提取
            extract = test_case.pop('extract',None)
            #print(extract)
            extract_list = test_case.pop('extract_list',None)
            #（解析）获取请求参数
            for key,value in test_case.items():
                if key in params_type:
                    test_case[key] = self.replace_load(value)
                    #print(test_case[key])


                # 处理文件接口
            file,files = test_case.pop('files',None),None
            if file is not None:
                for f_key,f_value in file.items():
                    allure.attach(json.dumps(file),'导入文件')
                    files = {f_key:open(f_value,mode = 'rb')}

            res = self.send.run_main(name=api_name,url=url,case_name=case_name,headers=headers,
                                     method=method,file=files,cookies=cookie,**test_case)
            #allure.attach(self.allure_attach_response(res.json()), '接口响应信息', allure.attachment_type.TEXT)
            #print(res.text)
            try:
                res_json = json.loads(res.text)
                if extract is not None:
                    self.extract_data(extract,res.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list,res.text)
                # 处理接口断言
                assert_res.assert_result(validation, res_json, res.status_code)
            except JSONDecodeError as js:
                logs.error('系统异常或接口未请求！')
                raise js
            except Exception as e:
                logs.error(e)
                raise e

        except Exception as e:
            #logs(e)
            raise e

    #提取extract的列表数据


    def extract_data_list(self,testcase_extract_list,response):
        """
            提取接口的返回值，支持正则表达式和json提取器
            :param testcase_extarct: testcase文件yaml中的extract值
            :param response: 接口的实际返回值
            :return:
            """
        pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
        try:
            for key,value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    #re.S  可以跨越换行符匹配  如果匹配内容在多行，即有换行，用了‘.’  就加 re.S
                    ext_list = re.findall(value,response,re.S)
                    if ext_list:
                        extract_data = {key:ext_list}
                        logs.info("正则提取到的参数：%s" % extract_data)
                        self.read.write_yaml_data(extract_data)
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response),value)
                    if ext_json:
                        extract_data = {key:ext_json}
                    else:
                        extract_data = {key:"未提取到数据，接口返回结果可能为空"}
                    logs.info("json提取到参数：%s" % extract_data)
                    self.read.write_yaml_data(extract_data)
        except:
            logs.error("接口返回值提取异常，请检查yaml文件extract_list的表达式是否正确")


    #提取extract数据
    def extract_data(self,testcase_extract,response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        #print(testcase_extract)
        pattern_list = ['(.+?)','(.*?)',r'(\d+)',r'(\d*)']  # 正则提取
        try:
            for key,value in testcase_extract.items():
                #print(key,value)
                for pat in pattern_list:
                    if pat in value:
                        #print(pat)
                        #使用 value 作为正则表达式，在 response 字符串中进行搜索，寻找第一个匹配的内容。
                        ext_list = re.search(value,response)
                        if pat in [r'(\d+)',r'(\d*)']:
                            extract_data = {key:int(ext_list.group(1))}
                        else:
                            extract_data = {key:ext_list.group(1)}
                        logs.info(f"正则表达式提取到的参数：{extract_data}")
                        self.read.write_yaml_data(extract_data)

            #json提取器
                if '$' in value:
                    # 若是yaml文件的问题，即value有问题，会被except
                    ext_json = jsonpath.jsonpath(json.loads(response),value)[0]
                    if ext_json: # 如果接口返回数据是正常的
                        extract_data = {key:ext_json}
                        #logs.info(f"json提取到的数据为：{extract_data}")
                    else:  # 如果接口返回是错误的
                        extract_data = {key:"未提取到数据，接口返回值可能为空！"}
                        logs.error({key:"未提取到数据，接口返回值可能为空！"})
                        #print(extract_data)
                    logs.info(f"json提取到的数据为：{extract_data}")
                    self.read.write_yaml_data(extract_data)
        except:
            logs.error("接口提取数据异常，请检查yaml文件")


if __name__ == '__main__':
    # print(data)
    # print(type(data))
    base = BaseRequest()
    #data = get_testcase_yaml('../testcase/SingleInterface/addUser.yaml')
    data = get_testcase_yaml('../testcase/Login/loginName.yaml')
    base_info = data[0][0]
    print(base_info)
    testcase = data[0][1]
    #print(testcase)
    base.specification_yaml(base_info,testcase)
    data2 = get_testcase_yaml('../testcase/SingleInterface/addUser.yaml')
    base_info1 = data2[0][0]
    testcase1 = data2[0][1]
    base.specification_yaml(base_info1,testcase1)

