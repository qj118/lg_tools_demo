import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import getopt
import time

class ShowWindow(QtWidgets.QWidget):

	def __init__(self):
		super(ShowWindow, self).__init__()
		self.initUI()

	def initUI(self):
		self.label_web = QtWidgets.QLabel("SAS Board")
		self.lineEdit_web = QtWidgets.QLineEdit()
		layout_web = QtWidgets.QHBoxLayout()
		layout_web.addWidget(self.label_web)
		layout_web.addWidget(self.lineEdit_web)

		self.label_ad = QtWidgets.QLabel("AD Account")
		self.lineEdit_ad = QtWidgets.QLineEdit()
		layout_ad = QtWidgets.QHBoxLayout()
		layout_ad.addWidget(self.label_ad)
		layout_ad.addWidget(self.lineEdit_ad)

		self.label_password = QtWidgets.QLabel("Password")
		self.lineEdit_password = QtWidgets.QLineEdit()
		layout_password = QtWidgets.QHBoxLayout()
		layout_password.addWidget(self.label_password)
		layout_password.addWidget(self.lineEdit_password)

		self.label_comment = QtWidgets.QLabel("Comment")
		self.lineEdit_comment = QtWidgets.QLineEdit()

		self.groupBox_comment = QtWidgets.QGroupBox("Choose One")
		self.radio1 = QtWidgets.QRadioButton("EMR")
		self.radio2 = QtWidgets.QRadioButton("SMR")
		self.radio3 = QtWidgets.QRadioButton("Factory")
		self.radio4 = QtWidgets.QRadioButton("S/W Event")
		self.radio5 = QtWidgets.QRadioButton("Pre")
		self.radio6 = QtWidgets.QRadioButton("Test")
		self.radio1.setChecked(False)
		self.radio2.setChecked(True)
		self.radio3.setChecked(False)
		self.radio4.setChecked(False)
		self.radio5.setChecked(False)
		self.radio6.setChecked(False)
		radio_layout = QtWidgets.QHBoxLayout()
		radio_layout.addWidget(self.radio1)
		radio_layout.addWidget(self.radio2)
		radio_layout.addWidget(self.radio3)
		radio_layout.addWidget(self.radio4)
		radio_layout.addWidget(self.radio5)
		radio_layout.addWidget(self.radio6)
		self.groupBox_comment.setLayout(radio_layout)

		layout_comment_1 = QtWidgets.QVBoxLayout()
		layout_comment_1.addWidget(self.lineEdit_comment)
		layout_comment_1.addWidget(self.groupBox_comment)
		layout_comment = QtWidgets.QHBoxLayout()
		layout_comment.addWidget(self.label_comment)
		layout_comment.addLayout(layout_comment_1)

		self.label_security = QtWidgets.QLabel("Apply Google Security Patch?")
		self.groupBox_security = QtWidgets.QGroupBox("Do you want?")
		self.radio_y = QtWidgets.QRadioButton("Yes")
		self.radio_n = QtWidgets.QRadioButton("No")
		self.radio_y.setChecked(False)
		self.radio_n.setChecked(True)
		radio_layout_security = QtWidgets.QHBoxLayout()
		radio_layout_security.addWidget(self.radio_y)
		radio_layout_security.addWidget(self.radio_n)
		self.groupBox_security.setLayout(radio_layout_security)
		layout_security = QtWidgets.QHBoxLayout()
		layout_security.addWidget(self.label_security)
		layout_security.addWidget(self.groupBox_security)

		self.pushButton_start = QtWidgets.QPushButton("Start!")
		self.pushButton_start.clicked.connect(self.startCheck) # When the button is clicked, call startCheck()

		self.label_author = QtWidgets.QLabel("Developer: Qu Jin")
		self.label_contact = QtWidgets.QLabel("Email: jin.qu@lge.com")
		self.label_version = QtWidgets.QLabel("Version: 1.0.0")
		layout_copyright = QtWidgets.QHBoxLayout()
		layout_copyright.addWidget(self.label_author)
		layout_copyright.addWidget(self.label_contact)
		layout_copyright.addWidget(self.label_version)

		layout = QtWidgets.QVBoxLayout()
		layout.addLayout(layout_web)
		layout.addLayout(layout_ad)
		layout.addLayout(layout_password)
		layout.addLayout(layout_comment)
		layout.addLayout(layout_security)
		layout.addWidget(self.pushButton_start)
		layout.addLayout(layout_copyright)

		self.setLayout(layout)
		self.setWindowTitle("Key Issue Check")
		self.show()

	def getComment(self): # Get user's choice
		comment_choose = ""
		if(self.radio1.isChecked()):
			comment_choose = "1"
		if(self.radio2.isChecked()):
			comment_choose = "2"
		if(self.radio3.isChecked()):
			comment_choose = "3"
		if(self.radio4.isChecked()):
			comment_choose = "4"
		if(self.radio5.isChecked()):
			comment_choose = "5"
		if(self.radio6.isChecked()):
			comment_choose = "6"
		return comment_choose

	def getSecurityFlag(self):
		flag = False
		if(self.radio_n.isChecked()):
			flag = False
		if(self.radio_y.isChecked()):
			flag = True
		return flag

	def startCheck(self):
		web_text = self.lineEdit_web.text()
		ad_text = self.lineEdit_ad.text()
		password_text = self.lineEdit_password.text()
		comment_text = self.lineEdit_comment.text()
		comment_choose = self.getComment()
		flag = self.getSecurityFlag()

		if web_text == "" or comment_text == "":
			QtWidgets.QMessageBox.information(self, "Empty", "The SAS Board and Comment can't be empty.")
		else:
			self.runScript(web_text, ad_text, password_text, comment_text, comment_choose, flag)

	def runScript(self, destination, user_name, password, comment_text, comment_choose, security):
		options = webdriver.ChromeOptions() # configurate Chrome
		options.add_argument('--start-maximized')

		if user_name == "" or password == "" : # default log in
			options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default")
			browser = webdriver.Chrome(chrome_options = options)
			browser.get(destination)
			try:
				ad = browser.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[1]/td[3]/input')
				QtWidgets.QMessageBox.information(self, "Warning", "Default configuration has no user information, please log in.")
				browser.close()
				return
			except NoSuchElementException:
				time.sleep(3)
		else: # command log in
			browser = webdriver.Chrome(chrome_options = options)
			browser.get(destination)
			ad = browser.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[1]/td[3]/input')
			ad.send_keys(user_name)
			pwd = browser.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[3]/td[3]/input')
			pwd.send_keys(password)
			browser.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[1]/td[5]/input').click()
			time.sleep(20)

		# click "Key Issue Check" button, but if you are not a board manager you can't check the key issue.
		try:
			browser.find_element_by_xpath('//*[@id="boardDetailBottomBtn"]/tbody/tr/td[10]/input').click()
			time.sleep(3)
		except NoSuchElementException:
			QtWidgets.QMessageBox.information(self, "Warning", "You are not the board manager.")
			browser.close()
			return

		# click "Key Issue Manager" button
		browser.find_element_by_xpath('//*[@id="keyIssueManagerBtn"]').click()
		time.sleep(3)

		# If you want to apply all of Google Security Patch, you should set 'security' to True.
		if security:
			browser.find_element_by_xpath('//*[@id="googleSecurityManager"]').click()
			time.sleep(3)
			browser.find_element_by_xpath('//*[@id="keyIssueManagerTR"]/td[1]/input').click()
			browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[1]/table/tbody/tr[2]/td[1]/input[1]').click()
			browser.find_element_by_xpath('//*[@id="googleSecurityManager"]').click()
			time.sleep(3)

		# Loop processing until the corresponding elements are not found
		i = 2
		while i > 0:
			try:
				status = browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]' % i).find_element_by_tag_name('font').text
				if status == "Uncheck" or status == "Recheck": # Only deal with uncheck key issue
					select = Select(browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[1]/td/select' % i))
					select.select_by_value(comment_choose)
					comment = browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[1]/textarea' % i)
					comment.send_keys(comment_text)
					browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[2]/input' % i).click()
					browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]/td[7]/input[3]' % i).click()

				i = i + 1

			except NoSuchElementException as e:
				QtWidgets.QMessageBox.information(self, "Done", "Success!")
				browser.close()
				break

		time.sleep(10)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	form = ShowWindow()
	sys.exit(app.exec_())
