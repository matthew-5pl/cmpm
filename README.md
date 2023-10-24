# cmpm
canta uma música para mim discord bot

plays music from *THE* website :p

# setup 
to run this bot you'll first need to set two environment variables, `CMPM_TOK` and `CMPM_DLP`, which should be set to your discord bot's token and a local path to store the currently playing music file respectively.

the dependencies to run this bot are:

- a decently recent version of python 3
- pip

# running
to actually run the bot:

- clone the repository locally
	```sh
	git clone https://github.com/matthew-5pl/cmpm
	```
- install python dependencies
	```sh
	pip install -r requirements.txt
	```
- run the bot:
	on windows:
	```
	run.bat
	```
	on linux/macos:
	```sh
	./run.sh
	```

# run as a systemd service
if you're running a linux distro that uses systemd you can also run this bot as a systemd service.

this allows you to easily keep it running in the background and (if you want to) starts it automatically after the system boots.

WARNING: BEFORE ADDING THIS SERVICE YOU NEED TO EDIT IT WITH SOME INFO! please read the `cmpm.service` file before proceeding.

instructions on doing this *can* be distro dependent, but this worked for me on a system running ubuntu server 22.04.2 lts: 

(might require sudo)
```sh
cp cmpm.service /etc/systemd/system/
systemctl start cmpm
```

if you want the service to start after boot you also need to run:
```sh
systemctl enable cmpm
```
