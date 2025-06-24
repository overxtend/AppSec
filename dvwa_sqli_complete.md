
# 🛠️ DVWA – SQL Injection Vulnerability Analysis (Low / Medium / High Security)

---

## 🔢 Input Code – LOW Security Level

```php
<?php

if( isset( $_REQUEST[ 'Submit' ] ) ) {
    $id = $_REQUEST[ 'id' ];

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
            $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

            while( $row = mysqli_fetch_assoc( $result ) ) {
                $first = $row["first_name"];
                $last  = $row["last_name"];
                $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
            }

            mysqli_close($GLOBALS["___mysqli_ston"]);
            break;
        case SQLITE:
            global $sqlite_db_connection;
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
            try {
                $results = $sqlite_db_connection->query($query);
            } catch (Exception $e) {
                echo 'Caught exception: ' . $e->getMessage();
                exit();
            }

            if ($results) {
                while ($row = $results->fetchArray()) {
                    $first = $row["first_name"];
                    $last  = $row["last_name"];
                    $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
                }
            }
            break;
    } 
}
?>
```

## 🛡️ LOW Security Level

### 📌 Overview
The code takes direct user input from the `id` parameter and injects it into an SQL query without any validation or escaping. This exposes the application to **classic SQL injection**, allowing attackers to manipulate the query, access unauthorized data, or compromise the backend.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Unfiltered User Input | No input validation or escaping allows SQL manipulation  
Dynamic Query Construction | The `$id` variable is injected directly into the SQL string  
Database Disclosure | Errors may reveal DB info due to `die(mysqli_error(...))`  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: Browser, Burp Suite, curl

🔧 Setup:
- Navigate to: `/vulnerabilities/sqli/`
- Enter payload in ID field

🔁 Payload:
?id=1' OR '1'='1--+

🎯 Success Indicator:
- Displays all user records instead of one
- Errors may disclose SQL structure

📸 Screenshot: Include Burp Repeater or browser result page
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Full DB Dump | Attacker can extract all data using UNION queries  
Authentication Bypass | Logic flaws enable unauthorized access  
Privilege Escalation | Potential lateral movement inside the app  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Raw SQL concatenation | Use parameterized queries (prepared statements)  
Lack of input filtering | Enforce strict type checking on input  
Exposed DB errors | Disable verbose error messages in production  
```

---

## 🔢 Input Code – MEDIUM Security Level

```php
<?php

if( isset( $_POST[ 'Submit' ] ) ) {
    $id = $_POST[ 'id' ];
    $id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $id);

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
            $result = mysqli_query($GLOBALS["___mysqli_ston"], $query) or die( '<pre>' . mysqli_error($GLOBALS["___mysqli_ston"]) . '</pre>' );

            while( $row = mysqli_fetch_assoc( $result ) ) {
                $first = $row["first_name"];
                $last  = $row["last_name"];
                $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
            }
            break;
    }
}
?>
```

## 🛡️ MEDIUM Security Level

### 📌 Overview
This version introduces `mysqli_real_escape_string()` to sanitize input. Although this mitigates some risk, the protection is insufficient against **numeric-based** or **blind** SQL injection, especially when string quotes are removed and logic injection is attempted.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Partial Input Sanitization | Escaping only applies to strings; logic operators may pass  
No Parameterization | Query is still built with raw input  
Error Handling | Die function can still leak DB structure  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: Burp Suite, curl, sqlmap

🔧 Setup:
Submit POST request with `id=1 OR 1=1`

🔁 Payload:
curl -X POST -d "id=1 OR 1=1&Submit=Submit" http://localhost/vulnerabilities/sqli/

🎯 Success Indicator:
- Multiple users displayed instead of just one

📸 Screenshot: Burp Suite Repeater or curl output
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Data Exposure | Attacker can still extract full tables  
Injection via Type Confusion | Integer logic can bypass escaping  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Escaping input | Replace with parameterized queries (e.g., `mysqli_prepare`)  
No input type enforcement | Apply strict casting or regex filters  
Error display | Replace with generic error handling  
```

---

## 🔢 Input Code – HIGH Security Level

```php
<?php

if( isset( $_SESSION [ 'id' ] ) ) {
    $id = $_SESSION[ 'id' ];

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
            $result = mysqli_query($GLOBALS["___mysqli_ston"], $query ) or die( '<pre>Something went wrong.</pre>' );

            while( $row = mysqli_fetch_assoc( $result ) ) {
                $first = $row["first_name"];
                $last  = $row["last_name"];
                $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
            }

            mysqli_close($GLOBALS["___mysqli_ston"]);
            break;
    }
}
?>
```

## 🛡️ HIGH Security Level

### 📌 Overview
Input is now sourced from the session, not the user, and includes a `LIMIT 1` to reduce SQL query scope. Although risk is minimized, the query is still dynamically constructed using `$id`, leaving edge-case vectors open in session manipulation or logic flaw exploits.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Unsafe Session Usage | Relies on session data without validation  
Still Builds Dynamic Query | `$id` inserted directly into SQL  
Potential Session Fixation | If session is hijacked, injection is possible  
```

---

### 2️⃣ Exploitation Phase

```markdown
🔨 Tool: Browser Dev Tools, Intercepted Cookie Injection

🔧 Setup:
Hijack or inject a session with a malicious `id` value

🔁 Payload:
Set session cookie to a malicious ID with injected SQL

🎯 Success Indicator:
Manipulated session results in data leak or logic bypass

📸 Screenshot: Browser dev tools session injection
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Session Injection | Session ID manipulation may allow SQLi  
Residual Code Risk | Poor session hygiene leaves SQLi surfaces exposed  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Session trust assumption | Validate all session data  
Dynamic queries | Use bound variables and `mysqli_prepare()`  
Session fixation | Implement secure session lifecycle management  
```

---
