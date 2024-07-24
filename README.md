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
- Importing codes with serial barcode scanner, camera, or manual entry
- Secure? key storage with 'keyring'

### Issues:
- migration codes are buggy, only sha1/6/30
- Only supports Sha1
- Code editing, not implemented
- Not sure how secure dumping keys in kwallet is
- No Export function (planning QR or JSON)
- Settings are not persistant

## Installation
It can be installed directly as a pip module with
```
pip install https://github.com/BlackHeart-TF/KFactor/archive/refs/heads/main.zip
python -m kfactor
```

## Screenshots
### Pinephone Pro on Majaro
<img src="https://i.imgur.com/TXtywTF.png" width="200" />
### Kubuntu Desktop
<img src="https://i.imgur.com/dODr9LJ.png" width="200" />