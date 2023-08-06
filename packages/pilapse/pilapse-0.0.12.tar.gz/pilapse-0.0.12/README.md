# pilapse
A simple time-lapse service for Raspberry Pi. It uses `raspistill` binary to capture images. It's currently capable of periodically capturing of still images and serving last captured image to the web browser.

# Installation and usage
 *requires Python3*

### Using Pip

```bash
sudo apt update
sudo apt install python3-pip
pip3 install pilapse --user

# If your ~/.local/bin directory was created only during install
# you will likely need to re-login or update your PATH variable to include it
export PATH=$HOME/.local/bin:$PATH

# Start the server
mkdir ~/my-timelapse
pilapse --port 8888 --path ~/my-timelapse --period 60
```

### Manual
```bash
git clone https://github.com/yix/pilapse
cd pilapse
pip3 install -r requirements.txt --user
# Start the server
mkdir ~/my-timelapse
python3 -m pilapse --port 8888 --path ~/my-timelapse --period 60
```
