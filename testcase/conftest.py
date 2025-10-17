import time
import allure
import pytest

from base.apiutil import BaseRequest
from common.recordlog import logs
from common.readyaml import ReadYamlData, get_testcase_yaml
from pytest import Config, ExitCode  # 导入 Config 和 ExitCode
from _pytest.terminal import TerminalReporter
from common.readyaml import ReadYamlData
from common.dingRobot import send_dingding_msg

read = ReadYamlData()
@pytest.fixture(scope='session',autouse=True)
def clear_extractData():
    read.clear_yaml_data()


@pytest.fixture(scope='session',autouse=True)
def fixture_test():
    logs.info("-----------接口测试开始--------------")
    yield
    logs.info("-----------接口测试结束--------------")

# 测试开始之初，先执行登录的接口测试，获取token，cookie等关键数据
@pytest.fixture(scope='session',autouse=True)
def system_login():
    login_data = get_testcase_yaml('./testcase/Login/loginName.yaml')
    case_info = login_data[0][0]
    testcase = login_data[0][1]
    allure.dynamic.title(testcase['case_name'])
    BaseRequest().specification_yaml(case_info,testcase)

def pytest_terminal_summary(
    terminalreporter: TerminalReporter,  # 带类型注解：指定为 TerminalReport 类型
    exitstatus: ExitCode,             # 带类型注解：指定为 ExitCode 类型
    config: Config,                   # 带类型注解：指定为 Config 类型
) -> None:
    """
    每次pytest测试完成后，自动搜集测试结果的数据
    :param terminalreporter: 内部终端，对象的stats属性
    :param exitstatus: 将报告回操作系统的退出状态
    :param config: pytest配置对象
    :return:
    """
    print(terminalreporter.stats)
    total = terminalreporter._numcollected
    print(f'测试用例总数:{total}')
    passed = len(terminalreporter.stats.get('passed',[]))
    print(f'通过数:{passed}')
    failed = len(terminalreporter.stats.get('failed',[]))
    print(f'失败数:{failed}')
    error = len(terminalreporter.stats.get('error', []))
    print(f'错误数:{error}')
    skipped = len(terminalreporter.stats.get('skipped', []))
    print(f'跳过执行:{skipped}')
    duration = time.time() - terminalreporter._sessionstarttime
    print(f'测试用例执行总时长:{duration}秒')

    content = f"""
    各位好，本次xx项目的自动化测试结果如下：
    测试用例总共：{total}
    通过：{passed}
    失败：{failed}
    跳过：{skipped}
    异常：{error}
    总时长:{duration}
    点击查看测试报告：www.baidu.com
    """
    send_dingding_msg(content=content)