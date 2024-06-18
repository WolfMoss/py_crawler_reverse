const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const { window } = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
const $ = require("jquery")(window);
location = window.location
navigator = window.navigator
document = window.document;
history = window.history;
screen = window.screen;

jQuery = $;

(function ($) {
    $.jCryption = function (el, options) {
        var base = this;
        base.$el = $(el);
        base.el = el;
        base.$el.data("jCryption", base);
        base.$el.data("salt", null);
        base.$el.data("key", null);
        base.init = function () {
            base.options = $.extend({}, $.jCryption.defaultOptions, options);
            base.$el.bind('mousemove', function (e) {
                if (base.$el.data("salt") === null) {
                    base.$el.data("salt", (e.pageX + e.pageY) * Math.random());
                } else {
                    base.$el.unbind('mousemove');
                }
            });
            $encryptedElement = $("<input />", {
                type: 'hidden',
                name: base.options.postVariable
            });
            if (base.options.submitElement !== false) {
                var $submitElement = base.options.submitElement;
            } else {
                var $submitElement = base.$el.find(":input:submit");
            }
            $submitElement.bind(base.options.submitEvent, function () {
                $(this).attr("disabled", true);
                if (base.options.beforeEncryption()) {
                    base.authenticate(function (AESEncryptionKey) {
                        var toEncrypt = base.$el.serialize();
                        if ($submitElement.is(":submit")) {
                            toEncrypt = toEncrypt + "&" + $submitElement.attr("name") + "=" + $submitElement.val();
                        }
                        $encryptedElement.val($.jCryption.encrypt(toEncrypt, AESEncryptionKey));
                        $(base.$el).find(base.options.formFieldSelector).attr("disabled", true).end().append($encryptedElement).submit();
                    }, function () {
                        $(base.$el).submit();
                    });
                }
                return false;
            });
        }
            ;
        base.init();
        base.getKey = function () {
            if (base.$el.data("key") !== null) {
                return base.$el.data("key");
            }
            var seed = base.$el.data("salt");
            if (seed === null) {
                seed = Math.floor(Math.random() * Math.random());
            }
            var hashObj = new jsSHA(seed.toString(), "ASCII");
            base.$el.data("key", hashObj.getHash("SHA-512", "HEX"));
            return base.getKey();
        }
            ;
        base.authenticate = function (success, failure) {
            var key = base.getKey();
            $.jCryption.authenticate(key, base.options.getKeysURL, base.options.handshakeURL, success, failure);
        }
            ;
    }
        ;
    $.jCryption.authenticate = function (AESEncryptionKey, publicKeyURL, handshakeURL, success, failure) {
        $.jCryption.getKeys(publicKeyURL, function (keys) {
            $.jCryption.encryptKey(AESEncryptionKey, keys, function (encryptedKey) {
                $.jCryption.handshake(handshakeURL, encryptedKey, function (response) {
                    if ($.jCryption.challenge(response.challenge, AESEncryptionKey)) {
                        success.call(this, AESEncryptionKey);
                    } else {
                        failure.call(this);
                    }
                });
            });
        });
    }
        ;
    $.jCryption.getKeys = function (url, callback) {
        var jCryptionKeyPair = function (encryptionExponent, modulus, maxdigits) {
            setMaxDigits(parseInt(maxdigits, 10));
            this.e = biFromHex(encryptionExponent);
            this.m = biFromHex(modulus);
            this.chunkSize = 2 * biHighIndex(this.m);
            this.radix = 16;
            this.barrett = new BarrettMu(this.m);
        };
        $.getJSON(url, function (data) {
            var keys = new jCryptionKeyPair(data.e, data.n, data.maxdigits);
            if ($.isFunction(callback)) {
                callback.call(this, keys);
            }
        });
    }
        ;
    $.jCryption.decrypt = function (data, key) {
        return Aes.Ctr.decrypt(data, key, 256);
    }
        ;
    $.jCryption.encrypt = function (data, key) {
        return Aes.Ctr.encrypt(data, key, 256);
    }
        ;
    $.jCryption.challenge = function (challenge, key) {
        if ($.jCryption.decrypt(challenge, key) == key) {
            return true;
        }
        return false;
    }
        ;
    $.jCryption.handshake = function (url, key, callback) {
        $.ajax({
            url: url,
            dataType: "json",
            type: "POST",
            data: {
                key: key
            },
            success: function (response) {
                callback.call(this, response);
            }
        });
    }
        ;
    $.jCryption.encryptKey = function (string, keyPair, callback) {
        var charSum = 0;
        for (var i = 0; i < string.length; i++) {
            charSum += string.charCodeAt(i);
        }
        var tag = '0123456789abcdef';
        var hex = '';
        hex += tag.charAt((charSum & 0xF0) >> 4) + tag.charAt(charSum & 0x0F);
        var taggedString = hex + string;
        var encrypt = [];
        var j = 0;
        while (j < taggedString.length) {
            encrypt[j] = taggedString.charCodeAt(j);
            j++;
        }
        while (encrypt.length % keyPair.chunkSize !== 0) {
            encrypt[j++] = 0;
        }
        function encryption(encryptObject) {
            var charCounter = 0;
            var j, block;
            var encrypted = "";
            function encryptChar() {
                block = new BigInt();
                j = 0;
                for (var k = charCounter; k < charCounter + keyPair.chunkSize; ++j) {
                    block.digits[j] = encryptObject[k++];
                    block.digits[j] += encryptObject[k++] << 8;
                }
                var crypt = keyPair.barrett.powMod(block, keyPair.e);
                var text = keyPair.radix == 16 ? biToHex(crypt) : biToString(crypt, keyPair.radix);
                encrypted += text + " ";
                charCounter += keyPair.chunkSize;
                if (charCounter < encryptObject.length) {
                    encryptChar();
                } else {
                    var encryptedString = encrypted.substring(0, encrypted.length - 1);
                    if ($.isFunction(callback)) {
                        callback(encryptedString);
                    } else {
                        return encryptedString;
                    }
                }
            }
            encryptChar();
        }
        encryption(encrypt);
    }
        ;
    $.jCryption.defaultOptions = {
        submitElement: false,
        submitEvent: "click",
        getKeysURL: "main.php?generateKeypair=true",
        handshakeURL: "main.php?handshake=true",
        beforeEncryption: function () {
            return true
        },
        postVariable: "jCryption",
        formFieldSelector: ":input"
    };
    $.fn.jCryption = function (options) {
        return this.each(function () {
            (new $.jCryption(this, options));
        });
    }
        ;
}
)(jQuery);
var biRadixBase = 2;
var biRadixBits = 16;
var bitsPerDigit = biRadixBits;
var biRadix = 1 << 16;
var biHalfRadix = biRadix >>> 1;
var biRadixSquared = biRadix * biRadix;
var maxDigitVal = biRadix - 1;
var maxInteger = 9999999999999998;
var maxDigits;
var ZERO_ARRAY;
var bigZero, bigOne;
var dpl10 = 15;
var highBitMasks = new Array(0x0000, 0x8000, 0xC000, 0xE000, 0xF000, 0xF800, 0xFC00, 0xFE00, 0xFF00, 0xFF80, 0xFFC0, 0xFFE0, 0xFFF0, 0xFFF8, 0xFFFC, 0xFFFE, 0xFFFF);
var hexatrigesimalToChar = new Array('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z');
var hexToChar = new Array('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f');
var lowBitMasks = new Array(0x0000, 0x0001, 0x0003, 0x0007, 0x000F, 0x001F, 0x003F, 0x007F, 0x00FF, 0x01FF, 0x03FF, 0x07FF, 0x0FFF, 0x1FFF, 0x3FFF, 0x7FFF, 0xFFFF);
function setMaxDigits(value) {
    maxDigits = value;
    ZERO_ARRAY = new Array(maxDigits);
    for (var iza = 0; iza < ZERO_ARRAY.length; iza++)
        ZERO_ARRAY[iza] = 0;
    bigZero = new BigInt();
    bigOne = new BigInt();
    bigOne.digits[0] = 1;
}
function BigInt(flag) {
    if (typeof flag == "boolean" && flag == true) {
        this.digits = null;
    } else {
        this.digits = ZERO_ARRAY.slice(0);
    }
    this.isNeg = false;
}
function biFromDecimal(s) {
    var isNeg = s.charAt(0) == '-';
    var i = isNeg ? 1 : 0;
    var result;
    while (i < s.length && s.charAt(i) == '0')
        ++i;
    if (i == s.length) {
        result = new BigInt();
    } else {
        var digitCount = s.length - i;
        var fgl = digitCount % dpl10;
        if (fgl == 0)
            fgl = dpl10;
        result = biFromNumber(Number(s.substr(i, fgl)));
        i += fgl;
        while (i < s.length) {
            result = biAdd(biMultiply(result, biFromNumber(1000000000000000)), biFromNumber(Number(s.substr(i, dpl10))));
            i += dpl10;
        }
        result.isNeg = isNeg;
    }
    return result;
}
function biCopy(bi) {
    var result = new BigInt(true);
    result.digits = bi.digits.slice(0);
    result.isNeg = bi.isNeg;
    return result;
}
function biFromNumber(i) {
    var result = new BigInt();
    result.isNeg = i < 0;
    i = Math.abs(i);
    var j = 0;
    while (i > 0) {
        result.digits[j++] = i & maxDigitVal;
        i >>= biRadixBits;
    }
    return result;
}
function reverseStr(s) {
    var result = "";
    for (var i = s.length - 1; i > -1; --i) {
        result += s.charAt(i);
    }
    return result;
}
function biToString(x, radix) {
    var b = new BigInt();
    b.digits[0] = radix;
    var qr = biDivideModulo(x, b);
    var result = hexatrigesimalToChar[qr[1].digits[0]];
    while (biCompare(qr[0], bigZero) == 1) {
        qr = biDivideModulo(qr[0], b);
        digit = qr[1].digits[0];
        result += hexatrigesimalToChar[qr[1].digits[0]];
    }
    return (x.isNeg ? "-" : "") + reverseStr(result);
}
function biToDecimal(x) {
    var b = new BigInt();
    b.digits[0] = 10;
    var qr = biDivideModulo(x, b);
    var result = String(qr[1].digits[0]);
    while (biCompare(qr[0], bigZero) == 1) {
        qr = biDivideModulo(qr[0], b);
        result += String(qr[1].digits[0]);
    }
    return (x.isNeg ? "-" : "") + reverseStr(result);
}
function digitToHex(n) {
    var mask = 0xf;
    var result = "";
    for (i = 0; i < 4; ++i) {
        result += hexToChar[n & mask];
        n >>>= 4;
    }
    return reverseStr(result);
}
function biToHex(x) {
    var result = "";
    var n = biHighIndex(x);
    for (var i = biHighIndex(x); i > -1; --i) {
        result += digitToHex(x.digits[i]);
    }
    return result;
}
function charToHex(c) {
    var ZERO = 48;
    var NINE = ZERO + 9;
    var littleA = 97;
    var littleZ = littleA + 25;
    var bigA = 65;
    var bigZ = 65 + 25;
    var result;
    if (c >= ZERO && c <= NINE) {
        result = c - ZERO;
    } else if (c >= bigA && c <= bigZ) {
        result = 10 + c - bigA;
    } else if (c >= littleA && c <= littleZ) {
        result = 10 + c - littleA;
    } else {
        result = 0;
    }
    return result;
}
function hexToDigit(s) {
    var result = 0;
    var sl = Math.min(s.length, 4);
    for (var i = 0; i < sl; ++i) {
        result <<= 4;
        result |= charToHex(s.charCodeAt(i))
    }
    return result;
}
function biFromHex(s) {
    var result = new BigInt();
    var sl = s.length;
    for (var i = sl, j = 0; i > 0; i -= 4,
        ++j) {
        result.digits[j] = hexToDigit(s.substr(Math.max(i - 4, 0), Math.min(i, 4)));
    }
    return result;
}
function biFromString(s, radix) {
    var isNeg = s.charAt(0) == '-';
    var istop = isNeg ? 1 : 0;
    var result = new BigInt();
    var place = new BigInt();
    place.digits[0] = 1;
    for (var i = s.length - 1; i >= istop; i--) {
        var c = s.charCodeAt(i);
        var digit = charToHex(c);
        var biDigit = biMultiplyDigit(place, digit);
        result = biAdd(result, biDigit);
        place = biMultiplyDigit(place, radix);
    }
    result.isNeg = isNeg;
    return result;
}
function biDump(b) {
    return (b.isNeg ? "-" : "") + b.digits.join(" ");
}
function biAdd(x, y) {
    var result;
    if (x.isNeg != y.isNeg) {
        y.isNeg = !y.isNeg;
        result = biSubtract(x, y);
        y.isNeg = !y.isNeg;
    } else {
        result = new BigInt();
        var c = 0;
        var n;
        for (var i = 0; i < x.digits.length; ++i) {
            n = x.digits[i] + y.digits[i] + c;
            result.digits[i] = n & 0xffff;
            c = Number(n >= biRadix);
        }
        result.isNeg = x.isNeg;
    }
    return result;
}
function biSubtract(x, y) {
    var result;
    if (x.isNeg != y.isNeg) {
        y.isNeg = !y.isNeg;
        result = biAdd(x, y);
        y.isNeg = !y.isNeg;
    } else {
        result = new BigInt();
        var n, c;
        c = 0;
        for (var i = 0; i < x.digits.length; ++i) {
            n = x.digits[i] - y.digits[i] + c;
            result.digits[i] = n & 0xffff;
            if (result.digits[i] < 0)
                result.digits[i] += biRadix;
            c = 0 - Number(n < 0);
        }
        if (c == -1) {
            c = 0;
            for (var i = 0; i < x.digits.length; ++i) {
                n = 0 - result.digits[i] + c;
                result.digits[i] = n & 0xffff;
                if (result.digits[i] < 0)
                    result.digits[i] += biRadix;
                c = 0 - Number(n < 0);
            }
            result.isNeg = !x.isNeg;
        } else {
            result.isNeg = x.isNeg;
        }
    }
    return result;
}
function biHighIndex(x) {
    var result = x.digits.length - 1;
    while (result > 0 && x.digits[result] == 0)
        --result;
    return result;
}
function biNumBits(x) {
    var n = biHighIndex(x);
    var d = x.digits[n];
    var m = (n + 1) * bitsPerDigit;
    var result;
    for (result = m; result > m - bitsPerDigit; --result) {
        if ((d & 0x8000) != 0)
            break;
        d <<= 1;
    }
    return result;
}
function biMultiply(x, y) {
    var result = new BigInt();
    var c;
    var n = biHighIndex(x);
    var t = biHighIndex(y);
    var u, uv, k;
    for (var i = 0; i <= t; ++i) {
        c = 0;
        k = i;
        for (j = 0; j <= n; ++j,
            ++k) {
            uv = result.digits[k] + x.digits[j] * y.digits[i] + c;
            result.digits[k] = uv & maxDigitVal;
            c = uv >>> biRadixBits;
        }
        result.digits[i + n + 1] = c;
    }
    result.isNeg = x.isNeg != y.isNeg;
    return result;
}
function biMultiplyDigit(x, y) {
    var n, c, uv;
    var result = new BigInt();
    n = biHighIndex(x);
    c = 0;
    for (var j = 0; j <= n; ++j) {
        uv = result.digits[j] + x.digits[j] * y + c;
        result.digits[j] = uv & maxDigitVal;
        c = uv >>> biRadixBits;
    }
    result.digits[1 + n] = c;
    return result;
}
function arrayCopy(src, srcStart, dest, destStart, n) {
    var m = Math.min(srcStart + n, src.length);
    for (var i = srcStart, j = destStart; i < m; ++i,
        ++j) {
        dest[j] = src[i];
    }
}
function biShiftLeft(x, n) {
    var digitCount = Math.floor(n / bitsPerDigit);
    var result = new BigInt();
    arrayCopy(x.digits, 0, result.digits, digitCount, result.digits.length - digitCount);
    var bits = n % bitsPerDigit;
    var rightBits = bitsPerDigit - bits;
    for (var i = result.digits.length - 1, i1 = i - 1; i > 0; --i,
        --i1) {
        result.digits[i] = ((result.digits[i] << bits) & maxDigitVal) | ((result.digits[i1] & highBitMasks[bits]) >>> (rightBits));
    }
    result.digits[0] = ((result.digits[i] << bits) & maxDigitVal);
    result.isNeg = x.isNeg;
    return result;
}
function biShiftRight(x, n) {
    var digitCount = Math.floor(n / bitsPerDigit);
    var result = new BigInt();
    arrayCopy(x.digits, digitCount, result.digits, 0, x.digits.length - digitCount);
    var bits = n % bitsPerDigit;
    var leftBits = bitsPerDigit - bits;
    for (var i = 0, i1 = i + 1; i < result.digits.length - 1; ++i,
        ++i1) {
        result.digits[i] = (result.digits[i] >>> bits) | ((result.digits[i1] & lowBitMasks[bits]) << leftBits);
    }
    result.digits[result.digits.length - 1] >>>= bits;
    result.isNeg = x.isNeg;
    return result;
}
function biMultiplyByRadixPower(x, n) {
    var result = new BigInt();
    arrayCopy(x.digits, 0, result.digits, n, result.digits.length - n);
    return result;
}
function biDivideByRadixPower(x, n) {
    var result = new BigInt();
    arrayCopy(x.digits, n, result.digits, 0, result.digits.length - n);
    return result;
}
function biModuloByRadixPower(x, n) {
    var result = new BigInt();
    arrayCopy(x.digits, 0, result.digits, 0, n);
    return result;
}
function biCompare(x, y) {
    if (x.isNeg != y.isNeg) {
        return 1 - 2 * Number(x.isNeg);
    }
    for (var i = x.digits.length - 1; i >= 0; --i) {
        if (x.digits[i] != y.digits[i]) {
            if (x.isNeg) {
                return 1 - 2 * Number(x.digits[i] > y.digits[i]);
            } else {
                return 1 - 2 * Number(x.digits[i] < y.digits[i]);
            }
        }
    }
    return 0;
}
function biDivideModulo(x, y) {
    var nb = biNumBits(x);
    var tb = biNumBits(y);
    var origYIsNeg = y.isNeg;
    var q, r;
    if (nb < tb) {
        if (x.isNeg) {
            q = biCopy(bigOne);
            q.isNeg = !y.isNeg;
            x.isNeg = false;
            y.isNeg = false;
            r = biSubtract(y, x);
            x.isNeg = true;
            y.isNeg = origYIsNeg;
        } else {
            q = new BigInt();
            r = biCopy(x);
        }
        return new Array(q, r);
    }
    q = new BigInt();
    r = x;
    var t = Math.ceil(tb / bitsPerDigit) - 1;
    var lambda = 0;
    while (y.digits[t] < biHalfRadix) {
        y = biShiftLeft(y, 1);
        ++lambda;
        ++tb;
        t = Math.ceil(tb / bitsPerDigit) - 1;
    }
    r = biShiftLeft(r, lambda);
    nb += lambda;
    var n = Math.ceil(nb / bitsPerDigit) - 1;
    var b = biMultiplyByRadixPower(y, n - t);
    while (biCompare(r, b) != -1) {
        ++q.digits[n - t];
        r = biSubtract(r, b);
    }
    for (var i = n; i > t; --i) {
        var ri = (i >= r.digits.length) ? 0 : r.digits[i];
        var ri1 = (i - 1 >= r.digits.length) ? 0 : r.digits[i - 1];
        var ri2 = (i - 2 >= r.digits.length) ? 0 : r.digits[i - 2];
        var yt = (t >= y.digits.length) ? 0 : y.digits[t];
        var yt1 = (t - 1 >= y.digits.length) ? 0 : y.digits[t - 1];
        if (ri == yt) {
            q.digits[i - t - 1] = maxDigitVal;
        } else {
            q.digits[i - t - 1] = Math.floor((ri * biRadix + ri1) / yt);
        }
        var c1 = q.digits[i - t - 1] * ((yt * biRadix) + yt1);
        var c2 = (ri * biRadixSquared) + ((ri1 * biRadix) + ri2);
        while (c1 > c2) {
            --q.digits[i - t - 1];
            c1 = q.digits[i - t - 1] * ((yt * biRadix) | yt1);
            c2 = (ri * biRadix * biRadix) + ((ri1 * biRadix) + ri2);
        }
        b = biMultiplyByRadixPower(y, i - t - 1);
        r = biSubtract(r, biMultiplyDigit(b, q.digits[i - t - 1]));
        if (r.isNeg) {
            r = biAdd(r, b);
            --q.digits[i - t - 1];
        }
    }
    r = biShiftRight(r, lambda);
    q.isNeg = x.isNeg != origYIsNeg;
    if (x.isNeg) {
        if (origYIsNeg) {
            q = biAdd(q, bigOne);
        } else {
            q = biSubtract(q, bigOne);
        }
        y = biShiftRight(y, lambda);
        r = biSubtract(y, r);
    }
    if (r.digits[0] == 0 && biHighIndex(r) == 0)
        r.isNeg = false;
    return new Array(q, r);
}
function biDivide(x, y) {
    return biDivideModulo(x, y)[0];
}
function biModulo(x, y) {
    return biDivideModulo(x, y)[1];
}
function biMultiplyMod(x, y, m) {
    return biModulo(biMultiply(x, y), m);
}
function biPow(x, y) {
    var result = bigOne;
    var a = x;
    while (true) {
        if ((y & 1) != 0)
            result = biMultiply(result, a);
        y >>= 1;
        if (y == 0)
            break;
        a = biMultiply(a, a);
    }
    return result;
}
function biPowMod(x, y, m) {
    var result = bigOne;
    var a = x;
    var k = y;
    while (true) {
        if ((k.digits[0] & 1) != 0)
            result = biMultiplyMod(result, a, m);
        k = biShiftRight(k, 1);
        if (k.digits[0] == 0 && biHighIndex(k) == 0)
            break;
        a = biMultiplyMod(a, a, m);
    }
    return result;
}
function BarrettMu(m) {
    this.modulus = biCopy(m);
    this.k = biHighIndex(this.modulus) + 1;
    var b2k = new BigInt();
    b2k.digits[2 * this.k] = 1;
    this.mu = biDivide(b2k, this.modulus);
    this.bkplus1 = new BigInt();
    this.bkplus1.digits[this.k + 1] = 1;
    this.modulo = BarrettMu_modulo;
    this.multiplyMod = BarrettMu_multiplyMod;
    this.powMod = BarrettMu_powMod;
}
function BarrettMu_modulo(x) {
    var q1 = biDivideByRadixPower(x, this.k - 1);
    var q2 = biMultiply(q1, this.mu);
    var q3 = biDivideByRadixPower(q2, this.k + 1);
    var r1 = biModuloByRadixPower(x, this.k + 1);
    var r2term = biMultiply(q3, this.modulus);
    var r2 = biModuloByRadixPower(r2term, this.k + 1);
    var r = biSubtract(r1, r2);
    if (r.isNeg) {
        r = biAdd(r, this.bkplus1);
    }
    var rgtem = biCompare(r, this.modulus) >= 0;
    while (rgtem) {
        r = biSubtract(r, this.modulus);
        rgtem = biCompare(r, this.modulus) >= 0;
    }
    return r;
}
function BarrettMu_multiplyMod(x, y) {
    var xy = biMultiply(x, y);
    return this.modulo(xy);
}
function BarrettMu_powMod(x, y) {
    var result = new BigInt();
    result.digits[0] = 1;
    while (true) {
        if ((y.digits[0] & 1) != 0)
            result = this.multiplyMod(result, x);
        y = biShiftRight(y, 1);
        if (y.digits[0] == 0 && biHighIndex(y) == 0)
            break;
        x = this.multiplyMod(x, x);
    }
    return result;
}
var Aes = {};
Aes.cipher = function (input, w) {
    var Nb = 4;
    var Nr = w.length / Nb - 1;
    var state = [[], [], [], []];
    for (var i = 0; i < 4 * Nb; i++)
        state[i % 4][Math.floor(i / 4)] = input[i];
    state = Aes.addRoundKey(state, w, 0, Nb);
    for (var round = 1; round < Nr; round++) {
        state = Aes.subBytes(state, Nb);
        state = Aes.shiftRows(state, Nb);
        state = Aes.mixColumns(state, Nb);
        state = Aes.addRoundKey(state, w, round, Nb);
    }
    state = Aes.subBytes(state, Nb);
    state = Aes.shiftRows(state, Nb);
    state = Aes.addRoundKey(state, w, Nr, Nb);
    var output = new Array(4 * Nb);
    for (var i = 0; i < 4 * Nb; i++)
        output[i] = state[i % 4][Math.floor(i / 4)];
    return output;
}
Aes.keyExpansion = function (key) {
    var Nb = 4;
    var Nk = key.length / 4
    var Nr = Nk + 6;
    var w = new Array(Nb * (Nr + 1));
    var temp = new Array(4);
    for (var i = 0; i < Nk; i++) {
        var r = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]];
        w[i] = r;
    }
    for (var i = Nk; i < (Nb * (Nr + 1)); i++) {
        w[i] = new Array(4);
        for (var t = 0; t < 4; t++)
            temp[t] = w[i - 1][t];
        if (i % Nk == 0) {
            temp = Aes.subWord(Aes.rotWord(temp));
            for (var t = 0; t < 4; t++)
                temp[t] ^= Aes.rCon[i / Nk][t];
        } else if (Nk > 6 && i % Nk == 4) {
            temp = Aes.subWord(temp);
        }
        for (var t = 0; t < 4; t++)
            w[i][t] = w[i - Nk][t] ^ temp[t];
    }
    return w;
}
Aes.subBytes = function (s, Nb) {
    for (var r = 0; r < 4; r++) {
        for (var c = 0; c < Nb; c++)
            s[r][c] = Aes.sBox[s[r][c]];
    }
    return s;
}
Aes.shiftRows = function (s, Nb) {
    var t = new Array(4);
    for (var r = 1; r < 4; r++) {
        for (var c = 0; c < 4; c++)
            t[c] = s[r][(c + r) % Nb];
        for (var c = 0; c < 4; c++)
            s[r][c] = t[c];
    }
    return s;
}
Aes.mixColumns = function (s, Nb) {
    for (var c = 0; c < 4; c++) {
        var a = new Array(4);
        var b = new Array(4);
        for (var i = 0; i < 4; i++) {
            a[i] = s[i][c];
            b[i] = s[i][c] & 0x80 ? s[i][c] << 1 ^ 0x011b : s[i][c] << 1;
        }
        s[0][c] = b[0] ^ a[1] ^ b[1] ^ a[2] ^ a[3];
        s[1][c] = a[0] ^ b[1] ^ a[2] ^ b[2] ^ a[3];
        s[2][c] = a[0] ^ a[1] ^ b[2] ^ a[3] ^ b[3];
        s[3][c] = a[0] ^ b[0] ^ a[1] ^ a[2] ^ b[3];
    }
    return s;
}
Aes.addRoundKey = function (state, w, rnd, Nb) {
    for (var r = 0; r < 4; r++) {
        for (var c = 0; c < Nb; c++)
            state[r][c] ^= w[rnd * 4 + c][r];
    }
    return state;
}
Aes.subWord = function (w) {
    for (var i = 0; i < 4; i++)
        w[i] = Aes.sBox[w[i]];
    return w;
}
Aes.rotWord = function (w) {
    var tmp = w[0];
    for (var i = 0; i < 3; i++)
        w[i] = w[i + 1];
    w[3] = tmp;
    return w;
}
Aes.sBox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16];
Aes.rCon = [[0x00, 0x00, 0x00, 0x00], [0x01, 0x00, 0x00, 0x00], [0x02, 0x00, 0x00, 0x00], [0x04, 0x00, 0x00, 0x00], [0x08, 0x00, 0x00, 0x00], [0x10, 0x00, 0x00, 0x00], [0x20, 0x00, 0x00, 0x00], [0x40, 0x00, 0x00, 0x00], [0x80, 0x00, 0x00, 0x00], [0x1b, 0x00, 0x00, 0x00], [0x36, 0x00, 0x00, 0x00]];
Aes.Ctr = {};
Aes.Ctr.encrypt = function (plaintext, password, nBits) {
    var blockSize = 16;
    if (!(nBits == 128 || nBits == 192 || nBits == 256))
        return '';
    plaintext = Utf8.encode(plaintext);
    password = Utf8.encode(password);
    var nBytes = nBits / 8;
    var pwBytes = new Array(nBytes);
    for (var i = 0; i < nBytes; i++) {
        pwBytes[i] = isNaN(password.charCodeAt(i)) ? 0 : password.charCodeAt(i);
    }
    var key = Aes.cipher(pwBytes, Aes.keyExpansion(pwBytes));
    key = key.concat(key.slice(0, nBytes - 16));
    var counterBlock = new Array(blockSize);
    var nonce = (new Date()).getTime();
    var nonceMs = nonce % 1000;
    var nonceSec = Math.floor(nonce / 1000);
    var nonceRnd = Math.floor(Math.random() * 0xffff);
    for (var i = 0; i < 2; i++)
        counterBlock[i] = (nonceMs >>> i * 8) & 0xff;
    for (var i = 0; i < 2; i++)
        counterBlock[i + 2] = (nonceRnd >>> i * 8) & 0xff;
    for (var i = 0; i < 4; i++)
        counterBlock[i + 4] = (nonceSec >>> i * 8) & 0xff;
    var ctrTxt = '';
    for (var i = 0; i < 8; i++)
        ctrTxt += String.fromCharCode(counterBlock[i]);
    var keySchedule = Aes.keyExpansion(key);
    var blockCount = Math.ceil(plaintext.length / blockSize);
    var ciphertxt = new Array(blockCount);
    for (var b = 0; b < blockCount; b++) {
        for (var c = 0; c < 4; c++)
            counterBlock[15 - c] = (b >>> c * 8) & 0xff;
        for (var c = 0; c < 4; c++)
            counterBlock[15 - c - 4] = (b / 0x100000000 >>> c * 8)
        var cipherCntr = Aes.cipher(counterBlock, keySchedule);
        var blockLength = b < blockCount - 1 ? blockSize : (plaintext.length - 1) % blockSize + 1;
        var cipherChar = new Array(blockLength);
        for (var i = 0; i < blockLength; i++) {
            cipherChar[i] = cipherCntr[i] ^ plaintext.charCodeAt(b * blockSize + i);
            cipherChar[i] = String.fromCharCode(cipherChar[i]);
        }
        ciphertxt[b] = cipherChar.join('');
    }
    var ciphertext = ctrTxt + ciphertxt.join('');
    ciphertext = Base64.encode(ciphertext);
    return ciphertext;
}
Aes.Ctr.decrypt = function (ciphertext, password, nBits) {
    var blockSize = 16;
    if (!(nBits == 128 || nBits == 192 || nBits == 256))
        return '';
    ciphertext = Base64.decode(ciphertext);
    password = Utf8.encode(password);
    var nBytes = nBits / 8;
    var pwBytes = new Array(nBytes);
    for (var i = 0; i < nBytes; i++) {
        pwBytes[i] = isNaN(password.charCodeAt(i)) ? 0 : password.charCodeAt(i);
    }
    var key = Aes.cipher(pwBytes, Aes.keyExpansion(pwBytes));
    key = key.concat(key.slice(0, nBytes - 16));
    var counterBlock = new Array(8);
    ctrTxt = ciphertext.slice(0, 8);
    for (var i = 0; i < 8; i++)
        counterBlock[i] = ctrTxt.charCodeAt(i);
    var keySchedule = Aes.keyExpansion(key);
    var nBlocks = Math.ceil((ciphertext.length - 8) / blockSize);
    var ct = new Array(nBlocks);
    for (var b = 0; b < nBlocks; b++)
        ct[b] = ciphertext.slice(8 + b * blockSize, 8 + b * blockSize + blockSize);
    ciphertext = ct;
    var plaintxt = new Array(ciphertext.length);
    for (var b = 0; b < nBlocks; b++) {
        for (var c = 0; c < 4; c++)
            counterBlock[15 - c] = ((b) >>> c * 8) & 0xff;
        for (var c = 0; c < 4; c++)
            counterBlock[15 - c - 4] = (((b + 1) / 0x100000000 - 1) >>> c * 8) & 0xff;
        var cipherCntr = Aes.cipher(counterBlock, keySchedule);
        var plaintxtByte = new Array(ciphertext[b].length);
        for (var i = 0; i < ciphertext[b].length; i++) {
            plaintxtByte[i] = cipherCntr[i] ^ ciphertext[b].charCodeAt(i);
            plaintxtByte[i] = String.fromCharCode(plaintxtByte[i]);
        }
        plaintxt[b] = plaintxtByte.join('');
    }
    var plaintext = plaintxt.join('');
    plaintext = Utf8.decode(plaintext);
    return plaintext;
}
var Base64 = {};
Base64.code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
Base64.encode = function (str, utf8encode) {
    utf8encode = (typeof utf8encode == 'undefined') ? false : utf8encode;
    var o1, o2, o3, bits, h1, h2, h3, h4, e = [], pad = '', c, plain, coded;
    var b64 = Base64.code;
    plain = utf8encode ? str.encodeUTF8() : str;
    c = plain.length % 3;
    if (c > 0) {
        while (c++ < 3) {
            pad += '=';
            plain += '\0';
        }
    }
    for (c = 0; c < plain.length; c += 3) {
        o1 = plain.charCodeAt(c);
        o2 = plain.charCodeAt(c + 1);
        o3 = plain.charCodeAt(c + 2);
        bits = o1 << 16 | o2 << 8 | o3;
        h1 = bits >> 18 & 0x3f;
        h2 = bits >> 12 & 0x3f;
        h3 = bits >> 6 & 0x3f;
        h4 = bits & 0x3f;
        e[c / 3] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
    }
    coded = e.join('');
    coded = coded.slice(0, coded.length - pad.length) + pad;
    return coded;
}
Base64.decode = function (str, utf8decode) {
    utf8decode = (typeof utf8decode == 'undefined') ? false : utf8decode;
    var o1, o2, o3, h1, h2, h3, h4, bits, d = [], plain, coded;
    var b64 = Base64.code;
    coded = utf8decode ? str.decodeUTF8() : str;
    for (var c = 0; c < coded.length; c += 4) {
        h1 = b64.indexOf(coded.charAt(c));
        h2 = b64.indexOf(coded.charAt(c + 1));
        h3 = b64.indexOf(coded.charAt(c + 2));
        h4 = b64.indexOf(coded.charAt(c + 3));
        bits = h1 << 18 | h2 << 12 | h3 << 6 | h4;
        o1 = bits >>> 16 & 0xff;
        o2 = bits >>> 8 & 0xff;
        o3 = bits & 0xff;
        d[c / 4] = String.fromCharCode(o1, o2, o3);
        if (h4 == 0x40)
            d[c / 4] = String.fromCharCode(o1, o2);
        if (h3 == 0x40)
            d[c / 4] = String.fromCharCode(o1);
    }
    plain = d.join('');
    return utf8decode ? plain.decodeUTF8() : plain;
}
var Utf8 = {};
Utf8.encode = function (strUni) {
    var strUtf = strUni.replace(/[\u0080-\u07ff]/g, function (c) {
        var cc = c.charCodeAt(0);
        return String.fromCharCode(0xc0 | cc >> 6, 0x80 | cc & 0x3f);
    });
    strUtf = strUtf.replace(/[\u0800-\uffff]/g, function (c) {
        var cc = c.charCodeAt(0);
        return String.fromCharCode(0xe0 | cc >> 12, 0x80 | cc >> 6 & 0x3F, 0x80 | cc & 0x3f);
    });
    return strUtf;
}
Utf8.decode = function (strUtf) {
    var strUni = strUtf.replace(/[\u00e0-\u00ef][\u0080-\u00bf][\u0080-\u00bf]/g, function (c) {
        var cc = ((c.charCodeAt(0) & 0x0f) << 12) | ((c.charCodeAt(1) & 0x3f) << 6) | (c.charCodeAt(2) & 0x3f);
        return String.fromCharCode(cc);
    });
    strUni = strUni.replace(/[\u00c0-\u00df][\u0080-\u00bf]/g, function (c) {
        var cc = (c.charCodeAt(0) & 0x1f) << 6 | c.charCodeAt(1) & 0x3f;
        return String.fromCharCode(cc);
    });
    return strUni;
}
var charSize = 8
    , b64pad = ""
    , hexCase = 0
    , Int_64 = function (msint_32, lsint_32) {
        this.highOrder = msint_32;
        this.lowOrder = lsint_32;
    }
    , str2binb = function (str) {
        var bin = [], mask = (1 << charSize) - 1, length = str.length * charSize, i;
        for (i = 0; i < length; i += charSize) {
            bin[i >> 5] |= (str.charCodeAt(i / charSize) & mask) << (32 - charSize - (i % 32));
        }
        return bin;
    }
    , hex2binb = function (str) {
        var bin = [], length = str.length, i, num;
        for (i = 0; i < length; i += 2) {
            num = parseInt(str.substr(i, 2), 16);
            if (!isNaN(num)) {
                bin[i >> 3] |= num << (24 - (4 * (i % 8)));
            } else {
                return "INVALID HEX STRING";
            }
        }
        return bin;
    }
    , binb2hex = function (binarray) {
        var hex_tab = (hexCase) ? "0123456789ABCDEF" : "0123456789abcdef", str = "", length = binarray.length * 4, i, srcByte;
        for (i = 0; i < length; i += 1) {
            srcByte = binarray[i >> 2] >> ((3 - (i % 4)) * 8);
            str += hex_tab.charAt((srcByte >> 4) & 0xF) + hex_tab.charAt(srcByte & 0xF);
        }
        return str;
    }
    , binb2b64 = function (binarray) {
        var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + "0123456789+/", str = "", length = binarray.length * 4, i, j, triplet;
        for (i = 0; i < length; i += 3) {
            triplet = (((binarray[i >> 2] >> 8 * (3 - i % 4)) & 0xFF) << 16) | (((binarray[i + 1 >> 2] >> 8 * (3 - (i + 1) % 4)) & 0xFF) << 8) | ((binarray[i + 2 >> 2] >> 8 * (3 - (i + 2) % 4)) & 0xFF);
            for (j = 0; j < 4; j += 1) {
                if (i * 8 + j * 6 <= binarray.length * 32) {
                    str += tab.charAt((triplet >> 6 * (3 - j)) & 0x3F);
                } else {
                    str += b64pad;
                }
            }
        }
        return str;
    }
    , rotl_32 = function (x, n) {
        return (x << n) | (x >>> (32 - n));
    }
    , rotr_32 = function (x, n) {
        return (x >>> n) | (x << (32 - n));
    }
    , rotr_64 = function (x, n) {
        if (n <= 32) {
            return new Int_64((x.highOrder >>> n) | (x.lowOrder << (32 - n)), (x.lowOrder >>> n) | (x.highOrder << (32 - n)));
        } else {
            return new Int_64((x.lowOrder >>> n) | (x.highOrder << (32 - n)), (x.highOrder >>> n) | (x.lowOrder << (32 - n)));
        }
    }
    , shr_32 = function (x, n) {
        return x >>> n;
    }
    , shr_64 = function (x, n) {
        if (n <= 32) {
            return new Int_64(x.highOrder >>> n, x.lowOrder >>> n | (x.highOrder << (32 - n)));
        } else {
            return new Int_64(0, x.highOrder << (32 - n));
        }
    }
    , parity_32 = function (x, y, z) {
        return x ^ y ^ z;
    }
    , ch_32 = function (x, y, z) {
        return (x & y) ^ (~x & z);
    }
    , ch_64 = function (x, y, z) {
        return new Int_64((x.highOrder & y.highOrder) ^ (~x.highOrder & z.highOrder), (x.lowOrder & y.lowOrder) ^ (~x.lowOrder & z.lowOrder));
    }
    , maj_32 = function (x, y, z) {
        return (x & y) ^ (x & z) ^ (y & z);
    }
    , maj_64 = function (x, y, z) {
        return new Int_64((x.highOrder & y.highOrder) ^ (x.highOrder & z.highOrder) ^ (y.highOrder & z.highOrder), (x.lowOrder & y.lowOrder) ^ (x.lowOrder & z.lowOrder) ^ (y.lowOrder & z.lowOrder));
    }
    , sigma0_32 = function (x) {
        return rotr_32(x, 2) ^ rotr_32(x, 13) ^ rotr_32(x, 22);
    }
    , sigma0_64 = function (x) {
        var rotr28 = rotr_64(x, 28)
            , rotr34 = rotr_64(x, 34)
            , rotr39 = rotr_64(x, 39);
        return new Int_64(rotr28.highOrder ^ rotr34.highOrder ^ rotr39.highOrder, rotr28.lowOrder ^ rotr34.lowOrder ^ rotr39.lowOrder);
    }
    , sigma1_32 = function (x) {
        return rotr_32(x, 6) ^ rotr_32(x, 11) ^ rotr_32(x, 25);
    }
    , sigma1_64 = function (x) {
        var rotr14 = rotr_64(x, 14)
            , rotr18 = rotr_64(x, 18)
            , rotr41 = rotr_64(x, 41);
        return new Int_64(rotr14.highOrder ^ rotr18.highOrder ^ rotr41.highOrder, rotr14.lowOrder ^ rotr18.lowOrder ^ rotr41.lowOrder);
    }
    , gamma0_32 = function (x) {
        return rotr_32(x, 7) ^ rotr_32(x, 18) ^ shr_32(x, 3);
    }
    , gamma0_64 = function (x) {
        var rotr1 = rotr_64(x, 1)
            , rotr8 = rotr_64(x, 8)
            , shr7 = shr_64(x, 7);
        return new Int_64(rotr1.highOrder ^ rotr8.highOrder ^ shr7.highOrder, rotr1.lowOrder ^ rotr8.lowOrder ^ shr7.lowOrder);
    }
    , gamma1_32 = function (x) {
        return rotr_32(x, 17) ^ rotr_32(x, 19) ^ shr_32(x, 10);
    }
    , gamma1_64 = function (x) {
        var rotr19 = rotr_64(x, 19)
            , rotr61 = rotr_64(x, 61)
            , shr6 = shr_64(x, 6);
        return new Int_64(rotr19.highOrder ^ rotr61.highOrder ^ shr6.highOrder, rotr19.lowOrder ^ rotr61.lowOrder ^ shr6.lowOrder);
    }
    , safeAdd_32_2 = function (x, y) {
        var lsw = (x & 0xFFFF) + (y & 0xFFFF)
            , msw = (x >>> 16) + (y >>> 16) + (lsw >>> 16);
        return ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
    }
    , safeAdd_32_4 = function (a, b, c, d) {
        var lsw = (a & 0xFFFF) + (b & 0xFFFF) + (c & 0xFFFF) + (d & 0xFFFF)
            , msw = (a >>> 16) + (b >>> 16) + (c >>> 16) + (d >>> 16) + (lsw >>> 16);
        return ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
    }
    , safeAdd_32_5 = function (a, b, c, d, e) {
        var lsw = (a & 0xFFFF) + (b & 0xFFFF) + (c & 0xFFFF) + (d & 0xFFFF) + (e & 0xFFFF)
            , msw = (a >>> 16) + (b >>> 16) + (c >>> 16) + (d >>> 16) + (e >>> 16) + (lsw >>> 16);
        return ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
    }
    , safeAdd_64_2 = function (x, y) {
        var lsw, msw, lowOrder, highOrder;
        lsw = (x.lowOrder & 0xFFFF) + (y.lowOrder & 0xFFFF);
        msw = (x.lowOrder >>> 16) + (y.lowOrder >>> 16) + (lsw >>> 16);
        lowOrder = ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
        lsw = (x.highOrder & 0xFFFF) + (y.highOrder & 0xFFFF) + (msw >>> 16);
        msw = (x.highOrder >>> 16) + (y.highOrder >>> 16) + (lsw >>> 16);
        highOrder = ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
        return new Int_64(highOrder, lowOrder);
    }
    , safeAdd_64_4 = function (a, b, c, d) {
        var lsw, msw, lowOrder, highOrder;
        lsw = (a.lowOrder & 0xFFFF) + (b.lowOrder & 0xFFFF) + (c.lowOrder & 0xFFFF) + (d.lowOrder & 0xFFFF);
        msw = (a.lowOrder >>> 16) + (b.lowOrder >>> 16) + (c.lowOrder >>> 16) + (d.lowOrder >>> 16) + (lsw >>> 16);
        lowOrder = ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
        lsw = (a.highOrder & 0xFFFF) + (b.highOrder & 0xFFFF) + (c.highOrder & 0xFFFF) + (d.highOrder & 0xFFFF) + (msw >>> 16);
        msw = (a.highOrder >>> 16) + (b.highOrder >>> 16) + (c.highOrder >>> 16) + (d.highOrder >>> 16) + (lsw >>> 16);
        highOrder = ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
        return new Int_64(highOrder, lowOrder);
    }
    , safeAdd_64_5 = function (a, b, c, d, e) {
        var lsw, msw, lowOrder, highOrder;
        lsw = (a.lowOrder & 0xFFFF) + (b.lowOrder & 0xFFFF) + (c.lowOrder & 0xFFFF) + (d.lowOrder & 0xFFFF) + (e.lowOrder & 0xFFFF);
        msw = (a.lowOrder >>> 16) + (b.lowOrder >>> 16) + (c.lowOrder >>> 16) + (d.lowOrder >>> 16) + (e.lowOrder >>> 16) + (lsw >>> 16);
        lowOrder = ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
        lsw = (a.highOrder & 0xFFFF) + (b.highOrder & 0xFFFF) + (c.highOrder & 0xFFFF) + (d.highOrder & 0xFFFF) + (e.highOrder & 0xFFFF) + (msw >>> 16);
        msw = (a.highOrder >>> 16) + (b.highOrder >>> 16) + (c.highOrder >>> 16) + (d.highOrder >>> 16) + (e.highOrder >>> 16) + (lsw >>> 16);
        highOrder = ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
        return new Int_64(highOrder, lowOrder);
    }
    , coreSHA1 = function (message, messageLen) {
        var W = [], a, b, c, d, e, T, ch = ch_32, parity = parity_32, maj = maj_32, rotl = rotl_32, safeAdd_2 = safeAdd_32_2, i, t, safeAdd_5 = safeAdd_32_5, appendedMessageLength, H = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0], K = [0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6];
        message[messageLen >> 5] |= 0x80 << (24 - (messageLen % 32));
        message[(((messageLen + 65) >> 9) << 4) + 15] = messageLen;
        appendedMessageLength = message.length;
        for (i = 0; i < appendedMessageLength; i += 16) {
            a = H[0];
            b = H[1];
            c = H[2];
            d = H[3];
            e = H[4];
            for (t = 0; t < 80; t += 1) {
                if (t < 16) {
                    W[t] = message[t + i];
                } else {
                    W[t] = rotl(W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16], 1);
                }
                if (t < 20) {
                    T = safeAdd_5(rotl(a, 5), ch(b, c, d), e, K[t], W[t]);
                } else if (t < 40) {
                    T = safeAdd_5(rotl(a, 5), parity(b, c, d), e, K[t], W[t]);
                } else if (t < 60) {
                    T = safeAdd_5(rotl(a, 5), maj(b, c, d), e, K[t], W[t]);
                } else {
                    T = safeAdd_5(rotl(a, 5), parity(b, c, d), e, K[t], W[t]);
                }
                e = d;
                d = c;
                c = rotl(b, 30);
                b = a;
                a = T;
            }
            H[0] = safeAdd_2(a, H[0]);
            H[1] = safeAdd_2(b, H[1]);
            H[2] = safeAdd_2(c, H[2]);
            H[3] = safeAdd_2(d, H[3]);
            H[4] = safeAdd_2(e, H[4]);
        }
        return H;
    }
    , coreSHA2 = function (message, messageLen, variant) {
        var a, b, c, d, e, f, g, h, T1, T2, H, numRounds, lengthPosition, i, t, binaryStringInc, binaryStringMult, safeAdd_2, safeAdd_4, safeAdd_5, gamma0, gamma1, sigma0, sigma1, ch, maj, Int, K, W = [], appendedMessageLength;
        if (variant === "SHA-224" || variant === "SHA-256") {
            numRounds = 64;
            lengthPosition = (((messageLen + 65) >> 9) << 4) + 15;
            binaryStringInc = 16;
            binaryStringMult = 1;
            Int = Number;
            safeAdd_2 = safeAdd_32_2;
            safeAdd_4 = safeAdd_32_4;
            safeAdd_5 = safeAdd_32_5;
            gamma0 = gamma0_32;
            gamma1 = gamma1_32;
            sigma0 = sigma0_32;
            sigma1 = sigma1_32;
            maj = maj_32;
            ch = ch_32;
            K = [0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA, 0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070, 0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2];
            if (variant === "SHA-224") {
                H = [0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939, 0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4];
            } else {
                H = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19];
            }
        } else if (variant === "SHA-384" || variant === "SHA-512") {
            numRounds = 80;
            lengthPosition = (((messageLen + 128) >> 10) << 5) + 31;
            binaryStringInc = 32;
            binaryStringMult = 2;
            Int = Int_64;
            safeAdd_2 = safeAdd_64_2;
            safeAdd_4 = safeAdd_64_4;
            safeAdd_5 = safeAdd_64_5;
            gamma0 = gamma0_64;
            gamma1 = gamma1_64;
            sigma0 = sigma0_64;
            sigma1 = sigma1_64;
            maj = maj_64;
            ch = ch_64;
            K = [new Int(0x428a2f98, 0xd728ae22), new Int(0x71374491, 0x23ef65cd), new Int(0xb5c0fbcf, 0xec4d3b2f), new Int(0xe9b5dba5, 0x8189dbbc), new Int(0x3956c25b, 0xf348b538), new Int(0x59f111f1, 0xb605d019), new Int(0x923f82a4, 0xaf194f9b), new Int(0xab1c5ed5, 0xda6d8118), new Int(0xd807aa98, 0xa3030242), new Int(0x12835b01, 0x45706fbe), new Int(0x243185be, 0x4ee4b28c), new Int(0x550c7dc3, 0xd5ffb4e2), new Int(0x72be5d74, 0xf27b896f), new Int(0x80deb1fe, 0x3b1696b1), new Int(0x9bdc06a7, 0x25c71235), new Int(0xc19bf174, 0xcf692694), new Int(0xe49b69c1, 0x9ef14ad2), new Int(0xefbe4786, 0x384f25e3), new Int(0x0fc19dc6, 0x8b8cd5b5), new Int(0x240ca1cc, 0x77ac9c65), new Int(0x2de92c6f, 0x592b0275), new Int(0x4a7484aa, 0x6ea6e483), new Int(0x5cb0a9dc, 0xbd41fbd4), new Int(0x76f988da, 0x831153b5), new Int(0x983e5152, 0xee66dfab), new Int(0xa831c66d, 0x2db43210), new Int(0xb00327c8, 0x98fb213f), new Int(0xbf597fc7, 0xbeef0ee4), new Int(0xc6e00bf3, 0x3da88fc2), new Int(0xd5a79147, 0x930aa725), new Int(0x06ca6351, 0xe003826f), new Int(0x14292967, 0x0a0e6e70), new Int(0x27b70a85, 0x46d22ffc), new Int(0x2e1b2138, 0x5c26c926), new Int(0x4d2c6dfc, 0x5ac42aed), new Int(0x53380d13, 0x9d95b3df), new Int(0x650a7354, 0x8baf63de), new Int(0x766a0abb, 0x3c77b2a8), new Int(0x81c2c92e, 0x47edaee6), new Int(0x92722c85, 0x1482353b), new Int(0xa2bfe8a1, 0x4cf10364), new Int(0xa81a664b, 0xbc423001), new Int(0xc24b8b70, 0xd0f89791), new Int(0xc76c51a3, 0x0654be30), new Int(0xd192e819, 0xd6ef5218), new Int(0xd6990624, 0x5565a910), new Int(0xf40e3585, 0x5771202a), new Int(0x106aa070, 0x32bbd1b8), new Int(0x19a4c116, 0xb8d2d0c8), new Int(0x1e376c08, 0x5141ab53), new Int(0x2748774c, 0xdf8eeb99), new Int(0x34b0bcb5, 0xe19b48a8), new Int(0x391c0cb3, 0xc5c95a63), new Int(0x4ed8aa4a, 0xe3418acb), new Int(0x5b9cca4f, 0x7763e373), new Int(0x682e6ff3, 0xd6b2b8a3), new Int(0x748f82ee, 0x5defb2fc), new Int(0x78a5636f, 0x43172f60), new Int(0x84c87814, 0xa1f0ab72), new Int(0x8cc70208, 0x1a6439ec), new Int(0x90befffa, 0x23631e28), new Int(0xa4506ceb, 0xde82bde9), new Int(0xbef9a3f7, 0xb2c67915), new Int(0xc67178f2, 0xe372532b), new Int(0xca273ece, 0xea26619c), new Int(0xd186b8c7, 0x21c0c207), new Int(0xeada7dd6, 0xcde0eb1e), new Int(0xf57d4f7f, 0xee6ed178), new Int(0x06f067aa, 0x72176fba), new Int(0x0a637dc5, 0xa2c898a6), new Int(0x113f9804, 0xbef90dae), new Int(0x1b710b35, 0x131c471b), new Int(0x28db77f5, 0x23047d84), new Int(0x32caab7b, 0x40c72493), new Int(0x3c9ebe0a, 0x15c9bebc), new Int(0x431d67c4, 0x9c100d4c), new Int(0x4cc5d4be, 0xcb3e42b6), new Int(0x597f299c, 0xfc657e2a), new Int(0x5fcb6fab, 0x3ad6faec), new Int(0x6c44198c, 0x4a475817)];
            if (variant === "SHA-384") {
                H = [new Int(0xcbbb9d5d, 0xc1059ed8), new Int(0x0629a292a, 0x367cd507), new Int(0x9159015a, 0x3070dd17), new Int(0x0152fecd8, 0xf70e5939), new Int(0x67332667, 0xffc00b31), new Int(0x98eb44a87, 0x68581511), new Int(0xdb0c2e0d, 0x64f98fa7), new Int(0x047b5481d, 0xbefa4fa4)];
            } else {
                H = [new Int(0x6a09e667, 0xf3bcc908), new Int(0xbb67ae85, 0x84caa73b), new Int(0x3c6ef372, 0xfe94f82b), new Int(0xa54ff53a, 0x5f1d36f1), new Int(0x510e527f, 0xade682d1), new Int(0x9b05688c, 0x2b3e6c1f), new Int(0x1f83d9ab, 0xfb41bd6b), new Int(0x5be0cd19, 0x137e2179)];
            }
        }
        message[messageLen >> 5] |= 0x80 << (24 - messageLen % 32);
        message[lengthPosition] = messageLen;
        appendedMessageLength = message.length;
        for (i = 0; i < appendedMessageLength; i += binaryStringInc) {
            a = H[0];
            b = H[1];
            c = H[2];
            d = H[3];
            e = H[4];
            f = H[5];
            g = H[6];
            h = H[7];
            for (t = 0; t < numRounds; t += 1) {
                if (t < 16) {
                    W[t] = new Int(message[t * binaryStringMult + i], message[t * binaryStringMult + i + 1]);
                } else {
                    W[t] = safeAdd_4(gamma1(W[t - 2]), W[t - 7], gamma0(W[t - 15]), W[t - 16]);
                }
                T1 = safeAdd_5(h, sigma1(e), ch(e, f, g), K[t], W[t]);
                T2 = safeAdd_2(sigma0(a), maj(a, b, c));
                h = g;
                g = f;
                f = e;
                e = safeAdd_2(d, T1);
                d = c;
                c = b;
                b = a;
                a = safeAdd_2(T1, T2);
            }
            H[0] = safeAdd_2(a, H[0]);
            H[1] = safeAdd_2(b, H[1]);
            H[2] = safeAdd_2(c, H[2]);
            H[3] = safeAdd_2(d, H[3]);
            H[4] = safeAdd_2(e, H[4]);
            H[5] = safeAdd_2(f, H[5]);
            H[6] = safeAdd_2(g, H[6]);
            H[7] = safeAdd_2(h, H[7]);
        }
        switch (variant) {
            case "SHA-224":
                return [H[0], H[1], H[2], H[3], H[4], H[5], H[6]];
            case "SHA-256":
                return H;
            case "SHA-384":
                return [H[0].highOrder, H[0].lowOrder, H[1].highOrder, H[1].lowOrder, H[2].highOrder, H[2].lowOrder, H[3].highOrder, H[3].lowOrder, H[4].highOrder, H[4].lowOrder, H[5].highOrder, H[5].lowOrder];
            case "SHA-512":
                return [H[0].highOrder, H[0].lowOrder, H[1].highOrder, H[1].lowOrder, H[2].highOrder, H[2].lowOrder, H[3].highOrder, H[3].lowOrder, H[4].highOrder, H[4].lowOrder, H[5].highOrder, H[5].lowOrder, H[6].highOrder, H[6].lowOrder, H[7].highOrder, H[7].lowOrder];
            default:
                return [];
        }
    }
    , jsSHA = function (srcString, inputFormat) {
        this.sha1 = null;
        this.sha224 = null;
        this.sha256 = null;
        this.sha384 = null;
        this.sha512 = null;
        this.strBinLen = null;
        this.strToHash = null;
        if ("HEX" === inputFormat) {
            if (0 !== (srcString.length % 2)) {
                return "TEXT MUST BE IN BYTE INCREMENTS";
            }
            this.strBinLen = srcString.length * 4;
            this.strToHash = hex2binb(srcString);
        } else if (("ASCII" === inputFormat) || ('undefined' === typeof (inputFormat))) {
            this.strBinLen = srcString.length * charSize;
            this.strToHash = str2binb(srcString);
        } else {
            return "UNKNOWN TEXT INPUT TYPE";
        }
    };
jsSHA.prototype = {
    getHash: function (variant, format) {
        var formatFunc = null
            , message = this.strToHash.slice();
        switch (format) {
            case "HEX":
                formatFunc = binb2hex;
                break;
            case "B64":
                formatFunc = binb2b64;
                break;
            default:
                return "FORMAT NOT RECOGNIZED";
        }
        switch (variant) {
            case "SHA-1":
                if (null === this.sha1) {
                    this.sha1 = coreSHA1(message, this.strBinLen);
                }
                return formatFunc(this.sha1);
            case "SHA-224":
                if (null === this.sha224) {
                    this.sha224 = coreSHA2(message, this.strBinLen, variant);
                }
                return formatFunc(this.sha224);
            case "SHA-256":
                if (null === this.sha256) {
                    this.sha256 = coreSHA2(message, this.strBinLen, variant);
                }
                return formatFunc(this.sha256);
            case "SHA-384":
                if (null === this.sha384) {
                    this.sha384 = coreSHA2(message, this.strBinLen, variant);
                }
                return formatFunc(this.sha384);
            case "SHA-512":
                if (null === this.sha512) {
                    this.sha512 = coreSHA2(message, this.strBinLen, variant);
                }
                return formatFunc(this.sha512);
            default:
                return "HASH NOT RECOGNIZED";
        }
    },
    getHMAC: function (key, inputFormat, variant, outputFormat) {
        var formatFunc, keyToUse, blockByteSize, blockBitSize, i, retVal, lastArrayIndex, keyBinLen, hashBitSize, keyWithIPad = [], keyWithOPad = [];
        switch (outputFormat) {
            case "HEX":
                formatFunc = binb2hex;
                break;
            case "B64":
                formatFunc = binb2b64;
                break;
            default:
                return "FORMAT NOT RECOGNIZED";
        }
        switch (variant) {
            case "SHA-1":
                blockByteSize = 64;
                hashBitSize = 160;
                break;
            case "SHA-224":
                blockByteSize = 64;
                hashBitSize = 224;
                break;
            case "SHA-256":
                blockByteSize = 64;
                hashBitSize = 256;
                break;
            case "SHA-384":
                blockByteSize = 128;
                hashBitSize = 384;
                break;
            case "SHA-512":
                blockByteSize = 128;
                hashBitSize = 512;
                break;
            default:
                return "HASH NOT RECOGNIZED";
        }
        if ("HEX" === inputFormat) {
            if (0 !== (key.length % 2)) {
                return "KEY MUST BE IN BYTE INCREMENTS";
            }
            keyToUse = hex2binb(key);
            keyBinLen = key.length * 4;
        } else if ("ASCII" === inputFormat) {
            keyToUse = str2binb(key);
            keyBinLen = key.length * charSize;
        } else {
            return "UNKNOWN KEY INPUT TYPE";
        }
        blockBitSize = blockByteSize * 8;
        lastArrayIndex = (blockByteSize / 4) - 1;
        if (blockByteSize < (keyBinLen / 8)) {
            if ("SHA-1" === variant) {
                keyToUse = coreSHA1(keyToUse, keyBinLen);
            } else {
                keyToUse = coreSHA2(keyToUse, keyBinLen, variant);
            }
            keyToUse[lastArrayIndex] &= 0xFFFFFF00;
        } else if (blockByteSize > (keyBinLen / 8)) {
            keyToUse[lastArrayIndex] &= 0xFFFFFF00;
        }
        for (i = 0; i <= lastArrayIndex; i += 1) {
            keyWithIPad[i] = keyToUse[i] ^ 0x36363636;
            keyWithOPad[i] = keyToUse[i] ^ 0x5C5C5C5C;
        }
        if ("SHA-1" === variant) {
            retVal = coreSHA1(keyWithIPad.concat(this.strToHash), blockBitSize + this.strBinLen);
            retVal = coreSHA1(keyWithOPad.concat(retVal), blockBitSize + hashBitSize);
        } else {
            retVal = coreSHA2(keyWithIPad.concat(this.strToHash), blockBitSize + this.strBinLen, variant);
            retVal = coreSHA2(keyWithOPad.concat(retVal), blockBitSize + hashBitSize, variant);
        }
        return (formatFunc(retVal));
    }
};
window.jsSHA = jsSHA;
$.jCryption.setkey = function (e, n, maxdigits) {
    var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
    var string_length = 128;
    var randomstring = '';
    for (var i = 0; i < string_length; i++) {
        var rnum = Math.floor(Math.random() * chars.length);
        randomstring += chars.substring(rnum, rnum + 1);
    }
    $.jCryption.key0 = (new jsSHA(randomstring, "ASCII")).getHash("SHA-512", "HEX");
    $.jCryption.key1 = "";
    var jCryptionKeyPair = function (encryptionExponent, modulus, maxdigits) {
        setMaxDigits(parseInt(maxdigits, 10));
        this.e = biFromHex(encryptionExponent);
        this.m = biFromHex(modulus);
        this.chunkSize = 2 * biHighIndex(this.m);
        this.radix = 16;
        this.barrett = new BarrettMu(this.m);
    };
    $.jCryption.encryptKey($.jCryption.key0, new jCryptionKeyPair(e, n, maxdigits), function (key) {
        $.jCryption.key1 = key;
    });
}


function getkey_value() {
    $.jCryption.setkey("10001","858d40ed9c006a37fa9163448a3177901046abdc4c6bf5cae180d21a0f811044bb980a346b2e31b8a57c9aa3572db69c1d0b978df5037d1b0e3a670c352ebcf8ad389123b5cb24511768e322e8c9c3e04e3fd1f528fba50446d99b3dfd9d2dd446f38245a84271fae1c92161bc5894e3a6615fe3e9afcc0e46071fe156e1cc09",131)

    let userpswd = "username=axibaxxxx&password=xxxaaa&repassword=";


    let jCryptionKey = $.jCryption.key1;
    let jCryptionValue = $.jCryption.encrypt(userpswd,$.jCryption.key0);
    return {
        jCryptionKey:jCryptionKey,
        jCryptionValue:jCryptionValue
    }
}
