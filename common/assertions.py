import operator
import os.path
import jsonpath
import allure
from common.recordlog import logs
from common.connection import ConnectMysql
import json
import copy

class Assertions:
    """
    接口断言封装，
    1、字符串包含    2、结果相等包含
    3、结果不相等断言
    4、断言接口返回值里面任意一个值
    5、数据库断言
    """

    def contains_assert(self,value,response,status_code):
        """
        :param value: 预期结果，yaml文件的的对应key的value值
        :param response: 实际的返回结果
        :param status_code:状态码
        :return:
        """
        flag = 0
        for assert_key,assert_value in value.items():
            #print(assert_key,assert_value)
            if assert_key == 'status_code':
                if assert_value != status_code:
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{status_code}", '响应代码断言结果:失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    logs.error("contains断言失败，接口返回码【%s】不等于【%s]" % (status_code,assert_value))
                    flag += 1
                else:
                    logs.info(f'包含断言成功，接口实际返回状态码为：{assert_value},预期返回状态码为:{status_code}')
            else:
                resp_list = jsonpath.jsonpath(response,'$..%s' % assert_key)
                if isinstance(resp_list[0],str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    if assert_value in resp_list:
                        logs.info(f"包含断言成功，接口实际返回结果为：{assert_value},预期结果为:{value}")
                    else:
                        flag += 1
                        logs.error(f'包含断言失败，接口实际返回结果为：{assert_value},预期结果为：{value}')
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应代码断言结果:失败',
                                      attachment_type=allure.attachment_type.TEXT)
        return flag

    def equal_assert(self,value,response,status_code):
        """
        相等断言模式
        :param value: 预期结果，yaml文件validation的参数，要为字典类型
        :param response: 实际结果
        :status_code 实际的请求状态码
        :return:
        """
        flag = 0
        res_list = []
        response_eq = copy.deepcopy(response)

        for assert_key,assert_value in value.items():
            #print(assert_key,assert_value)
            if assert_key == 'status_code':
                if assert_value != status_code:
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{status_code}", '响应代码断言结果:失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    logs.error("contains断言失败，接口返回码【%s】不等于【%s]" % (status_code,assert_value))
                    flag += 1
                else:
                    logs.info(f"相等断言成功：接口实际返回结果为：{assert_value},预期结果为:{status_code}")
                    return flag

        if isinstance(value,dict) and isinstance(response_eq,dict):
            for res in response_eq:
                #print(list(value.keys())[0])
                # 如果与断言无效的字段，就放入res_list,后续用于删除，list(value.keys())[0]是获取字典的第一个键
                if list(value.keys())[0] != res:
                    res_list.append(res)
            for rl in res_list:
                del response_eq[rl]
            print(f'实际结果为:{response_eq}')
            eq_assert = operator.eq(response_eq,value)
            if eq_assert:
                logs.info(f"相等断言成功：接口实际返回结果为：{response_eq},预期结果为:{value}")
            else:
                logs.error(f"相等断言失败，接口实际返回结果为：{response_eq},预期结果为：{value}")
                allure.attach(f"预期结果：{value}\n实际结果：{response_eq}", '响应代码断言结果:失败',
                              attachment_type=allure.attachment_type.TEXT)
                flag += 1
        else:
            flag += 1
        return flag

    # def not_equal_assert(self):
    #     pass

    def assert_mysql(self,expected_sql):
        """
        数据库断言模式
        :param expected_sql: 预期结果，yaml文件的sql语句
        :return:
        """
        flag = 0
        coon = ConnectMysql()

        db_value = coon.query(expected_sql)
        if db_value is not None:
            logs.info('数据库断言成功')
        else:
            flag += 1
            logs.error('数据库断言失败，请检查数据库是否存在该数据')
        return flag

    def assert_result(self,expected,response,status_code):
        """
        :param expected: 预期
        :param response: 实际
        :param status_code: 状态码
        :return:
        """
        all_flag = 0
        try:
            for yq in expected:
                for key,value in yq.items():
                    if key == 'contains':
                        flag = self.contains_assert(value,response,status_code)
                        #print(flag)
                        all_flag += flag
                    elif key == 'eq':
                        flag = self.equal_assert(value,response,status_code)
                        all_flag += flag
                    elif key == 'db':
                        flag = self.assert_mysql(value)

            if all_flag > 0:
                raise AssertionError(f"共有{all_flag}处断言失败，请查看日志")

        except AssertionError as e:
            # 捕获断言异常，记录日志并重新抛出（让测试框架感知）
            logs.error(f"测试失败：{str(e)}")
            allure.attach(str(e), "测试失败", attachment_type=allure.attachment_type.TEXT)
            raise  # 重新抛出异常，确保测试框架标记为失败
        except Exception as e:
            print(e)

if __name__ == '__main__':
    from common.readyaml import get_testcase_yaml

    data = get_testcase_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)),r'testcase/Login','login.yaml'))[0]
    value = data['testCase'][0]['validation']
    #print(value)
    response = {
        'error_code':None,
        'msg':"登录成功",
        'status_code': 200,
        'token':'c5eC47c0DDAE0e31Fa6dE13b4B0be'
    }

    ass = Assertions()
    # for i in value:
    #     for k,v in i.items():
    #         ass.contains_assert(v,response,200)
    ass.equal_assert()
