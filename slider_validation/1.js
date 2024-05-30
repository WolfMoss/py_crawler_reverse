//加载2.js
const {ciphertext_base64} = require('./2.js')


let oua = decrypt(ciphertext_base64)
console.log('oua:::',oua)

function u(t) {
    var e = t.length;
    if (e % 4 > 0)
        throw new Error("Invalid string. Length must be a multiple of 4");
    var i = t.indexOf("=");
    return -1 === i && (i = e),
        [i, i === e ? 0 : 4 - i % 4]
}

function base64ToArrayBuffer(base64) {
    // 使用Buffer对象进行Base64解码
    const buffer = Buffer.from(base64, 'base64');

    // 创建一个ArrayBuffer，长度为Buffer对象的字节长度
    const arrayBuffer = new ArrayBuffer(buffer.length);
    const uint8Array = new Uint8Array(arrayBuffer);

    // 将Buffer对象的数据拷贝到Uint8Array中
    for (let i = 0; i < buffer.length; i++) {
        uint8Array[i] = buffer[i];
    }

    return arrayBuffer;
}

function dePadding(e) {
    if (null === e)
        return null;
    var c = e[e.length - 1];
    return e.slice(0, e.length - c)
}

function uint8ToUint32Block(e, c) {
    void 0 === c && (c = 0);
    var n = new Uint32Array(4);
    return n[0] = e[c] << 24 | e[c + 1] << 16 | e[c + 2] << 8 | e[c + 3],
        n[1] = e[c + 4] << 24 | e[c + 5] << 16 | e[c + 6] << 8 | e[c + 7],
        n[2] = e[c + 8] << 24 | e[c + 9] << 16 | e[c + 10] << 8 | e[c + 11],
        n[3] = e[c + 12] << 24 | e[c + 13] << 16 | e[c + 14] << 8 | e[c + 15],
        n
}
function rotateLeft(e, c) {
    return e << c | e >>> 32 - c
}
function tauTransform(e) {
    f   = Uint8Array
    return f[e >>> 24 & 255] << 24 | f[e >>> 16 & 255] << 16 | f[e >>> 8 & 255] << 8 | f[255 & e]
}
function linearTransform1(e) {
    return e ^ rotateLeft(e, 2) ^ rotateLeft(e, 10) ^ rotateLeft(e, 18) ^ rotateLeft(e, 24)
}

function tTransform1(e) {
    var c = tauTransform(e);
    return linearTransform1(c)
}

function doBlockCrypt(e, c) {
    var n = new Uint32Array(36);
    n.set(e, 0);
    for (var t = 0; t < 32; t++)
        n[t + 4] = n[t] ^ tTransform1(n[t + 1] ^ n[t + 2] ^ n[t + 3] ^ Uint32Array[t]);
    var a = new Uint32Array(4);
    return a[0] = n[35],
        a[1] = n[34],
        a[2] = n[33],
        a[3] = n[32],
        a
}


function decrypt(e) {
    this.key = '105301254077073220393000606678240'
    this.mode = "cbc"
    this.iv = this.key.substring(0, 8) + this.key.substring(this.key.length - 8, this.key.length)

    var c = new Uint8Array

        // 根据 cipherType 选择转换函数并获取 ArrayBuffer
    c = base64ToArrayBuffer(e);
    var n = c.byteLength / 16;
    var t = new Uint8Array(c.byteLength);
    if ("cbc" === this.mode) {
        console.log("进入cbc")
        for (var a = uint8ToUint32Block(this.iv), s = 0; s < n; s++) {
            var u = 16 * s
                , i = uint8ToUint32Block(c, u)
                , o = doBlockCrypt(i, this.decryptRoundKeys);
            (h = new Uint32Array(4))[0] = a[0] ^ o[0],
                h[1] = a[1] ^ o[1],
                h[2] = a[2] ^ o[2],
                h[3] = a[3] ^ o[3],
                a = i;
            for (var r = 0; r < 16; r++)
                t[u + r] = h[parseInt(r / 4)] >> (3 - r) % 4 * 8 & 255
        }
    }

    var d = dePadding(t);
    console.log("出cbc,d",d.length)
    return utf8ArrayBufferToString(d)
}

// function utf8ArrayBufferToString(e) {
//     console.log("e",e)
//     const c = [];
//     for (let n = 0, t = e.length; n < t; n++)
//         e[n] >= 240 && e[n] <= 247 ? (c.push(String.fromCodePoint(((7 & e[n]) << 18) + ((63 & e[n + 1]) << 12) + ((63 & e[n + 2]) << 6) + (63 & e[n + 3]))),
//         n += 3) : e[n] >= 224 && e[n] <= 239 ? (c.push(String.fromCodePoint(((15 & e[n]) << 12) + ((63 & e[n + 1]) << 6) + (63 & e[n + 2]))),
//         n += 2) : e[n] >= 192 && e[n] <= 223 ? (c.push(String.fromCodePoint(((31 & e[n]) << 6) + (63 & e[n + 1]))),
//         n++) : c.push(String.fromCodePoint(e[n]));
//     console.log("c",c)
//     return c.join("")
// }

function utf8ArrayBufferToString(arrayBuffer) {
    console.log("arrayBuffer:::",arrayBuffer)
    console.log("Hello, World!:::",new Uint8Array([72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33]))
    arrayBuffer = arrayBuffer.buffer;
    console.log("arrayBufferbuffer:::",arrayBuffer)

    // 使用 TextDecoder 将 ArrayBuffer 转换为字符串
    const decoder = new TextDecoder('utf-8');
    const decodedString = decoder.decode(arrayBuffer);
    console.log("decodedString:::",decodedString)
    return decodedString;
}