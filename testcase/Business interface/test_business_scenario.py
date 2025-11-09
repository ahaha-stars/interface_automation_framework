import allure
import pytest

from common.readyaml import get_testcase_yaml
from base.apiutil import BaseRequest
from base.generateId import model_id, case_id


# 注意：业务场景的接口测试要调用base目录下的apiutil_business文件

@allure.feature(next(model_id) + '电子商务管理系统（业务场景）')
class TestEBusinessScenario:

    @allure.story(next(case_id) + '商品列表到下单支付流程')
    @pytest.mark.parametrize('case_info', get_testcase_yaml('./testcase/Business interface/BusinessScenario.yaml'))
    def test_business_scenario(self, case_info):
        allure.dynamic.title(case_info['baseInfo']['api_name'])
        BaseRequest().specification_business_yaml(case_info)
