# Comprehensive Red Teaming and Penetration Testing Walkthrough with crAPI

> **Note**: This guide targets **OWASP crAPI**, an intentionally vulnerable API for safe and educational red teaming and penetration testing.

---

## 📖 Overview

This document provides a **first-principles-based**, step-by-step walkthrough for red teaming crAPI. You will:

- Explore the **OWASP API Security Top 10 (2023)**
- Simulate realistic attacks like account takeovers and data breaches
- Understand **why each vulnerability works** and **how to exploit it**
- Learn how to identify, validate, and mitigate real-world API security flaws

> ✅ Ideal for penetration testers, API security learners, and red teamers

---

## 🚀 Getting Started

To run crAPI locally:

```bash
# Clone the repository
https://github.com/OWASP/crAPI

# Launch the application
cd crAPI
docker-compose up -d
```

Visit: [`http://127.0.0.1:8888`](http://127.0.0.1:8888)\
Ensure Docker & Docker Compose ≥ **v1.27.0** are installed.

---

## 🛡️ OWASP API Top 10 (2023) vs crAPI Challenges

| **Risk ID** | **Risk Name**                                   | **crAPI Challenges** |
| ----------- | ----------------------------------------------- | -------------------- |
| API1:2023   | Broken Object Level Authorization (BOLA)        | 1, 2, 7              |
| API2:2023   | Broken Authentication                           | 3, 14                |
| API3:2023   | Broken Object Property Level Authorization      | 4, 8, 9              |
| API4:2023   | Unrestricted Resource Consumption               | 5                    |
| API5:2023   | Broken Function Level Authorization (BFLA)      | 6                    |
| API6:2023   | Unrestricted Access to Sensitive Business Flows | 7                    |
| API7:2023   | Server Side Request Forgery (SSRF)              | 10                   |
| API8:2023   | Security Misconfiguration                       | Not covered          |
| API9:2023   | Improper Inventory Management                   | 11                   |
| API10:2023  | Unsafe Consumption of APIs                      | 12, 13               |

---

## 🧪 Lab Format

Each challenge includes:

- **Risk Category**
- **Description** & **Attack Scenario**
- **Step-by-step Exploitation Guide**
- **Explanation** of Vulnerability, Logic, and Impact

---

## ✅ Security Concepts Reinforced

- 🔒 **Strict Authorization** — BOLA & BFLA require role & object-level checks
- 🔐 **Strong Authentication** — OTPs, tokens, JWTs need validation, lockout, rotation
- 🧹 **Input Validation** — Sanitize inputs to prevent injection (SQL, NoSQL, SSRF)
- 📉 **Rate Limiting** — Prevent API misuse, abuse, or DoS
- 📦 **Data Minimization** — Never expose more than what’s required

---

## 📚 Continue Learning

- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [OWASP crAPI GitHub](https://github.com/OWASP/crAPI)
- Tools: **Burp Suite**, **Postman**, **Swagger UI**, **MailHog**

---

## 📎 References

- OWASP Top 10 API Security: [https://owasp.org/API-Security/editions/2023/en/0x11-t10/](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- Lab Docs: BOLA, BFLA, Excessive Data Exposure, Mass Assignment, Auth Attacks

> *All challenges remain below, unmodified, in the original format.* ✅

