import json


def downgrade_dict(something):
    return json.loads(json.dumps(something))
