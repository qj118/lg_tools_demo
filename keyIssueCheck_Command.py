from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import sys, getopt
import time

# Get Command Line Parameters
def getInfo(argv):
	dewebsite = ""
	user_name = ""
	password = ""

	try:
		opts, args = getopt.getopt(argv, "hd:u:p:", ["dest=", "user=", "pwd="])
	except getopt.GetoptError:
		print 'Error: keyIssueCheck_Command.py -d <destination>'
		print 'or: keyIssueCheck_Command.py --dest=<destination>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			# destination is SAS address, username is AD accout
			print 'keyIssueCheck_Command.py -d <destination> -u <username> -p <password>'
			print 'or: keyIssueCheck_Command.py --dest=<destination> --user=<username> --pwd=<password>'
		elif opt in ("-d", "--dest"):
			dewebsite = arg
		elif opt in ("-u", "--user"):
			user_name = arg
		elif opt in ("-p", "--pwd"):
			password = arg

	return (dewebsite, user_name, password)

def main():
	destination, user_name, password = getInfo(sys.argv[1:])
	security = False

	options = webdriver.ChromeOptions() # configurate Chrome
	options.add_argument('--start-maximized')

	if destination != "":
		if user_name == "" or password == "" : # default log in
			options.add_argument("--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default")
			browser = webdriver.Chrome(chrome_options = options)
			browser.get(destination)
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
			print "Sorry, you are not the board manager."
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
					select.select_by_value("2")
					comment = browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[1]/textarea' % i)
					comment.send_keys("SMR Version.")
					browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[2]/input' % i).click()
					browser.find_element_by_xpath('//*[@id="issueResultForm"]/div[2]/table/tbody/tr[%d]/td[7]/input[3]' % i).click()

				i = i + 1

			except NoSuchElementException as e:
				print e, i
				break

		time.sleep(10)

if __name__ == '__main__':
	main()

