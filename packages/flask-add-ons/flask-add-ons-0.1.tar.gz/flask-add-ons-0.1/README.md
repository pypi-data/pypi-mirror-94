# Flask add ons
Add ons for flask.

## Installation

```bash
pip install flask-add-ons
```

## Usage

```python
import logging
from flask-add-ons import colorize_werkzeug

# Logging
logging.basicConfig(level=logging.DEBUG)
colorize_werkzeug()
```