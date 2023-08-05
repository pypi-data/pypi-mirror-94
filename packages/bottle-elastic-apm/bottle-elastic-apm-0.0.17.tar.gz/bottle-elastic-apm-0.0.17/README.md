# Bottle Elastic APM

Simple plugin to use ELK with APM server for your bottle application

```python
# Keep this first
import elasticapm
elasticapm.instrument()

from bottle import default_app, run
from bottle_elastic_apm import ELKApmPLugin

ELK_CONFIG = {
    'SERVICE_NAME': 'my-app',
}

app = default_app()
app.install(ELKApmPLugin(ELK_CONFIG))

@app.get('/')
def index():
    return 'Hello world!'

run(app)
```