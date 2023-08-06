import json
from ..RequestManager import RequestManager
from ..UrlBuilder import UrlBuilder


class Items:

    def __init__(self, type, tags, construct):
        self.type = type
        self.tags = tags
        self.url_manager = UrlBuilder()
        self.request = RequestManager()
        self.construct = construct
        self.query_supplement = "tags:" + self.tags + " AND type:" + self.type

    def _verify(self, req, true, false):
        """
        Check if the query is well executed
        :param req: result of the query
        :param true: message if the query is successful
        :param false: message if the query is not successful
        """
        if "error" in req.keys():
            if isinstance(req["error"], dict):
                if "message" in req["error"].keys():
                    raise ValueError(req["error"]["message"])
            raise ValueError(req["error"])
        if "success" in req.keys():
            if req["success"]:
                print(true)
                return
            else:
                raise ValueError(false)
        print(true)

    def search(self, q="", start=-1, num=100, all=False):
        """
        Method to search items with a query q
        :param q: query
        :param start: number of the first result, default value : -1
        :param num: number of results, default value : 100
        :param all: True to search in portal and elasticsearch, default: False to search in portal
        :return: results of the query (json), containing a list of items
        """
        result = []
        if num <= 0:
            raise ValueError("num must be > 0")
        count = 0

        #url construction
        if all is True:
            url = self.url_manager.search_all_feature_url(self.type)
        else:
            url = self.url_manager.search_feature_url(self.type)

        #request parameters
        data_q = self.query_supplement
        if len(q.strip()) != 0:
            data_q = " AND " + data_q
        data = {"start": start, "num": num, "q": q + data_q}

        #request
        while True:
            req = self.request.get(url, data).json()
            for feat in req["results"]:
                result.append(self.construct(feat))
                count += 1
                if count == num:
                    if len(result) == 0:
                        raise ValueError("No item found with this query : " + q)
                    return result
            if req["nextStart"] == -1:
                if len(result) == 0:
                    raise ValueError("No item found with this query : " + q)
                return result
            data["start"] = req["nextStart"]

    def data(self, itemId):
        """
        Method to get the data of the item with the id 'itemId'
        :param itemId: id of the item (geonote or project) you want the data
        :return: Geonote or Project, depend on the object that call this method
        """
        url = self.url_manager.data_feature_url(itemId, self.type)
        req = self.request.get(url).json()
        print("Item : "+itemId)
        self._verify(req, "Data found", "Data NOT found")
        result = json.dumps(req, indent=4, ensure_ascii=False)
        return result

    def data_export(self, itemId, export_file):
        """
        Method to get the data of the item with the id 'itemId' and export it in a json file
        It is necessary to add '.json' at the end of the path
        :param itemId: id of the item (geonote or project) you want the data
        :param export_file: path of the file where to export the data
        :return: Geonote or Project, depend on the object that call this method
        """
        if export_file[-5:] != ".json":
            raise ValueError("File must end with '.json'")
        data = self.data(itemId)
        try:
            file = open(export_file, 'w', encoding="utf-8")
            file.write(data)
            file.close()
        except:
            error = "Cannot write in file " + export_file
            print(error)
        return data


    def add_item(self, owner, title, text, snippet=None):
        """
        Add an item in aob
        :param title: title of the item
        :param text: content for the item
        :param snippet:
        :return: result of the query (a boolean for "success", the id of the item and the id of the folder)
        """
        url = self.url_manager.add_item_feature_url(self.type, owner)
        data = {"title": title, "snippet": snippet, "text": text, "type": self.type, "tags": self.tags}
        req = self.request.post(url, data).json()
        self._verify(req, "Item \"" + str(title) + "\" was added successfully.\nitemId : " + req["id"],
                     "WARNING : Item \"" + str(title) + "\" was NOT added successfully")
        return req

    def add_item_from_file(self, title, json_path, snippet=None):
        """
        Add an item in aob from a json file
        :param json_path: path of the json file
        :return: result of the query (a boolean for "success", the id of the item and the id of the folder)
        """
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.dumps(json.load(file), indent=4, ensure_ascii=False)
        print(json_data)
        return self.add_item(title, json_data, snippet)

    def update_item(self, itemId, title, text, snippet=None):
        """
        Update an item in aob
        :param itemId: id of the item you want to update
        :param title: new title of the item
        :param text: content for the item to be updated
        :param snippet:
        :return: result of the query (a boolean for "success" and the id of the item)
        """
        url = self.url_manager.update_item_feature_url(self.type, self._get_owner_from_id(itemId), itemId)
        data = {"title": title, "snippet": snippet, "text": text, "type": self.type, "tags": self.tags}
        req = self.request.post(url, data).json()
        self._verify(req, "Item with id: \"" + str(itemId) + "\" was updated successfully\nTitle : " + title,
                     "WARNING : Item with id: \"" + str(itemId) + "\" was NOT updated successfully")
        return req

    def update_item_from_file(self, itemId, title, json_path, snippet=None):
        """
        Update an item in aob from a json file
        :param json_path: path of the json file
        :return: result of the query (a boolean for "success", the id of the item and the id of the folder)
        """
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.dumps(json.load(file), indent=4, ensure_ascii=False)
        return self.update_item(itemId, title, json_data, snippet)

    def _get_owner_from_id(self, itemId):
        """
        Return the owner of the item that correspond to the item id 'itemId'
        :param itemId: id of the item you want the owner
        :return: owner of the item
        """
        return self._get_info_from_id(itemId, "owner")

    def _get_info_from_id(self, itemId, info):
        """
        Return the info wanted of the item that correspond to the itemId
        :param itemId: id of the item you want the owner
        :return: owner of the item
        """
        search = self.search(q="id:"+itemId)
        if len(search) == 0 or self.tags not in search[0].get("tags"):
            error = "There is no " + self.tags[4::] + " with this id"
            raise ValueError(error)
        result = search[0].get(info)
        return result

    def delete(self, itemId):
        """
        Delete the item with the id itemId
        :param itemId: id of the item you want to delete
        :return: result of the query (a boolean for "success" and the id of the item)
        """
        url = self.url_manager.delete_feature_url(self.type, self._get_owner_from_id(itemId), itemId)
        req = self.request.post(url).json()
        self._verify(req, "Item with id: \"" + str(itemId) + "\" was deleted successfully",
                     "WARNING : Item with id: \"" + str(itemId) + "\" was NOT deleted successfully")
        return req

    def reassign(self, itemId, targetUsername):
        """
        Change the owner of the item with the id itemId for the user "targetUsername")
        :param itemId: id of the item you want to reassign
        :param targetUsername: username of the user you want to reassign the item
        :return: result of the query (a boolean for "success" and the id of the item)
        """
        url = self.url_manager.reassign_feature_url(self.type, self._get_owner_from_id(itemId), itemId)
        data = {"targetUsername": targetUsername}
        req = self.request.post(url, data).json()
        self._verify(req, "Item with id: \"" + str(itemId) + "\" was reassigned successfully\nNew owner : " + str(targetUsername),
                     "WARNING : Item with id: \"" + str(itemId) + "\" was NOT reassigned successfully")
        return req
