import os
import pytest
import shutil

if __name__ == '__main__':
    pytest.main(['-vs','./testcase','--alluredir=./report/temp',
                 '--clean-alluredir'])
    shutil.copy('./environment.xml','./report/temp')
    #启动allure服务命令，Jenkins服务时要关闭
    #os.system(f'allure serve ./report/temp')
