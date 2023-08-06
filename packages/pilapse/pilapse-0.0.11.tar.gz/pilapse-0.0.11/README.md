# pilapse
A simple time-lapse service for Raspberry Pi. It uses `raspistill` binary to capture images. It's currently capable of periodically capturing of still images and serving last captured image to the web browser.

# Installation
 *requires Python3*

### Using Pip

```bash
pip3 install pilapse --user
```

### Manual
```bash
git clone https://github.com/yix/pilapse
cd pilapse
pip3 install -r requirements.txt --user
```

# Usage

```bash
pilapse --port 8888 --path ~/pylapse_images --period 60

# or if just cloned the repo (repository should be your current directory)
python3 -m pilapse --port 8888 --path ~/pylapse_images --period 60
```
