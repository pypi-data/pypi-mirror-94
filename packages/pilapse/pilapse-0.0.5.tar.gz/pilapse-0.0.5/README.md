# pilapse
A simple time lapse service for Raspberry Pi. It uses `raspistill` binary to capture images.

# Installation
 *requires Python3*

### Using Pip

```bash
pip install pilapse
```

### Manual
```bash
git clone https://github.com/yix/pilapse
cd pilapse
python3 -mvenv venv
. ./venv/bin/activate
pip install -r requirements.txt
python -mpilapse --period=300 --path=~/my/timelapse/images
```

# Usage

### if installed via pip
```bash
pilapse --port 8888 --path ~/pylapse_images --period 60
```

### if just cloned the repo
```bash
python3 -m pilapse --port 8888 --path ~/pylapse_images --period 60
```
