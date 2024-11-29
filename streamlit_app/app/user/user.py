import pandas as pd

class User():

    def __init__(self) -> None:

        self.id: int
        self.email: str
        self.name: str

        self.adm: bool

        self.bookmarks_id: list[int] = []

    def set_bookmarks(self, bookmarks: pd.DataFrame):

        if not bookmarks.empty:
            for id in bookmarks['escola_id']:
                self.bookmarks_id.append(id)


    def add_bookmark(self, school_id: int):
        self.bookmarks_id.append(school_id)

    def remove_bookmark(self, school_id: int):
        self.bookmarks_id.remove(school_id)


    