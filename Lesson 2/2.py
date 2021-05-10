import json

orders = {'items': ['колбаса', 'тушенка'], "quantity": 2, 'price': {'колбаса': '7€', 'тушенка': '3€'},
          'buyer': 'Мясоедов', 'date': '8.05.2021'}


def write_order_to_json(data):
    with open('example/orders.json', 'w', encoding='cp1251') as w_file:
        json.dump(data, w_file, ensure_ascii=False, indent=4)


write_order_to_json(orders)
