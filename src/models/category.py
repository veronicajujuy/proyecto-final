class Category:
    def __init__(self, category_id, category_name):
        self.__category_id = category_id
        self.category_name = category_name


@property
def category_name(self):
    return self.__category_name


@category_name.setter
def category_name(self, value):
    if not value:
        raise ValueError("Category name cannot be empty")
    self.__category_name = value
