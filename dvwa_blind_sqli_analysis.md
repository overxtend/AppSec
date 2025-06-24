
# 🛠️ DVWA – Blind SQL Injection Vulnerability Analysis (Low / Medium / High Security)

---

## 🔢 Input Code – LOW Security Level

```php
<?php

if( isset( $_GET[ 'Submit' ] ) ) {
    $id = $_GET[ 'id' ];
    $exists = false;

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
            try {
                $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query );
            } catch (Exception $e) {
                print "There was an error.";
                exit;
            }

            $exists = ($result !== false) ? (mysqli_num_rows( $result ) > 0) : false;
            mysqli_close($GLOBALS["___mysqli_ston"]);
            break;
    }

    if ($exists) {
        $html .= '<pre>User ID exists in the database.</pre>';
    } else {
        header( $_SERVER[ 'SERVER_PROTOCOL' ] . ' 404 Not Found' );
        $html .= '<pre>User ID is MISSING from the database.</pre>';
    }
}
?>
```

## 🛡️ LOW Security Level

### 📌 Overview
The application takes user input from the URL and directly injects it into an SQL query. Although it suppresses error messages, it allows inference of database behavior through response differences—classic **blind SQL injection**.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Unvalidated Input | Direct use of `$_GET['id']` in query  
Blind SQL Injection | Server behavior changes based on input  
No Parameterization | Vulnerable to logic and timing-based attacks  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: sqlmap, curl, browser

🔧 Setup: Navigate to `/vulnerabilities/sqli_blind/` and test with blind injection payloads

🔁 Payload:
?id=1' AND SLEEP(5)--+
?id=1' AND 1=1--+

🎯 Success Indicator:
- Delayed or different response behavior
- “User ID exists” or 404

📸 Screenshot: Use curl or sqlmap output showing delay
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Data Extraction | Time-based or boolean-based enumeration  
Privilege Escalation | Access other tables, bypass authentication  
Stealth Attacks | Hard to detect without verbose errors  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Raw SQL usage | Replace with prepared statements  
Blind logic paths | Do not reflect logic in response codes  
Suppressed errors | Implement proper error logging, not silent fail  
```

---

## 🔢 Input Code – MEDIUM Security Level

```php
<?php

if( isset( $_POST[ 'Submit' ]  ) ) {
    $id = $_POST[ 'id' ];
    $exists = false;

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $id );
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
            try {
                $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query );
            } catch (Exception $e) {
                print "There was an error.";
                exit;
            }

            $exists = ($result !== false) ? (mysqli_num_rows( $result ) > 0) : false;
            break;
    }

    if ($exists) {
        $html .= '<pre>User ID exists in the database.</pre>';
    } else {
        $html .= '<pre>User ID is MISSING from the database.</pre>';
    }
}
?>
```

## 🛡️ MEDIUM Security Level

### 📌 Overview
This level includes escaping via `mysqli_real_escape_string()`, which protects against certain string-based injections but does not defend against logic-based injections using numeric input or timing-based attacks.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Escape Only | Fails to protect against numeric and boolean-based injections  
Blind SQLi | Response still reveals logic via boolean or delay  
No Parameter Binding | Still uses dynamic query with input  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: sqlmap, curl

🔧 Setup: Submit POST request with numeric blind payload

🔁 Payload:
POST id=1 OR IF(1=1, SLEEP(5), 0)

🎯 Success Indicator:
- Delayed response = injected logic evaluated

📸 Screenshot: Use Burp Repeater or sqlmap result with time delay
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Database Enumeration | Attacker can extract full schema  
High Stealth | No SQL error output, hard to detect  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Escaping user input | Use prepared statements with bound parameters  
Blind output | Normalize all application responses  
Time-based injection | Limit execution time and add alerting  
```

---

## 🔢 Input Code – HIGH Security Level

```php
<?php

if( isset( $_COOKIE[ 'id' ] ) ) {
    $id = $_COOKIE[ 'id' ];
    $exists = false;

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
            try {
                $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query );
            } catch (Exception $e) {
                $result = false;
            }

            $exists = ($result !== false) ? (mysqli_num_rows( $result ) > 0) : false;
            mysqli_close($GLOBALS["___mysqli_ston"]);
            break;
    }

    if ($exists) {
        $html .= '<pre>User ID exists in the database.</pre>';
    } else {
        if( rand( 0, 5 ) == 3 ) {
            sleep( rand( 2, 4 ) );
        }
        header( $_SERVER[ 'SERVER_PROTOCOL' ] . ' 404 Not Found' );
        $html .= '<pre>User ID is MISSING from the database.</pre>';
    }
}
?>
```

## 🛡️ HIGH Security Level

### 📌 Overview
The application sources the ID from a cookie and includes a random sleep to thwart timing-based blind SQLi. This is a strong defense, but the SQL query is still constructed unsafely using raw cookie input.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Session-Based Injection | Cookie input is still attacker-controlled  
Randomized Timing | Sleep obfuscation can be bypassed by repetition  
Dynamic Query | Input still directly included in SQL  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: sqlmap

🔧 Setup: Modify `id` cookie with logic payload

🔁 Payload:
Cookie: id=1' AND IF(1=1, SLEEP(5), 0)--

🎯 Success Indicator:
- sqlmap detects and bypasses randomized delay through retries

📸 Screenshot: sqlmap dump and timing result
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Stealthy Extraction | Advanced attacker can still enumerate data  
Obfuscated Detection | Delay-based controls slow detection but don’t block it  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Dynamic SQL | Use parameterized queries  
Untrusted Cookie Input | Validate and sanitize cookies server-side  
Timing Obfuscation | Combine with prepared statements for full mitigation  
```

---
