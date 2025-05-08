{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.by import By\n",
    "\n",
    "driver = webdriver.Chrome()\n",
    "driver.get(\"https://naver.com\")\n",
    "\n",
    "driver.find_element(By.CSS_SELECTOR,\".MyView-module__link_login___HpHMW\").click()\n",
    "\n",
    "while True:\n",
    "    pass"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.by import By\n",
    "import time\n",
    "\n",
    "driver = webdriver.Chrome()\n",
    "driver.get(\"https://naver.com\")\n",
    "\n",
    "driver.find_element(By.CSS_SELECTOR,\".MyView-module__link_login___HpHMW\").click()\n",
    "\n",
    "try:\n",
    "    while True:\n",
    "        # driver 객체가 여전히 유효한지 검사\n",
    "        driver.title  # 강제로 호출해서 예외 발생 유도\n",
    "        time.sleep(1)\n",
    "except:\n",
    "    print(\"브라우저가 닫혔습니다. 스크립트를 종료합니다.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.chrome.options import Options\n",
    "\n",
    "options = Options()\n",
    "options.add_experimental_option(\"detach\", True)\n",
    "\n",
    "driver = webdriver.Chrome(options=options)\n",
    "driver.get(\"https://www.naver.com\")\n",
    "\n",
    "driver.find_element(By.CSS_SELECTOR,\".MyView-module__link_login___HpHMW\").click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.chrome.options import Options\n",
    "from selenium.webdriver.common.by import By\n",
    "from selenium.webdriver.common.keys import Keys\n",
    "import pyperclip\n",
    "\n",
    "options = Options()\n",
    "options.add_experimental_option(\"detach\", True)\n",
    "\n",
    "ID = input(\"아이디를 입력하세요.\")\n",
    "PW = input(\"비밀번호를 입력하세요.\")\n",
    "\n",
    "driver = webdriver.Chrome(options=options)\n",
    "driver.get(\"https://www.naver.com\")\n",
    "\n",
    "driver.find_element(By.CSS_SELECTOR, \".MyView-module__link_login___HpHMW\").click()\n",
    "\n",
    "driver.find_element(By.CSS_SELECTOR, \"#id\").click()\n",
    "pyperclip.copy(ID)\n",
    "driver.find_element(By.CSS_SELECTOR, \"#id\").send_keys(Keys.CONTROL + 'v')\n",
    "\n",
    "driver.find_element(By.CSS_SELECTOR, \"#pw\").click()\n",
    "pyperclip.copy(PW)\n",
    "driver.find_element(By.CSS_SELECTOR, \"#pw\").send_keys(Keys.CONTROL + 'v')\n",
    "\n",
    "driver.find_element(By.CSS_SELECTOR, \".btn_login.next_step.nlog-click\").click()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.by import By\n",
    "\n",
    "#searchWord = input(\"검색할 단어를 입력하세요.\")\n",
    "searchWord = \"빵\"\n",
    "\n",
    "driver = webdriver.Chrome()\n",
    "#driver.get(f\"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query={searchWord}\")\n",
    "driver.get(\"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=\" + searchWord)\n",
    "\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "base",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
