
# 🛠️ DVWA – Weak Session ID Vulnerability Analysis (Low / Medium / High Security)

---

## 🔢 Input Code – LOW Security Level

```php
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset ($_SESSION['last_session_id'])) {
        $_SESSION['last_session_id'] = 0;
    }
    $_SESSION['last_session_id']++;
    $cookie_value = $_SESSION['last_session_id'];
    setcookie("dvwaSession", $cookie_value);
}
?>
```

## 🛡️ LOW Security Level

### 📌 Overview
The application uses a predictable numeric counter stored in the session to generate the session ID. Each new POST request simply increments this value and sets it as the session ID cookie, making session hijacking trivial.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Predictable Session ID | Uses incremented integer as cookie value  
No Entropy | Easy to guess next or previous session IDs  
No Expiry or Scope | Cookie lacks expiration, path, and secure attributes  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: Browser, curl

🔧 Setup:
Observe session cookie (e.g., dvwaSession=3). Guess previous/next ID.

🔁 Payload:
Manually set `dvwaSession=4` in browser and refresh

🎯 Success Indicator:
Gain access to another user’s session or bypass logic

📸 Screenshot: Show dev tools or intercepted cookie manipulation
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Session Hijacking | Attackers guess active sessions  
Account Takeover | Gain unauthorized access via guessed ID  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Predictable values | Use cryptographically secure random tokens  
No expiration | Set secure expiry and flags (`HttpOnly`, `Secure`)  
Session ID logic | Delegate session management to PHP session engine  
```

---

## 🔢 Input Code – MEDIUM Security Level

```php
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $cookie_value = time();
    setcookie("dvwaSession", $cookie_value);
}
?>
```

## 🛡️ MEDIUM Security Level

### 📌 Overview
This version uses the current UNIX timestamp as the session ID. While less predictable than a counter, it's still guessable with timing attacks or brute force within a narrow time window.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Timestamp-Based ID | Predictable based on server time  
Short Brute Window | Easy to guess within ± few seconds  
No Secure Flags | Missing `Secure`, `HttpOnly`, and proper path  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: Burp Suite, script

🔧 Setup:
Submit login, record timestamp cookie, estimate valid time range

🔁 Payload:
Try `dvwaSession=timestamp±N`

🎯 Success Indicator:
Reuse or predict valid session

📸 Screenshot: Burp cookie brute logic
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Predictable Auth | Timestamp guessing leads to hijack  
Session Replay | Reuse old timestamps before expiration  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Time-based session | Use random UUIDs or secure hashes  
Lack of flags | Always use `HttpOnly`, `Secure`, `SameSite`  
No session backend | Use PHP native session handlers  
```

---

## 🔢 Input Code – HIGH Security Level

```php
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset ($_SESSION['last_session_id_high'])) {
        $_SESSION['last_session_id_high'] = 0;
    }
    $_SESSION['last_session_id_high']++;
    $cookie_value = md5($_SESSION['last_session_id_high']);
    setcookie("dvwaSession", $cookie_value, time()+3600, "/vulnerabilities/weak_id/", $_SERVER['HTTP_HOST'], false, false);
}
?>
```

## 🛡️ HIGH Security Level

### 📌 Overview
This version hashes the counter using MD5, making session ID less obvious. It also includes cookie attributes such as path and expiry. However, the underlying value is still predictable due to its base being an incremented counter.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
MD5 Is Weak | Fast hashing allows brute-forcing small values  
Underlying Pattern | Based on a simple counter, not entropy  
Missing Flags | No `Secure` or `HttpOnly` flags  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: Custom Python script

🔧 Setup:
Observe a few generated session IDs

🔁 Payload:
Generate MD5 hashes of integers 1–100 and test

🎯 Success Indicator:
Session matches one of the brute-forced hashes

📸 Screenshot: Brute force script session match
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Session Brute Force | MD5 hash of counter is quickly enumerable  
Partial Obfuscation | Hashing weak base doesn't ensure security  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Weak randomness | Use `random_bytes()` or `bin2hex()`  
MD5 usage | Replace with `hash('sha256', ...)` or secure libs  
No secure cookie | Enable `Secure`, `HttpOnly`, `SameSite`  
```

---
