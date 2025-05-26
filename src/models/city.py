class City:
    def __init__(self, city_id, city_name, zipcode, country_id):
        self.__city_id = city_id
        self.__city_name = city_name
        self.__zipcode = zipcode
        self.__country_id = country_id


@property
def label(self):
    return f"{self.__city_name} ({self.__zipcode})"
