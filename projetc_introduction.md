# 项目文件功能详解（除testcase目录外）
## 一、base/ 目录 - 基础工具层
### 1. apiutil.py
核心接口工具类 ，提供接口测试的核心功能：

- BaseRequest 类：处理接口请求的基类
- replace_load() ：动态参数替换，解析 ${function(param)} 格式的数据
- specification_yaml() ：处理单个接口测试用例
- specification_business_yaml() ：处理业务场景测试用例
- extract_data() ：单个数据提取（支持正则和JSON提取）
- extract_data_list() ：列表数据提取（支持正则和JSON提取）
### 2. generateId.py
测试ID生成工具 ：

- generate_model_id() ：生成模型ID（如 M01_ , M02_ ）
- generate_testcase_id() ：生成测试用例ID（如 01_ , 02_ ）
- 使用生成器模式，支持批量生成唯一ID
## 二、common/ 目录 - 通用功能层
### 1. assertions.py
断言模块 ，提供多种断言方法：

- contains_assert() ：包含断言，检查响应是否包含预期值
- equal_assert() ：相等断言，检查响应是否等于预期值
- assert_mysql() ：数据库断言，检查数据库数据
- assert_result() ：统一的断言入口方法
### 2. connection.py
数据库连接模块 ：

- ConnectMysql 类：MySQL数据库连接和操作
- query() ：执行查询语句
- insert() ：执行插入语句
- delete() ：执行删除语句
- 自动处理连接关闭和异常处理
### 3. debugtalk.py
动态参数处理模块 ：

- get_extract_data() ：从extract.yaml获取提取的数据
- get_extract_order_data() ：按顺序获取提取数据
- timestamp() ：获取当前时间戳（10位）
- 支持随机获取、全部获取、列表获取等多种方式
### 4. dingRobot.py
钉钉机器人通知模块 ：

- generate_sign() ：生成钉钉签名
- send_dingding_msg() ：发送钉钉消息通知
- 支持@所有人功能
### 5. operationcsv.py
CSV文件操作模块 ：

- read_csv_data() ：读取CSV测试数据文件
### 6. readyaml.py
YAML文件处理模块 ：

- get_testcase_yaml() ：读取测试用例YAML文件
- ReadYamlData 类：
  - write_yaml_data() ：写入数据到extract.yaml
  - clear_yaml_data() ：清空extract.yaml数据
  - get_extract_yaml() ：从extract.yaml读取数据 调用get_extract_yaml获取全部数据，在进行加工
### 7. recordlog.py
日志记录模块 ：

- RecordLog 类：日志记录器
- handle_overdue_log() ：清理过期日志（30天前）
- output_logging() ：配置日志格式和输出方式
- 支持文件日志和控制台日志双输出
### 8. sendrequests.py
HTTP请求发送模块 ：

- SendRequests 类：封装requests库
- run_main() ：组合封装的主方法
- send_request() ：发送HTTP请求
- 自动处理Cookie并保存到extract.yaml
- 支持各种HTTP方法（GET、POST等）
## 三、conf/ 目录 - 配置管理层
### 1. config.ini
配置文件 ，存储环境配置信息：

- [api_envi] ：API环境配置（host等）
- [MYSQL] ：数据库配置（host、port、username、password、database）
### 2. operationConfig.py
配置文件操作类 ：

- OperationConfig 类：读取config.ini配置
- get_envi() ：获取API环境配置
- get_mysql_conf() ：获取数据库配置
- get_section_for_data() ：通用配置获取方法
### 3. setting.py
项目设置 ：

- DIR_BASE ：项目基础路径
- LOG_LEVEL ：日志输出级别
- STREAM_LOG_LEVEL ：控制台日志级别
- FILE_PATH ：文件路径配置（extract、conf、LOG）
## 四、根目录文件
### 1. extract.yaml
提取数据存储文件 ，保存接口提取的数据：

- 存储token、Cookie、订单号、用户ID等数据
- 支持单个值和列表数据的存储
- 供后续接口动态引用
### 2. pytest.ini
pytest配置文件 ：

- testpaths ：测试用例路径
- python_files ：测试文件命名规则（test_*.py）
- python_class ：测试类命名规则（Test*）
- python_functions ：测试函数命名规则（test*）
### 3. environment.xml
环境信息配置文件 ：

- 记录系统环境信息（Windows 11）
- Python版本（3.11.9）
- Allure版本（2.15.0）
- 项目名称（电商平台项目接口自动化测试）
## 五、其他目录
### 1. data/
- test_data.csv ：CSV格式的测试数据文件
### 2. logs/
- 日志文件存储目录，按日期命名（如 test.20260326.log ）
### 3. report/
- temp/ ：Allure报告临时文件目录
- 存储测试执行过程中的附件和结果文件
## 项目架构总结
该项目采用 分层架构设计 ：

1. 基础层（base/） ：提供核心接口测试功能
2. 通用层（common/） ：提供各种通用工具和功能
3. 配置层（conf/） ：管理配置信息
4. 数据层 ：存储测试数据和提取数据
5. 报告层 ：生成测试报告