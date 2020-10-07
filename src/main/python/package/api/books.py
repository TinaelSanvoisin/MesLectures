import os
import json
import logging

from package.api.constants import MESLECTURES_FILE, MESLECTURES_DIR
print(MESLECTURES_DIR)
def get_books():
    if os.path.exists(MESLECTURES_FILE):
        with open(MESLECTURES_FILE, "r", encoding="utf-8") as f:
            try:
                dic_books = json.load(f)
            except:
                print('The file is corrupted.')
                return []
        if not isinstance(dic_books, dict):
            print("The file is not a dictionnary.")
            return []
        books = []
        for key_auteur, value_genre in dic_books.items():
            if isinstance(value_genre, dict) and str(value_genre.items()) != "dict_items([])":
                for key_genre, value_titre in value_genre.items():
                    if isinstance(value_titre, dict) and str(value_titre.items()) != "dict_items([])" :
                        for key_titre, value_resume in value_titre.items():
                            if value_resume == "" :
                                books.append(Book(key_auteur, key_genre, key_titre))
                            else :
                                books.append(Book(key_auteur, key_genre, key_titre, value_resume))

                    else :
                        books.append(Book(key_auteur, key_genre))
            else:
                books.append(Book(key_auteur))
    else:
        books = []

    return books

class Book:
    def __init__(self, author, genre = None, title = None, note = None):
        self.author = author
        self.genre = genre
        self.title = title
        self.note = note

    def __str__(self):
        return f"Auteur : {self.author}, Genre : {self.genre}, Titre : {self.title}, Résumé : {self.note}"

    def _get_book(self):
        if os.path.exists(MESLECTURES_FILE):
            with open(MESLECTURES_FILE, "r", encoding="utf-8") as f:
                try:
                    dic_books = json.load(f)
                except:
                    print('The file is corrupted.')
                    return {}
            if not isinstance(dic_books, dict):
                print("The file is not a dictionnary.")
                return {}
            return dic_books
        else :
            return {}

    def _write_book(self, book):
        if os.path.exists(MESLECTURES_DIR):
            with open(MESLECTURES_FILE, "w", encoding="utf-8") as f:
                json.dump(book, f, indent = 4)
        else :
            os.makedirs(MESLECTURES_DIR)
            with open(MESLECTURES_FILE, "w", encoding="utf-8") as f:
                json.dump(book, f, indent = 4)

    def add_to_book(self, characteristic):
        list_book = self._get_book()

        #Verify if the file is empty and if we had something whose is not an author we return False
        if characteristic != "author" and list_book == {}:
            return False

        if characteristic == "author" :
            if self.author in list_book:
                logging.warning(f"L'auteur {self.author} est déjà enregistré !")
                return False
            else :
                list_book[self.author] = {}

        if characteristic == "genre":
            if self.author in list_book:
                if self.genre in list_book[self.author]:
                    logging.warning(f"Le genre {self.genre} est déjà enregistré !")
                    return False
                else:
                    if self.genre != None:
                        list_book[self.author][self.genre] = {}

        if characteristic == "title":
            if self.author in list_book:
                if self.genre in list_book[self.author]:
                    if self.title in list_book[self.author][self.genre]:
                        logging.warning(f"Le titre {self.title} est déjà enregistré !")
                        return False
                    else:
                        if self.title != None:
                            list_book[self.author][self.genre][self.title] = self.note

        if characteristic == "note":
            if self.author in list_book:
                if self.genre in list_book[self.author]:
                    if self.title in list_book[self.author][self.genre]:
                        list_book[self.author][self.genre][self.title] = self.note

        self._write_book(list_book)
        return True

    def remove(self, characteristic):
        list_book = self._get_book()

        if characteristic == "author" and self.author in list_book:
            del list_book[self.author]
        if characteristic == "genre" and self.genre in list_book[self.author]:
            del list_book[self.author][self.genre]
        if characteristic == "title" and self.title in list_book[self.author][self.genre]:
            del list_book[self.author][self.genre][self.title]
        if characteristic == "note" and self.author in list_book and self.genre in list_book[self.author] and self.title in list_book[self.author][self.genre]:
            list_book[self.author][self.genre][self.title]=""

        self._write_book(list_book)






if __name__ == '__main__':
    get_books()



