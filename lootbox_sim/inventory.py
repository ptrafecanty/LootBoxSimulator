class Inventory:
    def __init__(self):
        self.items = {}  # item_name -> count

    def add_item(self, item_name):
        self.items[item_name] = self.items.get(item_name, 0) + 1

    def print_inventory(self):
        print("Inventory:")
        for name, count in self.items.items():
            print(f"{name}: {count}")
