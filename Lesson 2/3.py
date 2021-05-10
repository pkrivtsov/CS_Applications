import json
import yaml

with open('example/orders.json') as r_j:
    objs = json.load(r_j)

with open('example/file.yaml', 'w') as w_y:
    yaml.dump(objs, w_y, default_flow_style=False, allow_unicode=True)

with open('example/file.yaml') as r_y:
    print(r_y.read())
