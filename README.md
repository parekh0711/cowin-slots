# Update!

To download a built executable for Windows, for a simple double-click run, head over to yashjakhotiya.github.io

# Cowin Slots

_Are vaccination slots available for my age group in my pin code?_ 

This script should sound an alarm when slots become available.

## How to use

1. `pip install -r requirements.txt`
2. `python cowin_slots.py --pin_code 445102 --age 23`

Multiple pin codes like below are supported.<br>
`python cowin_slots.py -p 445102 -p 411005 -a 23`<br>
Long or short versions of arguments don't matter.

Use `-h` for all optional arguments. If you don't pass pin code or age, it'll be asked in an input prompt.

### Platform specifics
As a Windows user, if you don't have `python` installed, you can download it via Microsoft Store. Ensure that you check the box that adds the executable to `$PATH` during installation.

Launch `Windows Powershell` from Start Menu to run the commands above.

This was tested on Windows Powershell. To test this somewhere else, you might want to do
```
$ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from playsound import playsound
>>> playsound('alarm.wav')
```

## Note
This script uses the API provided by the Government of India [here](https://apisetu.gov.in/public/marketplace/api/cowin).