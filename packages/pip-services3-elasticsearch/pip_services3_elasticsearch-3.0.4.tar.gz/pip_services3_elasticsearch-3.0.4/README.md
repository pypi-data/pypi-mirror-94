# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> ElasticSearch components for Python

This module is a part of the [Pip.Services](http://pipservices.org) polyglot microservices toolkit.

The Elasticsearch module contains logging components with data storage on the Elasticsearch server.

The module contains the following packages:
- **Build** - contains a factory for the construction of components
- **Log** - Logging components

<a name="links"></a> Quick links:

* [Configuration](https://www.pipservices.org/recipies/configuration)
* [Logging](https://www.pipservices.org/recipies/active-logic)
* [Virtual memory configuration](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144)
* [API Reference](https://pip-services3-python.github.io/pip-services3-elasticsearch-python)
* [Change Log](CHANGELOG.md)
* [Get Help](https://www.pipservices.org/community/help)
* [Contribute](https://www.pipservices.org/community/contribute)

## Use

Install the Python package as
```bash
pip install pip-services3-elasticsearch
```

Microservice components shall perform logging usual way using CompositeLogger component.
The CompositeLogger will get ElasticSearchLogger from references and will redirect log messages
there among other destinations.

```python
from pip_services3_commons.config import IConfigurable
from pip_services3_commons.refer import IReferenceable
from pip_services3_components.log import CompositeLogger


class MyComponent(IConfigurable, IReferenceable):
    def __init__(self):
        super(MyComponent, self).__init__()
        self.__logger = CompositeLogger()

    def configure(self, config):
        self.__logger.configure(config)

    def set_references(self, references):
        self.__logger.set_references(references)

    def my_method(self, correlation_id, param1):
        self.__logger.trace(correlation_id, 'Executed method mycomponent.mymethod')
        # ...
```

Configuration for your microservice that includes ElasticSearch logger may look the following way.

```yaml
...
{{#if ELASTICSEARCH_ENABLED}}
- descriptor: pip-services:logger:elasticsearch:default:1.0
  connection:
    uri: {{{ELASTICSEARCG_SERVICE_URI}}}
    host: {{{ELASTICSEARCH_SERVICE_HOST}}}{{#unless ELASTICSEARCH_SERVICE_HOST}}localhost{{/unless}}
    port: {{ELASTICSEARCG_SERVICE_PORT}}{{#unless ELASTICSEARCH_SERVICE_PORT}}9200{{/unless}}\ 
{{/if}}
...
```

## Develop

For development you shall install the following prerequisites:
* Python 3.7+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Run automated tests:
```bash
python test.py
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./clear.ps1
```

## Contacts

The library is created and maintained by **Sergey Seroukhov**.

The documentation is written by:
- **Mark Makarychev**