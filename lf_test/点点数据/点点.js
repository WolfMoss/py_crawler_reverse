//t.params.k
//n.proxy=="/app" && e=="/app/v1/user/favorite/app"

let app_id ="y21ulux1r7mwra1"
let country_id =75
let start_time =1719417600
let end_time =1719504000

function ya(e, path, n, r) {
    var  v = n.d
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
            for (var d in n){
                r.push(n[d]);
            }

            r.sort()
            aaa = r.join("")
            return aaa


        }(e, r), parseInt((new Date).getTime() / 1e3) - 655876800 - v, path, h), '6bf8$&io9s', k);
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

restext = ya(r, "/v1/user/favorite/app", c, "get")
console.log(restext)