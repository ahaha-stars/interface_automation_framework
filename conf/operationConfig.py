import configparser
from conf.setting import FILE_PATH

# 获取config.ini里的基础数据，包含基础接口地址，mysql数据库的连接等信息
class OperationConfig:

    def __init__(self,file_path = None):
        if file_path is None:
            self.__file_path = FILE_PATH['conf']
        else:
            self.__file_path = file_path
        # 初始化对象 可以调用这个对象的函数
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__file_path,encoding='utf-8')
        except Exception as e:
            print(e)

    def get_section_for_data(self,section,option):
        """
        :param section:  ini 头部值
        :param option:  选项值的key
        :return:
        """
        try:
            data = self.conf.get(section, option)
            return data
        except Exception as e:
            print(e)

    #获取config.ini中的api_envi,option 是对应的key
    def get_envi(self,option):
        return self.get_section_for_data('api_envi',option)
    #获取config.ini中的
    def get_mysql_conf(self,option):
        return self.get_section_for_data('MYSQL',option)



if __name__ == '__main__':
    oper = OperationConfig()
    print(oper.get_envi('host'))
    print(oper.get_mysql_conf('host'))

