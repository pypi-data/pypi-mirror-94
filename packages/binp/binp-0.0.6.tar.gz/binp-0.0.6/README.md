# Basic Integration Platform

![PyPI](https://img.shields.io/pypi/v/binp)
![PyPI - License](https://img.shields.io/pypi/l/binp)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/binp)

![logo-192](https://user-images.githubusercontent.com/6597086/107153224-4dc2d080-69a7-11eb-96d1-31c304fb821f.png)

Provides a platform for automation with code-first approach,
with embedded batteries:

* Tracing (journals)
* Internal and user-defined API
* Ultra-light but rich mobile-first UI
* Embedded key-value storage

It is heavily inspired by node-red and aims to provide same
enjoyment during development but without mess of nodes and connections
for tasks a little bit more complicated than just hello world.

The platform also tries to be easy in deployment and maintaining.
Code could be stored in a SCM (ex: git) and persistent storage is just a single file that
could be backed up and restored trivially.

Because memory and CPU consumption relatively low a solution based on the platform
could be launched even on Raspberry Pi Zero with 512MB RAM.

## Install

`pip install binp uvicorn[standard]`

Example:

```python
from random import randint

from binp import BINP

binp = BINP()


@binp.app.post('/random', response_model=int)
@binp.journal
async def generate_random():
    """
    Generate random number in range 0 ... 1024
    """
    return randint(0, 1024)


@binp.action
@binp.journal
async def currency_rate():
    """
    Fetch currency rate for EUR -> USD
    """
    # go to external service
    euro = 1.3
    await binp.journal.record('rates fetched', base_currency='USD', euro=euro)
```

Save as 'example.py' and run it by

```
uvicorn example:binp.app
```

> TIP: pass `--reload` flag to `uvicorn` to support automatic reload during development

It will expose

* http://127.0.0.1:8000 - UI and API
* http://127.0.0.1:8000/docs - Swagger docs for user-defined APIs
* http://127.0.0.1:8000/internal/docs - Swagger docs for internal APIs


![Peek 2021-02-08 17-27](https://user-images.githubusercontent.com/6597086/107200766-14d03d80-6a33-11eb-96fc-5d132cb2862e.gif)

![image](https://user-images.githubusercontent.com/6597086/107201190-a049ce80-6a33-11eb-94ac-dd4117d0ed52.png)


## Configuration

Default configuration can be changed by environment variables:

* `DEV` - set `DEV=true` to enable development mode
* `DB_URL` - database SQLITE URL, default `sqlite:///data.db`

HTTP port and binding address configured by `uvicorn`:

* `--port` - set listening port, default `8000`
* `--host` - set binding host, default `127.0.0.1`


For `uvicorn` command should be like

    uvicorn <python file without .py>:<binp instance>.app