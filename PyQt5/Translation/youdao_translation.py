#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 23:37:29 2018

@author: kindy

python 调用有道翻译api实现简单翻译软件

（1）前往http://ai.youdao.com/注册账号， 登录后台创建应用和实例并完成绑定， 可获得应用ID和密钥等信息，其中应用ID就是appKey（ 注意不是应用密钥）

"""
 
import http.client as httplib
from hashlib import md5
import urllib
import random
import json
import sys
import time
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QAction, qApp
from PyQt5.QtGui import QIcon, QPixmap



qtCreatorFile = "youdao.ui"
# 使用uic加载
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class YouDaoTrans(Ui_MainWindow):
    appKey = '456c555f2a44bee7' # 就是应用ID
    secretKey = 'a0qWrDUZ9ehKPxEXA53Css2RjEWsyFum'    # 就是应用密钥
    def __init__(self):
        Ui_MainWindow.__init__(self)
        super().__init__()
        self.httpClient = None
        self.myurl = '/api'
        self.q = self.transInput.text()          # 查询的单词
        self.fromLang = self.transFrom.currentText()     # 源语言
        self.toLang = self.transTo.currentText()   # 目标语言
        self.salt = random.randint(1, 65536) # 随机数
    def get_translation(self):
        
        sign = appKey+q+str(salt)+secretKey     # 签名
        m1 = md5()
        m1.update( sign.encode() )
        sign = m1.hexdigest()       # 计算签名的哈希值
        self.myurl = self.myurl+'?appKey='+appKey+'&q='+self.q+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(self.salt)+'&sign='+sign
 
        try:
            httpClient = httplib.HTTPConnection('openapi.youdao.com')
            httpClient.request('GET', self.myurl)
 
            #response是HTTPResponse对象
            response = httpClient.getresponse()
            res = response.read().decode()
            hjson = json.loads(res)
            #print (hjson['basic']['explains'])
            exp = str(hjson['basic']['explains'])
            print( type(exp) )
            print(exp.replace(',','\r\n'))
        
        except Exception as e:
            print (e)
        finally:
            if httpClient:
                httpClient.close()


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        super().__init__()
        self.initUI()       # 调用自定义的UI初始化函数initUI()
        self.initYouDao()
    
    def initYouDao(self):
        self.appKey = '456c555f2a44bee7' # 就是应用ID
        self.secretKey = 'a0qWrDUZ9ehKPxEXA53Css2RjEWsyFum'    # 就是应用密钥
        self.httpClient = None
        self.myurl = '/api'
        self.q = self.transInput.toPlainText()          # 获取控件内容，得到询的内容
        self.fromLang =  self.lang_transform (self.transFrom.currentText())     # 源语言
        self.toLang = self.lang_transform(self.transTo.currentText() )  # 目标语言
        self.salt = random.randint(1, 65536) # 随机数
    
    def lang_transform(self, lang):
        '''
        tranform the language into correct format that ai.youdao.com accepted
        中文	zh-CHS
        日文	ja
        英文	EN
        韩文	ko
        法文	fr
        俄文	ru
        葡萄牙文	pt
        西班牙文	es
        '''
        if lang == "Chinese":
            return "zh-CHS"
        if lang == "Japanease":
            return "ja"
        if lang == "English":
            return "EN"
        if lang == "Korea":
            return "ko"
        if lang == "Russia":
            return "ru"
        if lang == "French":
            return "fr"
        

    def initUI(self):
        '''
        Initialize the window's UI
        '''
        self.setupUi(self)
        self.setWindowTitle("Dict Translate")
        self.setWindowIcon(QIcon("translate.png"))   # 设置图标，linux下只有任务栏会显示图标
        
        self.initMenuBar()      # 初始化菜单栏
        self.initToolBar()      # 初始化工具栏
        self.initButton()       # 初始化按钮
        
        self.show()             # 显示
    
    def initMenuBar(self):
        '''
        初始化菜单栏
        '''
        menubar = self.menuBar()
        #self.actionExit.triggered.connect(qApp.quit)    # 按下菜单栏的Exit按钮会退出程序
        #self.actionExit.setStatusTip("退出程序")         # 左下角状态提示
        #self.actionExit.setShortcut('Ctrl+Q')           # 添加快捷键
        exitAct = QAction(QIcon('exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        
        fileMenu = menubar.addMenu('&Help')
        
    def initToolBar(self):
        '''
        初始化工具栏
        创建一个QAction实例exitAct，然后添加到designer已经创建的默认的工具栏toolBar里面
        '''
        exitAct = QAction(QIcon('exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        
        self.toolBar.addAction(exitAct)
        
    def initButton(self):
        '''
        
        '''
        self.btnClear.clicked.connect(self.clearButton_callback) # 按下按钮调用回调函数
        self.btnClear.setToolTip("清除文本输入内容")                     # 设置提示
        #self.btnBrowse.setStyleSheet("{border-image: url(/home/kindy/Files/python/gui/pyq/play.ico);}") # 此代码没有效果
        self.btnExchange.clicked.connect(self.exchangeButton_callback)      # 一旦按下按钮，连接槽函数进行处理
        self.btnExchange.setToolTip("转换翻译语言")
        
        self.btnTranslate.clicked.connect(self.transButton_callback)
        self.btnTranslate.setToolTip("翻译内容")
        
    def clearButton_callback(self):
        self.transInput.clear()
        self.transInput.setFocus()
        
    def exchangeButton_callback(self):
        pass
    
    def transButton_callback(self, filename):
        '''
        调用有道词典API进行文字识别
        
        '''
        start = time.time()
        end = time.time()
        trans = self.get_translation( self.transInput.toPlainText())
#        self.transOutput.setPlainText(self.transInput.toPlainText()+self.fromLang)
        self.transOutput.setPlainText(trans)
        self.transOutput.setStatusTip("翻译时间：%.2fs"%(end-start))
        
    def get_translation(self, query):
        
        sign = self.appKey + query + str(self.salt) + self.secretKey     # 签名
        m1 = md5()
        m1.update( sign.encode() )
        sign = m1.hexdigest()       # 计算签名的哈希值
        self.myurl = self.myurl+'?appKey=' + self.appKey + '&q='+ urllib.parse.quote(query) + '&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(self.salt)+'&sign='+sign
        try:
            httpClient = httplib.HTTPConnection('openapi.youdao.com')
            httpClient.request('GET', self.myurl)
 
            #response是HTTPResponse对象
            response = httpClient.getresponse()
            res = response.read().decode()

            hjson = json.loads(res)

            exp = str(hjson['basic']['explains'])
            
            exp = exp.replace(',','\r\n')
            exp = exp.replace('[',' ')
            exp = exp.replace(']',' ')
            exp = exp.replace('\'',' ')
            
            return exp
        
        except Exception as e:
            print (e)
        finally:
            if httpClient:
                httpClient.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
    