# -*- coding: utf-8 -*-

from linepy import *
import time, re, ast, sys, os, datetime

try:
   args = sys.argv
   if len(args)>=2 and args[1] is not None:
      cl = LINE(args[1])
   else:
      print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
      print("|||   Read Bot  by kokarare1212   |||")
      print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
      print("")
      print("___Login Mode List______")
      print("| 1, URL Auth (Default)|")
      print("| 2, authToken         |")
      print("| 3, Email and Password|")
      print("________________________")
      print("")
      startCmdInt = input ("Please Choose Login Mode [1]: ")
      print("")
      if startCmdInt == "" or startCmdInt == "1":
         cl = LINE()
      elif startCmdInt == "2":
         authToken = input("authToken: ")
         print("")
         cl = LINE(authToken)
      elif startCmdInt == "3":
         email = input("Email: ")
         password = input("Password: ")
         print("")
         cl = LINE(email, password)
      else:
         cl = LINE()
except Exception as e:
   print("")
   print(e)
   print("")
   input("Press Enter to Finish...")
   exit()

channelToken = cl.getChannelResult()
cl.log("authToken: "+str(cl.authToken))
cl.log("channelToken: "+str(channelToken))

oepoll = OEPoll(cl)
clMID = cl.profile.mid

def restartBOT():
   time.sleep(3)
   os.execl(sys.executable, sys.executable, [args[0], cl.authToken])

def clBot(op):
   try:

      if os.path.isfile("line.log") == True:
         with open("line.log","r", encoding="utf-8", errors="ignore") as f:
            log = f.read()
      else:
         log = ""
      if op.type == 0:
         cl.log("[ 0 ] END OF OPERATION")
      if op.type == 5:
         cl.log("[ 5 ] NOTIFIED ADD CONTACT")
         displayName = cl.getContact(op.param1).displayName
         mid = cl.getContact(op.param1).mid
         print("Add Contact: "+mid+"/"+displayName)
         log = "["+str(datetime.datetime.now())+"] Add Contact: "+mid+"/"+displayName+"\n\n"+log
      if op.type == 13:
         cl.log("[ 13 ] NOTIFIED INVITE GROUP")
         gid = op.param1
         gname = cl.getGroup(gid).name
         print("Invite Group: "+gid+"/"+gname)
         log = "["+str(datetime.datetime.now())+"] Invite Group: "+gid+"/"+gname+"\n\n"+log
         time.sleep(10)
         cl.acceptGroupInvitation(gid)
         print("Joined Group: "+gid+"/"+gname)
         log = "["+str(datetime.datetime.now())+"] Joined Group: "+gid+"/"+gname+"\n\n"+log
      if op.type == 24:
         cl.log("[ 24 ] NOTIFIED LEAVE ROOM")
         #mid = op.param1
         #cl.leaveRoom(mid)
         #print("Left Room: "+mid)
      if op.type == 25:
         cl.log("[ 25 ] SEND MESSAGE")
         to = op.message.to
         contentType = op.message.contentType
         messageId = op.message.id
         text = op.message.text
         if contentType == 0:
            if text is None:
               return
            if to.startswith("u"):
               displayName = cl.getContact(to).displayName
               print("Send Message: "+to+"/"+displayName+" "+messageId+" "+text)
               log = "["+str(datetime.datetime.now())+"] Send Message: "+to+"/"+displayName+" "+messageId+" "+text+"\n\n"+log
            if to.startswith("r"):
               print("Send Message: Room "+to+" "+messageId+" "+text)
               log = "["+str(datetime.datetime.now())+"] Send Message: Room "+to+" "+messageId+" "+text+"\n\n"+log
            if to.startswith("c"):
               name = cl.getGroup(to).name
               print("Send Message: Group "+to+"/"+name+" "+messageId+" "+text)
               log = "["+str(datetime.datetime.now())+"] Send Message: Group "+to+"/"+name+" "+messageId+" "+text+"\n\n"+log
         if contentType == 7:
            stickerId = op.message.contentMetadata["STKID"]
            stickerVersion = op.message.contentMetadata["STKVER"]
            packageId = op.message.contentMetadata["STKPKGID"]
            if to.startswith("u"):
               displayName = cl.getContact(to).displayName
               print("Send Message: "+to+"/"+displayName+" "+messageId+" "+stickerId+","+stickerVersion+","+packageId)
               log = "["+str(datetime.datetime.now())+"] Send Message: "+to+"/"+displayName+" "+messageId+" "+stickerId+","+stickerVersion+","+packageId+"\n\n"+log
            if to.startswith("r"):
               print("Send Message: Room "+to+" "+messageId+" "+messageId+" "+stickerId+","+stickerVersion+","+packageId)
               log = "["+str(datetime.datetime.now())+"] Send Message: Room "+to+" "+messageId+" "+messageId+" "+stickerId+","+stickerVersion+","+packageId+"\n\n"+log
            if to.startswith("c"):
               name = cl.getGroup(to).name
               print("Send Message: Group "+to+"/"+name+" "+messageId+" "+messageId+" "+stickerId+","+stickerVersion+","+packageId)
               log = "["+str(datetime.datetime.now())+"] Send Message: Group "+to+"/"+name+" "+messageId+" "+messageId+" "+stickerId+","+stickerVersion+","+packageId+"\n\n"+log
         if text.lower() == "restart":
            with open("line.log", "w", encoding="utf-8", errors="ignore") as f:
               f.write(log)
            restartBOT()
      if op.type == 26:
         cl.log("[ 26 ] RECEIVE MESSAGE")
         to = op.message.to
         _from = op.message._from
         messageId = op.message.id
         text = op.message.text
         if to == clMID:
            displayName = cl.getContact(_from).displayName
            cl.sendChatChecked(_from, messageId)
         else:
            name = cl.getGroup(to).name
            displayName = cl.getContact(_from).displayName
            cl.sendChatChecked(to, messageId)
         if op.message.contentType == 0:
            if "MENTION" in op.message.contentMetadata.keys() != None:
               names = re.findall(r'@(\w+)', text)
               mention = ast.literal_eval(op.message.contentMetadata["MENTION"])
               mentionees = mention["MENTIONEES"]
               lists = []
               for mention in mentionees:
                  if clMID in mention["M"]:
                     if to == clMID:
                        print("Receive Message: "+_from+"/"+displayName+" "+messageId+" Mention")
                        log = "["+str(datetime.datetime.now())+"] Receive Message: "+_from+"/"+displayName+" "+messageId+" Mention"+"\n\n"+log
                     else:
                        print("Receive Message: "+to+"/"+name+" "+_from+"/"+displayName+" "+messageId+" Mention")
                        log = "["+str(datetime.datetime.now())+"] Receive Message: "+to+"/"+name+" "+_from+"/"+displayName+" "+messageId+" Mention"+"\n\n"+log
         if text is None:
            return
         if to == clMID:
            print("Receive Message: "+_from+"/"+displayName+" "+messageId+" "+text)
            log = "["+str(datetime.datetime.now())+"] Receive Message: "+_from+"/"+displayName+" "+messageId+" "+text+"\n\n"+log
         else:
            print("Receive Message: "+to+"/"+name+" "+_from+"/"+displayName+" "+messageId+" "+text)
            log = "["+str(datetime.datetime.now())+"] Receive Message: "+to+"/"+name+" "+_from+"/"+displayName+" "+messageId+" "+text+"\n\n"+log
         if text.lower() == "restart":
            with open("line.log", "w", encoding="utf-8", errors="ignore") as f:
               f.write(log)
            restartBOT()
      if op.type == 15:
         cl.log("[ 15 ] MEMBER JOIN TO GROUP")
         gid = op.param1
         name = cl.getGroup(gid).name
         if op.param2 in clMID:
            print("Member Join To Group: "+gid+"/"+name+" Me")
            log = "["+str(datetime.datetime.now())+"] Member Join To Group: "+gid+"/"+name+" Me"+"\n\n"+log
            return
         mid = op.param2
         displayName = cl.getContact(mid),displayName
         print("Member Join To Group: "+gid+"/"+name+" "+mid+"/"+displayName)
         log = "["+str(datetime.datetime.now())+"] Member Join To Group: "+gid+"/"+name+" "+mid+"/"+displayName+"\n\n"+log
      if op.type == 15:
         cl.log("[ 15 ] MEMBER LEAVE TO GROUP")
         mid = op.param2
         gid = op.param1
         name = cl.getGroup(gid).name
         if mid == clMID:
            print("Member Leave To Group: "+gid+"/"+name+" Me")
            log = "["+str(datetime.datetime.now())+"] Member Leave To Group: "+gid+"/"+name+" Me"+"\n\n"+log
         displayName = cl.getContact(mid).displayName
         print("Member Leave To Group: "+gid+"/"+name+" "+mid+"/"+"displayName")
         log = "["+str(datetime.datetime.now())+"] Member Leave To Group: "+gid+"/"+name+" "+mid+"/"+"displayName"+"\n\n"+log
      with open("line.log", "w", encoding="utf-8", errors="ignore") as f:
         f.write(log)


   except Exception as e:
      cl.log(e)

while True:
   try:
      ops = oepoll.singleTrace(count=50)
      if ops is not None:
         for op in ops:
            clBot(op)
            oepoll.setRevision(op.revision)
   except Exception as e:
        cl.log(e)
