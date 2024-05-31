import asyncio
import json
import pygetwindow as gw
from playwright.async_api import async_playwright
from playwright.sync_api import Playwright, sync_playwright, expect
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

gpage = None

async def gpageaaaaa():
    print("运行gpageaaaaa")
    global gpage
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])  # headless=False 便于调试
        gcontext = await browser.new_context(viewport={"width": 1920, "height": 1080}, no_viewport=True)
        gpage = await gcontext.new_page()
        await gpage.goto("https://95598.cn/osgweb/login")
        try:
            await gpage.wait_for_load_state('networkidle',timeout=30000)
        except Exception as e:
            print(f"Page loading timed out: {e}")
        # 最小化窗口
        browser_window = gw.getWindowsWithTitle("95598")[0]  # Replace with the actual title
        browser_window.minimize()


        await gpage.add_script_tag(path="./page.js")
        # 等待脚本加载并检查函数是否可用
        await gpage.wait_for_function("() => typeof window.axibafuc1 === 'function'")
        print("启动成功，可以开始UIBOT程序")
        await capture_image_requests()

async def capture_image_requests():
    print("运行capture_image_requests")
    global gpage
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])  # headless=False 便于调试
        context = await browser.new_context(viewport={"width": 1920, "height": 1080}, no_viewport=True)
        page = await context.new_page()
        await page.goto("https://95598.cn/osgweb/login")

        # 定义响应拦截处理函数
        async def log_response(response):
            request = response.request
            if request.url.startswith("https://95598.cn/api/osg-web0004/open/c44/f05"):
                body = await response.body()
                # 将字节序列解码为字符串
                body_str = body.decode('utf-8')
                # 将字符串解析为 JSON 对象
                body_json = json.loads(body_str)
                #print(f"验证码返回=== {body_json}")
                #打印request的请求头中的Keycode
                #print(f"Keycode=== {request.headers['keycode']}")

                imgres= await gpage.evaluate('({ arg1, arg2 }) => window.axibafuc1(arg1, arg2)', {'arg1': body_json['encryptData'], 'arg2': request.headers['keycode']})
                print(f"解密后的图片=== {imgres}")
        # 设置拦截器
        page.on("response", log_response)

        print("Start listening for image requests. Press Ctrl+C to stop.")

        try:
            # 保持浏览器和页面打开状态
            while True:
                await asyncio.sleep(1)  # 防止阻塞事件循环
        except KeyboardInterrupt:
            print("Stopped listening for image requests.")
            await browser.close()



# 主程序入口
async def main():
    await gpageaaaaa()  # 初始化 gpage

# 运行异步主程序
asyncio.run(main())
