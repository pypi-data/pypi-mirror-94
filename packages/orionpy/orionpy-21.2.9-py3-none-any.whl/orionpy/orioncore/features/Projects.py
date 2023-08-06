from .Items import Items
from .Project import Project


class Projects(Items):

    def __init__(self):
        super().__init__("Document Link", "aob_project", lambda data: Project(data))
        self.tags_complement = self.tags+",aob_appId_null"

    def add_item(self, title, text, snippet=None):
        """
        Add a project in aob
        :param title: title of the project
        :param text: content for the project
        :param snippet:
        :return: result of the query (a boolean for "success", the id of the project and the id of the folder)
        """
        url = self.url_manager.add_item_feature_url(self.type)
        data = {"title": title, "snippet": snippet, "text": text, "type": self.type, "tags": self.tags_complement}
        req = self.request.post(url, data).json()
        self._verify(req, "Item \"" + title + "\" was added successfully.\nitemId : " + req["id"],
                     "WARNING : Item \"" + title + "\" was NOT added successfully")
        return req

    def update_item(self, itemId, title, text, snippet=None):
        """
        Update a project in aob
        :param itemId: id of the project you want to update
        :param title: new title of the project
        :param text: content for the project to be updated
        :param snippet:
        :return: result of the query (a boolean for "success" and the id of the project)
        """
        url = self.url_manager.update_item_feature_url(self.type, self._get_owner_from_id(itemId), itemId)
        json_search = self.search(q="id:"+itemId)
        json_url = json_search[0].get("url")
        data = {"title": title, "snippet": snippet, "text": text, "type": self.type, "tags": self.tags_complement,
                "url": json_url}
        req = self.request.post(url, data).json()
        self._verify(req, "Item with id: \"" + itemId + "\" was updated successfully\nTitle : " + title,
                     "WARNING : Item with id: \"" + itemId + "\" was NOT updated successfully")
        return req
