import json

from Homework12.classes.exceptions import DataSourceBrokenException


class DataManager:

    def __init__(self, path):
        self.path = path  # path to file
        pass

    def _load_data(self):
        """ Load data from file to use by other methods"""
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise DataSourceBrokenException("File is damaged")

        return data

    def _save_data(self, data):
        """" Saves loaded data in file"""
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """ Returns whole list of data"""
        data = self._load_data()
        return data

    def search(self, substring):
        """" Returns posts containing substring"""
        posts = self._load_data()
        substring = substring.lower()
        matching_posts = [post for post in posts if substring in post["content"].lower()]

        return matching_posts

    def add(self, post):
        """"Add to post database new post"""
        if type(post) != dict:
            raise TypeError("This is not a a dictionary")

        posts = self._load_data()
        posts.append(post)
        self._save_data(posts)
