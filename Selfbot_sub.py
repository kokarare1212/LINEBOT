# -*- coding: utf-8 -*-

from pprint import pprint
from linepy import *
from akad.ttypes import Message
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator

botStart = time.time()

whitelist = ["ucb72ccefed623f35d8370f38857f93ae"]

cl = LINE()
#cl = LINE("TOKEN")
#cl = LINE("Email","Password")
#cl = LINE()
cl.log("認証トークン : " + str(cl.authToken))
channelToken = cl.getChannelResult()
cl.log("チャンネルトークン : " + str(channelToken))

readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

clMID = cl.profile.mid
clProfile = cl.getProfile()
clSettings = cl.getSettings()
oepoll = OEPoll(cl)
call = cl
read = json.load(readOpen)
settings = json.load(settingsOpen)


settings = {
    "autoAdd": False,
    "autoJoin": False,
    "autoLeave": False,
    "autoRead": False,
    "lang":"JP",
    "detectMention": True,
    "changeGroupPicture":[],
    "notifikasi": False,
    "Sider":{},
    "checkSticker": False,
    "userAgent": [
        "Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
        "Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
        "Mozilla/5.0 (X11; Linux) Gecko Firefox/5.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 FirePHP/0.5",
        "Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Firefox/5.0",
        "Mozilla/5.0 (X11; Linux x86_64) Gecko Firefox/5.0",
        "Mozilla/5.0 (X11; Linux ppc; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (X11; Linux AMD64) Gecko Firefox/5.0",
        "Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20110619 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.1; U; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.0; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.0; rv:5.0) Gecko/20100101 Firefox/5.0"
    ],
    "mimic": {
        "copy": False,
        "status": False,
        "target": {}
    }
}

read = {
    "readPoint": {},
    "readMember": {},
    "readTime": {},
    "ROM": {}
}

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

cctv = {
    "cyduk":{},
    "point":{},
    "MENTION":{},
    "sidermem":{}
}

myProfile["displayName"] = clProfile.displayName
myProfile["statusMessage"] = clProfile.statusMessage
myProfile["pictureStatus"] = clProfile.pictureStatus

def restartBot():
    print ("[ INFO ] BOT RESETTED")
    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMention(to, mid, firstmessage, lastmessage):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@x "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        cl.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        cl.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def sendMessage(to, Message, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes._from = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1

def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def mentionMembers(to, mid):
    try:
        arrData = ""
        textx = "╔══[合計 {} ユーザー]\n╠ ".format(str(len(mid)))
        arr = []
        no = 1
        for i in mid:
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
            if no < len(mid):
                no += 1
                textx += "╠ "
            else:
                try:
                    textx += "╚══[ {} ]".format(str(cl.getGroup(to).name))
                except:
                    pass
        cl.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        cl.sendMessage(to, "[ INFO ] Error :\n" + str(error))
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False

def helpmessage():
    helpMessage = "━━━━┅═❉ই۝ई❉═┅━━━━\n          ❇    SELFBOT    ❇\n╭━━━━━━━━━━━━━━━━\n║╭❉ MENU HELP ❇\n║┝───────────────" + "\n" + \
                  "║┝──[❇ ステータス ❇ ]" + "\n" + \
                  "║│ Restart" + "\n" + \
                  "║│ Runtime" + "\n" + \
                  "║│ Speed" + "\n" + \
                  "║│ Status" + "\n" + \
                  "║│ About" + "\n" + \
                  "║│ Dell「Removechat」" + "\n" + \
                  "║┝───────────────" + "\n" + \
                  "║┝──[ ❇ 設定 ❇ ]" + "\n" + \
                  "║│ Allstatus「On/Off」" + "\n" + \
                  "║│ Notif「On/Off」" + "\n" + \
                  "║│ Sider「On/Off」" + "\n" + \
                  "║│ AutoAdd「On/Off」" + "\n" + \
                  "║│ AutoJoin「On/Off」" + "\n" + \
                  "║│ AutoLeave「On/Off」" + "\n" + \
                  "║│ AutoRead「On/Off」" + "\n" + \
                  "║│ CheckSticker「On/Off」" + "\n" + \
                  "║│ DetectMention「On/Off」" + "\n" + \
                  "║┝───────────────" + "\n" + \
                  "║┝──[ ❇  セルフ  ❇]" + "\n" + \
                  "║│ Me" + "\n" + \
                  "║│ MyMid" + "\n" + \
                  "║│ MyName" + "\n" + \
                  "║│ MyBio" + "\n" + \
                  "║│ MyPicture" + "\n" + \
                  "║│ MyVideoProfile" + "\n" + \
                  "║│ MyCover" + "\n" + \
                  "║│ StealContact「@」" + "\n" + \
                  "║│ StealMid「@」" + "\n" + \
                  "║│ StealName「@」" + "\n" + \
                  "║│ StealBio「@」" + "\n" + \
                  "║│ StealPicture「@」" + "\n" + \
                  "║│ StealVideoProfile「@」" + "\n" + \
                  "║│ StealCover「@」" + "\n" + \
                  "║│ CloneProfile「@」" + "\n" + \
                  "║│ RestoreProfile" + "\n" + \
                  "║┝───────────────" + "\n" + \
                  "║┝──[ ❇ グループ ❇ ]" + "\n" + \
                  "║│ GroupCreator" + "\n" + \
                  "║│ GroupId" + "\n" + \
                  "║│ GroupName" + "\n" + \
                  "║│ GroupPicture" + "\n" + \
                  "║│ GroupTicket" + "\n" + \
                  "║│ GroupTicket「On/Off」" + "\n" + \
                  "║│ GroupList" + "\n" + \
                  "║│ GroupMemberList" + "\n" + \
                  "║│ GroupInfo" + "\n" + \
                  "║│ Mimic「On/Off」" + "\n" + \
                  "║│ MimicList" + "\n" + \
                  "║│ MimicAdd「@」" + "\n" + \
                  "║│ MimicDel「@」" + "\n" + \
                  "║│ Tag" + "\n" + \
                  "║│ Lurking「On/Off/Reset」" + "\n" + \
                  "║│ Lurking" + "\n" + \
                  "║┝───────────────" + "\n" + \
                  "║┝──[ ❇ メディア ❇]" + "\n" + \
                  "║│ Kalender" + "\n" + \
                  "║│ CheckDate「Date」" + "\n" + \
                  "║┝───────────────\n║╰❉      DPK BOT      ❇\n╰━━━━━━━━━━━━━━━━\n━━━━┅═❉ই۝ई❉═┅━━━━"
    return helpMessage
    
def clBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                cl.sendMessage(op.param1, "Halo {} terimakasih telah menambahkan saya sebagai teman :D".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = cl.getGroup(op.param1)
            if settings["autoJoin"] == True:
                cl.acceptGroupInvitation(op.param1)
        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                elif text.lower() == 'dell':
                    cl.removeAllMessages(op.param2)
                    cl.sendMessage(to, "チャットを削除")
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.sendMessage(to, "⭐")
                    cl.sendMessage(to, "⭐⭐")
                    cl.sendMessage(to, "⭐⭐⭐")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    cl.sendMessage(to, "再起動しています...")
                    restartBot()
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "アクティブなボート {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner = "u07a73b6bce4383ec6ba42e8f266af3e2"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ セルフについて ]"
                        ret_ += "\n╠ Line : {}".format(contact.displayName)
                        ret_ += "\n╠ グループ : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 友達 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ ブロック : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ セルフBOTについて ]"
                        ret_ += "\n╠ バージョン : Premium"
                        ret_ += "\n╠ クリエーター : {}".format(creator.displayName)
                        ret_ += "\n╚══[ SELFBOT ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'status':
                    try:
                        ret_ = "━━━━┅═❉ই۝ई❉═┅━━━━\n          ❇    ステータス    ❇\n╭━━━━━━━━━━━━━━━━\n║╭❉ 🔵[ON]|[OFF]🔴 ❇\n║┝───────────────"
                        if settings["autoAdd"] == True: ret_ += "\n║│🔵 自動追加 [ON]"
                        else: ret_ += "\n║│🔴 自動追加 [OFF]"
                        if settings["autoJoin"] == True: ret_ += "\n║│🔵 自動参加 [ON]"
                        else: ret_ += "\n║│🔴 自動参加 [OFF]"
                        if settings["autoLeave"] == True: ret_ += "\n║│🔵 自動退会 [ON]"
                        else: ret_ += "\n║│🔴 自動退会 [OFF]"
                        if settings["autoRead"] == True: ret_ += "\n║│🔵 自動既読 [ON]"
                        else: ret_ += "\n║│🔴 自動既読 [OFF]"
                        if settings["notifikasi"] == True: ret_ += "\n║│🔵 通知 [ON]"
                        else: ret_ += "\n║│🔴 通知 [OFF]"
                        if settings["detectMention"] == True: ret_ += "\n║│🔵 メンションを検出 [ON]"
                        else: ret_ += "\n║│🔴 メンションを検出 [OFF]"
                        ret_ += "\n║┝───────────────\n║╰❉      DPK BOT      ❇\n╰━━━━━━━━━━━━━━━━\n━━━━┅═❉ই۝ई❉═┅━━━━"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "🔵 自動追加 [ON]")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "🔴 自動追加 [OFF]")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "🔵 自動参加 [ON]")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "🔴 自動参加 [OFF]")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "🔵 自動退会 [ON]")
                elif text.lower() == 'autojoin off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "🔴 自動退会 [OFF]")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "🔵 自動既読 [ON]")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "🔴 自動既読 [OFF]")
                elif text.lower() == 'checksticker on':
                    settings["checkSticker"] = True
                    cl.sendMessage(to, "🔵 スタンプチェック [ON]")
                elif text.lower() == 'checksticker off':
                    settings["checkSticker"] = False
                    cl.sendMessage(to, "🔴 スタンプチェック [OFF]")
                elif text.lower() == 'detectmention on':
                    settings["datectMention"] = True
                    cl.sendMessage(to, "🔵 メンションを検出 [ON]")
                elif text.lower() == 'detectmention off':
                    settings["datectMention"] = False
                    cl.sendMessage(to, "🔴 メンションを検出 [OFF]")

                elif text.lower() == 'allstatus on':
                    settings["notifikasi"] = True
                    settings["autoAdd"] = True
                    settings["autoJoin"] = True
                    settings["autoLeave"] = True
                    settings["autoRead"] = True
                    settings["datectMention"] = True
                    cl.sendMessage(to, "🔵 全てのステータス [ON]")

                elif text.lower() == 'allstatus off':
                    settings["notifikasi"] = False
                    settings["autoAdd"] = False
                    settings["autoJoin"] = False
                    settings["autoLeave"] = False
                    settings["autoRead"] = False
                    settings["datectMention"] = False
                    cl.sendMessage(to, "🔴 全てのステータス [OFF]")

                elif text.lower() == 'me':
                    sendMessageWithMention(to, clMID)
                    cl.sendContact(to, clMID)
                elif text.lower() == 'mymid':
                    cl.sendMessage(msg.to,"[MID]\n" +  clMID)
                elif text.lower() == 'myname':
                    me = cl.getContact(clMID)
                    cl.sendMessage(msg.to,"[名前]\n" + me.displayName)
                elif text.lower() == 'mybio':
                    me = cl.getContact(clMID)
                    cl.sendMessage(msg.to,"[ステータスメッセージ]\n" + me.statusMessage)
                elif text.lower() == 'mypicture':
                    me = cl.getContact(clMID)
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideoprofile':
                    me = cl.getContact(clMID)
                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = cl.getContact(clMID)
                    cover = cl.getProfileCoverURL(clMID)    
                    cl.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("stealcontact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("stealmid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n{}" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("stealname "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 名前 ]\n" + contact.displayName)
                elif msg.text.lower().startswith("stealbio "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ ステータスメッセージ ]\n{}" + contact.statusMessage)
                elif msg.text.lower().startswith("stealpicture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealvideoprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.cl.naver.jp/" + cl.getContact(ls).pictureStatus + "/vp"
                            cl.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealcover "):
                    if cl != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = cl.getProfileCoverURL(ls)
                                cl.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cloneprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            cl.cloneContactProfile(contact)
                            cl.sendMessage(msg.to, "メンバーをクローン ")
                        except:
                            cl.sendMessage(msg.to, "メンバーのクローンに失敗")
                elif text.lower() == 'restoreprofile':
                    try:
                        clProfile.displayName = str(myProfile["displayName"])
                        clProfile.statusMessage = str(myProfile["statusMessage"])
                        clProfile.pictureStatus = str(myProfile["pictureStatus"])
                        cl.updateProfileAttribute(8, clProfile.pictureStatus)
                        cl.updateProfile(clProfile)
                        cl.sendMessage(msg.to, "プロフィールを復元 ")
                    except:
                        cl.sendMessage(msg.to, "プロフィールの復元に失敗")

                elif msg.text.lower().startswith("mimicadd "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            cl.sendMessage(msg.to,"ターゲットを追加")
                            break
                        except:
                            cl.sendMessage(msg.to,"ターゲットの追加に失敗")
                            break
                elif msg.text.lower().startswith("mimicdel "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["mimic"]["target"][target]
                            cl.sendMessage(msg.to,"ターゲットを削除")
                            break
                        except:
                            cl.sendMessage(msg.to,"ターゲットの削除に失敗")
                            break
                elif text.lower() == 'mimiclist':
                    if settings["mimic"]["target"] == {}:
                        cl.sendMessage(msg.to,"Tidak Ada Target")
                    else:
                        mc = "╔══[ 模倣リスト ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ 終わり ]")
                    
                elif "mimic" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            cl.sendMessage(msg.to,"🔵 メッセージの返信 [ON]")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            cl.sendMessage(msg.to,"🔴 メッセージの返信 [OFF]")

                elif text.lower() == 'groupcreator':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'groupid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[グループID : ]\n" + gid.id)
                elif text.lower() == 'grouppicture':
                    group = cl.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'groupname':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[グループ名 : ]\n" + gid.name)
                elif text.lower() == 'groupticket':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to, "[ グループチケット ]\nhttps://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            cl.sendMessage(to, "グループチケットは開いていません。まずコマンドで開いてください {}openqr".format(str(settings["keyCommand"])))
                elif text.lower() == 'groupticket on':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendMessage(to, "🔵 グループチケット [ON]")
                        else:
                            group.preventedJoinByTicket = False
                            cl.updateGroup(group)
                            cl.sendMessage(to, "グループチケットONに失敗")
                elif text.lower() == 'groupticket off':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendMessage(to, "🔴 グループチケット [OFF]")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendMessage(to, "グループチケットOFFに失敗")
                elif text.lower() == 'groupinfo':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Tidak ditemukan"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "Tertutup"
                        gTicket = "Tidak ada"
                    else:
                        gQr = "Terbuka"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ グループInfo ]"
                    ret_ += "\n╠ グループ名 : {}".format(str(group.name))
                    ret_ += "\n╠ グループID : {}".format(group.id)
                    ret_ += "\n╠ 作成者 : {}".format(str(gCreator))
                    ret_ += "\n╠ グループ人数 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 保留中のユーザー : {}".format(gPending)
                    ret_ += "\n╠ グループQR : {}".format(gQr)
                    ret_ += "\n╠ グループチケット : {}".format(gTicket)
                    ret_ += "\n╚══[ グループInfo ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'groupmemberlist':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ メンバーリスト ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ トータル {} ]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'grouplist':
                        groups = cl.groups
                        ret_ = "╔══[ グループリスト ]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ トータル {} グループ ]".format(str(len(groups)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'notif on':
                   if settings["notifikasi"] == True:
                       if settings["lang"] == "JP":
                           cl.sendMessage(msg.to,"🔵 通知 [ON]")
                   else:
                       settings["notifikasi"] = True
                       if settings["lang"] == "JP":
                           cl.sendMessage(msg.to,"🔵 通知 [ON]")

                elif text.lower() == 'notif off':
                   if settings["notifikasi"] == False:
                       if settings["lang"] == "JP":
                          cl.sendMessage(msg.to,"🔴 通知 [OFF]")
                   else: 
                       settings["notifikasi"] = False
                       if settings["lang"] == "JP":
                           cl.sendMessage(msg.to,"🔴 通知 [OFF]")
                elif text.lower() == 'tag':
                            if msg.toType == 0:
                                sendMention(to, to, "", "")
                            elif msg.toType == 2:
                                group = cl.getGroup(to)
                                midMembers = [contact.mid for contact in group.members]
                                midSelect = len(midMembers)//20
                                for mentionMembers in range(midSelect+1):
                                    no = 0
                                    ret_ = "╔══[ メンション メンバー ]"
                                    dataMid = []
                                    for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
                                        dataMid.append(dataMention.mid)
                                        no += 1
                                        ret_ += "\n╠ {}. @!".format(str(no))
                                    ret_ += "\n╚══[ トータル {} メンバー]".format(str(len(dataMid)))
                                    cl.sendMention(msg.to, ret_, dataMid)
                elif text.lower() == 'changepictureprofile':
                            settings["changePicture"] = True
                            cl.sendMessage(to, "写真を送ってください")
                elif text.lower() == 'changegrouppicture':
                            if msg.toType == 2:
                                if to not in settings["changeGroupPicture"]:
                                    settings["changeGroupPicture"].append(to)
                                cl.sendMessage(to, "写真を送ってください")
                elif text.lower() == 'lurking on':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                cl.sendMessage(msg.to,"Lurking already on")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            cl.sendMessage(msg.to, "既読ポイントを設定:\n" + readTime)
                            
                elif text.lower() == 'lurking off':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        cl.sendMessage(msg.to,"すでに潜んでいます")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        cl.sendMessage(msg.to, "既読ポイントを削除:\n" + readTime)
    
                elif text.lower() == 'lurking reset':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        cl.sendMessage(msg.to, "既読ポイントをリセット:\n" + readTime)
                    else:
                        cl.sendMessage(msg.to, "しかし、なぜリセットされないのですか？")
                        
                elif text.lower() == 'lurking':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            cl.sendMessage(receiver,"[ リーダー ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = cl.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ Reader ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ Lurking time ]: \n" + readTime
                        try:
                            cl.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        cl.sendMessage(receiver,"潜んで設定されていません")

                elif text.lower() == 'sider on':
                    try:
                        del cctv['point'][msg.to]
                        del cctv['sidermem'][msg.to]
                        del cctv['cyduk'][msg.to]
                    except:
                        pass
                    cctv['point'][msg.to] = msg.id
                    cctv['sidermem'][msg.to] = ""
                    cctv['cyduk'][msg.to]=True 
                    settings["Sider"] = True
                    cl.sendMessage(msg.to,"🔵 サイダー [ON]")

                elif text.lower() == 'sider off':
                    if msg.to in cctv['point']:
                       cctv['cyduk'][msg.to]=False
                       settings["Sider"] = False
                       cl.sendMessage(msg.to,"🔴 サイダー [OFF]")
                    else:
                        cl.sendMessage(msg.to,"🔴 サイダー [OFF]")

                elif text.lower() == 'kalender':
                    tz = pytz.timezone("Asia/Makassar")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    cl.sendMessage(msg.to, readTime)                 
                elif "checkdate" in msg.text.lower():
                    sep = msg.text.split(" ")
                    tanggal = msg.text.replace(sep[0] + " ","")
                    r=requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                    data=r.text
                    data=json.loads(data)
                    ret_ = ""
                    ret_ += "Date Of Birth : {}".format(str(data["data"]["lahir"]))
                    ret_ += "\nAge : {}".format(str(data["data"]["usia"]))
                    ret_ += "\nBirthday : {}".format(str(data["data"]["ultah"]))
                    ret_ += "\nZodiak : {}".format(str(data["data"]["zodiak"]))
                    ret_ += ""
                    cl.sendMessage(to, str(ret_))
            elif msg.contentType == 7:
                if settings["checkSticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = ""
                    ret_ += "STICKER ID : {}".format(stk_id)
                    ret_ += "\nSTICKER PACKAGES ID : {}".format(pkg_id)
                    ret_ += "\nSTICKER VERSION : {}".format(stk_ver)
                    ret_ += "\nSTICKER URL : line://shop/detail/{}".format(pkg_id)
                    ret_ += ""
                    cl.sendMessage(to, str(ret_))

            elif msg.contentType == 1:
                    if settings["changePicture"] == True:
                        path = cl.downloadObjectMsg(msg_id)
                        settings["changePicture"] = False
                        cl.updateProfilePicture(path)
                        cl.sendMessage(to, "mengubah foto profile")
                    if msg.toType == 2:
                        if to in settings["changeGroupPicture"]:
                            path = cl.downloadObjectMsg(msg_id)
                            settings["changeGroupPicture"].remove(to)
                            cl.updateGroupPicture(to, path)
                            cl.sendMessage(to, "mengubah foto group")

        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        cl.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                              if settings["detectMention"] == True:
                                 sendMention(receiver, sender, "", "")
                if text.lower() == "help":
                    cl.sendMessage(msg.to,helpmessage())
                print("[ INFO ] GroupID:"+str(msg.to))
                print("[ INFO ] MID:"+str(sender))
                print("[ INFO ] DisplayName:"+cl.getContact(sender).displayName)
                print("[ INFO ] Message:"+str(text))

        if op.type == 17:
           print ("MEMBER JOIN TO GROUP")
           if settings["notifikasi"] == True:
             if op.param2 in clMID:
                 return
             ginfo = cl.getGroup(op.param1)
             contact = cl.getContact(op.param2)
             image = "http://dl.profile.line.naver.jp/" + contact.pictureStatus
             cl.sendMessage(op.param1,"こんにちは " + cl.getContact(op.param2).displayName + "さん\n" + str(ginfo.name) + "\nへようこそ(*^_^*)")
             cl.sendImageWithURL(op.param1,image)

        if op.type == 15:
           print ("MEMBER LEAVE TO GROUP")
           print("[ INFO ] GroupID:"+str(op.param1))
           print("[ INFO ] MID:"+str(op.param2))
           pprint(cl.getContact(op.param2))
           if str(op.param2) in whitelist:
               cl.inviteIntoGroup(op.param1,cl.getContact(op.param2).mid)
           if settings["notifikasi"] == True:
             if op.param2 in clMID:
                 return
             ginfo = cl.getGroup(op.param1)
             contact = cl.getContact(op.param2)
             image = "http://dl.profile.line.naver.jp/" + contact.pictureStatus
             cl.sendImageWithURL(op.param1,image)
             cl.sendMessage(op.param1,cl.getContact(op.param2).displayName + "さん\nさようなら(。・∀・。)ノ")

        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if cctv['cyduk'][op.param1]==True:
                    if op.param1 in cctv['point']:
                        Name = cl.getContact(op.param2).displayName
                        if Name in cctv['sidermem'][op.param1]:
                            pass
                        else:
                            cctv['sidermem'][op.param1] += "\nâ¢ " + Name
                            if " " in Name:
                                nick = Name.split(' ')
                                if len(nick) == 2:
                                    cl.sendMessage(op.param1, "╭━━━━┅═❉ই۝ई❉═┅━━━━\n║╭❉ SIDER TERDETEKSI\n║┝───────────────\n" + "║│" + nick[0] + "\n║┝─────────────── " + "\n║│Yuk kak chat sini 🙋\n║╰❉ Jangan ngelamun😁\n╰━━━━━━━━━━━━━━━━\n━━━━┅═❉ই۝ई❉═┅━━━━ ")
                                    time.sleep(0.2)
                                    mentionMembers(op.param1,[op.param2])
                                else:
                                    cl.sendMessage(op.param1, "╭━━━━┅═❉ই۝ई❉═┅━━━━\n║╭❉ SIDER TERDETEKSI\n║┝───────────────\n" + "║│" + nick[0] + "\n║┝─────────────── " + "\n║│Yuk kak chat sini 🙋\n║╰❉ Jangan ngelamun😁\n╰━━━━━━━━━━━━━━━━\n━━━━┅═❉ই۝ई❉═┅━━━━ ")
                                    time.sleep(0.2)
                                    mentionMembers(op.param1,[op.param2])
                            else:
                                cl.sendMessage(op.param1, "╭━━━━┅═❉ই۝ई❉═┅━━━━\n║╭❉ SIDER TERDETEKSI\n║┝───────────────\n" + "║│" + Name + "\n║┝─────────────── " + "\n║│Yuk kak chat sini 🙋\n║╰❉ Jangan ngelamun😁\n╰━━━━━━━━━━━━━━━━\n━━━━┅═❉ই۝ई❉═┅━━━━ ")
                                time.sleep(0.2)
                                mentionMembers(op.param1,[op.param2])
                    else:
                        pass
                else:
                    pass
            except:
                pass


        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)

while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
