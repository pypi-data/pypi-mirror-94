import yaml
import json
from pygrok import Grok


def read_yaml():
    with open("main.yml", "r") as stream:
        return yaml.safe_load(stream)[0]


def parseable_expr(string):
    if str(string).startswith("{{") and str(string).endswith("}}"):
        return True
    return False


def parse_var(val):
    pattern = "{{ %{WORD:key} \"%{WORD:field}\" }}"
    grok = Grok(pattern)
    key = grok.match(str(val))["key"]; field = grok.match(str(val))["field"]
    with open(".register") as fj:
        data = json.load(fj)
        return data[key][field]

