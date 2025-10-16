import os
import random
from common.readyaml import ReadYamlData
import time
class DebugTalk:
    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self,data,randoms):
        if randoms not in [0,-1,-2]:
            return data[randoms - 1]


    #读取接口yaml文件数据
    def get_extract_data(self,node_name,randoms=None):
        """
        :param node_name: extract.yaml 的 key值
        :param random: 读取数据的方式，随机或者全部或者列表
        :return:
        """
        #print(node_name)
        #print("当前工作目录:", os.getcwd())
        data = self.read.get_extract_yaml(node_name)
        #print(data)
        if randoms is not None:
            randoms = int(randoms)
            # 0 随机一个数据，-1，获取全部数据，-2获取数据列表
            data_value = {
                randoms:self.get_extract_order_data(data,randoms),
                0:random.choice(data),
                -1:','.join(data),
                -2:','.join(data).split(',')
            }
            data = data_value[randoms]
        return data

    def md5_params(self,params):
        pass

    def timestamp(self):
        """获取当前时间戳，10位"""
        t = int(time.time())
        return t
if __name__ == '__main__':
    debug = DebugTalk()
    data = debug.get_extract_data('goodsId',-1)
    print(data)
    print(type(data))
