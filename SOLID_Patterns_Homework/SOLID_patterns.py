# Создайте приложение для эмуляции работа киоска по продаже хот-догов.
# Приложение должно иметь следующую функциональность:

# 1. Пользователь может выбрать из трёх стандартных рецептов хот-дога или создать свой рецепт.
# 2. Пользователь может выбирать добавлять ли майонез, горчицу, кетчуп, топпинги
# (сладкий лук, халапеньо, чили, соленный огурец и т.д.).
# 3. Информацию о заказанном хот-доге нужно отображать на экран и сохранять в файл.
# 4. Если пользователь заказывает от трёх хот-догов нужно предусмотреть скидку.
# Скидка зависит от количества хот-догов.
# 5. Расчет может производиться, как наличными, так и картой.
# 6. Необходимо иметь возможность просмотреть количество проданных хот-догов, выручку, прибыль.
# 7. Необходимо иметь возможность просмотреть информацию о наличии компонентов для создания хот-дога.
# 8. Если компоненты для создания хот-догов заканчиваются нужно вывести информационное сообщение
# о тех компонентах, которые требуется приобрести.
# 9. Классы приложения должны быть построены с учетом принципов SOLID и паттернов проектирования.


import json
from abc import ABC, abstractmethod
from typing import List


# INGREDIENT

class Ingredient:
    def __init__(self, name: str, price: float, quantity: int = 50):
        self.name = name
        self.price = price
        self.quantity = quantity

    def use(self, amount: int = 1):
        if self.quantity < amount:
            raise Exception(f"Недостаточно {self.name}!")
        self.quantity -= amount


# INVENTORY

class Inventory:
    def __init__(self):
        self.ingredients = {
            "bun": Ingredient("Булочка", 50),
            "sausage": Ingredient("Сосиска", 50),
            "ketchup": Ingredient("Кетчуп", 50),
            "mustard": Ingredient("Горчица", 20),
            "mayonnaise": Ingredient("Майонез", 20),
            "sweet_onion": Ingredient("Сладкий лук", 10),
            "jalapeno": Ingredient("Халапеньо", 5),
            "chili": Ingredient("Чили", 20),
            "pickle": Ingredient("Солёный огурец", 20),
        }

    def get_ingredient(self, name: str) -> Ingredient:
        if name not in self.ingredients:
            raise Exception(f"Ингредиент {name} не найден!")
        return self.ingredients[name]

    def print_inventory(self):
        print("\nСклад ингредиентов:")
        for ing in self.ingredients.values():
            print(f"{ing.name}: {ing.quantity} шт.")

    def missing_ingredients(self):
        return [i.name for i in self.ingredients.values() if i.quantity <= 0]


# HOTDOG AND BUILDER

class HotDog:
    def __init__(self, name: str = "Custom"):
        self.name = name
        self.ingredients: List[Ingredient] = []

    def add_ingredient(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)

    def calculate_price(self):
        return sum(i.price for i in self.ingredients)

    def show(self):
        ing_names = [i.name for i in self.ingredients]
        print(f"{self.name}: {', '.join(ing_names)}. Цена: {self.calculate_price()}₽")

class HotDogBuilder:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.hotdog = HotDog()

    def add(self, ingredient_name: str):
        ingredient = self.inventory.get_ingredient(ingredient_name)
        ingredient.use()
        self.hotdog.add_ingredient(ingredient)
        return self

    def build(self):
        return self.hotdog


# PAYMENT STRATEGY

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class CashPayment(PaymentStrategy):
    def pay(self, amount: float):
        print(f"Оплачено наличными: {amount:.2f}₽")

class CardPayment(PaymentStrategy):
    def pay(self, amount: float):
        print(f"Оплачено картой: {amount:.2f}₽")


# ORDER

class Order:
    DISCOUNT_THRESHOLD = 3
    DISCOUNT_PERCENT = 0.1

    def __init__(self):
        self.hotdogs: List[HotDog] = []

    def add_hotdog(self, hotdog: HotDog):
        self.hotdogs.append(hotdog)

    def calculate_total(self):
        total = sum(hd.calculate_price() for hd in self.hotdogs)
        if len(self.hotdogs) >= self.DISCOUNT_THRESHOLD:
            total *= (1 - self.DISCOUNT_PERCENT)
        return total

    def show_order(self):
        print("\nВаш заказ:")
        for hd in self.hotdogs:
            hd.show()
        print(f"Итого с учетом скидки: {self.calculate_total():.2f}₽")


# SALES REPORT

class SalesReport:
    def __init__(self):
        self.total_sales = 0
        self.total_hotdogs = 0

    def record_sale(self, order: Order):
        self.total_hotdogs += len(order.hotdogs)
        self.total_sales += order.calculate_total()

    def print_report(self):
        print("\n--- Отчёт по продажам ---")
        print(f"Продано хот-догов: {self.total_hotdogs}")
        print(f"Выручка: {self.total_sales:.2f}₽")


# FILE MANAGER

class FileManager:
    def save_order(self, order: Order, filename: str = "orders.json"):
        data = []
        for hd in order.hotdogs:
            data.append({
                "name": hd.name,
                "ingredients": [i.name for i in hd.ingredients],
                "price": hd.calculate_price()
            })
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")


# STANDARD RECIPES

STANDARD_RECIPES = {
    "Classic": ["bun", "sausage", "ketchup", "mustard"],
    "Spicy": ["bun", "sausage", "chili", "jalapeno"],
    "Sweet": ["bun", "sausage", "sweet_onion", "ketchup"]
}


# KIOSK INTERFACE

def main():
    inventory = Inventory()
    report = SalesReport()
    file_manager = FileManager()

    print("Добро пожаловать в киоск хот-догов!")
    while True:
        print("\nМеню:")
        print("1. Сделать заказ")
        print("2. Просмотреть склад")
        print("3. Статистика продаж")
        print("4. Выйти")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            order = Order()
            while True:
                print("\nВыберите тип хот-дога:")
                print("1. Стандартный")
                print("2. Создать свой")
                print("3. Завершить заказ")
                type_choice = input("Выбор: ").strip()

                if type_choice == "1":
                    print("Выберите рецепт:")
                    for i, name in enumerate(STANDARD_RECIPES.keys(), 1):
                        print(f"{i}. {name}")
                    idx = int(input("Номер: ")) - 1
                    recipe_name = list(STANDARD_RECIPES.keys())[idx]
                    recipe_ingredients = STANDARD_RECIPES[recipe_name]

                    builder = HotDogBuilder(inventory)
                    for ing in recipe_ingredients:
                        builder.add(ing)
                    hotdog = builder.build()
                    hotdog.name = recipe_name
                    order.add_hotdog(hotdog)

                elif type_choice == "2":
                    builder = HotDogBuilder(inventory)
                    print("Введите ингредиенты через запятую (bun, sausage, ketchup и т.д.):")
                    ing_names = input().split(",")
                    for ing in ing_names:
                        builder.add(ing.strip())
                    hotdog = builder.build()
                    order.add_hotdog(hotdog)

                elif type_choice == "3":
                    break

            # Показываем заказ
            order.show_order()

            # Предупреждаем о нехватке ингредиентов
            missing = inventory.missing_ingredients()
            if missing:
                print("⚠ Недостающие ингредиенты:", ", ".join(missing))

            # Оплата
            print("\nВыберите способ оплаты:\n1. Наличные\n2. Карта")
            pay_method = input("Способ: ").strip()
            payment = CashPayment() if pay_method == "1" else CardPayment()
            payment.pay(order.calculate_total())

            # Сохраняем и обновляем статистику
            file_manager.save_order(order)
            report.record_sale(order)

        elif choice == "2":
            inventory.print_inventory()

        elif choice == "3":
            report.print_report()
            missing = inventory.missing_ingredients()
            if missing:
                print("⚠ Необходимо закупить ингредиенты:", ", ".join(missing))

        elif choice == "4":
            print("Спасибо за заказ!")
            break

        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
