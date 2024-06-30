//t.params.k
//n.proxy=="/app" && e=="/app/v1/user/favorite/app"
const crypto = require('crypto');
const request = require('request');
getmiyao();

// 创建解密函数
function lb(e, n, o) {
    let d111 = "";
    n = Buffer.from(n, "utf8");
    o = Buffer.from(o, "utf8");
    let c111 = crypto.createDecipheriv("aes-128-cbc", n, o);
    d111 += c111.update(e, "hex", "utf8");
    d111 += c111.final("utf8");
    return d111;
}

let app_id = "y21ulux1r7mwra1"
let country_id = 75
let start_time = 1719590400
let end_time = 1719676800


function getmiyao() {

    var options = {
        'method': 'GET',
        'url': 'https://app.diandian.com/',
        'headers': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'cookie': 'i18n_redirected=zh; deviceid=c47ae2eec882622413b975263e00b1f; _ga=GA1.1.1770411766.1719490841; Hm_lvt_4b46d92b8c2be1622e347873de8ada00=1719499004; Hm_lvt_c420cc498e4250baa6114afe2947045e=1719499004; Hm_lvt_e1382854e68f4d69f837bb54a6d1e22f=1719499004; Hm_lvt_8a5bd6e095cd118016489cab0443c2d7=1719490837,1719746697; Hm_lvt_d185b2974609101d8f9340b5f861ca70=1719490837,1719746697; Hm_lvt_beac6fc75c36ba113cbffa9a59b1b18d=1719490837,1719746697; Qs_lvt_404253=1719490837%2C1719746696; mediav=%7B%22eid%22%3A%221089729%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22%3AE%5E_DaIhJY9H%60%60c)ssaF%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22%3AE%5E_DaIhJY9H%60%60c)ssaF%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; showMajorDialog=true; Hm_lpvt_d185b2974609101d8f9340b5f861ca70=1719746953; Qs_pv_404253=1058955644823644900%2C4410044463684567000%2C3177350388874449400%2C1411212668103342800%2C761732556480286800; Hm_lpvt_beac6fc75c36ba113cbffa9a59b1b18d=1719746954; Hm_lpvt_8a5bd6e095cd118016489cab0443c2d7=1719746954; _ga_GVCWL6PNZ2=GS1.1.1719746699.5.1.1719746956.0.0.0',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }
    };
    request(options, function (error, response) {
        if (error) {
            console.error('Error:', error.message);
            return;
        }
        let fenge = response.body.split("u:")[1].split(",activeNav:")[0].toString();
        let regex = /s:"([^"]+)",k:"([^"]+)",l:"([^"]+)"/;
        let match = fenge.match(regex);
        let sValue = match[1];
        let kValue = match[2];
        let lValue = match[3];
        let miyao = lb(sValue, kValue, lValue);
        restext = ya(r, "/v1/user/favorite/app", c, "get",miyao)
        console.log(restext)
    });
}


function ya(e, path, n, r,miyao) {
    var v = n.d
        , h = n.sort
        , k = n.num
        , y = function (content, t, e) {
        for (var a = Array.from(content), n = Array.from(t), r = a.length, o = n.length, d = String.fromCodePoint, i = 0; i < r; i++)
            a[i] = d(a[i].codePointAt(0) ^ n[(i + e) % o].codePointAt(0));
        return a.join("")
    }(function (s, t, path, e) {
        return [s, t, e, path].join("(&&)")
    }(function (t, e) {
        //var n = c()(t);
        var n = {
            "app_id": app_id,
            "country_id": country_id,
            "market_id": 1,
            "device_id": 1,
            "start_time": start_time,
            "end_time": end_time
        }

        var r = [];
        for (var d in n) {
            r.push(n[d]);
        }

        r.sort()
        aaa = r.join("")
        return aaa


    }(e, r), parseInt((new Date).getTime() / 1e3) - 655876800 - v, path, h), miyao, k);
    return Buffer.from(y).toString("base64")
}

let c = {
    d: -1,
    sort: "dd",
    num: 10
}


let r = {
    "app_id": app_id,
    "country_id": country_id,
    "market_id": 1,
    "device_id": 1,
    "start_time": start_time,
    "end_time": end_time,
    "k": undefined
}

