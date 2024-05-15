const CryptoJS = require('crypto-js');
require("./ddq.js")

var md5jm = function(tt) {
    return encrypted = CryptoJS.MD5(tt).toString().toLowerCase();
}

function ed(tt, te, tr, ti) {


    var ta = tr.zse93
      , tu = tr.dc0
      , tc = tr.xZst81
        ///api/v4/comment_v5/answers/3495978425/root_comment?order_by=score&limit=20&offset=
      , tf = tt.toString().replace("https://www.zhihu.com", "")
      , td = ""
      , tp = [ta, tf, tu, false && td, tc].filter(Boolean).join("+");

     return self.D(md5jm(tp))

}

var t9 = RegExp("d_c0=([^;]+)")

var er = function(cookie) {
            var tt = t9.exec(cookie);
            return tt && tt[1]
        }

function solution(pl_url,cookie) {
    let tO = ed(pl_url, undefined, {
                            zse93: "101_3_3.0",
                            dc0: er(cookie),
                            xZst81: null
                        }, undefined)
    console.log("to="+tO)
    return "2.0" + "_" + tO
}

//101_3_3.0+/api/v4/comment_v5/answers/3495978425/root_comment?order_by=score&limit=20&offset=+ATCarVYtLRePTkgpGsTD-7SCKHinpiNPNTc=|1690948775
//101_3_3.0+/api/v4/comment_v5/answers/3495978425/root_comment?order_by=score&limit=20&offset=+ATCarVYtLRePTkgpGsTD-7SCKHinpiNPNTc=|1690948775

//算的md5=1a0b278fbd1876dfc1c3f463511c1476
//浏览器的md5=1a0b278fbd1876dfc1c3f463511c1476
//算的x-zse-96 8zmB32uziWyawFYiK2m6Cer2hLUQqI3ZqN1R0brno1tuMJ7VojYovmgzY1v=fb4+
//浏览器的x-zse-96 2z3urgNy8Q6Y3FZCY16qmGJYxN6Or6yw6V2bLZVb9zFTGCkdV430r=ynuFNx7CGl

cookie = '_zap=94493b23-bd6d-4aed-ad54-43aa58f22967; d_c0=ATCarVYtLRePTkgpGsTD-7SCKHinpiNPNTc=|1690948775; YD00517437729195%3AWM_TID=k53Crj2LOo5FQBERFRLRguIa2dS%2ByAIZ; __snaker__id=EptotAO9EklQWiGa; YD00517437729195%3AWM_NI=oR8ekfEExKXCZXdjLRq8zR6DT510WuoD1lIq033eNkHuHU5wzVcEzbWg8h8owjQfQpQTkkCvTPQGa667eiVtpZU2dw0NLMi3N0UgedULKgxGZsnDMzGd%2F1INU5jzBFUiYTc%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee96e23db1b48bd5f86396928ea6d14e829b9f86c83a81bafcd6b434b7adaca9d02af0fea7c3b92aad8ef886ea6e879bb8acdb499a88ac8bcf5ab3e8b6b3b55098ebffd1d67fad9cff8dcc7bf4edfd86cd618cab88b6b87dba8aada6f96a95b9f889bb65b5b69f87d47c938ca58cc27e98909fa8e43ef6e9ab8ad580b4869bd3e77df49284aeec398ef09b88e87097948588fb4d9aada2a5d07285bce1d2cc4697eba69bc14e97b797b5e237e2a3; q_c1=983ee025f4964258a624af2d03fb87d2|1714981696000|1714981696000; z_c0=2|1:0|10:1714982436|4:z_c0|80:MS4xUVBTcUhnQUFBQUFtQUFBQVlBSlZUVU9oSEdjQ1BFLV9veFF2bzM3QjlYR0M2bjNRbDR0bnRRPT0=|d98667071ef98922378c8abe5f1f82ab139a6d4a25f70f9f67770c9bc667f6db; _xsrf=4d819104-e756-4f82-9fa1-e6027a3e3620; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1715152558,1715333695,1715412841,1715586118; SESSIONID=L5hpTXKbC6TelOkvu56hDYBuArF1tF4f40vnXxnG4D0; JOID=UFgRBkvtLcaPCiTzBOoNV4rn3scVoxyv-lx-vGesGZbrY2madhPsg-4KIvYA_wjv26PA5aO5zxVyaMMEdnp-pog=; osd=U1wQBk3uKcePDCf3BeoLVI7m3sEWpx2v_F96vWeqGpLqY2-ZchLshe0OI_YG_Azu26XD4aK5yRZ2acMCdX5_po4=; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1715760031; BEC=b7b0f394f3fd074c6bdd2ebbdd598b4e; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1715762381|1715743174'
pl_url = 'https://www.zhihu.com/api/v4/comment_v5/answers/3495978425/root_comment?order_by=score&limit=20&offset='
console.log(solution(pl_url,cookie))