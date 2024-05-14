const CryptoJS = require('crypto-js');
require("./ddq.js")

var md5jm = function(tt) {
    return encrypted = CryptoJS.MD5(tt).toString().toLowerCase();
}

function ed(tt, te, tr, ti) {


    var ta = tr.zse93
      , tu = tr.dc0
      , tc = tr.xZst81
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

    return "2.0" + "_" + tO
}

