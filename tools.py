import requests
import json
import time
import base64
import os


# 微信公众号的AppID和AppSecret
app_id = 'xxxxx'
app_secret = 'xxxxxxx'

# 定义全局变量存储access_token及其过期时间
access_token_info = {'access_token': None, 'expires_at': 0}


def get_access_token():
    global access_token_info

    # 如果access_token还未过期，直接返回
    if access_token_info['expires_at'] > time.time() and access_token_info['access_token']:
        return access_token_info['access_token']

    # 发送请求获取新的access_token
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}'
    response = requests.get(url)
    data = response.json()

    # 提取新的access_token和过期时间
    access_token = data.get('access_token')
    if access_token:
        expires_in = data.get('expires_in', 7200)  # 默认有效期为7200秒
        expires_at = time.time() + expires_in

        # 更新全局变量中的access_token信息
        access_token_info['access_token'] = access_token
        access_token_info['expires_at'] = expires_at

        return access_token
    else:
        # 如果获取失败，输出错误信息
        print(f"Failed to get access_token. Error: {data.get('errmsg')}")
        return None


# # 使用示例
# access_token = get_access_token()
# if access_token:
#     print(f"Access Token: {access_token}")
#     # 在这里可以使用access_token调用其他接口


def upload_image_and_get_media_id(access_token, base64_image):
    #print(base64_image)
    base64_image = base64_image.split(',')[1]
    #print(base64_image)
    #base64_image = re.sub('^data:image/.+;base64,', '', base64_image)
    upload_url = f'https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
    # 计算需要添加的填充字符数量
    padding = 4 - (len(base64_image) % 4)
    # 添加填充字符 "="
    base64_image += "=" * padding

    try:
        # 将 base64 字符串解码为二进制数据
        image_data = base64.b64decode(base64_image)
        #image_data = base64.urlsafe_b64decode(base64_image)

        # 设置文件名为 file.jpg，确保文件名中包含正确的文件扩展名
        #files = {'media': ('file.jpg', image_data, 'image/jpeg')}
        #files = {'media': ('image.jpg', image_data, 'image/jpeg', {'Content-Disposition': 'form-data; name="media"; filename="image.jpg"'})}
        files = {'media': ('file.png', image_data, 'image/png', {
            'Content-Disposition': 'form-data; name="media"; filename="file.png"',
            'Content-Length': str(len(image_data)),
            'Content-Type': 'image/png'
        })}

        # 发起上传请求
        response = requests.post(upload_url, files=files)

        # 处理响应
        result = response.json()
        if 'media_id' in result:
            return result['media_id']
        else:
            print(result)
            return None
    except Exception as e:
        print(f"Error decoding Base64: {e}")
        return None


# 替换下面的值为你的 Base64 字符串
#base64_image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAAJAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5r+zL/k0VJRVnfdn/2Q=="


#media_id = upload_image_and_get_media_id(get_access_token(), base64_image)
#print(f'Media ID: {media_id}')
#print(get_access_token())



#def save_base64_image_locally(base64_image, filename='temp_image.png'):
#    try:
#        # 计算需要添加的填充字符数量
#        padding = 4 - (len(base64_image) % 4)
#        # 添加填充字符 "="
#        base64_image += "=" * padding
#
#        # 将 base64 字符串解码为二进制数据
#        image_data = base64.b64decode(base64_image)
#
#        # 保存图片到本地
#        with open(filename, 'wb') as file:
#            file.write(image_data)
#
#        return filename
#    except Exception as e:
#        print(f"Error saving Base64 image locally: {e}")
#        return None
#
#def upload_image_and_get_media_id(access_token, filename):
#    upload_url = f'https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
#
#    try:
#        # 设置文件名为 file.jpg，确保文件名中包含正确的文件扩展名
#        files = {'media': ('file.png', open(filename, 'rb'), 'image/png')}
#
#        # 发起上传请求
#        response = requests.post(upload_url, files=files)
#
#        # 删除本地图片
#        #os.remove(filename)
#
#        # 处理响应
#        result = response.json()
#        if 'media_id' in result:
#            return result['media_id']
#        else:
#            print(result)
#            return None
#    except Exception as e:
#        print(f"Error uploading image: {e}")
#        return None
#
#
## 保存图片到本地
#local_filename = save_base64_image_locally(base64_image)
#
## 上传图片并获取 media_id
#media_id = upload_image_and_get_media_id(get_access_token(), local_filename)
#
## 打印结果
#print(f"Media ID: {media_id}")
#
