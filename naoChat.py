# -*- coding: utf-8 -*-
import aiml,os,globalVar
from tools import textTools
from tools import query,voice2txt
from naoMotion import Motion


def getVoiceMsg(motion):
    motion.recordSound("record.wav", "../sound/sound.wav")
    txt = voice2txt.wav2txt('../sound/sound.wav')
    return txt


def chat(motion):
    os.chdir(globalVar.CHAT_PATH)
    robot = aiml.Kernel()
    robot.learn("std-startup.xml")
    robot.respond('LOAD AIML TEST1')
    # if os.path.isfile("brain.brn"):
    #     robot.bootstrap(brainFile="brain.brn")
    # else:
    #     robot.bootstrap(learnFiles="std-startup.xml", commands="load aiml test1")
    #     robot.saveBrain("brain.brn")
    message = raw_input("Enter your message>> ")
    # message = u'左转'

    # 语音识别出现无法识别的问题
    # message = getVoiceMsg(motion).strip()
    if message == None:
        motion.say(u'我听不懂')
        return


    respond = ''
    if message == "quit":#仅用于测试时
        exit()
    # elif message == "save":
    #     robot.saveBrain('brain.brn')
    else:
        respond = robot.respond(message)
        print respond
        respond = textTools.subReplace(respond.decode('utf8'))
        print respond
        print 'chat responce:' + respond

    if respond.__contains__('$'):
        motion.say(u'好的')
        doInstruction(respond.replace('$',''),motion)
        return

    if respond.__contains__('#NoMatchingTemplate'):
        # print 'msg: ', message
        ask(message,motion)
        return

    motion.say(respond)
#问答系统
def ask(question,motion):
    # str = textTools.subReplace(question)
    str = question
    print 'str', str
    queryWords = textTools.wordSegment(str)
    print 'query words :  '+ queryWords.encode('utf8')
    result = query.query(queryWords)

    print 'result: ', result
    if result is None:
        motion.say(u'我听不懂')
    else:
        result = textTools.subReplace(result.decode('utf8'))
        motion.say(result)

def doInstruction(mode,motion):
    if mode == '0':
        motion.turnleft()
    elif mode == '1':
        motion.turnright()
    elif mode == '2':
        motion.turnback()
    elif mode == '3':
        motion.goahead()
    elif mode == '4':
        motion.stop()
    elif mode == '5':
        motion.sitdown()
    elif mode == '6':
        motion.standup()
    else:
        motion.dance()

