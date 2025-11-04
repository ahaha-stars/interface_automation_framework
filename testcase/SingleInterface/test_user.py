import pytest
from base.generateId import model_id,case_id
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.sendrequests import SendRequests
from base.apiutil import BaseRequest
import allure

@allure.feature(next(model_id) + '用户功能接口')
class TestUserManger:
    @allure.story(next(case_id) + "新增用户")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase',get_testcase_yaml('./testcase/SingleInterface/addUser.yaml'))
    #@pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./addUser.yaml'))
    def test_add_user(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info,testcase)

    @allure.story(next(case_id) + "修改用户")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/SingleInterface/queryUser.yaml"))
    def test_update_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)
    #
    @allure.story(next(case_id) + "删除用户")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/SingleInterface/deleteUser.yaml"))
    def test_delete_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)