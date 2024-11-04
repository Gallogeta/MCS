---
layout: default
---

# Navigation<br>
### **[Work History](WorkHistory.md)   [Education](Education.md)   [Achivements](Achivements.md)   [Coding](Coding.md)**<br>

**[BACK TO INDEX](index.md)**


## Windows winks

** How to scare your friends **

open cmd and type:<br>
>@echo off
>setlocal enabledelayedexpansion
>set "enc=^0x4e6f682c20536169646b692048c36b6974756421"
>set "dec="
>for %%a in (%%enc: = ) do set "dec=!dec!%%a"
>set /a dec=%dec%
>set "msg="
>for /l %%i in (0,1,%dec%) do set "msg=!msg!%%~xi"
>msg * /sound beep !msg! 

**Change the Color of the Command Prompt Window**

> Launch CMD and Right-click on the title bar
>Click on “Properties” and in the separate window that opens, click on “Colors”`
>Here you can choose the colors for the screen text or background as well as for the popup text and background, and also change the transparency of the CMD window
>After you’re done choosing the most fitting colors for your personality, Click OK
<br>

**List Every Driver Installed on Your Windows 10 PC**<br>
> driverquery /FO list /v in CMD

**Windows Recall**<br>
To see if it is on. Go in as Administrator into Powershell. change <username> to your own user (Like john, Mary, Pekka, Jussi):<br>
>Get-Mailbox -Identity <username> | Select-Object -ExpandProperty RecallEnabled<br><br>

**To Disable it**<br>
>Set-Mailbox -Identity <username> -RecallEnabled $false<br><br>

### Recall check through CMD(admin)<br>

>dism /online /get-featureinfo /featurename:Recall


