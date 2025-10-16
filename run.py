import os
import pytest
import shutil

if __name__ == '__main__':
    #注释
    pytest.main(['-vs','./testcase','--alluredir=./report/temp','--clean-alluredir'])
    shutil.copy('./environment.xml','./report/temp')
    os.system(f'allure serve ./report/temp')
