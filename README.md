## fediTTY
source for the fediverse bot (currently) at [@tty@fedi.computernewb.com](https://fedi.computernewb.com/@tty)  

## running
- Clone the repo:
```shell
git clone https://github.com/b0vik/fediTTY.git
cd fediTTY
```
- Create a libvirt VM.
- Set the constants in `constants.py` according to your setup. You may have to change `qemu:///session` to `qemu:///system` depending on how your libvirt is set up.
- Copy dotenv_example to `.env` and set `BOT_ACCESS_TOKEN` to your access token.
- Then...
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```