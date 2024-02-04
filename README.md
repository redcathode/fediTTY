## fediTTY
source for the fediverse bot (currently) at [@tty@fedi.computernewb.com](https://fedi.computernewb.com/@tty)  

## running
- Create a libvirt VM.
- Set the constants in `constants.py` according to your setup. You may have to change `qemu:///session` to `qemu:///system` depending on how your libvirt is set up.
- Copy dotenv_example to `.env` and set `BOT_ACCESS_TOKEN` to your access token.
- Then...
```shell
pip install -r requirements.txt
python3 main.py
```