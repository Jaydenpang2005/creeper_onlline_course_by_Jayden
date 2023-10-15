from operator import inv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

username = str(input("your phone numeber: "))
password = str(input("your password: "))


skipChapter = 1
skipCell = 1
skipNCell = 1

isSkip = str(input("跳過章節?(y/n): "))

if isSkip == "y":

    try:
        skipChapter = int(input("第幾課開始: "))
        skipCell = int(input("第幾章開始: "))
        skipNCell = int(input("第幾節開始: "))
    except:
        print("輸入錯誤")
        exit()

    if skipChapter < 1 or skipCell < 1 or skipNCell < 1:
        print("輸入錯誤")
        exit()

service = Service(executable_path=r'.\chromedriver_v117.exe')
options = webdriver.ChromeOptions()
drive = webdriver.Chrome(service=service, options=options)

response = drive.get("http://passport2.chaoxing.com/login?loginType=4&newversion=true&fid=2880&refer=http://i.mooc.chaoxing.com")

userTextField = drive.find_element("id", 'phone')
pwdTextField = drive.find_element("id", 'pwd')
loginBtn = drive.find_element("id", 'phoneLoginBtn')

userTextField.send_keys(username)  #輸入帳號
pwdTextField.send_keys(password)  #輸入密碼
loginBtn.click()

time.sleep(2)

try:
    stupidframe = drive.find_element("id", 'frame_content')
    drive.switch_to.frame(stupidframe)

except:
    print("********************************************************************************")
    print("登入失敗 :(")
    print("********************************************************************************")
    drive.quit()
    exit()

courses = drive.find_elements(By.CLASS_NAME, "courseItem")

if isSkip == "y" and skipChapter > len(courses):

    print("********************************************************************************")
    print(f"輸入開始章數大於已有章數\n你輸入的課數為：{skipChapter}，已有課數為：{len(courses)}")
    print("********************************************************************************")
    drive.quit()
    exit()



# time.sleep(10000)
# /html/body/div/div[2]/div[3]/ul/li[1]/div[1]/a[1]
# /html/body/div/div[2]/div[3]/ul/li[2]/div[1]/a[1]

for c in range(skipChapter, len(courses) + 1):

    if c != skipChapter:

        stupidframe = drive.find_element("id", 'frame_content')
        drive.switch_to.frame(stupidframe)
    
    xpath = f"/html/body/div/div[2]/div[3]/ul/li[{c}]/div[1]/a[1]"
    course_url = drive.find_element("xpath", xpath) 

    drive.get(course_url.get_attribute('href'))


    time.sleep(2)

    sXpath = f"/html/body/div[5]/div[1]/div[2]/div[3]/div[1]/div[1]/h3/a"

    s_url = drive.find_element(By.XPATH, sXpath)

    drive.get(s_url.get_attribute('href'))


    drive.switch_to.default_content()
  

    cells = drive.find_elements(By.CLASS_NAME, "cells")

    if isSkip == "y" and skipCell > len(cells):

        print("********************************************************************************")
        print(f"輸入開始章數大於已有章數\n你輸入的章數為：{skipCell}，已有章數為：{len(cells)}")
        print("********************************************************************************")

        drive.quit()
        exit()

    ncells_num = []

    for cell in cells:

        ncells = cell.find_elements(By.CLASS_NAME, "ncells")
        ncells_num.append(len(ncells))
    
    


    for cell in range(skipCell, len(cells) + 1):

        if isSkip == "y" and skipNCell > ncells_num[cell - 1]:

            print("********************************************************************************")
            print(f"輸入開始章數大於已有章數\n你輸入的章數為：{skipNCell}，已有章數為：{ncells_num[cell - 1]}")
            print("********************************************************************************")
            drive.quit()
            exit()

        for ncell in range(skipNCell, ncells_num[cell - 1] + 1): 

            isSkip = "n"
            skipNCell = 1
            skipChapter = 1
            skipCell = 1


            ncellDiv = drive.find_element(By.XPATH, f"/html/body/div[4]/div[1]/div[2]/div[1]/div/div[{cell}]/div[{ncell}]/h4/a")
            ncellDiv.click()
            time.sleep(2)

            try:
                videoSpan = drive.find_element(By.XPATH, "//*[@title=\"视频\"]")
            except:
                continue
            videoSpan.click()
            time.sleep(2)

            outVideoFrame = drive.find_element("id", 'iframe')
            drive.switch_to.frame(outVideoFrame)
            inVideoFrame = drive.find_element(By.XPATH, "/html/body/div[2]/div/p/div/iframe")
            drive.switch_to.frame(inVideoFrame)


            startBtn = drive.find_element(By.XPATH, "//*[@id=\"video\"]/button")
            startBtn.click()

            time.sleep(2)

            durationString =  drive.find_element(By.CLASS_NAME, "vjs-duration-display").text.split(":")

            for a in range(len(durationString)):
                durationString[a] = int(durationString[a])

            buf = 10

            duration = durationString[0] * 60 + durationString[1] + buf

            drive.switch_to.default_content()

            time.sleep(duration)
            print("********************************************************************************")
            print(f"已完成第{c}課，第{cell}章，第{ncell}節")
            print("********************************************************************************")
            # time.sleep(10)

    
    backBtn = drive.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/a")
    backBtn.click()

    time.sleep(2)

    lobbyBtn = drive.find_element(By.XPATH, "//*[@id=\"zt_u_abs\"]/p/a[1]")
    lobbyBtn.click()
    time.sleep(5)

print("********************************************************************************")
print("恭喜你已完成，去他媽的網課")
print("********************************************************************************")
drive.quit()
exit()
