from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as cs
from passwd import ID, PASSWD

PURPLE 	= '\033[35m'
YELLOW	= '\033[93m'
GREEN	= '\033[92m'
ENDC	= '\033[0m'
STATUS = ["未実施", "未参照", "未提出"]
page = 1
i = 0

chrome_service = cs.Service(executable_path="./chromedriver")
d = webdriver.Chrome(service = chrome_service)
W = open("./memo.txt", "w")

def ft_get_next_page(url):
	global page
	d.get(url)
	print(f"[{page}]", "current page is...", PURPLE, "---", d.title, "---", GREEN, d.current_url, ENDC)
	page += 1

def ft_isinvalid_link(link):
	if link is None:
		return True
	if "form" in link:
		return False
	return True


# homepage
ft_get_next_page("https://newportal2.cst.nihon-u.ac.jp/cst2/lginLgir/")
d.find_element(By.NAME, "userId").send_keys(ID)
d.find_element(By.NAME, "password").send_keys(PASSWD)
# d.find_element(By.NAME, "loginButton").click()
d.execute_script("loginSubmit();")
subjects = d.find_elements(By.XPATH, "//table/tbody/tr/td/a")

links = []
subject_names = []
for subject in subjects:
	onclick = subject.get_attribute('onclick')
	subject_name = subject.text
	if ft_isinvalid_link(onclick):
		continue
	subject_names.append(subject_name)
	links.append(onclick)
for link in links:
	d.execute_script(link)
	d.find_element(By.CSS_SELECTOR, 'input[value="すべて開く"]').click()
	homeworks = d.find_elements(By.XPATH, "//table/tbody/tr")
	W.write(f"----- {subject_names[i]} -----\n")
	for homework in homeworks:
		statuses = homework.find_elements(By.CLASS_NAME, "td02")
		for status in statuses:
			if status.text in STATUS:
				msg = status.text + " : " + homework.find_element(By.CLASS_NAME, "td01").text + " (" + homework.find_element(By.CLASS_NAME, "td03").text + ") "
				print(msg)
				W.write(msg + "\n")
	ft_get_next_page("https://newportal2.cst.nihon-u.ac.jp/cst2/homeHoml/")
	i += 1
	W.write("\n")
W.write(datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') + "現在")
W.close()
d.quit()

