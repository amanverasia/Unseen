# UNSEEN                                                          
<pre>@@@  @@@  @@@  @@@   @@@@@@   @@@@@@@@  @@@@@@@@  @@@  @@@  
@@@  @@@  @@@@ @@@  @@@@@@@   @@@@@@@@  @@@@@@@@  @@@@ @@@  
@@!  @@@  @@!@!@@@  !@@       @@!       @@!       @@!@!@@@  
!@!  @!@  !@!!@!@!  !@!       !@!       !@!       !@!!@!@!  
@!@  !@!  @!@ !!@!  !!@@!!    @!!!:!    @!!!:!    @!@ !!@!  
!@!  !!!  !@!  !!!   !!@!!!   !!!!!:    !!!!!:    !@!  !!!  
!!:  !!!  !!:  !!!       !:!  !!:       !!:       !!:  !!!  
:!:  !:!  :!:  !:!      !:!   :!:       :!:       :!:  !:!  
::::: ::   ::   ::  :::: ::    :: ::::   :: ::::   ::   ::  
 : :  :   ::    :   :: : :    : :: ::   : :: ::   ::    :   </pre>
                                                        

## Disclaimer
I take no responsiblity legal or otherwise if Instagram decides to ban your account, please use at your own discretion and choice.

## Prerequisites
If on Unix based system
```bash
pip3 install -r requirements.txt
```

If on Windows
```cmd
pip install -r requirements.txt
```

## Running the script
If on Unix based system
```bash
python3 main.py
```

If on Windows
```cmd
python main.py
```

## Additional Information
You will need to enable 2FA in your Instagram account using TOTP and not SMS. It is were you use an app like Authy or Google Authenticator to generate 2FA codes on the fly. You will also have to approve the Instagram login one time from your app to generate the session.json file.

## Pending Tasks
- [ ] Media Download
- [ ] Highlights Download
- [ ] Story Download
- [ ] Profile Picture Download