# CryptoHash 🦀

> A fast, cross-platform cryptographic hash generator with a dark-themed GUI.

![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
![Build](https://github.com/SoloBeing/CryptoHash/actions/workflows/build.yml/badge.svg)

---

## What is CryptoHash?

CryptoHash is a desktop application for computing, comparing, and monitoring
cryptographic hashes. Whether you're verifying a downloaded file, detecting
unauthorized modifications to a directory, or exploring how hash functions work,
CryptoHash gives you a clean, fast interface to do it.

Built with Python and PyQt5. No internet connection required. Fully offline.

---

## Screenshots

> *(Add screenshots here once you have them)*

---

## Supported Algorithms

| Algorithm | Output Size | Category |
|-----------|------------|----------|
| MD5 | 128-bit | Legacy |
| SHA-1 | 160-bit | Legacy |
| SHA-224 | 224-bit | SHA-2 |
| SHA-256 | 256-bit | SHA-2 |
| SHA-384 | 384-bit | SHA-2 |
| SHA-512 | 512-bit | SHA-2 |
| SHA3-224 | 224-bit | SHA-3 |
| SHA3-256 | 256-bit | SHA-3 |
| SHA3-384 | 384-bit | SHA-3 |
| SHA3-512 | 512-bit | SHA-3 |
| BLAKE2b | 512-bit | Modern |
| BLAKE2s | 256-bit | Modern |
| CRC32 | 32-bit | Checksum |
| Adler-32 | 32-bit | Checksum |

---

## Features

### 🔤 Text Hashing
- Hash any string in real time as you type
- Supports UTF-8, UTF-16, ASCII, and Latin-1 encodings
- Toggle uppercase output
- Copy individual hashes or all at once

### 📄 File Hashing
- Hash any file on disk using a background thread (UI never freezes)
- Live progress bar based on file size
- Real-time speed indicator (MB/s)
- Adjustable chunk size for performance tuning
- Pause and resume hashing mid-file

### 📁 Directory Monitor
- Watch an entire directory for file changes
- Automatically re-hashes modified files
- Alerts you when a hash mismatch is detected
- Recursive directory scanning with sorted file order
- Useful for tamper detection and file integrity auditing

### 🔍 Hash Comparison
- Paste two hash strings side by side
- Instantly see MATCH ✅ or MISMATCH ❌
- Character-level diff count shown on mismatch

### 🔐 HMAC Generator
- Generate Hash-based Message Authentication Codes
- Selectable algorithm (MD5 through SHA-512)
- Secret key input with show/hide toggle

---

## Download

Pre-built binaries are available on the
[Releases](https://github.com/SoloBeing/CryptoHash/releases) page.

| Platform | File |
|----------|------|
| 🐧 Linux (x86_64) | `CryptoHash-linux-x86_64` |
| 🪟 Windows 11 | `CryptoHash-windows-x86_64.exe` |
| 🍎 macOS | `CryptoHash-macos` |

---

## Run from Source

**Requirements:** Python 3.11+

```bash
