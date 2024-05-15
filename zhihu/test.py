import requests

url = "https://www.zhihu.com/api/v4/comment_v5/answers/3246747600/root_comment?order_by=score&limit=20&offset="

payload = {}
headers = {
  'cookie': '_zap=a0bd719d-cf14-44fd-94ca-a1838a5ec147; d_c0=APBWZW7knhiPTqPOjEjzXRVKGrdAenGCgOA=|1715759942; gdxidpyhxdE=UCET%2B2mcbb%5C5Acc7gSVWh7L%2B8NwagRor8YVhffC%5CzAmHqH3lfhPTW%2Bdumx%5CWvNa8%5CBAqOpr7cJ78%5C712hybwUNK%5CSNZshyIBUvyCKeatuIQaG2oP6tnqmAopOUqvYxLUq%2B3%5CfYuyJxJq0kI%5CI%2FdrKn2V5AKvqjwfJqnmrdh9kWdzsNja%3A1715760845563; captcha_session_v2=2|1:0|10:1715760110|18:captcha_session_v2|88:WVFDWDFYSGZOaFJLakNaTWFtK2lRaGlMdFpYMGVxQUxTM1hMWCt4RmpDaVpUbzM5amR5Q2dNK05hV2s3a2lUNA==|8ff2b160bd4c1c7e8dacc3d6d62998b2e6ea057adf03f382629ebb81e86ecfba; __snaker__id=0xnH4NvDoBbuSjiK; q_c1=2d16b6a89d004e5986da7f3c9eb6b2e6|1715760117000|1715760117000; z_c0=2|1:0|10:1715760196|4:z_c0|92:Mi4xUVBTcUhnQUFBQUFBOEZabGJ1U2VHQ1lBQUFCZ0FsVk45Ymt4WndBa1J3cXd1NzZPS0lrRTQ0bGhtejlTMzJKZlJn|daae1da354d70abf7678fcfd4ff472da0303dbc59dadfa9f158d653c5148aeb4; BEC=d5e2304fff7e4240174612484fe7ffa4; _xsrf=49798e8c-fa0e-457e-bfe8-c50a424f3ded; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1715760127,1715760195,1715760216,1715760324; SESSIONID=tuCcISGMFyAsVTj7keOKKwjIbghFARWI8nISm8LBUEL; JOID=U1kSCkpo7eDuXYPfVmAdcHwpb0FIHJ6thRTQnhUulKeTA9e1Z6mJooBdhddQokMAaVGj98BVECOHfTywHkOeDL8=; osd=UVkUB0Jq7ebjVYHfUG0VcnwvYklKHJigjRbQmBgmlqeVDt-3Z6-EqoJdg9pYoEMGZFmh98ZYGCGHezG4HEOYAbc=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1715760328; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1715760370|1715760323; _xsrf=22HTlYCR9fGNfOqQuy24LoSiER31u8tq; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1715760979|1715760323',
  'x-zse-93': '101_3_3.0',
  'x-zse-96': '2.0_cKQJJwxOxWDL0tmAf+MZAS8294ZQ548pKBJtKvQyabb9Nj5+fB14ilPaIUd6l1ie'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
