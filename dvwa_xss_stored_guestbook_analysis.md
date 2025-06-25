
# 📘 DVWA – Stored XSS (Guestbook) Writeup

This document provides a full analysis of the **Stored Cross-Site Scripting (XSS)** vulnerability in the DVWA "Guestbook" module across Low, Medium, and High security levels.

---

## 🔍 Vulnerable Code Review

### 🔓 Low Security

```php
$message = trim( $_POST[ 'mtxMessage' ] );
$name    = trim( $_POST[ 'txtName' ] );

$message = stripslashes( $message );
$message = mysqli_real_escape_string( $conn, $message );
$name = mysqli_real_escape_string( $conn, $name );

$query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
```

- ❌ **No output encoding**
- ❌ **No HTML filtering**
- ❌ **Stored raw in DB, rendered unsanitized**

### ✅ Exploitation

Payload:
```html
<script>alert("Stored XSS")</script>
```
Will be stored in the database and **executed every time** someone views the guestbook.

---

### 🟡 Medium Security

```php
$message = strip_tags( addslashes( $message ) );
$message = mysqli_real_escape_string( $conn, $message );
$message = htmlspecialchars( $message );
$name = str_replace( '<script>', '', $name );
```

- ✅ Some tag filtering with `strip_tags()`
- ⚠️ Only removes `<script>` exactly
- ❌ Allows event handlers like `onmouseover`
- ❌ Still reflects in guestbook

### 🧪 Bypass Example

Payload:
```html
<img src=x onerror=alert('XSS')>
```

This bypasses the `<script>` filter entirely and is stored.

---

### 🔐 High Security

```php
$message = strip_tags( addslashes( $message ) );
$message = mysqli_real_escape_string( $conn, $message );
$message = htmlspecialchars( $message );

$name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $name );
```

- ✅ Filters `<script>` using regex
- ✅ Applies `htmlspecialchars()` for encoding
- ⚠️ Regex bypasses possible with malformed tag sequences
- ✅ Safer but still imperfect

### ⚔️ Advanced Bypass (Theoretical)

If the HTML rendering is weak or double encoded elsewhere, payloads using:
```html
<svg onload=alert(1)>
```
might still slip through, depending on output context.

---

## 🔍 Vulnerability Summary

| Security Level | Issues Present | Can Store Payload? | Executable in Browser? |
|----------------|----------------|---------------------|-------------------------|
| Low            | No filtering, no encoding | ✅ Yes | ✅ Yes |
| Medium         | Poor filtering, tag-specific | ✅ Yes | ✅ With tag bypass |
| High           | Regex/script filtering, encoded | ✅ Yes | ⚠️ Depends on context |

---

## 🔐 Mitigation Recommendations

| ❌ Vulnerability | ✅ Secure Approach |
|------------------|--------------------|
| No encoding      | Use `htmlspecialchars()` or templating engine |
| Bad filtering    | Use CSP, sanitize on input and encode on output |
| Regex filtering  | Use vetted libraries like DOMPurify (JS) or OWASP Java Encoder |

---

## 📌 Key Lessons

- **Stored XSS** is dangerous due to **persistent payloads**.
- Input sanitization is not enough: **encode on output**.
- **Filter evasion** is easy with modern obfuscation techniques.
- Defense-in-depth: **combine validation, encoding, and CSP**.

