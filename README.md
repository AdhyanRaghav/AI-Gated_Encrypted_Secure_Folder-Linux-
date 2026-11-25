# AI-Gated Encrypted Secure Folder (Linux)

A face-recognition based encrypted folder access system built using OpenCV and gocryptfs on Linux.

This project combines:

- Face detection & recognition (LBPH)
- Encrypted storage (gocryptfs)
- Automatic mounting & unmounting
- Inactivity-based auto-lock
- Desktop launcher integration

Only after successful face authentication does the encrypted folder mount and open.

---

## Project Structure

```
face_detection_system/
│
├── registry.py        # Face data collection & model training
├── auth.py            # Face authentication + mount logic
└── face_model.yml     # Trained LBPH face model
```

---

## How It Works

1. User clicks the Secure Folder launcher.
2. `auth.py` runs face authentication for 3 seconds.
3. If confidence threshold passes:
   - Encrypted storage is mounted.
   - Folder opens automatically.
   - Inactivity monitor starts.
4. If no activity for 2 minutes:
   - Folder auto-unmounts.
5. If authentication fails:
   - Access denied notification is shown.

Encryption is handled using `gocryptfs`, so files remain unreadable unless mounted.

---

## Requirements

### System Packages

```bash
sudo apt update
sudo apt install gocryptfs lsof
```

---

### Python Requirements (Virtual Environment Recommended)

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install opencv-contrib-python numpy
```

> `opencv-contrib-python` is required for the `cv2.face` module.

---

## Setting Up Encrypted Storage

Create encrypted storage:

```bash
mkdir ~/SecureEncrypted
mkdir ~/SecureMount

gocryptfs -init ~/SecureEncrypted
```

Create a secure key file:

```bash
nano ~/.secret_key
chmod 600 ~/.secret_key
```

---

## Training Your Face Model

Run:

```bash
python registry.py
```

This:
- Captures face samples
- Trains LBPH model
- Generates `face_model.yml`

---

## Running Authentication

```bash
/home/your_username/face_detection_system/.venv/bin/python auth.py
```

Or create a `.desktop` launcher pointing to your virtual environment Python.

---

## Inactivity Auto-Unmount

After mounting, a background thread:

- Checks every 10 seconds
- If no file activity for 2 minutes
- Automatically runs:

```bash
fusermount -u ~/SecureMount
```

---

## Security Notes

- The encryption key file (`~/.secret_key`) must be protected.
- This system is intended for personal use on Linux.
- Face recognition is threshold-based, not biometric-grade.

---

## Tested On

- Zorin OS (GNOME-based)
- Python 3.10
- OpenCV 4.x

---

## Future Improvements

- Multi-user support
- Retry attempts
- GUI overlay notifications
- Key file encryption
- Systemd background service
- Packaging as standalone tool

---

## License

MIT License

---

## Author

Adhyan Raghav  
Cybersecurity & Systems Enthusiast

