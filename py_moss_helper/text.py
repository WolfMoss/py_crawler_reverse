import py_moss_helper

#获取默认请求头
helper = py_moss_helper.Helper()
print(helper.headers)

proxy_cycle={'iterator':[]}
#设置一个代理,如果没有ip池，会先获取ip池
helper.choose_func_getproxy(proxy_cycle)
print(helper.proxies)