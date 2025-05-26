class Country:
    def __init__(self, country_id, country_name, country_code):
        self.__country_id = country_id
        self.__country_name = country_name
        self.__country_code = country_code


@property
def label(self):
    return f"{self.__country_name} ({self.__country_code})"
