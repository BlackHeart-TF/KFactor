KFactor - 2FA Authenticator
=============================
This is a TOTP Authentication Code generator made with Python and QT. It aims to be a drop in replacement for Google Authenticator for plasma-mobile.

### Tested on 
- Manjaro/Pinephone, 
- Kubuntu/x64 PC, 
- Windows/x64 PC

## Status
### Working:
- TOTP Code generation from Base32 keys
- internal parser for "otpauth" and "otpauth-migration" Uri from QR codes
- Serial QR scanner support
- Secure? key storage with 'keyring'

### Not Working:
- the remove/import/export buttons
- importing codes (planning camera, manual entry)

## Screenshots
### Pinephone Pro on Majaro
![Pinephone Screenshot](https://i.imgur.com/TXtywTF.png)
