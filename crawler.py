import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from markdownify import markdownify
import os
import re
import visual_class
# 登录落谷网

# 创建一个浏览器对象用于访问网页
options = webdriver.ChromeOptions()
# 无头模式
options.add_argument('--headless')
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
# 创建 Chrome WebDriver 对象
driver = webdriver.Chrome(options=options)
driver.get("https://www.luogu.com.cn/")

# 删除没加入Cookies前，网页浏览器对象自行生成的Cookies
driver.delete_all_cookies()

# 给浏览器加入之前保存好的Cookies
with open('cookies.txt', 'r') as f:
    cookies_list = json.load(f)
    for cookie in cookies_list:
        driver.add_cookie(cookie)

# 刷新一下网页，就进入到已经登录的网站了
driver.refresh()

problem_num = []
problem_title = []
problem_difficulty = []

problem_details = []
problem_solution = []

# 爬取题目
def crawl(difficulty , label, num):
    driver.get("https://www.luogu.com.cn/problem/list")
    # 选择难度
    if difficulty == '':
        pass
    else:
        driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/main/div/section/div/section[2]/div/div[1]/div[1]/span').click()  #点出标签
        hard=('入门', '普及-', '普及/提高-', '普及+/提高', '提高+/省选-', '省选/NOI-', 'NOI/NOI+/CTSC')
        for i in range(len(hard)):
            if difficulty == hard[i]:
                driver.find_element(By.XPATH,'/html/body/div[2]/ul/li['+str(i+2)+']').click()
                break

    # 键入搜索框
    time.sleep(1)
    for key in label:
        driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/main/div/section/div/section[2]/div/div[2]/input').send_keys(key + ' ')
    # 键入enter
    driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/main/div/section/div/section[2]/div/div[2]/input').send_keys(Keys.ENTER)
    time.sleep(3)
    # 检索并获取当前题号、标题、难度
    problem_id_s = driver.find_elements(By.CLASS_NAME, 'row')
    num = int(num)
    if num >= len(problem_id_s):
        num = len(problem_id_s)
    for i in range(num):
        problem_num.append(problem_id_s[i].find_elements(By.TAG_NAME, 'span')[1].text)     # 题号
        problem_title.append(problem_id_s[i].find_element(By.CLASS_NAME, 'title').text)  # 标题
        problem_difficulty.append(problem_id_s[i].find_element(By.CLASS_NAME, 'difficulty').text)  # 难度

    # 将搜索条件以“难度-label1-label2-......”的形式命名文件夹
    for j in range(len(label)):
        difficulty += '-' + label[j]

    # 爬取题目详情和题解
    for i in range(num):
        problem_id = problem_num[i]
        # 开始爬取题目
        problem_url = "https://www.luogu.com.cn/problem/" + problem_id
        driver.get(problem_url)
        time.sleep(2)
        # python创建一个problem_id+title.md文件，并生成一级标题“problem_id + title”，获取的网页元素以markdown格式写入文件中
        title = driver.title
        pattern = r'\s+(.*?)-'  # r'^.{5}(.*?)-'
        title = re.search(pattern, title).group(1).strip()
        problem_file_name = f"{problem_id}-{title}.md"
        with open(problem_file_name, 'w', encoding="utf-8") as f:
            f.write('# ' + title + '\n')
            # 获取题目描述
            try:
                element = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/section[2]/section/div/div[2]')
                html = element.get_attribute("innerHTML")
                f.write(markdownify(html))
                problem_details.append(markdownify(html))
            except:
                pass

        # 爬取题解
        solution_url = "https://www.luogu.com.cn/problem/solution/" + problem_id
        driver.get(solution_url)
        time.sleep(2)
        # python创建一个problem_id+title.md文件，并生成一级标题“problem_id + title”，获取的网页元素以markdown格式写入文件中
        solution_file_name = f"{problem_id}-{title}-题解.md"
        with open(solution_file_name, 'w', encoding="utf-8") as f:
            f.write('# ' + title + '\n')
            # 获取第一篇题解
            try:
                element = driver.find_element(By.XPATH,
                                              '//*[@id="app"]/div[2]/main/div/section[2]/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[1]/div/div')
                html = element.get_attribute("innerHTML")
                f.write(markdownify(html))
                problem_solution.append(markdownify(html))
            except:
                f.write('暂无题解')
                problem_solution.append('暂无题解')

        # 将相同problem的md文件放入同一个文件夹中，文件夹名为“problem_id+title”
        folder_name = f"{problem_id}-{title}"  # 构建题目文件夹名
        os.makedirs(folder_name, exist_ok=True)  # 创建题目文件夹（如果不存在）
        os.rename(problem_file_name, os.path.join(folder_name, problem_file_name))  # 移动题目文件至题目文件夹
        os.rename(solution_file_name, os.path.join(folder_name, solution_file_name))  # 移动题解文件至题目文件夹
        # 将“题目编号-标题”文件夹放到“difficulty-label”目录下，若搜索时存在多个label，则以“label1-label2-......”展示
        os.makedirs(difficulty, exist_ok=True)
        os.rename(folder_name, os.path.join(difficulty, folder_name))

def main():
    # 获取筛选条件
    driver.quit()