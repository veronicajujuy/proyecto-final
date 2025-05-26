class Customer:
    def __init__(
        self, customer_id, first_name, middle_initial, last_name, city_id, address
    ):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__middle_initial = middle_initial
        self.__last_name = last_name
        self.city_id = city_id
        self.address = address


@property
def address(self):
    return self.__address


@address.setter
def address(self, value):
    if not value:
        raise ValueError("Address cannot be empty")
    self.__address = value


def full_name(self):
    return f"{self.__first_name} {self.__middle_initial} {self.__last_name}".strip()
