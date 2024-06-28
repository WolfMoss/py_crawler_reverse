import asyncio
import json
import traceback
import random
from playwright.async_api import async_playwright
import os
import subprocess
import base64
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import re
with open('config.json', 'r') as f:
    config = json.load(f)

# 保存当前工作目录
original_directory = os.getcwd()
# 切换到目标目录
target_directory = r"C:\Program Files (x86)\Microsoft\Edge\Application"
os.chdir(target_directory)
# 构建命令和参数列表
command = "msedge.exe"

#配置--------------------------------------
tjuser = config['tjuser']
tjpsw = config['tjpsw']
#-----------------------------------------

urls = {
1: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=eacf172b",
5: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=275802a2",
7: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=69a357b6",
10: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=8c8ea2b7",
15: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=cb7354c5",
17: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=e997e4eb",
20: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=08c53ae6",
25: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=2e52a015",
27: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=483d7b8d",
30: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=8c238f88",
35: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=cc98f9f2",
37: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=e8726b6a",
40: "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=03acb380"
}

def base64_api(uname, pwd, img, typeid):
    response = requests.get(img)  # 从URL获取图片内容
    base64_data = base64.b64encode(response.content)  # 编码图片内容为base64
    b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    ers = requests.post("http://api.ttshitu.com/predict", json=data)
    result = json.loads(ers.text)
    if result['success']:
        return result["data"]["result"]
    else:
        #！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]
    return ""

#随机弹幕
def random_danmu(i):
    danmu_content = [
        "好菜啊，这个游戏太难了！",
        "666，主播太强了！",
        "快来围观，这里有个大神在玩游戏！",
        "哈哈，主播被打败了！",
        "加油加油，拿下这个BOSS！",
        "这个技能好厉害，我也想学！",
        "看着主播打游戏，心情好舒畅！",
        "主播的操作简直就是艺术！",
        "新来的观众，点个关注支持下！",
        "主播好帅啊，一言不合就开启操作秀！"
    ]

    return danmu_content[i]


def get_time_beijing(url):
    response = requests.get(url)
    if response.status_code == 200:
        date_time = response.headers['Date']
        date_time_obj = datetime.strptime(date_time, '%a, %d %b %Y %H:%M:%S GMT')
        gmt_time = date_time_obj.replace(tzinfo=ZoneInfo("UTC"))
        beijing_time = gmt_time.astimezone(ZoneInfo("Asia/Shanghai"))
        return beijing_time
    else:
        return None

def calculate_day_difference(start_date_str):
    start_date = datetime.strptime(start_date_str, '%Y%m%d')
    current_date = datetime.now()  # 获取当前日期和时间
    current_date_str = current_date.strftime('%Y%m%d')  # 格式化当前日期为字符串
    current_date = datetime.strptime(current_date_str, '%Y%m%d')  # 再次转换以去除时间部分
    return (current_date - start_date).days + 1

async def open_browser_fans(userobj):
    try:
        usertype = sorted(userobj.keys())[0]
        username = userobj[usertype]


        zb_zbj_url = config['zb_zbj_url']

        async with async_playwright() as p:

            psw = userobj[sorted(userobj.keys())[1]]
            browser = await p.chromium.connect_over_cdp(f"http://localhost:{userobj['port']}")
            context = browser.contexts[0]
            # browser = await p.chromium.launch_persistent_context(
            #     user_data_dir='userdata/'+username,
            #     accept_downloads=True,
            #     headless=False,
            #     bypass_csp=True,
            #     #executable_path=edge_path
            #     channel="msedge",
            #     args=['--start-maximized',"--disable-blink-features=AutomationControlled"],viewport={"width": 1920, "height": 1080}, no_viewport=True
            #
            # )

            await context.add_init_script(path='stealth.min.js')
            page = await context.new_page()

            await page.goto('https://space.bilibili.com/')


            dengdai = True
            shurumima = False
            while dengdai:
                await page.wait_for_load_state('networkidle')
                login_button = await page.query_selector_all('input[placeholder="请输入账号"]')
                if login_button:
                    #print(username,"尚未登录")
                    if not shurumima:
                        await page.fill('input[placeholder="请输入账号"]', username)
                        await page.fill('input[placeholder="请输入密码"]', psw)
                        shurumima=True
                    await page.wait_for_timeout(1000)
                else:
                    print(username,"已登录或元素不存在")
                    dengdai = False
            print(username,"登录成功")

            #跳转到直播间
            await page.goto(zb_zbj_url)

            await page.wait_for_timeout(3000)


            while True:


                #print(username,'开始获取当前时间')
                # 获取当前时间
                current_time_str  = await page.evaluate("new Date().toLocaleTimeString()")
                current_time = datetime.strptime(current_time_str, '%H:%M:%S').time()
                if current_time >datetime.strptime('0:05:00', '%H:%M:%S').time() and current_time < datetime.strptime('4:00:00', '%H:%M:%S').time():
                    print(username,'到第二天发弹幕6条，牛娃牛蛙1个')

                    # 循环6次
                    for i in range(8):
                        # 输入文字到当前焦点所在的元素（文本框）
                        element_handle = await page.query_selector('textarea[placeholder="发个弹幕呗~"]')
                        await element_handle.click()
                        await page.keyboard.type(random_danmu(i));
                        await page.click('span.txt:text("发送")')
                        await page.wait_for_timeout(2000)

                    xpath_selector = '//div[@data-v-1cf64c42="" and @data-v-bd2cfcf2="" and contains(@class, "gift-panel-switch") and contains(@class, "pointer")]'
                    await page.locator(xpath_selector).nth(1).click()
                    await page.wait_for_timeout(1000)
                    await page.locator('div[data-report*="牛哇牛哇"]').nth(1).click()
                    await page.wait_for_timeout(1000)
                    await page.click('.user-click-send-area')

                    break
                else:
                    #print(username,'还没到第二天')
                    await asyncio.sleep(1)

            try:
                # 保持浏览器和页面打开状态
                while True:
                    await asyncio.sleep(1)  # 防止阻塞事件循环
            except KeyboardInterrupt:
                print("Stopped listening for image requests.")
                await browser.close()
    except Exception as e:
        traceback.print_exc()

async def open_browser_zb(userobj):
    try:
        username = userobj['zb_user']

        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f"http://localhost:{userobj['port']}")
            context = browser.contexts[0]
            # browser = await p.chromium.launch_persistent_context(
            #     user_data_dir='userdata/'+ username,
            #     accept_downloads=True,
            #     headless=False,
            #     bypass_csp=True,
            #     #executable_path=edge_path
            #     channel="msedge",
            #     args=['--start-maximized',"--disable-blink-features=AutomationControlled"],viewport={"width": 1920, "height": 1080}, no_viewport=True
            # )


            await context.add_init_script(path='stealth.min.js')
            page0 = context.pages[0]

            page = await context.new_page()
            await page.goto('https://space.bilibili.com/')

            # 测试验证码+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # await page0.goto('https://space.bilibili.com/')
            # await page0.wait_for_load_state('networkidle')
            # await page0.fill('input[placeholder="请输入账号"]', username)
            # await page0.fill('input[placeholder="请输入密码"]', userobj['zb_user_psw'])
            # await page0.wait_for_selector('div[class="btn_primary "]', state="visible")
            # await page0.locator('div[class="btn_primary "]').nth(0).click()
            # await page0.wait_for_timeout(2000)
            #
            # # 定位到具有class="geetest_item_wrap"的div
            # items = page0.locator('div.geetest_item_wrap')
            # # 遍历所有找到的元素
            # for i in range(await items.count()):
            #     try:
            #         imgelement = items.nth(i)
            #         # 获取每个元素的data-attribute属性值
            #         attribute_value = await items.nth(i).get_attribute('style')
            #         print(f'第{i + 1}个元素的data-attribute属性值是: {attribute_value}')
            #
            #         # 使用正则表达式提取URL
            #         url_match = re.search(r'url\("([^"]+)"\)', attribute_value)
            #         if url_match:
            #             background_url = url_match.group(1)
            #             if "https://static.geetest.com/captcha_v3" in background_url:
            #                 print("提取到的URL是:", background_url)
            #                 break
            #         else:
            #             print("没有找到匹配的URL")
            #     except Exception as e:
            #         print("获取style属性值时出错:", e)
            #
            # imageCaptchaCode = base64_api(uname=tjuser, pwd=tjpsw, img=background_url,typeid=27)
            # pots=[]
            # imgpos = imageCaptchaCode.split("|")
            # for imgpotstr in imgpos:
            #     imgpotarr = imgpotstr.split(",")
            #     pots.append([int(imgpotarr[0]) -10,int(imgpotarr[1])-10])
            # print(pots)
            # for pot in pots:
            #     #在1000~3000随机一个值
            #     await page0.wait_for_timeout(random.randint(1000,3000))
            #     # 步骤2: 获取元素的边界框
            #     box = await imgelement.bounding_box()
            #     # 步骤4: 计算出最终的点击坐标
            #     click_x = box['x'] + pot[0]
            #     click_y = box['y'] + pot[1]
            #     # 步骤5: 点击坐标
            #     await page0.mouse.click(click_x, click_y)
            #
            # await page0.wait_for_timeout(random.randint(1000, 3000))
            # await page0.click('.geetest_commit_tip')

            # 测试验证码------------------------------------------------------------

            dengdai = True
            shurumima = False
            while dengdai:
                await page.wait_for_load_state('networkidle')
                login_button = await page.query_selector_all('input[placeholder="请输入账号"]')
                if login_button:
                    #print(username,"尚未登录")
                    if not shurumima:
                        await page.fill('input[placeholder="请输入账号"]', username)
                        await page.fill('input[placeholder="请输入密码"]', userobj['zb_user_psw'])
                        shurumima = True
                    await page.wait_for_timeout(1000)
                else:
                    print(username,"已登录或元素不存在")
                    dengdai = False
            print(username,"登录成功")

            #循环判断当前时间，是否超过0:59:56秒，如果超过则点击按钮，如果超过1:00:05秒，则退出循环
            while True:
                #print(username,'开始获取当前时间')
                # 获取当前时间
                current_time_str  = await page.evaluate("new Date().toLocaleTimeString()")
                current_time = datetime.strptime(current_time_str, '%H:%M:%S').time()
                if current_time >datetime.strptime('0:57:00', '%H:%M:%S').time() and current_time < datetime.strptime('2:00:00', '%H:%M:%S').time():
                    # 先领取一个日常奖励过验证+++++++++++++++++++++++++++++++++++++++++
                    await page0.goto(config['zb_jl_url'])
                    await page0.locator('div[data-fid="MJQhIGtbTzf"]').nth(0).click()

                    second_a_locator = page0.locator(
                        'div[style="position: absolute; top: 50%; left: 50%; margin-top: -475px; margin-left: -450px; width: 900px; height: 950px; overflow: auto;"] a:nth-child(5)')

                    # 在点击前设置监听器来捕获新页面
                    async with context.expect_page() as new_page_info:
                        await second_a_locator.click()

                    # 获取新页面对象
                    new_page = await new_page_info.value
                    await new_page.wait_for_timeout(2000)
                    await new_page.click('section.tool-wrap') #领取奖励
                    await new_page.wait_for_timeout(2000)
                    # 定位到具有class="geetest_item_wrap"的div
                    items = new_page.locator('div.geetest_item_wrap')
                    print("验证码元素师数量===",await items.count())
                    # 遍历所有找到的元素
                    for i in range(await items.count()):
                        try:
                            imgelement = items.nth(i)
                            # 获取每个元素的data-attribute属性值
                            attribute_value = await items.nth(i).get_attribute('style')
                            print(f'第{i + 1}个元素的data-attribute属性值是: {attribute_value}')

                            # 使用正则表达式提取URL
                            url_match = re.search(r'url\("([^"]+)"\)', attribute_value)
                            if url_match:
                                background_url = url_match.group(1)
                                if "https://static.geetest.com/captcha_v3" in background_url:
                                    print("提取到的URL是:", background_url)
                                    break
                            else:
                                print("没有找到匹配的URL")
                        except Exception as e:
                            print("获取style属性值时出错:", e)

                    imageCaptchaCode = base64_api(uname=tjuser, pwd=tjpsw, img=background_url, typeid=27)
                    pots = []
                    imgpos = imageCaptchaCode.split("|")
                    for imgpotstr in imgpos:
                        imgpotarr = imgpotstr.split(",")
                        pots.append([int(imgpotarr[0]) - 10, int(imgpotarr[1]) - 10])
                    print(pots)
                    for pot in pots:
                        # 在1000~3000随机一个值
                        await new_page.wait_for_timeout(random.randint(300, 800))
                        # 步骤2: 获取元素的边界框
                        box = await imgelement.bounding_box()
                        # 步骤4: 计算出最终的点击坐标
                        click_x = box['x'] + pot[0]
                        click_y = box['y'] + pot[1]
                        # 步骤5: 点击坐标
                        await new_page.mouse.click(click_x, click_y)

                    await new_page.wait_for_timeout(random.randint(300, 800))
                    await new_page.click('.geetest_commit_tip')

                    # 先领取一个日常奖励过验证------------------------------------------

                    #print("到第二天",current_time)
                    #判断当前是第几天
                    start_date_str = '20240605'  # 定义起始日期
                    day_difference = calculate_day_difference(start_date_str)
                    #print('day_difference===',current_time,day_difference)
                    if day_difference in urls:


                        beijing_time = get_time_beijing('https://www.bilibili.com/favicon.ico')
                        start_time = beijing_time.strftime('%H:%M:%S')
                        print('当前时间===', start_time)
                        start_time = datetime.strptime(start_time, '%H:%M:%S')
                        end_time = datetime.strptime("00:59:57", '%H:%M:%S')  # 设定结束时间

                        time_difference = end_time - start_time  # 计算时间差
                        # 对于 page.wait_for_timeout(),我们需要时间差的毫秒数
                        wait_time = time_difference.total_seconds() * 1000
                        print("wait_time===", wait_time)
                        await page.wait_for_timeout(wait_time)

                        while True:

                            print("时间到了，刷新按钮",start_time)
                            await page.goto(urls[day_difference])
                            # 点击按钮
                            # await page.evaluate(
                            #     '''() => {document.querySelector("#app > div > div.home-wrap.select-disable > section.tool-wrap > div").click();}''')

                            asyncio.create_task(page.evaluate('''() => {
                                    var button = document.querySelector("#app > div > div.home-wrap.select-disable > section.tool-wrap > div");
                                    setInterval(function() { button.click(); }, 100);
                                }'''))

                            # 等待 0.1 秒
                            await page.wait_for_timeout(100)

                            current_time_str = await page.evaluate("new Date().toLocaleTimeString()")
                            current_time = datetime.strptime(current_time_str, '%H:%M:%S').time()
                            breaktime = datetime.strptime('1:10:00', '%H:%M:%S').time()
                            #print("时间没到",current_time)
                            if current_time >= breaktime:
                                print("时间到了，退出循环",current_time)
                                break
                    break
                else:
                    #print(username,'还没到第二天')
                    #await asyncio.sleep(1)
                    await page.wait_for_timeout(1000)


            # # 执行 JavaScript 代码
            # await page.evaluate("""
            #     var button = document.querySelector("#app > div > div.home-wrap.select-disable > section.tool-wrap > div");
            #     setInterval(function() {button.click();},100);
            # """)

            try:
                # 保持浏览器和页面打开状态
                while True:
                    await asyncio.sleep(1)  # 防止阻塞事件循环
            except KeyboardInterrupt:
                print("Stopped listening for image requests.")
                await browser.close()
    except Exception as e:
        traceback.print_exc()

async def main():


    zb_user = {
        'zb_user': config['zb_user'],
        'zb_user_psw': config['zb_user_psw'],
        'port': 9223
    }

    auxiliary_users = [
        {
            'fs_user1': config['fs_user1'],
            'fs_user1_psw': config['fs_user1_psw'],
            'port': 9224
        },
        {
            'fs_user2': config['fs_user2'],
            'fs_user2_psw': config['fs_user2_psw'],
            'port': 9225
        }
    ]

    # 构建命令和参数列表
    args = [
        f"--remote-debugging-port=9223",
        f"--user-data-dir=15268317813"  # 注意路径字符串应为原始字符串以避免转义问题，或适当处理含有空格的情况
    ]
    try:
        subprocess.Popen([command] + args)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错，错误代码：{e.returncode}")
    args = [
        f"--remote-debugging-port={auxiliary_users[0]['port']}",
        f"--user-data-dir={auxiliary_users[0]['fs_user1']}"  # 注意路径字符串应为原始字符串以避免转义问题，或适当处理含有空格的情况
    ]
    try:
        subprocess.Popen([command] + args)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错，错误代码：{e.returncode}")
    args = [
        f"--remote-debugging-port={auxiliary_users[1]['port']}",
        f"--user-data-dir={auxiliary_users[1]['fs_user2']}"  # 注意路径字符串应为原始字符串以避免转义问题，或适当处理含有空格的情况
    ]
    try:
        subprocess.Popen([command] + args)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错，错误代码：{e.returncode}")

    # 执行完毕后，切换回原始目录
    os.chdir(original_directory)

    tasks = []
    for i, userobj in enumerate(auxiliary_users):

        task = open_browser_fans(userobj)
        tasks.append(task)

    task_zb = open_browser_zb(zb_user)
    tasks.append(task_zb)

    await asyncio.gather(*tasks)

asyncio.run(main())
