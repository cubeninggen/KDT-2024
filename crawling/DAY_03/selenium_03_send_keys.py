from selenium import webdriver
from selenium.webdriver.common.by import By 
import time

# User Agent 정보추가
agent_option= webdriver.ChromeOptions()
user_agent_string= 'Mozilla/5.0'
agent_option.add_argument('user-agent=' + user_agent_string)

driver = webdriver.Chrome(options=agent_option)
driver.get('https://nid.naver.com/nidlogin.login')

# <input>의이름이id를검색
driver.find_element(By.NAME, 'id').send_keys('아이디')
driver.find_element(By.NAME, 'pw').send_keys('패스워드')

#//*[@id="log.login"]
# #driver.find_element(By.XPATH,'//*[@id="log.login"]').click()
driver.find_element(By.ID, 'log.login').click()
time.sleep(3)
driver.quit()