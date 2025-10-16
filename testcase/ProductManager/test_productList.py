import allure
import  pytest

from base.apiutil import BaseRequest
from common.readyaml import ReadYamlData, get_testcase_yaml


@allure.feature("商品管理")
class TestGetProduct:
    @allure.story("商品管理")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("base_info,testcase",get_testcase_yaml('./testcase/ProductManager/getProductList.yaml'))
    def test_get_product_list(self,base_info,testcase):
        BaseRequest().specification_yaml(base_info,testcase)


    @allure.story("获取商品详情信息")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase',get_testcase_yaml('./testcase/ProductManager/productDetail.yaml'))
    def test_get_product_detail(self,base_info,testcase):
        BaseRequest().specification_yaml(base_info,testcase)


    @allure.story("提交订单")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcase/ProductManager/commitOrder.yaml'))
    def test_commit_order(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)

    @allure.story("订单支付")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcase/ProductManager/orderPay.yaml'))
    def test_order_pay(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequest().specification_yaml(base_info, testcase)
