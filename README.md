<div align="center">

```
 _   _  ___  ____     ____  _____ ____ _   _ ____  ___ _______   __
| | | |/ ___|| __ )   / ___|| ____/ ___| | | |  _ \|_ _|_   _\ \ / /
| | | |\___ \|  _ \   \___ \|  _|| |   | | | | |_) || |  | |  \ V /
| |_| | ___) | |_) |   ___) | |__| |___| |_| |  _ < | |  | |   | |
 \___/ |____/|____/   |____/|_____\____|\___/|_| \_|___| |_|   |_|

 _____  ___   ___  _
|_   _|/ _ \ / _ \| |
  | | | | | | | | | |
  | | | |_| | |_| | |___
  |_|  \___/ \___/|_____|
```

**Portable USB encryption tool — no installation required**

![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=flat-square&logo=windows)
![Cipher](https://img.shields.io/badge/Cipher-AES--256--GCM-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## What is this?

**USB Security Tool** encrypts and decrypts files directly on your USB drive using **AES-256-GCM** — one of the strongest encryption standards available. Everything runs from the drive itself: no Python installation needed on the host machine.

---

## How it works

```
Your password
      ↓
PBKDF2-SHA256 (480,000 iterations) + random salt
      ↓
AES-256-GCM key (generated in RAM, never stored)
      ↓
Files encrypted → saved as .enc on the USB drive
```

- Each file gets its own **random salt + nonce** — identical files produce different ciphertext
- The **GCM tag** detects tampering — any modification to an encrypted file is detected
- Wrong password = instant failure, no partial data exposed
- **100% offline** — no network calls after setup

---

## Requirements

| Requirement | Details |
|---|---|
| OS | Windows 7, 8, 10, 11 (64-bit) |
| Python | None — bundled in the drive |
| Internet | Only during first-time setup |
| Drive | Must be a removable USB drive |

---

## Installation

### Step 1 — Clone the repo onto your USB drive

```cmd
git clone https://github.com/youruser/usb-security-tool E:\
```

Or download the ZIP and extract to your USB drive root.

### Step 2 — Download Python Embeddable

Go to: https://www.python.org/downloads/windows/

Download **"Windows embeddable package (64-bit)"** for the latest version.

Extract the contents into the `python\` folder on your USB drive:

```
E:\
└── python\
    ├── python.exe   ← must be here
    └── ...
```

### Step 3 — Run the installer

Open CMD and run:

```cmd
E:\INSTALL.bat
```

The installer will automatically:

- ✅ Verify you are running from a USB drive
- ✅ Check that portable Python is present
- ✅ Install the `cryptography` library into `Lib\`
- ✅ Hide all system files from plain sight
- ✅ Open a ready-to-use secure terminal

> If you run `INSTALL.bat` again on an already configured drive, it will ask before doing anything.

---

## Usage

### Interactive menu

```cmd
E:\usb
```

```
====================================================
   USB SECURITY TOOL  |  AES-256-GCM
====================================================

  select option:

  [1] encrypt directory
  [2] decrypt directory
  [3] inspect directory
  [0] exit
```

### Command line

```cmd
usb --enc   "E:\my-folder"       encrypt a directory
usb --dec   "E:\my-folder"       decrypt a directory
usb --inspect "E:\my-folder"     show encryption status
usb --help                       show all commands
```

> Paths with spaces work with or without quotes:
> ```cmd
> usb --enc "E:\My Documents"
> usb --enc E:\My Documents
> ```

---

## File structure

```
USB Drive
├── python\                ← portable Python runtime (hidden after setup)
├── Lib\                   ← cryptography library (hidden after setup)
├── pendrive_cripto.py     ← core script (hidden after setup)
├── usb.bat                ← main command
├── cmd_usb.bat            ← opens terminal with usb command ready
├── INSTALL.bat            ← run once to set everything up
├── SETUP.bat              ← installs dependencies (called by INSTALL)
├── HIDE.bat               ← hides system files manually
├── SHOW.bat               ← restores file visibility
└── README.md
```

After setup, system files are hidden. The drive appears empty to anyone who opens it in File Explorer.

---

## Security model

| Feature | Detail |
|---|---|
| Encryption | AES-256-GCM |
| Key derivation | PBKDF2-SHA256, 480,000 iterations |
| Salt | 16 bytes, random per file |
| Nonce | 12 bytes, random per file |
| Integrity | GCM authentication tag (detects tampering) |
| Network | Zero — fully offline after setup |

> **Important:** If you forget your password, your files cannot be recovered. There is no backdoor.

---

## Recovering hidden files

If you need to see the system files again, open CMD from the drive and run:

```cmd
attrib -h -s E:\SHOW.bat
E:\SHOW.bat
```

---

## License

MIT — do whatever you want with it.

---

<div align="center">
  Made with Python + AES-256-GCM
</div>
