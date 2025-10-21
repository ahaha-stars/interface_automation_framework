import allure
import pytest

from base.apiutil import BaseRequest
from base.generateId import model_id, case_id
from common.readyaml import get_testcase_yaml


@allure.feature(next(model_id) + "物流管理")
class TestLogistics:
    @allure.story(next(case_id) + "下单物料信息")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml('./testcase/Logistics/getMaterial.yaml'))
    def test_get_material(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)

    @allure.story(next(case_id) + "货主（托运人）下订单")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml('./testcase/Logistics/shipperOrder.yaml'))
    def test_shipper_order(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)

    @allure.story(next(case_id) + "集团接收货主订单")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml('./testcase/Logistics/masterReceive.yaml'))
    def test_master_receive(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)

    @allure.story(next(case_id) + "集团分配订单给物流公司")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml('./testcase/Logistics/orderAssign.yaml'))
    def test_order_assign(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)

    @allure.story(next(case_id) + "物流公司接单")
    @pytest.mark.run(order=5)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml('./testcase/Logistics/transReceive.yaml'))
    def test_trans_receive(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)

    @allure.story(next(case_id) + "物流公司拆分订单")
    @pytest.mark.run(order=6)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml('./testcase/Logistics/handSplitOrder.yaml'))
    def test_hand_split_order(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)

    @allure.story(next(case_id) + "物流公司调度派车")
    @pytest.mark.run(order=7)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml('./testcase/Logistics/handCapacityDispatch.yaml'))
    def test_hand_capacity_dispatch(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)