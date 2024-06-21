import os
import json
import traceback
import asyncio
from playwright.async_api import async_playwright
import subprocess
from screeninfo import get_monitors
import ast
with open('config.json', 'r') as f:
    config = json.load(f)
# import km_yanzheng
# km_yanzheng.method_name(config['km'])
maxi = 0

command = config['chromepath']

def get_chrome_profiles():
    profile_folder = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    profiles = []

    # 确保用户数据目录存在
    if not os.path.exists(profile_folder):
        print(f"Chrome 用户数据目录未找到: {profile_folder}")
        return profiles

        # 默认的Profile名称
    default_profile = "Default"
    profiles.append(default_profile)

    # 获取其他Profile的文件夹
    for folder_name in os.listdir(profile_folder):
        if folder_name.startswith('Profile '):
            profiles.append(folder_name)

    return profiles


def get_profile_name(profile_path):
    preferences_path = os.path.join(profile_path, 'Preferences')

    if os.path.exists(preferences_path):
        with open(preferences_path, 'r', encoding='utf-8') as f:
            preferences = json.load(f)
            profile_name = preferences['account_info'][0]['full_name']
            return profile_name
    return None

def close_browser(browser_process):
    # 关闭浏览器进程
    browser_process.terminate()
    try:
        browser_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        browser_process.kill()

async def main():
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height
    profiles = get_chrome_profiles()

    if profiles:
        print("找到的 Chrome 用户 Profile 目录：")
        for profile in profiles:
            profile_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data') + f"\\{profile}"
            #profile_name = get_profile_name(profile_path)
            print(f"Profile 目录: {profile}")
    else:
        print("未找到任何 Chrome 用户 Profile。")
        return

    shibais=[]
    chenggonged=[]


    with open('zhiding.txt', 'r') as f:
        try:
            content = f.read().strip()
            if len(content)>0:
                list_data = ast.literal_eval(content)
                if len(list_data)>0:
                    print("执行指定浏览器",list_data)
                    profiles= list_data
                else:
                    raise Exception("")
            else:
                raise Exception("")
        except Exception as e:
            traceback.print_exc()
            print("没有指定浏览器，执行所有。")

    for profile in profiles:
        try:
            print(f"正在打开 {profile}...")
            # 构建命令和参数列表
            args = [
                #f"--start-maximized",
                f"--remote-debugging-port=9223",
                f"--profile-directory={profile}"  # 注意路径字符串应为原始字符串以避免转义问题，或适当处理含有空格的情况
            ]

            browser_process = subprocess.Popen([command] + args)

            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(f"http://localhost:9223")
                context = browser.contexts[0]

                await context.add_init_script(path='stealth.min.js')

                page = await context.new_page()
                await page.set_viewport_size({"width": screen_width, "height": screen_height})

                # 等待弹出的窗口并捕获它
                async with context.expect_page() as new_page_info:
                    await page.goto('https://app.galxe.com/quest/IoTeX/GCqr8tgiEu')
                    await page.wait_for_load_state('load',timeout=60000)
                    await page.wait_for_timeout(2000)
                    await page.wait_for_selector("button:has-text('Log in')",timeout=60000)
                    await page.locator("button:has-text('Log in')").nth(0).click()
                    await page.wait_for_load_state('load')
                    await page.wait_for_timeout(2000)
                    # # 查找包含MetaMask子元素的父div
                    # target_div = page.locator(
                    #     "div.col-span-2.sm\\:col-span-4.text-sm.font-bold >> div.flex.justify-between.items-center.h-\\[56px\\].rounded-8.cursor-pointer.border-component-dialog.border.hover\\:border-white.active\\:border-\\[\\#FFFFFF80\\].px-4.py-3\\.5:has(div:has-text('MetaMask'))")
                    # # 验证找到的div数量
                    # count = await target_div.count()
                    # print(f"Found {count} div(s) containing a child div with text 'MetaMask'")
                    # # 示例操作: 如果找到了至少一个这样的div，点击第一个
                    # if count > 0:
                    #     await target_div.nth(0).click()
                    # else:
                    #     raise Exception("找不到登录按钮")
                    await page.wait_for_selector("div.ml-3:has-text('MetaMask')", timeout=60000)
                    await page.locator("div.ml-3:has-text('MetaMask')").click()
                    await page.wait_for_timeout(2000)

                metamask_page = await new_page_info.value
                await metamask_page.wait_for_timeout(1000)
                # 在 MetaMask 窗口上执行操作
                await metamask_page.wait_for_load_state('load',timeout=60000)
                # 示例操作：输入密码并点击登录
                await metamask_page.fill('input[type="password"]', '12345678')  # 替换为实际的密码字段选择器
                await metamask_page.wait_for_selector("button:has-text('登录')", timeout=60000)
                await metamask_page.locator("button:has-text('登录')").click()
                await metamask_page.wait_for_load_state('load')
                await metamask_page.wait_for_selector("button:has-text('下一步')", timeout=60000)
                await metamask_page.locator("button:has-text('下一步')").click()
                await metamask_page.wait_for_load_state('load')
                await metamask_page.wait_for_selector("button:has-text('确认')", timeout=60000)
                await metamask_page.locator("button:has-text('确认')").click()
                try:
                    await metamask_page.wait_for_selector("button:has-text('登录')", timeout=5000)
                    await metamask_page.locator("button:has-text('登录')").click()
                except:
                    print("已登录")
                await metamask_page.wait_for_load_state('load')
                # 按下ESC键
                await page.wait_for_timeout(1000)
                await page.keyboard.press("Escape")

                try:
                    async with context.expect_page(timeout=10000) as new_page_info:
                        await page.wait_for_selector("p:has-text('Daily Visit the IoTeX Website')", timeout=10000)
                        await page.locator("p:has-text('Daily Visit the IoTeX Website')").click()

                    yanzheng_page = await new_page_info.value
                    await yanzheng_page.wait_for_selector("button:has-text('Continue to Access')", timeout=60000)
                    await yanzheng_page.locator("button:has-text('Continue to Access')").click()
                    await asyncio.sleep(3)
                except:
                    print(profile,"已验证")

                await page.bring_to_front()

                #等待领取++++++++++++++++++++++++++++++++++++++++
                shangxian = 0
                while True:
                    if shangxian>1 :
                        print(profile,"超过2次找不到领取按钮")
                        raise Exception("超过2次找不到领取按钮")
                    try:
                        await page.reload()
                        await page.wait_for_load_state('load')
                        await page.wait_for_load_state('domcontentloaded')
                        await page.wait_for_timeout(3000)

                        #selector = "body > div > main > div > div.style_bottom-section__67Akm > div > div.flex.items-center.justify-end.z-\\[2\\].w-full > div.style_claim-button__XFPGx.ml-\\[4px\\] > div > button > div"
                        selector = "div.style_claim-button__XFPGx.ml-\\[4px\\] > div > button > div"
                        await page.locator(selector).wait_for(timeout=27000)

                        element_text = await page.evaluate('''
                            () => {
                                var element = document.querySelector('div[class*="style_claim-button__XFPGx ml-\\[4px\\]"] > div > button > div');
                                return element ? element.textContent : null;
                            }
                        ''')
                        print(element_text)
                        if  element_text == "Claim 5 Points": #可领取，算成功
                            #await page.wait_for_selector("div:has-text('Claim 5 Points')", timeout=27000)
                            await page.add_script_tag(content="""
                                    function aaaa(){
                                        let clicked = false;
                                        document.querySelectorAll('button').forEach(button => {
                                            const div = button.querySelector('div');
                                            if (div && div.textContent.includes('Claim 5 Points')) {
                                                button.click();
                                                console.log('Clicked a button containing a child div with text "Claim 5 Points"');
                                                clicked = true;
                                                return;  // 只点击第一个匹配项，然后退出循环
                                            }else {
                                                console.log('000000');
                                            }
                                        });
                                        return clicked;  // 返回是否找到并点击了按钮
                                    }
                                """)
                            # 使用 JavaScript 查找并点击包含特定子元素文本的 button
                            result = await page.evaluate("console.log('11111111');aaaa()")
                            print("领取成功")
                            if result:
                                print(
                                    "Successfully clicked the button with a child div containing text 'Claim 5 Points'")
                                await page.wait_for_timeout(4000)
                                break
                            else:
                                raise Exception("No button found with a child div containing text 'Claim 5 Points'")
                        elif element_text == "Claimed": #已领取，算已领取
                            print("检测到已领取")
                            chenggonged.append(profile)
                            break
                        else: #未加载
                            raise Exception("未加载")

                    except Exception as e:
                        shangxian= shangxian+1
                        print("还没有可领取",e)
                        await asyncio.sleep(2)
                #领取结束------------------------------------


        except Exception as e:
            try:
                print(f" {profile}失败: {e}")
                shibais.append(f"{profile}")
                traceback.print_exc()
            except Exception as e:
                traceback.print_exc()
        finally:
            try:
                close_browser(browser_process)
            except Exception as e:
                traceback.print_exc()

    print("运行结束，以下是失败的+++++++++++++++++++++++++++")
    print(shibais)
    print("以下是还未运行的+++++++++++++++++++++++++++")
    result1 = [item for item in profiles if item not in shibais]
    result = [item for item in result1 if item not in chenggonged]
    print(result)


asyncio.run(main())