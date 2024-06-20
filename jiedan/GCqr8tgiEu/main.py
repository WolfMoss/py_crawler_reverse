import os
import json
import traceback
import asyncio
from playwright.async_api import async_playwright
import subprocess
with open('config.json', 'r') as f:
    config = json.load(f)
import km_yanzheng
km_yanzheng.method_name(config['km'])
maxi = 1

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
            profile_name = preferences.get('profile', {}).get('name', None)
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
    profiles = get_chrome_profiles()

    if profiles:
        print("找到的 Chrome 用户 Profile 目录：")
        for profile in profiles:
            profile_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data') + f"\\{profile}"
            profile_name = get_profile_name(profile_path)
            print(f"Profile 目录: {profile} -> 名称: {profile_name if profile_name else '未命名'}")
    else:
        print("未找到任何 Chrome 用户 Profile。")
        return

    i = 0
    for profile in profiles:
        if i>=10 and maxi==1:
            break
        print(f"正在打开 {profile}...")
        # 构建命令和参数列表
        args = [
            f"--remote-debugging-port=9223",
            f"--profile-directory={profile}"  # 注意路径字符串应为原始字符串以避免转义问题，或适当处理含有空格的情况
        ]
        try:
            browser_process = subprocess.Popen([command] + args)
        except subprocess.CalledProcessError as e:
            print(f"命令执行出错，错误代码：{e.returncode}")
            continue

        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f"http://localhost:9223")
            context = browser.contexts[0]
            await context.add_init_script(path='stealth.min.js')
            try:
                page = await context.new_page()
                extension_id = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
                # 等待弹出的窗口并捕获它
                async with context.expect_page() as new_page_info:
                    await page.goto('https://app.galxe.com/quest/IoTeX/GCqr8tgiEu')
                    await page.wait_for_load_state('load')
                    await page.locator("button:has-text('Log in')").click()
                    # 查找包含MetaMask子元素的父div
                    target_div = page.locator(
                        "div.col-span-2.sm\\:col-span-4.text-sm.font-bold >> div.flex.justify-between.items-center.h-\\[56px\\].rounded-8.cursor-pointer.border-component-dialog.border.hover\\:border-white.active\\:border-\\[\\#FFFFFF80\\].px-4.py-3\\.5:has(div:has-text('MetaMask'))")
                    # 验证找到的div数量
                    count = await target_div.count()
                    print(f"Found {count} div(s) containing a child div with text 'MetaMask'")
                    # 示例操作: 如果找到了至少一个这样的div，点击第一个
                    if count > 0:
                        await target_div.nth(0).click()
                    else:
                        raise Exception("找不到登录按钮")

                    # 打开 MetaMask 弹出窗口

                metamask_page = await new_page_info.value



                # 在 MetaMask 窗口上执行操作
                await metamask_page.wait_for_load_state('load')
                # 示例操作：输入密码并点击登录
                await metamask_page.fill('input[type="password"]', '12345678')  # 替换为实际的密码字段选择器
                await metamask_page.locator("button:has-text('登录')").click()
                await metamask_page.wait_for_load_state('load')
                await metamask_page.locator("button:has-text('下一步')").click()
                await metamask_page.wait_for_load_state('load')
                await metamask_page.locator("button:has-text('确认')").click()
                await metamask_page.wait_for_load_state('load')
                # 按下ESC键
                await page.wait_for_timeout(1000)
                await page.keyboard.press("Escape")

                try:
                    async with context.expect_page(timeout=5000) as new_page_info:
                        await page.locator("p:has-text('Daily Visit the IoTeX Website')").click()

                    yanzheng_page = await new_page_info.value
                    await yanzheng_page.locator("button:has-text('Continue to Access')").click()
                    await asyncio.sleep(1)
                except:
                    print(profile,"已验证")

                await page.bring_to_front()

                #等待领取++++++++++++++++++++++++++++++++++++++++
                shangxian = 0
                while True:
                    if shangxian>2 :
                        print(profile,"超过2次找不到领取按钮")
                        break #超过5次找不到领取按钮就放弃
                    try:
                        await page.reload()
                        await page.wait_for_load_state('load')
                        await page.wait_for_timeout(3000)
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
                        if result:
                            print("Successfully clicked the button with a child div containing text 'Claim 5 Points'")
                            await page.wait_for_timeout(5000)
                            break
                        else:
                            raise Exception("No button found with a child div containing text 'Claim 5 Points'")
                    except Exception as e:
                        shangxian= shangxian+1
                        print("还没有可领取",e)
                        await asyncio.sleep(2)
                #领取结束------------------------------------


            except Exception as e:
                print(f" {profile} 失败: {e}")
                traceback.print_exc()
            finally:
                close_browser(browser_process)
        i = i + 1

asyncio.run(main())