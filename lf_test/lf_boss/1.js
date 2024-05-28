//t = 获取cookie中的__zp_sseed__
t = "InZUA4w/K1dI3DRsaDIFu1FUTQ0JpnkJ0ZgiwEwnHOo="
r = (new e).z(t, Date.now())
set(r)
function set(token) {
    const key = '__zp_stoken__';
    const maxAgeInMinutes = 3840; // 64 hours
    const domain = ".zhipin.com";
    const path = "/";

    // Construct the cookie string
    let cookiePair = `${key}=${encodeURIComponent(token)}`;

    // Set expiration date if max age is provided
    if (maxAgeInMinutes) {
        const expirationDate = new Date();
        expirationDate.setTime(expirationDate.getTime() + maxAgeInMinutes * 60 * 1000);
        cookiePair += `;expires=${expirationDate.toGMTString()}`;
    }

    // Add domain and path to cookie pair if they exist
    cookiePair = domain ? `${cookiePair};domain=${domain}` : cookiePair;
    cookiePair = path ? `${cookiePair};path=${path}` : cookiePair;

    // Set the cookie in the document
    document.cookie = cookiePair;
}