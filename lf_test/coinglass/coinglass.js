const ee = require('crypto-js');
// 引入pako库
const pako = require('pako');



function en(t) {
    var e, n = pako.inflate(new Uint8Array(t.match(/[\da-f]{2}/gi).map(function(t) {
        return parseInt(t, 16)
    }))), r = "";
    for (e = 0; e < n.length / 16384; e++)
        r += String.fromCharCode.apply(null, n.slice(16384 * e, (e + 1) * 16384));
    return decodeURIComponent(escape(r += String.fromCharCode.apply(null, n.slice(16384 * e))))
}


function er(data,key) {
    return en(ee.AES.decrypt(data,  ee.enc.Utf8.parse(key), {
                    mode: ee.mode.ECB,
                    padding: ee.pad.Pkcs7
                }).toString(ee.enc.Hex))
}
function jiemi(data,headersuser,n) {
    var r = er(data, er(headersuser, n));
    return r;
}
