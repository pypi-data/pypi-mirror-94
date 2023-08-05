import yaml
import json
from jinja2.ext import Extension


class YamlifyExtension(Extension):
    """Jinja2 extension to convert a Python object to YAML."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def yamlify(obj):
            return yaml.dump(obj)

        environment.filters["yamlify"] = yamlify


class JsonifyExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def jsonify(obj):
            return json.dumps(obj)

        environment.filters["jsonify"] = jsonify
