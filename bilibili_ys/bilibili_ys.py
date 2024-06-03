import asyncio
import json

from playwright.async_api import async_playwright

async def open_browser_instance(url, instance_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        print(f"{instance_name} opened {url}")
        try:
            # 保持浏览器和页面打开状态
            while True:
                await asyncio.sleep(1)  # 防止阻塞事件循环
        except KeyboardInterrupt:
            print("Stopped listening for image requests.")
            await browser.close()

async def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    main_user = {
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
        # Add more auxiliary users as needed
    ]

    users = [main_user] + auxiliary_users


    tasks = [open_browser_instance(url, f"instance_{i}") for i, url in enumerate(users)]
    await asyncio.gather(*tasks)

asyncio.run(main())
