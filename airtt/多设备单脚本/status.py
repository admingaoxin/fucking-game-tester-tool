import requests
import json

def send_wechat_work_message(webhook_url, msg_type, content):
    """
    向企业微信发送消息
    :param webhook_url: 企业微信的Webhook URL
    :param msg_type: 消息类型，如'text'
    :param content: 消息内容，需要根据msg_type来格式化
    """
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": msg_type,
        "agentid": "你的应用ID",  # 根据你的企业微信应用设置填写
        "text": {
            "content": content
        },
        "safe": 0
    }
    # 对于不同类型的消息，需要调整data的结构
    if msg_type == 'markdown':
        data['markdown'] = {'content': content}
    
    response = requests.post(webhook_url, headers=headers, json=data)
    return response.json()

# 示例：发送文本消息
webhook_url = '你的企业微信Webhook URL'
if __name__ == "__main__":
    response = send_wechat_work_message(webhook_url, 'text', 'Jenkins构建成功！')
    print(response)

    # 或者发送Markdown消息
    # response = send_wechat_work_message(webhook_url, 'markdown', '#### Jenkins构建通知\n> **状态**：成功\n> **项目**：你的项目名\n> **详情**：[点击查看](你的构建详情链接)')
    # print(response)