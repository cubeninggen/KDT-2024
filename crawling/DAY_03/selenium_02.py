from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('http://www.pythonscraping.com/pages/warandpeace.html')
driver.implicitly_wait(5)

# find_element(By.CLASS_NAME, '클래스이름'): 하나의클래스이름검색
name = driver.find_element(By.CLASS_NAME, "green")
print(name.text)

print('-' * 20)

# find_elements(By.CLASS_NAME, '클래스이름'): 해당클래스이름을모두검색
name_list= driver.find_elements(By.CLASS_NAME, "green")
for name in name_list:
    print(name.text)

driver.quit()