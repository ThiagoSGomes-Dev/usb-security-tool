import os
import sys

# Add external libs path (USB portable Python)
_BASE = os.path.dirname(os.path.abspath(__file__))
_LIBS = os.path.join(_BASE, "Lib", "site-packages")
if _LIBS not in sys.path:
    sys.path.insert(0, _LIBS)

import getpass
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import argparse

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
EXTENSION      = ".enc"
KDF_ITERATIONS = 480_000
SALT_SIZE      = 16
NONCE_SIZE     = 12

# Files/folders that should never be encrypted
IGNORE_NAMES   = {"pendrive_cripto.py", "usb.bat", "ABRIR.bat", "SETUP.bat", "README.txt", "LEIA-ME.txt"}
IGNORE_SUFFIXES = {".bat", ".py", ".exe", ".dll", ".pyd", ".pth"}
IGNORE_DIRS    = {"python", "lib"}


# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


BANNER = r"""
 _   _  ____  ____     ____  _____ ____ _   _ ____  ___ ____ __   __
| | | |/ ___|| __ )   / ___|| ____/ ___| | | |  _ \|_ _|_   _\ \ / /
| | | |\___ \|  _ \   \___ \|  _|| |   | | | | |_) || |  | |  \ V /
| |_| | ___) | |_) |   ___) | |__| |___| |_| |  _ < | |  | |   | |
 \___/ |____/|____/   |____/|_____\____|\___/|_| \_|___| |_|   |_|

 _____  ___   ___  _
|_   _|/ _ \ / _ \| |
  | | | | | | | | | |
  | | | |_| | |_| | |___
  |_|  \___/ \___/|_____|

"""

def header():
    print("=" * 52)
    print("   USB SECURITY TOOL  |  AES-256-GCM")
    print("=" * 52)


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def human_size(n_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} TB"


def should_ignore(p: Path) -> bool:
    """Returns True for system files that must never be encrypted."""
    if p.name in IGNORE_NAMES:
        return True
    if p.suffix.lower() in IGNORE_SUFFIXES:
        return True
    parts = [part.lower() for part in p.parts]
    if any(d in parts for d in IGNORE_DIRS):
        return True
    return False


# ─────────────────────────────────────────────
# CORE PROCESS
# ─────────────────────────────────────────────
def process_directory(directory: Path, password: str, mode: str):

    if mode == "enc":
        all_files    = [p for p in directory.rglob("*") if p.is_file() and not should_ignore(p)]
        already_enc  = [p for p in all_files if p.suffix == EXTENSION]
        files        = [p for p in all_files if p.suffix != EXTENSION]
        action       = "encrypting"
        done         = "encrypted"

        if already_enc:
            print(f"\n  info: {len(already_enc)} already encrypted file(s) will be skipped:")
            for p in already_enc[:10]:
                print(f"    - {p.name}")
            if len(already_enc) > 10:
                print(f"    ... and {len(already_enc) - 10} more.")
    else:
        files  = [p for p in directory.rglob("*") if p.is_file() and p.suffix == EXTENSION and not should_ignore(p)]
        action = "decrypting"
        done   = "decrypted"

    if not files:
        print("\n  no files found to process.")
        return

    total   = len(files)
    success = 0
    errors  = []

    print(f"\n  files found: {total}\n")

    for i, file in enumerate(files, 1):
        size = human_size(file.stat().st_size)
        print(f"  [{i:>3}/{total}] {action}: {file.name} ({size}) ... ", end="", flush=True)

        try:
            if mode == "enc":
                salt  = os.urandom(SALT_SIZE)
                key   = derive_key(password, salt)
                nonce = os.urandom(NONCE_SIZE)

                aesgcm    = AESGCM(key)
                data      = file.read_bytes()
                encrypted = aesgcm.encrypt(nonce, data, None)

                out = file.with_suffix(file.suffix + EXTENSION)
                out.write_bytes(salt + nonce + encrypted)
                file.unlink()

            else:
                content = file.read_bytes()
                salt    = content[:SALT_SIZE]
                nonce   = content[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
                cipher  = content[SALT_SIZE + NONCE_SIZE:]

                key    = derive_key(password, salt)
                aesgcm = AESGCM(key)
                data   = aesgcm.decrypt(nonce, cipher, None)

                out = file.parent / file.stem
                out.write_bytes(data)
                file.unlink()

            print("ok")
            success += 1

        except Exception as e:
            print("fail")
            errors.append((file.name, str(e)))

    print(f"\n{'-'*52}")
    print(f"  success: {success} file(s) {done}.")
    if errors:
        print(f"  errors : {len(errors)}")
        for name, msg in errors:
            print(f"    - {name}: {msg}")
    print(f"{'-'*52}")


# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────
def menu_encrypt():
    clear_screen()
    header()
    print("\n  [ ENCRYPT DIRECTORY ]\n")

    path = input("  target path: ").strip()
    directory = Path(path)

    if not directory.exists() or not directory.is_dir():
        print("\n  error: directory not found.")
        input("\n  press enter...")
        return

    password = getpass.getpass("  password: ")
    confirm  = getpass.getpass("  confirm password: ")

    if password != confirm:
        print("\n  error: passwords do not match.")
        input("\n  press enter...")
        return

    if len(password) < 8:
        print("\n  warning: password must be at least 8 characters.")
        input("\n  press enter...")
        return

    print("\n  deriving key...")
    process_directory(directory, password, "enc")
    input("\n  press enter...")


def menu_decrypt():
    clear_screen()
    header()
    print("\n  [ DECRYPT DIRECTORY ]\n")

    path = input("  target path: ").strip()
    directory = Path(path)

    if not directory.exists() or not directory.is_dir():
        print("\n  error: directory not found.")
        input("\n  press enter...")
        return

    password = getpass.getpass("  password: ")

    print("\n  deriving key...")
    process_directory(directory, password, "dec")
    input("\n  press enter...")


def menu_inspect():
    clear_screen()
    header()
    print("\n  [ DIRECTORY INSPECTION ]\n")

    path = input("  target path: ").strip()
    directory = Path(path)

    if not directory.exists() or not directory.is_dir():
        print("\n  error: directory not found.")
        input("\n  press enter...")
        return

    files      = [p for p in directory.rglob("*") if p.is_file() and not should_ignore(p)]
    enc        = [p for p in files if p.suffix == EXTENSION]
    plain      = [p for p in files if p.suffix != EXTENSION]
    total_size = sum(p.stat().st_size for p in files)

    print(f"\n  path      : {directory}")
    print(f"  files     : {len(files)} ({human_size(total_size)})")
    print(f"  encrypted : {len(enc)}")
    print(f"  plaintext : {len(plain)}")

    if plain:
        print("\n  unencrypted files:")
        for p in plain[:20]:
            print(f"    - {p.relative_to(directory)}")
        if len(plain) > 20:
            print(f"    ... and {len(plain) - 20} more.")

    input("\n  press enter...")


# ─────────────────────────────────────────────
# CLI MODE — handles paths with spaces correctly
# ─────────────────────────────────────────────
def cli():
    # argparse with nargs='+' collects multi-token paths caused by
    # unquoted spaces in CMD and joins them back into the full path.
    class BannerHelp(argparse.HelpFormatter):
        def format_help(self):
            return (
                BANNER +
                "  AES-256-GCM  |  PBKDF2-SHA256  |  v1.0.0\n" +
                "=" * 52 + "\n\n" +
                "  USAGE:\n" +
                "    usb.bat                      open interactive menu\n" +
                "    usb.bat --enc  <path>        encrypt directory\n" +
                "    usb.bat --dec  <path>        decrypt directory\n" +
                "    usb.bat --inspect <path>     inspect directory\n" +
                "    usb.bat --help               show this help\n\n" +
                "  EXAMPLES:\n" +
                "    usb.bat --enc E:\\Docs\n" +
                "    usb.bat --enc \"E:\\Pasta - Joel\"\n" +
                "    usb.bat --dec E:\\Docs\n" +
                "    usb.bat --inspect E:\\\n\n" +
                "  NOTES:\n" +
                "    - password must be at least 8 characters\n" +
                "    - already encrypted files (.enc) are skipped\n" +
                "    - original files are deleted after encryption\n" +
                "=" * 52 + "\n"
            )

    parser = argparse.ArgumentParser(
        description="USB Security Tool",
        formatter_class=BannerHelp,
        add_help=True
    )
    parser.add_argument("--enc",     nargs="+", metavar="PATH", help="encrypt directory")
    parser.add_argument("--dec",     nargs="+", metavar="PATH", help="decrypt directory")
    parser.add_argument("--inspect", nargs="+", metavar="PATH", help="inspect directory")

    args = parser.parse_args()

    def resolve(tokens):
        """Join tokens back into a single path string."""
        return Path(" ".join(tokens))

    if args.enc:
        directory = resolve(args.enc)
        if not directory.exists():
            print(f"  error: directory not found: {directory}")
            return True

        # Check if all files are already encrypted
        all_files = [p for p in directory.rglob("*") if p.is_file() and not should_ignore(p)]
        plain     = [p for p in all_files if p.suffix != EXTENSION]
        already   = [p for p in all_files if p.suffix == EXTENSION]

        if not plain and already:
            print(f"  info: all {len(already)} file(s) are already encrypted. nothing to do.")
            return True

        if already:
            print(f"  info: {len(already)} already encrypted file(s) will be skipped.")

        password = getpass.getpass("  password: ")
        confirm  = getpass.getpass("  confirm password: ")
        if password != confirm:
            print("  error: passwords do not match.")
            return True
        if len(password) < 8:
            print("  error: password must be at least 8 characters.")
            return True

        process_directory(directory, password, "enc")
        return True

    elif args.dec:
        directory = resolve(args.dec)
        if not directory.exists():
            print(f"  error: directory not found: {directory}")
            return True

        # Check if there is anything to decrypt
        enc_files = [p for p in directory.rglob("*") if p.is_file() and p.suffix == EXTENSION and not should_ignore(p)]
        if not enc_files:
            print("  info: no encrypted files found. nothing to do.")
            return True

        password = getpass.getpass("  password: ")
        process_directory(directory, password, "dec")
        return True

    elif args.inspect:
        directory = resolve(args.inspect)
        if not directory.exists():
            print(f"  error: directory not found: {directory}")
            return True
        files = [p for p in directory.rglob("*") if p.is_file() and not should_ignore(p)]
        enc   = [p for p in files if p.suffix == EXTENSION]
        plain = [p for p in files if p.suffix != EXTENSION]
        print(f"  path      : {directory}")
        print(f"  files     : {len(files)}")
        print(f"  encrypted : {len(enc)}")
        print(f"  plaintext : {len(plain)}")
        return True

    return False


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    while True:
        clear_screen()
        header()
        print("""
  select option:

  [1] encrypt directory
  [2] decrypt directory
  [3] inspect directory
  [0] exit
""")
        option = input("  > ").strip()

        if option == "1":
            menu_encrypt()
        elif option == "2":
            menu_decrypt()
        elif option == "3":
            menu_inspect()
        elif option == "0":
            print("\n  exiting...\n")
            sys.exit(0)
        else:
            print("\n  invalid option.")
            input("  press enter...")


if __name__ == "__main__":
    if not cli():
        main()
