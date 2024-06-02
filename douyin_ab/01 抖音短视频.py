import requests
import execjs
import urllib.parse
import chardet
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '__ac_signature=_02B4Z6wo00f01XejlHQAAIDCJVy0bCqqtLl3g5DAADu03c; ttwid=1%7CscTLfSFIoB-1tE6Q19V6FuUwzsGyqWkQo_FpYlSm0fk%7C1717069161%7C4a58220e77dc115a2d7db449989e1d4f1c093750611c28006756e2dca9f7599c; douyin.com; s_v_web_id=verify_lwt6nat6_YIARdulB_KsUI_4GG3_8BM1_kW9umwolPAuD; device_web_cpu_core=10; device_web_memory_size=8; home_can_add_dy_2_desktop=%220%22; dy_swidth=1728; dy_sheight=1117; csrf_session_id=1fdd23429e50b7104b8c1d822253b652; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; strategyABtestKey=%221717069165.02%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; passport_csrf_token=e2faac6fa33c13bc1fd363b1bf7c5954; passport_csrf_token_default=e2faac6fa33c13bc1fd363b1bf7c5954; bd_ticket_guard_client_web_domain=2; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; SEARCH_RESULT_LIST_TYPE=%22single%22; download_guide=%221%2F20240530%2F0%22; __ac_nonce=066586d22000b7a7e67cf; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1728%2C%5C%22screen_height%5C%22%3A1117%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A10%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRVl3N1dvWlA2dnNBRUhCaGhYNjV0Ky9mQnFZOC82cnJnRDNiWHh5dU93UkVtMGdYZ3lnUzVzMEltUm02OHlEL0xtQnpTTnFDQStHQXVmZlVlL3dkcWc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; msToken=duue8yOqy5R0BGHED0iyFMN8k5XO8evp3S6zWK5wNSXDVUkMWmN7oPKfeURqi8M9OSfYlD8dUQ_eBgm7r8_L7IDd1GL5EG8_S3GVUqcd-Kj-5VbzM4KDqtwQ8Xcelw==; IsDouyinActive=true',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.douyin.com/user/MS4wLjABAAAAQERLUS1XLl1qZMZDkibRWUdHGBAoG0pJq_5hAj3XjIZXnxgtW_CcE17nuHHfikpQ',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

user_id = "MS4wLjABAAAAO5P9hirn8_P4k6bQRfVeueXbvsJRIsPTmDM18lEZScY"
# user_id = "MS4wLjABAAAAQERLUS1XLl1qZMZDkibRWUdHGBAoG0pJq_5hAj3XjIZXnxgtW_CcE17nuHHfikpQ"

params = {
    'device_platform': 'webapp',
    'aid': '6383',
    'channel': 'channel_pc_web',
    'sec_user_id': user_id,
    'max_cursor': '0',
    'locate_query': 'false',
    'show_live_replay_strategy': '1',
    'need_time_list': '1',
    'time_list_query': '0',
    'whale_cut_token': '',
    'cut_version': '1',
    'count': '18',
    'publish_video_strategy_type': '2',
    'update_version_code': '170400',
    'pc_client_type': '1',
    'version_code': '290100',
    'version_name': '29.1.0',
    'cookie_enabled': 'true',
    'screen_width': '1728',
    'screen_height': '1117',
    'browser_language': 'zh-CN',
    'browser_platform': 'MacIntel',
    'browser_name': 'Chrome',
    'browser_version': '124.0.0.0',
    'browser_online': 'true',
    'engine_name': 'Blink',
    'engine_version': '124.0.0.0',
    'os_name': 'Mac OS',
    'os_version': '10.15.7',
    'cpu_core_num': '10',
    'device_memory': '8',
    'platform': 'PC',
    'downlink': '10',
    'effective_type': '4g',
    'round_trip_time': '100',
    'webid': '7374755802923714087',
    'msToken': 'ycLKKyMbKmBW1bJDt95xLmkbjEtUSuNND4RAt0yxH7WF910DeuwbzGwlK8cwFvC7GDvPy7PRhHsXW5v8uMoWWG0Q0u75n3zQHyp9KBwyzhgi-s6CjwlgNmdku1L1ERw=',
    'verifyFp': 'verify_lwt6nat6_YIARdulB_KsUI_4GG3_8BM1_kW9umwolPAuD',
    'fp': 'verify_lwt6nat6_YIARdulB_KsUI_4GG3_8BM1_kW9umwolPAuD',
}

params_str = urllib.parse.urlencode(params)
print("params_str:::",params_str)

# 检测文件编码
with open("douyin.js", "rb") as f:
    result = chardet.detect(f.read())
# 使用检测到的编码读取文件
encoding = result['encoding']
with open("douyin.js", "r", encoding=encoding) as f:
    js_content = f.read()
# 编译并调用 JavaScript 代码
a_bogus = execjs.compile(js_content.encode('utf-8').decode('utf-8')).call("get_a_bogus", params_str)

#a_bogus = execjs.compile(open("douyin.js",encoding="utf-8").read()).call("get_a_bogus",params_str)
print("a_bogus:::",a_bogus)


params["a_bogus"] = a_bogus

url = 'https://www.douyin.com/aweme/v1/web/aweme/post/'
response = requests.get(url, params=params, headers=headers)
print(":::",response.text)
