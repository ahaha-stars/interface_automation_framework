import urllib.parse
import requests
import time
import hmac
import hashlib
import base64

def generate_sign():
    """
        签名计算
        把timestamp+"\n"+密钥当做签名字符串，使用HmacSHA256算法计算签名，然后进行Base64 encode，
        最后再把签名参数再进行urlEncode，得到最终的签名（需要使用UTF-8字符集）
        :return: 返回当前时间戳、加密后的签名
        """
    # 当前时间戳
    #以下是钉钉说明文档的代码
    timestamp = str(round(time.time() * 1000))
    # 钉钉机器人中的加签密钥
    secret = 'SEC144e2264605ffee77368226dba4e67e7d457a6e8885165a81ac878b77619bd61'
    secret_enc = secret.encode('utf-8')
    str_to_sign = '{}\n{}'.format(timestamp, secret)
    # 转成byte类型
    str_to_sign_enc = str_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, str_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

def send_dingding_msg(content,at_all=True):
    """
    :param content: 发生的文本内容
    :param at_all: 是否@全部人，默认是true
    :return:
    """
    timestamp_sign = generate_sign()
    # 拼接url
    url = f"https://oapi.dingtalk.com/robot/send?access_token=282f24ca0379053138e6be593c090230f9b80bf2884523eca357dd7054fc0b93&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}"
    #print(url)
    headers = {'Content-Type':"application/json;charset=utf-8"}
    data = {
        "msgtype":"text",
        "text":{"content":content},
        "at":{"isAtAll":at_all}
    }
    # 调用api接口 发生钉钉信息
    res = requests.post(url=url,json=data,headers=headers)
    return res.text

if __name__ == "__main__":
    content = """
    各位好，本次项目的自动化测试结果如下：
    测试用例总共：100
    通过：98
    失败：2
    跳过：0
    点击查看测试报告：www.baidu.com
    """
    send_dingding_msg(content)