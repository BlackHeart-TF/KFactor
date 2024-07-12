KFactor - 2FA Authenticator
=============================
This is a TOTP Authentication Code generator made with Python and QT. It aims to be a drop in replacement for Google Authenticator for plasma-mobile.

# Notice
This is still very early in development and may change, always keep backups of your codes

### Tested on 
- Manjaro/Pinephone, 
- Kubuntu/x64 PC, 
- Windows/x64 PC

## Status
### Working:
- TOTP Code generation from Base32 keys
- Internal parser for "otpauth" and "otpauth-migration" Uri from QR codes
- Serial QR scanner support
- Secure? key storage with 'keyring'

### Coming Soon:
- The remove/import/export buttons
- Importing codes from camera
- Manual code editor
- Better key management
- Export to QR or JSON

## Installation
It can be installed directly as a pip module with
```
pip install https://github.com/BlackHeart-TF/KFactor/archive/refs/heads/main.zip
python -m kfactor
```

## Screenshots
### Pinephone Pro on Majaro
![Pinephone Screenshot](https://i.imgur.com/TXtywTF.png)
