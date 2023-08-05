# Dynamic Web Application (DWA)

<badges>[![version](https://img.shields.io/pypi/v/dwa.svg)](https://pypi.org/project/dwa/)
[![license](https://img.shields.io/pypi/l/dwa.svg)](https://pypi.org/project/dwa/)
[![pyversions](https://img.shields.io/pypi/pyversions/dwa.svg)](https://pypi.org/project/dwa/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Dynamic Web Application (DWA) framework written with Tornado.</i>

# Hierarchy

```
dwa
```

# Example

## python
### ./pages/__init__.py
```python
from . import root
from . import common
```
### ./pages/common.py
```python
from dwa import *


class static_file_page(handlers.StaticFileHandler):
    def validate_absolute_path(self, root, absolute_path):
        return super().validate_absolute_path(root, absolute_path)

    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'must-revalidate, max-age=0')
```
### ./pages/root.py
```python
from dwa import *
from . import common


server_name = "root"


class root_html(handlers.HTML):
    server = server_name


class index_page(root_html):
    file_name = "index"


def get_root_settings(app_root):
    app_root = os.path.join(app_root, server_name)
    return (
        server_name,
        [
            (r"/", index_page),
            (r"/((?:img|js|css|common)/.*)", common.static_file_page, {"path": app_root}),
        ]
    )
```
### ./app.py
```python
from dwa import *
import pages


def app_settings_template(app_root: str, domain: str, port: int, cookies_expires_day: float) -> dict:
    settings = {}
    db = "db/db.db"
    settings["cookie_secret"] = open(os.path.join(app_root, "cookie_secret.txt"), "rb").read()
    settings["port"] = port
    settings["db"] = db
    settings["domain"] = domain
    settings["cookies_expires_day"] = cookies_expires_day
    servers = [
        pages.root.get_root_settings(app_root),
    ]
    settings["servers"] = {k: v for k, v in servers}
    return settings


def app_settings(app_root: str) -> dict:
    return app_settings_template(app_root, "your.domain.com", 8888, 1)
```
### ./test.py
```python
import dwa
```
