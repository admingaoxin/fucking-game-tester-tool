
# desc: 封装http请求，写测试结果

from email import header
import json
import os
from unittest import result
import urllib.parse
import uuid
import requests
import jmespath
from util.copyXls import writeXls, copyXls
from util.readXlsUtil import readXlsUtil
from util.logUtil import Log
from util import deco

logger = Log('baseApi').getlogger()


def get_checkpoint_value(data, path):
    """
    从嵌套字典中根据路径获取值。
    路径可以是单个键（如'succ'）或多个键用点分隔（如'commResp.srv_t'）。
    """
    keys = path.split('.')
    current_level = data
    for key in keys:
        if key in current_level:
            current_level = current_level[key]
        else:
            # 如果键不存在，返回None
            return None
    return current_level





@deco.decoJudgeMethod
def sendRequest(session, testData):
    '''封装requests请求'''
    # print('testdata:%s'%testData)


    caseId = testData['caseId']
    method = testData['method']
    url = testData['url']
    bodyType = testData['bodyType']
    body = testData['body']
    case_class = testData['case_class']
    diff_value = testData['diffValue']
    # 判断bodyType，格式化body
    if bodyType == 'json':
        if body == '':
            body = {}
        else:
            try:
                body = eval(testData['body'])
                body = json.dumps(body)
            except:
                body = {}
                logger.info('body格式化为json失败，请检查')
    elif bodyType == 'file':
        body = testData['body']
    else:
        logger.info('请求body_type为其他格式，请填写json或file')

    # 格式化params
    try:
        params = eval(testData['params'])
    except:
        params = None
        logger.info('params格式化为json失败，请检查')

    # 格式化headers
    try:
        headers = eval(testData['headers'])
    except:
        headers = None
        logger.info('headers格式化为json失败，请检查')

    verify = False
    result = {
        "result": "",  # 默认值
        "error": "",
        "text": ""
    }

    logger.info("请求方式：%s, 请求url:%s" % (method, url))
    logger.info("请求params：%s" % params)
    logger.info("请求headers：%s" % headers)
    logger.info('请求body：%s' % body)
    try:
        response = None
        if bodyType == 'json':
            response = session.request(method=method,
                                       url=url,
                                       params=params,
                                       headers=headers,
                                       data=body,
                                       verify=verify
                                       )
        elif bodyType == 'file':
            uploadFile = {'file': open(body, 'rb')}
            response = session.request(method=method,
                                       url=url,
                                       params=params,
                                       headers=headers,
                                       files=uploadFile,
                                       verify=verify
                                       )
        # responseType = response.headers['Content-Type']
        # 判断响应的数据类型

        responseType = response.headers.get ('Content-Type', '').lower ()

        if responseType.startswith ('application/json'):
            logger.info ("返回信息：%s" % response.content.decode ('utf-8'))
            decoded_content = response.content.decode ("utf-8")
            result["text"] = f"{decoded_content}"
            print ('看下返回值是什么', response.content.decode ("utf-8"))

        elif responseType.startswith ('application/xml'):
            logger.info ("返回信息：%s" % response.content.decode ('utf-8'))
            decoded_content = response.content.decode ("utf-8")
            result["text"] = f"{decoded_content}"
            print ('看下返回值是什么', response.content.decode ("utf-8"))
        elif responseType.startswith ('text/html'):
            logger.info ("返回信息：%s" % response.content.decode ('utf-8'))
            decoded_content=response.content.decode ("utf-8")
            result["text"] = f"{decoded_content}"
            print ('看下返回值是什么', response.content.decode ("utf-8"))
        elif responseType.startswith ('application/octet-stream'):
            logger.info ('返回为字节流，大小为%sB' % response.headers.get ('Content-Length', '未知大小'))
            result["text"] = '字节流，大小为%sB' % response.headers.get ('Content-Length', '未知大小')
            result["result"] = "pass"
            result['error'] = ""
            result['id'] = testData['caseId']
            result['rowNum'] = testData['rowNum']
            result["statusCode"] = str (response.status_code)  # 状态码转成str
            result["times"] = str (response.elapsed.total_seconds ())
            # 将字节流保存到本地
            downloadPath = f'data\\download\\{caseId}'
            if not os.path.exists (downloadPath):
                os.makedirs (downloadPath, exist_ok=True)  # 使用 makedirs 并设置 exist_ok=True

            # 安全地获取文件名
            default_filename = 'default_filename'  # 设置默认文件名
            filename = None  # 初始化为None，稍后将根据Content-Disposition头部设置

            content_disposition = response.headers.get ('Content-Disposition')
            if content_disposition:
                # 尝试从Content-Disposition头部提取文件名
                parts = content_disposition.split (';')
                print('parts是',parts)
                for part in parts:
                    part = part.strip ()
                    if part.startswith ('filename='):
                        # 使用引号（如果有的话）来安全地提取文件名
                        value = part.split ('=', 1)[-1].strip ()
                        if value.startswith ('"') and value.endswith ('"'):
                            filename = value[1:-1]
                        elif value.startswith ("'") and value.endswith ("'"):
                            filename = value[1:-1]
                        else:
                            filename = value
                        break


            if filename is None:
                parsed_url = urllib.parse.urlparse (response.url)
                filename = os.path.basename (parsed_url.path) or default_filename

            # 使用 os.path.join 构建文件路径
            savedFile = os.path.join (downloadPath, filename)

            # 验证文件名以避免潜在的安全问题
            # 检查文件名是否包含路径分隔符或其他非法字符
            # 这里我们假设非法字符包括但不限于os.sep（路径分隔符）
            # if os.path.basename (savedFile) != filename or os.sep in filename:
            #     logger.warning ('检测到潜在的文件名安全问题，已使用默认文件名')
            #     filename = 'default_filename'  # 直接使用默认文件名
            savedFile = os.path.join (downloadPath, filename)  # 重新构建文件路径

            # 写入文件
            with open (savedFile, "wb") as code:
                code.write (response.content)
        else:

            logger.info ("未知的Content-Type: %s" % responseType)
            result["text"] = response.content.decode ("utf-8", errors='replace')
            result["result"] = "fail"
            result['error'] = "未知的Content-Type"
            # 待判断
            pass
        if 'sheetName' in testData.keys():
            result['sheetName'] = testData['sheetName']
        else:
            result['sheetName'] = 'Sheet1'

        result['id'] = testData['caseId']
        result['rowNum'] = testData['rowNum']
        result['caseName'] = testData['caseName']
        result["statusCode"] = str(response.status_code)  # 状态码转成str
        result["times"] = str(response.elapsed.total_seconds())  # 接口请求时间转str
        print('testdata',testData)
        print('testdata后的result',result)



        # 判断http状态码，如果不是200，判定为失败
        if result["statusCode"] != "200":
            result["error"] = result["text"]
            result["result"] = "fail"
            print ('result不是200', result)
        else:   # 如果http状态码是200，进行检查点的判断
            print('result是200', result)
            print ('responseType出问题的这步', responseType)
            response_text = result["text"].replace (" ", "").replace ("\n", "")
            checkpoint = testData["checkpoint"].replace (" ", "").replace ("\n", "")

            print ('返回值的校验',response_text)
            print ('用例里的校验',checkpoint)


            if int(case_class) == 1:
                #返回值等于用例里的校验
                result["error"] = ""
                if response_text == checkpoint:
                    result["result"] = "pass"
                else:
                    result["result"] = "fail"
            elif int(case_class) == 2:
                result["error"] = ""
                #值包含
                if testData["checkpoint"] in result["text"]:
                    result["result"] = "pass"
                else:
                    result["result"] = "fail"
            elif int(case_class) == 3:
                #值不等于
                result["error"] = ""
                if testData["checkpoint"] != result["text"]:
                    result["result"] = "pass"
                else:
                    result["result"] = "fail"
            elif int(case_class) == 4:
                text_dict = json.loads (response_text)
                srv_t_value = get_checkpoint_value (text_dict, testData["checkpoint"])
                print ('srv_t_value是：', srv_t_value)
                print ('这个是用例里的校验值，用来比较json字符串中的大小', srv_t_value)
                #值等于要取的值
                result["error"] = ""
                if  srv_t_value is not None and srv_t_value == diff_value:
                    result["result"] = "pass"
                else:
                    result["result"] = "fail"
            elif int(case_class) == 5:
                #响应里的值大于要判断的值
                text_dict = json.loads (response_text)
                srv_t_value = get_checkpoint_value (text_dict, testData["checkpoint"])
                result["error"] = ""
                if int(srv_t_value) > int(diff_value):
                    result["result"] = "pass"
                else:
                    result["result"] = "fail"
            elif int(case_class) == 6:
                text_dict = json.loads (response_text)
                srv_t_value = get_checkpoint_value (text_dict, testData["checkpoint"])
                #值小于要判断的值
                result["error"] = ""
                if int(srv_t_value) < int(diff_value):
                    result["result"] = "pass"
                else:
                    result["result"] = "fail"
            elif int(case_class) == 7:
                text_dict = json.loads (response_text)
                checkpoint_dict = json.loads (testData["checkpoint"])
                print(text_dict)
                print('checkpoint_dict是',checkpoint_dict)
                    # 遍历用例字典中的每个键值对
                for key, expected_value in checkpoint_dict.items ():
                    # 检查响应字典中是否存在该键，并且值是否匹配
                    if key in text_dict and text_dict[key] == expected_value:
                        result["result"] = "pass"

                    else:
                        result["result"] = "fail"
            elif int(case_class) == 8:
                 print('字节流下载测试',result)

                #使用any推导值包含
                # 写法是这样：checkpoints = {
                #         'commResp.srv_t': 1723778079,
                #         'commResp.anotherKey': 12345,  # 另一个可能的校验点
                #         # 可以添加更多校验点...
                #     }



            # if responseType == 'application/json':
            #     print('这是个json格式的数据')
            #     result["error"] = ""
            #     if checkpoint in response_text:
            #         result["result"] = "pass"
            #     else:
            #         result["result"] = "fail"
            # elif responseType == 'application/octet-stream' :
            #     print ('这是个二进制字节流')
            #     result["error"] = ""
            #     if checkpoint in response_text:
            #         result["result"] = "pass"
            #     else:
            #         result["result"] = "fail"
            # elif responseType == 'text/html;charset=utf-8':
            #     print ('这是个特殊的网页数据')
            #     result["error"] = ""
            #     if testData["checkpoint"] in result["text"]:
            #         result["result"] = "pass"
            #     else:
            #         result["result"] = "fail"
            # elif responseType == 'text/html':
            #     print ('这是个网页数据')
            #     result["error"] = ""
            #     if testData["checkpoint"] in result["text"]:
            #         result["result"] = "pass"
            #     else:
            #         result["result"] = "fail"
            # elif responseType == 'application/xml' :
            #     print ('这是个xml数据')
            #     result["error"] = ""
            #     if testData["checkpoint"] in result["text"]:
            #         result["result"] = "pass"
            #     else:
            #         result["result"] = "fail"
            # elif responseType == 'text/plain' :
            #     print ('这是个纯文本')
            #     result["error"] = ""
            #     if testData["checkpoint"] in result["text"]:
            #         result["result"] = "pass"
            #     else:
            #         result["result"] = "fail"
        # return result
    except Exception as e:
        result['error'] = str(e)
        result['result'] = 'fail'
        logger.error('请求报错，错误信息为：%s' % str(e))
        print ('result报错', result)
        # return result
    finally:
        print( '这个result老是报错，到底为啥',result)
        logger.info("用例%s测试结果[ %s ]" % (caseId, result["result"]))
        # print("result:%s" % result)
        return result


def writeResult(result, filename):
    rowNum = int(result['rowNum']) -1
    print(rowNum)
    wt = writeXls(filename)
    wt.write(rowNum, 11, result['statusCode'])
    wt.write(rowNum, 12, result['text'])
    wt.write(rowNum, 13, result['error'])
    wt.write(rowNum, 14, result['times'])
    wt.write(rowNum, 15, result['result'])


def writeResult2(result, filename):
    wt = writeXls(filename)
    wt.write2(result['sheetName'], result['rowNum'], 9, result['statusCode'])
    wt.write2(result['sheetName'], result['rowNum'], 10, result['text'])
    wt.write2(result['sheetName'], result['rowNum'], 11, result['error'])
    wt.write2(result['sheetName'], result['rowNum'], 12, result['times'])
    wt.write2(result['sheetName'], result['rowNum'], 13, result['result'])


if __name__ == '__main__':
    # testData = readXlsUtil('../data/case1.xlsx', 'sheet1').dict_data(1)
    # session = requests.session()
    # result = sendRequest(session, testData[0])
    # copyXls('../data/case1.xlsx', '../report/case1_result.xlsx')
    # writeResult(result, '../report/case1_result.xlsx')

    # 文件上传测试
    # file = {'file': open(
    #     'data\\files\\公章.png', 'rb')}
    # session = requests.session()
    # response = session.request(url='http://192.168.1.206:9000/api/v1/file/upload', method='post', params={"file_type": "impression", "file_name": "测试公章", "user_id": "00788730734155812864"}, headers={
    #                            "token": "0a5946bf-ae2c-4063-97a8-41d1fadf939d"}, files=file)
    # print(response.text)
    pass
