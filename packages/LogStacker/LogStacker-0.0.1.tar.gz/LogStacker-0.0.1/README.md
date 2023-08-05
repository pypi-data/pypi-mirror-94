# Log Stacker
> A colorful and less settings logger, based on the built-in package `logging`.

## What is this?
Contain the following features with the minimum settings.
+ stream logger(Colorful Stream)
+ file logger(strip color tags)
+ remote logger(In progress)

## How to use?
### Step 1
- Install
```bash
pip install log_stacker
```

- Import module in your entry point at the top
>entry point: startup python file, such as `main.py` `run.py` `start_api.py` etc.
### Step 2
- Basic setup
``` python
"""
start_api.py
"""

from log_stacker import LogStacker
LogStacker.logging(__file__)
```

or

- Advance setup
``` python
"""
start_api.py
"""

from log_stacker import LogStacker
LogStacker.logging(
    entry_point='path/to/your/log',
    stream_level=LogStacker.WARNING,
    file_level=LogStacker.INFO,
    remote_level=None
)
```

### Step 3
You can start logging in anywhere of your project!
>Note: If you got an initialized warning,
>please make sure you initial LogStacker correctly at the begging of the file your are running.

```python
"""
test.py which is called by start_api.py
"""

from log_stacker import LogStacker
try:
    1/0
except Exception as e:
    LogStacker.critical(e)
    LogStacker.error(e)
    LogStacker.warning(e, msg='It is a warning!')
    LogStacker.info('I wanna print something here!')
    LogStacker.debug()
```

## History
|#|      date|version|
|-|----------|-------|
|0|2021/02/07| v0.0.1|

#### v0.0.1
- Beta version

If you like my work, please consider buying me a coffee or [PayPal](https://paypal.me/RonDevStudio?locale.x=zh_TW)
Thanks for your support! Cheers! 🎉
<a href="https://www.buymeacoffee.com/ronchang" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" align="right"></a>
