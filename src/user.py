import random
import settings

class User:
    def __init__(self, chat_id, name):
        self.name = name
        self.chat_id = chat_id
        self.events = {}  # Словарь для хранения криптовалют
        self.tags = []

    def add_event(self, name, time, describe):
        pass
        #if name in self.cryptos:
        #    self.cryptos[name]['amount'] += float(amount)
        #else:
        #    self.cryptos[name] = {'amount': float(amount), 'price_per_coin': float(price_per_coin)}

    def remove_event(self, name, time, describe):
        #if name in self.cryptos and self.cryptos[name]['amount'] >= float(amount):
        #    self.cryptos[name]['amount'] -= float(amount)
        #    if self.cryptos[name]['amount'] == 0.0:
        #        del self.cryptos[name]
        #else:
        #    print(f"Недостаточно {name} для продажи или криптовалюта не найдена.")
        pass

    def get_event_amount(self, name):
    #    return self.cryptos.get(name, {}).get('amount', 0)
        pass
