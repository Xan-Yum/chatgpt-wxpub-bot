# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import reply
import receive
import web
import requests
import bot


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "xxxxxxx" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            list1 = [ x.encode('utf-8') for x in list]
            sha1 = hashlib.sha1()
            [sha1.update(x) for x in list1]
            #map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)   #后台打日志
            recMsg = receive.parse_xml(webData)
            #print(recMsg)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                #print(toUser,fromUser,recMsg.MsgType)
                if recMsg.MsgType == 'text':
                    # content = "test"
                    #print(recMsg.Content)
                    content_list = bot.send_request(recMsg.Content, fromUser, fromUser)
                    #print(content_list)
                    if content_list[0] == "msg":
                        message = content_list[1]
                        print(message)
                        replyMsg = reply.TextMsg(toUser, fromUser, content_list[1])
                        #print(replyMsg)
                        return replyMsg.send()
                    elif content_list[0] == 'img':
                        mediaId = content_list[1]
                        print(mediaId)
                        replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                        return replyMsg.send()

                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print("暂且不处理")
                return reply.Msg().send()
        except Exception as Argment:
            return Argment
