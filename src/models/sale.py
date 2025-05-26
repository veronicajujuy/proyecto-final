class Sale:
    def __init__(
        self,
        sale_id,
        salesperson_id,
        customer_id,
        product_id,
        quantity,
        discount,
        total_price,
        sales_date,
        transaction_number,
    ):
        self.__sale_id = sale_id
        self.__salesperson_id = salesperson_id
        self.__customer_id = customer_id
        self.__product_id = product_id
        self.quantity = quantity
        self.__discount = discount
        self.__total_price = total_price
        self.__sales_date = sales_date
        self.__transaction_number = transaction_number


@property
def quantity(self):
    return self.__quantity


@quantity.setter
def quantity(self, value):
    if value < 0:
        raise ValueError("Quantity cannot be negative")
    self.__quantity = value


def calculate_final_price(self):
    return self.__total_price - (self.__total_price * self.__discount / 100)
