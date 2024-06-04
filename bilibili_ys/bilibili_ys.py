import asyncio
import json
from datetime import datetime
import traceback
from playwright.async_api import async_playwright

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

async def open_browser_fans(userobj):
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        zb_zbj_url = config['zb_zbj_url']

        async with async_playwright() as p:
            usertype = sorted(userobj.keys())[0]
            username = userobj[usertype]
            psw = userobj[sorted(userobj.keys())[1]]
            browser = await p.chromium.launch_persistent_context(
                user_data_dir='userdata/'+username,
                accept_downloads=True,
                headless=False,
                bypass_csp=True,
                #executable_path=edge_path
                channel="msedge",
                args=['--start-maximized',"--disable-blink-features=AutomationControlled"],viewport={"width": 1920, "height": 1080}, no_viewport=True

            )
            await browser.add_init_script(path='./stealth.min.js')
            page = await browser.new_page()
            await page.goto('https://space.bilibili.com/')

            dengdai = True
            shurumima = False
            while dengdai:
                await page.wait_for_load_state('networkidle')
                login_button = await page.query_selector_all('input[placeholder="请输入账号"]')
                if login_button:
                    print(username,"尚未登录")
                    if not shurumima:
                        await page.type('input[placeholder="请输入账号"]', username)
                        await page.type('input[placeholder="请输入密码"]', psw)
                        shurumima=True
                    await page.wait_for_timeout(1000)
                else:
                    print(username,"已登录或元素不存在")
                    dengdai = False
            print(username,"登录成功")

            #跳转到直播间
            await page.goto(zb_zbj_url)
            await page.wait_for_timeout(2000)



            #等待到第二天发弹幕6条，牛娃牛蛙1个
            while True:


                print(username,'开始获取当前时间')
                # 获取当前时间
                current_time_str  = await page.evaluate("new Date().toLocaleTimeString()")
                current_time = datetime.strptime(current_time_str, '%H:%M:%S').time()
                if current_time >datetime.strptime('0:01:00', '%H:%M:%S').time() and current_time < datetime.strptime('1:00:00', '%H:%M:%S').time():
                    print(username,'到第二天发弹幕6条，牛娃牛蛙1个')

                    # 循环6次
                    for i in range(8):
                        # 输入文字到当前焦点所在的元素（文本框）
                        await page.mouse.click(1559, 880)
                        await page.wait_for_timeout(1000)
                        await page.keyboard.type(random_danmu(i));
                        await page.click('span.txt:text("发送")')
                        await page.wait_for_timeout(2000)

                    await page.mouse.click(1178, 891)
                    await page.wait_for_timeout(1000)
                    await page.mouse.move(1230, 676)
                    await page.wait_for_timeout(1000)
                    await page.mouse.click(1228, 734)

                    break
                else:
                    print(username,'还没到第二天')
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
        async with async_playwright() as p:
            usertype = sorted(userobj.keys())[0]
            username = userobj[usertype]
            browser = await p.chromium.launch_persistent_context(
                user_data_dir='userdata/'+ username,
                accept_downloads=True,
                headless=False,
                bypass_csp=True,
                #executable_path=edge_path
                channel="msedge",
                args=['--start-maximized',"--disable-blink-features=AutomationControlled"],viewport={"width": 1920, "height": 1080}, no_viewport=True
            )
            await browser.add_init_script(path='./stealth.min.js')
            page = await browser.new_page()
            await page.goto('https://space.bilibili.com/')

            dengdai = True
            shurumima = False
            while dengdai:
                await page.wait_for_load_state('networkidle')
                login_button = await page.query_selector_all('input[placeholder="请输入账号"]')
                if login_button:
                    print(username,"尚未登录")
                    if not shurumima:
                        await page.type('input[placeholder="请输入账号"]', username)
                        await page.type('input[placeholder="请输入密码"]', userobj['zb_user_psw'])
                        shurumima = True
                    await page.wait_for_timeout(1000)
                else:
                    print(username,"已登录或元素不存在")
                    dengdai = False
            print(username,"登录成功")

            await page.goto('https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id=7f920185')
            #循环判断当前时间，是否超过0:59:56秒，如果超过则点击按钮，如果超过1:00:05秒，则退出循环
            while True:
                print(username,'开始获取当前时间')
                # 获取当前时间
                current_time_str  = await page.evaluate("new Date().toLocaleTimeString()")
                current_time = datetime.strptime(current_time_str, '%H:%M:%S').time()
                if current_time < datetime.strptime('2:00:00', '%H:%M:%S').time():
                    clicktime = datetime.strptime('0:59:59', '%H:%M:%S').time()
                    breaktime = datetime.strptime('1:00:02', '%H:%M:%S').time()
                    # 判断当前时间是否超过0:59:56秒
                    if current_time >= clicktime:
                        # 点击按钮
                        await page.click("#app > div > div.home-wrap.select-disable > section.tool-wrap > div")
                        # 等待 1 秒
                        await asyncio.sleep(0.1)
                    if current_time >= breaktime:
                        break
                else:
                    print(username,'还没到第二天')
                    await asyncio.sleep(1)


            # 执行 JavaScript 代码
            await page.evaluate("""
                var button = document.querySelector("#app > div > div.home-wrap.select-disable > section.tool-wrap > div");
                setInterval(function() {button.click();},100);
            """)

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
    with open('config.json', 'r') as f:
        config = json.load(f)

    zb_user = {
        'zb_user': config['zb_user'],
        'zb_user_psw': config['zb_user_psw']
    }

    auxiliary_users = [
        {
            'fs_user1': config['fs_user1'],
            'fs_user1_psw': config['fs_user1_psw']
        },
        {
            'fs_user2': config['fs_user2'],
            'fs_user2_psw': config['fs_user2_psw']
        }
    ]

    tasks = []
    for i, userobj in enumerate(auxiliary_users):
        task = open_browser_fans(userobj)
        tasks.append(task)

    task_zb = open_browser_zb(zb_user)
    tasks.append(task_zb)

    await asyncio.gather(*tasks)

asyncio.run(main())
