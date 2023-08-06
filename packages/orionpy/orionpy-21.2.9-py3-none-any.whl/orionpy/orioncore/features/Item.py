import json


class Item:

    def __init__(self, data):
        self.data = data

    def get_id(self):
        """
        Return the id of the item
        :return: str id of the item
        """
        return self.data["id"]

    def get_owner(self):
        """
        Return the owner of the item
        :return: str owner of the item
        """
        return self.data["owner"]

    def get(self, element):
        """
        Return the element of the item
        :return: element of the item
        """
        return self.data[element]

    def __str__(self):
        return json.dumps(self.data, indent=4, ensure_ascii=False)

    def __repr__(self):
        return str(self)
