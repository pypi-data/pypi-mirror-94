__ALL__ = ["parse_params"]


def parse_params(items):
    params = dict(items)
    for k, v in params.items():
        params[k] = [_.decode() for _ in v]
    return params

