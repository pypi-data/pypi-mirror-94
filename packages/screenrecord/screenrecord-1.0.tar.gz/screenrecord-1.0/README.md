# SCREENRECORD
Record screen with python.

```bash
C:\Users\singhs>record usage.gif --bbox 10 10 1000 450 -d 0.1
```

# Usage
![usage screenshot for screenrecod with python](https://raw.githubusercontent.com/sukhbinder/screenrecord/master/img/usage.gif)


## Command line arguments

```python
usage: record [-h] [-i INITDELAY] [-d DELAY] [-dur DURATION]
              [--bbox BBOX [BBOX ...]] [-f]
              filename

Screen Recording with python

positional arguments:
  filename              filename can be mp4 or gif or mov

optional arguments:
  -h, --help            show this help message and exit
  -i INITDELAY, --initdelay INITDELAY
                        Initial delay in seconds, default 5 s
  -d DELAY, --delay DELAY
                        Delay between frames in seconds, default 0.5 s
  -dur DURATION, --duration DURATION
                        Duration of capture
  --bbox BBOX [BBOX ...]
                        Bounding box, default (0, 0, 800, 400)
  -f, --fullscreen

  ```
# Install

```python
pip install screenrecord

```
or 

```python
git clone this_repo
cd to/the/repo
pip install -e .
```

