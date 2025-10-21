import os.path
import yaml

from common.recordlog import logs
#from common.sendrequests import SendRequests
#from common.sendrequests import SendRequests
from conf.setting import FILE_PATH


def get_testcase_yaml(file):
    """
    :param file: yaml文件路径
    :return:
    """
    testcase_list = []
    try:
        with open(file,'r',encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # 当yaml只有一个测试用例，或者同一接口的不同结果的测试用例时，均在一个字典内，长度为1
            ## 1，只有一个用例，     2，同一接口但多种返回结果
            if len(data) <= 1:
                yaml_data = data[0]
                base_info = yaml_data.get('baseInfo')
                for ts in yaml_data.get('testCase'):
                    #两个元素，到时分配到 @pytest.mark.parametrize的baseinfo,testcase
                    param = [base_info,ts]
                    #print(param)
                    testcase_list.append(param)
                    #print(testcase_list)
                return testcase_list
            else:
                # 适用于yaml文件里有多个不同的接口测试用例，（如一系列的业务功能放在同一yaml文件中）
                return data

    except Exception as e:
        print(e)

class ReadYamlData:
    def __init__(self,yaml_file = None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = '../testcase/Login/login.yaml'


    #向extract.yaml写入数据
    def write_yaml_data(self,value):

        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path):
            os.system(file_path)
        #写入文件
        file = open(file_path,'a',encoding='utf-8')
        try:
            if isinstance(value,dict):
                write_data =  yaml.dump(value,allow_unicode=True,sort_keys=False)
                file.write(write_data)
            else:
                print("写入到[extract.yaml]数据类型必须为字典类型")
        except Exception as e:
            print(e)
        finally:
            file.close()

    #清楚yaml文件数据，每次运行脚本前执行
    def clear_yaml_data(self):
        with open(FILE_PATH['extract'],'w') as f:
            f.truncate()


    #获取yaml文件中的字符串
    def get_extract_yaml(self,node_name):
        file_path = FILE_PATH['extract']
        #print(file_path)
        #print(os.path.exists('../extract.yaml'))
        if os.path.exists(FILE_PATH['extract']):
            pass
        else:
            logs.error('extract.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            logs.info('extract.yaml创建成功！')
        with open(FILE_PATH['extract'], 'r', encoding='utf-8') as f:
            extract_data = yaml.safe_load(f)
            return extract_data[node_name]



if __name__ == '__main__':
    #print("当前工作目录：", os.getcwd())
    res = get_testcase_yaml("../testcase/Login/login.yaml")
    #res = get_testcase_yaml("../testcase/SingleInterface/addUser.yaml")
    print(res)