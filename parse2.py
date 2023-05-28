from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json

# 创建一个Chrome浏览器实例

# 创建一个Chrome浏览器实例
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# 打开淘宝网
driver.get("https://www.taobao.com")

# 检查是否有保存的cookie信息
try:
    with open("taobao_cookies.json", "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
except FileNotFoundError:
    # 等待用户在终端输入OK表示登录成功
    input("请在浏览器中登录淘宝网，然后在终端输入OK表示登录成功：")
    # 保存cookie信息
    cookies = driver.get_cookies()
    with open("taobao_cookies.json", "w") as f:
        json.dump(cookies, f)

# 在搜索框中输入搜索词
key_search = '银涛右归胶囊'
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(key_search)
search_box.send_keys(Keys.RETURN)

# 获取搜索结果
wait = WebDriverWait(driver, 10)
results = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='Card--doubleCardWrapper--L2XFE73']")))
df = pd.DataFrame(columns=['商品名', '价格', '销量', '店名', '地区', '链接'])
# 打印搜索结果
for i, result in enumerate(results):
    name = result.find_element(By.XPATH, ".//div[@class='Title--title--jCOPvpf']/span").text
    price = result.find_element(By.XPATH, ".//span[@class='Price--priceInt--ZlsSi_M']").text
    sale_num = result.find_element(By.XPATH, ".//span[@class='Price--realSales--FhTZc7U']").get_attribute('textContent')
    link = result.get_attribute("href")
    shop_name = result.find_element(By.XPATH, ".//a[@class='ShopInfo--shopName--rg6mGmy']").text
    locations = result.find_elements(By.XPATH, ".//span[@class='Price--procity--_7Vt3mX']")
    location = ' '.join([x.text for x in locations])
    df.loc[i] = [name, price, sale_num, shop_name, location, link]
    print(name, price, sale_num, shop_name, location, link)
# df.to_csv(key_search + '.csv', index=False)
df.to_excel(key_search + '.xlsx', index=False)
# 关闭浏览器
driver.close()
