from pymem import Pymem


def fix_version(pm: Pymem):
    WeChatWindll_base = 0
    for m in list(pm.list_modules()):
        path = m.filename
        if path.endswith("WeChatWin.dll"):
            WeChatWindll_base = m.lpBaseOfDll
            break

    # 这些是CE找到的标绿的内存地址偏移量
    ADDRS = [0x2367624, 0x2385AF0, 0x2385C44, 0x239C98C, 0x239EAFC, 0x23A1604]

    for offset in ADDRS:
        addr = WeChatWindll_base + offset
        v = pm.read_uint(addr)
        print(v)
        if v == 0x63090A1B:  # 是3.9.10.27，已经修复过了
            continue
        elif v != 0x6307001E:  # 不是 3.8.0.33 修复也没用，代码是hardcode的，只适配这一个版本
            raise Exception("别修了，版本不对，修了也没啥用。")

        pm.write_uint(addr, 0x63090A1B) # 改成要伪装的版本3.9.10.27，转换逻辑看链接

    input("好了，按回车退出本脚本，可以扫码登录了")
    #print("好了，可以扫码登录了")


if __name__ == "__main__":
    try:
        pm = Pymem("WeChat.exe")
        fix_version(pm)
    except Exception as e:
        input(f"{e}，请确认微信程序已经打开！")

