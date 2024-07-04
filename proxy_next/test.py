import asyncio
import proxy_next

async def main():
    helper = proxy_next.Helper()
    # 在异步函数中使用 await 调用异步函数
    res = await helper.get_url_autoproxy("https://www.baidu.com/")
    print(res.text)

# 运行异步函数
asyncio.run(main())
