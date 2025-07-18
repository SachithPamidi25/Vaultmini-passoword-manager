# VaultMini – Secure Password Manager

VaultMini is a lightweight, secure password manager built using FastAPI. It lets users **log in**, **securely store credentials**, **view/hide passwords**, and **shred all saved data**. The app uses **AES-GCM encryption**, **JWT authentication**, and **bcrypt** for hashing, offering a real-world look into authentication and data security practices.

# Features

**User Authentication** (JWT + bcrypt)
**Password Encryption** using AES-GCM (symmetric encryption)
**Toggle View/Hide Passwords**
**Add & Store Passwords by Service**
**Shred Vault** – permanently delete all stored passwords
Tested with Postman and browser frontend (HTML + JS)

---

# Tech Stack

**Backend**: Python, FastAPI
**Security**: AES-GCM, bcrypt, JWT
**Frontend**: HTML, CSS, JavaScript (Vanilla)
**Data Storage**: In-memory file handling (DB upgrade planned)

---

# Project Structure
VaultMini/
├── main.py
├── auth.py
├── file_op.py
├── models.py
├── templates/
│ └── index.html
├── static/
│ └── script.js
├── README.md
└── .gitignore
