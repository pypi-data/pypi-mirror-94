from utils.parsing.yaml import parse_var, parseable_expr, read_yaml


def publish(identifier, taskobj, confobj):
    pipeline_name = read_yaml()["name"]
    {
        "codebase": {},
        "sandbox": {},
        "input-data": {},
        "output-encrypt": {},
        "dockerize": {},
        "prepare-policy": {},
        "upload-policy": {},
        "execute-policy": {},
        "retrieve-ouput": {}
    }
    pass