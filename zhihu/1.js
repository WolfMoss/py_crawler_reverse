const CryptoJS = require('crypto-js');
require("./ddq.js")

var md5jm = function(tt) {
    return encrypted = CryptoJS.MD5(tt).toString().toLowerCase();
}

function getmd5(tt, te, tr, ti) {


    var ta = tr.zse93
      , tu = tr.dc0
      , tc = tr.xZst81
        ///api/v4/comment_v5/answers/3495978425/root_comment?order_by=score&limit=20&offset=
      , tf = tt.toString().replace("https://www.zhihu.com", "")
      , td = ""
      , tp = [ta, tf, tu, false && td, tc].filter(Boolean).join("+");
    return  md5jm(tp)


}

var t9 = RegExp("d_c0=([^;]+)")

var er = function(cookie) {
            var tt = t9.exec(cookie);
            return tt && tt[1]
        }

function solution(pl_url,cookie) {
    let md5str = getmd5(pl_url, undefined, {
                            zse93: "101_3_3.0",
                            dc0: er(cookie),
                            xZst81: null
                        }, undefined)
    let tO = self.D(md5str)
    console.log("to="+tO)
    return "2.0" + "_" + tO
}

function justmd5(pl_url,cookie) {
    let md5str = getmd5(pl_url, undefined, {
                            zse93: "101_3_3.0",
                            dc0: er(cookie),
                            xZst81: null
                        }, undefined)

    return md5str
}

//101_3_3.0+/api/v4/comment_v5/answers/3495978425/root_comment?order_by=score&limit=20&offset=+ATCarVYtLRePTkgpGsTD-7SCKHinpiNPNTc=|1690948775
//101_3_3.0+/api/v4/comment_v5/answers/3495978425/root_comment?order_by=score&limit=20&offset=+ATCarVYtLRePTkgpGsTD-7SCKHinpiNPNTc=|1690948775

//算的md5=1a0b278fbd1876dfc1c3f463511c1476
//浏览器的md5=1a0b278fbd1876dfc1c3f463511c1476
//算的x-zse-96 8zmB32uziWyawFYiK2m6Cer2hLUQqI3ZqN1R0brno1tuMJ7VojYovmgzY1v=fb4+
//浏览器的x-zse-96 2z3urgNy8Q6Y3FZCY16qmGJYxN6Or6yw6V2bLZVb9zFTGCkdV430r=ynuFNx7CGl

cookie = '_zap=a0bd719d-cf14-44fd-94ca-a1838a5ec147; d_c0=APBWZW7knhiPTqPOjEjzXRVKGrdAenGCgOA=|1715759942; gdxidpyhxdE=UCET%2B2mcbb%5C5Acc7gSVWh7L%2B8NwagRor8YVhffC%5CzAmHqH3lfhPTW%2Bdumx%5CWvNa8%5CBAqOpr7cJ78%5C712hybwUNK%5CSNZshyIBUvyCKeatuIQaG2oP6tnqmAopOUqvYxLUq%2B3%5CfYuyJxJq0kI%5CI%2FdrKn2V5AKvqjwfJqnmrdh9kWdzsNja%3A1715760845563; captcha_session_v2=2|1:0|10:1715760110|18:captcha_session_v2|88:WVFDWDFYSGZOaFJLakNaTWFtK2lRaGlMdFpYMGVxQUxTM1hMWCt4RmpDaVpUbzM5amR5Q2dNK05hV2s3a2lUNA==|8ff2b160bd4c1c7e8dacc3d6d62998b2e6ea057adf03f382629ebb81e86ecfba; __snaker__id=0xnH4NvDoBbuSjiK; q_c1=2d16b6a89d004e5986da7f3c9eb6b2e6|1715760117000|1715760117000; z_c0=2|1:0|10:1715760196|4:z_c0|92:Mi4xUVBTcUhnQUFBQUFBOEZabGJ1U2VHQ1lBQUFCZ0FsVk45Ymt4WndBa1J3cXd1NzZPS0lrRTQ0bGhtejlTMzJKZlJn|daae1da354d70abf7678fcfd4ff472da0303dbc59dadfa9f158d653c5148aeb4; _xsrf=4c0fc493-5157-47fe-a8f9-418ccad133d9; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1715829992,1715830263,1715832863,1715836137; SESSIONID=QvoNreIgeRoSwlCsInGfe5GNEBhtNKVOTUkr3IxbreM; JOID=V1oUAExG9OpxcyDlQ0ABeOoHwn5fEIGHOwNCryYhoYYgAE6hM6lhqRF2JORFd4uLSlFwm11X5FHI1QVZ--cSM8I=; osd=UV4RBENA8O91fCbhRkQOfu4CxnFZFISDNAVGqiIup4IlBEGnN6xlphdyIeBKcY-OTl52n1hT61fM0AFW_eMXN80=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1715836141; BEC=d5e2304fff7e4240174612484fe7ffa4; KLBRSID=f48cb29c5180c5b0d91ded2e70103232|1715836145|1715836134'
pl_url = 'https://www.zhihu.com/api/v4/comment_v5/answers/3487858937/root_comment?order_by=score&limit=20&offset='
console.log(justmd5(pl_url,cookie))