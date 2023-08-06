# Basic Integration Platform

![logo-192](https://user-images.githubusercontent.com/6597086/107153224-4dc2d080-69a7-11eb-96d1-31c304fb821f.png)

Provides all-in-one package with:

* tracing
* journal
* Web UI

Tends to help to create basic integration solutions.
Heavily inspired by node-red.

## Install

`pip install binp uvicorn`

Example:

```python
from random import randint

from binp import BINP

bip = BINP()


@bip.app.post('/random', response_model=int)
@bip.journal
async def generate_random():
    """
    Generate random number in range 0 ... 1024
    """
    return randint(0, 1024)


@bip.action
@bip.journal
async def currency_rate():
    """
    Fetch currency rate for EUR -> USD
    """
    # go to external service
    euro = 1.3
    await bip.journal.record('rates fetched', base_currency='USD', euro=euro)
```

Save as 'example.py' and run it by

```
uvicorn example:bip.app
```

It will expose

* http://127.0.0.1:8000 - UI and API
* http://127.0.0.1:8000/docs - Swagger docs for user-defined APIs
* http://127.0.0.1:8000/internal/docs - Swagger docs for internal APIs

