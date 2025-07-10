
# crAPI Penetration Testing Walkthrough — Challenges 1 to 14

> This document contains GitHub-ready Markdown formatting for all crAPI API Top 10 challenges.

---

### Challenge 1: Unauthorized Access to Another User’s Vehicle Data
**OWASP Risk**: API1:2023 — *Broken Object Level Authorization*

**Scenario**: Attacker accesses another user’s vehicle data.

**Steps**:
```bash
1. Sign up at http://127.0.0.1:8888
2. Add a vehicle
3. Intercept request: GET /identity/api/v2/vehicle/vehicles/{vehicleId}
4. Extract a GUID from /community/api/v2/community
5. Replace vehicleId with victim's and replay
```

**Why It Works**: The API lacks ownership validation — knowledge of ID grants access.

**Impact**: Vehicle tracking or PII exposure.

---

### Challenge 2: Access Mechanic Reports of Other Users
**OWASP Risk**: API1:2023 — *Broken Object Level Authorization*

**Scenario**: Attacker reads other users’ mechanic service reports.

**Steps**:
```bash
1. Submit a service request via POST /workshop/api/shop/service
2. Capture report_id in the response
3. Replay with GET /workshop/api/shop/service/{report_id} using another ID
```

**Why It Works**: Missing ownership check at object level.

**Impact**: Confidential report exposure.

---

### Challenge 3: Reset Another User’s Password
**OWASP Risk**: API2:2023 — *Broken Authentication*

**Scenario**: Attacker brute-forces OTP to reset another account.

**Steps**:
```bash
1. Extract email from /community/api/v2/community
2. POST /identity/api/auth/forgot-password
3. Get OTP via http://127.0.0.1:8025
4. Brute-force POST /identity/api/auth/reset-password
```

**Why It Works**: OTP is predictable + no rate limiting.

**Impact**: Full account takeover.

---

### Challenge 4: Find an API Endpoint Leaking Internal Video Properties
**OWASP Risk**: API3:2023 — *Excessive Data Exposure*

**Scenario**: Internal video parameters exposed to users.

**Steps**:
```bash
1. Load OpenAPI spec in Swagger Editor
2. Identify endpoint: GET /identity/api/v2/user/videos/{videoId}
3. Send request via Postman
4. Check response for internal fields: conversion_params, storage_location
```

**Why It Works**: API returns all object properties — no filtering.

**Impact**: Internal architecture exposure, sensitive info leaks.

---

### Challenge 5: Perform Layer 7 DoS Using Contact Mechanic Feature
**OWASP Risk**: API4:2023 — *Unrestricted Resource Consumption*

**Scenario**: Service unavailable via request flooding.

**Steps**:
```bash
1. Use endpoint: POST /workshop/api/shop/contact-mechanic
2. Set number_of_repeats = 10000 and repeat_request_if_failed = true
3. Send the request
```

**Why It Works**: No protection against excessive request loops.

**Impact**: Application becomes unresponsive.

---

### Challenge 6: Delete a Video of Another User (BFLA)
**OWASP Risk**: API5:2023 — *Broken Function Level Authorization*

**Scenario**: Delete another user’s content via admin path.

**Steps**:
```bash
1. Try DELETE /identity/api/v2/user/videos/{videoId} (fails)
2. Use admin endpoint: DELETE /identity/api/v2/admin/videos/{videoId}
3. Send request with normal token — deletion occurs
```

**Why It Works**: Role not enforced on admin endpoint.

**Impact**: Unauthorized access to privileged operations.

---

### Challenge 7: Delete a Video of Another User (BOLA)
**OWASP Risk**: API1:2023 — *Broken Object Level Authorization*

**Scenario**: Delete another user’s video without owning it.

**Steps**:
```bash
1. Identify video ID of another user
2. Send DELETE /identity/api/v2/user/videos/{videoId}
```

**Why It Works**: No ownership validation on destructive operations.

**Impact**: Data destruction.

---

### Challenge 8: Increase Your Balance by $1,000 or More
**OWASP Risk**: API3:2023 — *Mass Assignment*

**Scenario**: Modify hidden properties like balance using unexpected params.

**Steps**:
```bash
1. POST to /workshop/api/shop/orders
2. Add body fields like refund_amount: 1000 or total: -1000
3. Confirm balance change via balance endpoint
```

**Why It Works**: API trusts all user-submitted object fields.

**Impact**: Financial manipulation.

---

### Challenge 9: Update Internal Video Properties
**OWASP Risk**: API3:2023 — *Mass Assignment*

**Scenario**: User modifies internal-only properties.

**Steps**:
```bash
1. PUT /identity/api/v2/user/videos/{videoId}
2. Include field like conversion_params: manipulated_value
```

**Why It Works**: No separation of internal vs user-exposed fields.

**Impact**: Internal logic tampering.

---

### Challenge 10: Server-Side Request Forgery (SSRF)
**OWASP Risk**: API7:2023 — *Server-Side Request Forgery*

**Scenario**: Trick server to request arbitrary external URLs.

**Steps**:
```bash
1. POST /workshop/api/shop/contact-mechanic
2. Use parameter URL: www.google.com
```

**Why It Works**: API fetches user-supplied URLs with no validation.

**Impact**: Port scanning, internal service access.

---

### Challenge 11: Find Endpoint Without Authentication Checks
**OWASP Risk**: API9:2023 — *Improper Inventory Management*

**Scenario**: Access sensitive data with no auth.

**Steps**:
```bash
1. Try GET /workshop/api/shop/orders/{orderId} without token
```

**Why It Works**: Endpoint lacks auth enforcement.

**Impact**: Information leakage.

---

### Challenge 12: Get Free Coupons Without Knowing the Coupon Code
**OWASP Risk**: API10:2023 — *Unsafe Consumption of APIs*

**Scenario**: Redeem discounts via NoSQL injection.

**Steps**:
```bash
1. POST /workshop/api/shop/coupons
2. coupon_code: { "$ne": 1 }
```

**Why It Works**: No validation — payload interpreted as NoSQL logic.

**Impact**: Free unauthorized access.

---

### Challenge 13: Redeem Already Claimed Coupon by Modifying Database
**OWASP Risk**: API10:2023 — *Unsafe Consumption of APIs*

**Scenario**: Use SQLi to reuse expired coupons.

**Steps**:
```bash
1. Use coupon in frontend
2. Intercept POST /workshop/api/shop/coupons
3. Inject SQL payload like 0' OR '0'='0 or 0'; select version() --+
```

**Why It Works**: SQL injection allowed in coupon logic.

**Impact**: Fraud, system tampering.

---

### Challenge 14: Forge Valid JWT Tokens for Full Access
**OWASP Risk**: API2:2023 — *Broken Authentication*

**Scenario**: Modify JWT tokens to impersonate other users.

**Steps**:
```bash
1. Capture a JWT from frontend
2. Use jwt.io to edit it
3. Set algorithm: none, change email claim
4. Use in Authorization header
```

**Why It Works**: Server accepts unsigned tokens.

**Impact**: Admin takeover, lateral movement.
