import requests
import json
import tools


# 定义接口地址
ip = "xx.xx.xx.xx:xxxx"
api_url = "http://" + ip + "/v1/chat"  # 替换为实际的接口地址


def send_request(message, session_id, username):
    # 构建请求的数据
    data = {
        "message": message,
        "session_id": "777-" + session_id,
        "username": username
    }

    # 发送POST请求
    response = requests.post(api_url, json=data)
    #print(response)

    # v2版本
    #request_id = response.text.strip()
    #print(request_id)
    #async_response_url = "http://" + ip + "/v2/chat/response?request_id=" + request_id
    #print(async_response_url)
    #async_response = request.get(async_response_url)
    #print(async_response)
    #return async_response

    # 检查响应状态码
    if response.status_code == 200:
        # 解析JSON响应
        result = json.loads(response.text)
        #print(result)
        #return result['message']
        messages = result['message']
        images = result['image']
        voices = result['voice']

        if messages:
            #print(messages)
            for msg in messages:
                print(f"Received message: {msg[:170]}")
                return ["msg", msg]
        elif images:
            #print(images)
            for img in images:
                print(f"Received image: {img[:70]}")
                #print(img[:70])
                #print(img)
                #media_id = upload_image_and_get_media_id(get_access_token(), base64_image)
                media_id = tools.upload_image_and_get_media_id(tools.get_access_token(), img)
                #print(f'Media ID: {media_id}')
                #print(media_id)
                return ["img", media_id]
        elif voices:
            pass
        else:
            print("未知类型")

        # 处理响应结果
        #if result['result'] == "SUCCESS":
        #    messages = result['message']
        #    for msg in messages:
        #        print(f"Received message: {msg}")
        #        return msg
        #else:
        #    print(f"Request failed. Result: {result['result']}")
    else:
        print(f"Failed to send request. Status code: {response.status_code}")


# if __name__ == "__main__":
#     # 你可以在这里调用 send_request 函数，并传递要发送的消息
#     send_request("你好，这是一个测试消息。")
