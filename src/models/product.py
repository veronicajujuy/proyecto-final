class Product:
    def __init__(
        self,
        product_id,
        product_name,
        price,
        category_id,
        prod_class,
        modify_date,
        resistant,
        is_allergic,
        vitality_days,
    ):
        self.__product_id = product_id
        self.__product_name = product_name
        self.__price = price
        self.__category_id = category_id
        self.__prod_class = prod_class
        self.__modify_date = modify_date
        self.__resistant = resistant
        self.__is_allergic = is_allergic
        self.__vitality_days = vitality_days

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

    def apply_discount(self, percentage):
        if 0 <= percentage <= 100:
            self.__price *= 1 - percentage / 100
        else:
            raise ValueError("Discount percentage must be between 0 and 100")

    def is_expired(self, days_passed):
        if days_passed < 0:
            raise ValueError("Days passed cannot be negative")
        return self.__vitality_days <= days_passed
