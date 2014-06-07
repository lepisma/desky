#desky

Wrap your web app in a desktop window

###Why ?

- Making GUIs using web technology is immensely powerful
- Apps look nice (atleast to me) when they are not in a browser's tab
- **Why Qt webkit !** Why not a simple chrome app wrapping ? : Not everyone uses chrome plus I am on KDE, so Qt comes naturally

###Usage

- `pip install requirements`
- Make `desky_config.json` using the sample in your project directory
    - `url` is the url of the web application or link to static html
    - `cmd` is the command desky will run to start the app e.g. `python server.py`
    - `check_port` is the port that the app is using, desky opens `url` only if this port is listening
    - `name` is the name of app
- Copy `desky.py` to project directory
- Run app using `python desky.py`
- Pack using `python desky.py pack`
- For upx compression use `python desky.py packupx <upx-dir-path>`

###License

MIT

Copyright (c) 2014 Abhinav Tushar