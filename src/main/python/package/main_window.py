from PySide2 import QtWidgets, QtCore, QtGui
from package.api.books import *


class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.get_books_interface()

    def create_widgets(self):
        self.lw_authors = QtWidgets.QListWidget()
        self.text_author = QtWidgets.QLabel("Auteurs")
        self.btn_add_author = QtWidgets.QPushButton()
        self.btn_del_author = QtWidgets.QPushButton()

        self.lw_genres = QtWidgets.QListWidget()
        self.text_genre = QtWidgets.QLabel("Genres")
        self.btn_add_genre = QtWidgets.QPushButton()
        self.btn_del_genre = QtWidgets.QPushButton()

        self.lw_titles = QtWidgets.QListWidget()
        self.text_title = QtWidgets.QLabel("Titres")
        self.btn_add_title = QtWidgets.QPushButton()
        self.btn_del_title = QtWidgets.QPushButton()

        self.note = QtWidgets.QTextEdit()
        self.btn_save = QtWidgets.QPushButton()


    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        self.btn_add_author.setIcon(QtGui.QIcon(self.ctx.get_resource("add.svg")))
        self.btn_add_author.setFixedSize(36, 36)
        self.btn_del_author.setIcon(QtGui.QIcon(self.ctx.get_resource("clean.svg")))
        self.btn_del_author.setFixedSize(36, 36)

        self.btn_add_genre.setIcon(QtGui.QIcon(self.ctx.get_resource("add.svg")))
        self.btn_add_genre.setFixedSize(36, 36)
        self.btn_del_genre.setIcon(QtGui.QIcon(self.ctx.get_resource("clean.svg")))
        self.btn_add_genre.setFixedSize(36, 36)

        self.btn_add_title.setIcon(QtGui.QIcon(self.ctx.get_resource("add.svg")))
        self.btn_del_title.setIcon(QtGui.QIcon(self.ctx.get_resource("clean.svg")))

        self.btn_save.setIcon(QtGui.QIcon(self.ctx.get_resource("saveIcon.png")))



    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

        self.layout_author = QtWidgets.QVBoxLayout()
        self.layout_butons_author = QtWidgets.QHBoxLayout()

        self.layout_genre = QtWidgets.QVBoxLayout()
        self.layout_butons_genre = QtWidgets.QHBoxLayout()

        self.layout_title = QtWidgets.QVBoxLayout()
        self.layout_butons_title = QtWidgets.QHBoxLayout()

        self.layout_note = QtWidgets.QVBoxLayout()

    def add_widgets_to_layouts(self):
        self.main_layout.addLayout(self.layout_author, 0, 0, 1, 1)
        self.main_layout.addLayout(self.layout_genre, 0, 1, 1, 1)
        self.main_layout.addLayout(self.layout_title, 0, 2, 1, 1)
        self.main_layout.addLayout(self.layout_note, 1, 0, 1, 3)

        # Authors
        self.layout_author.addWidget(self.text_author)
        self.layout_author.addWidget(self.lw_authors)
        self.layout_author.addLayout(self.layout_butons_author)
        self.layout_butons_author.addWidget(self.btn_add_author)
        self.layout_butons_author.addStretch()
        self.layout_butons_author.addWidget(self.btn_del_author)

        # Genres
        self.layout_genre.addWidget(self.text_genre)
        self.layout_genre.addWidget(self.lw_genres)
        self.layout_genre.addLayout(self.layout_butons_genre)
        self.layout_butons_genre.addWidget(self.btn_add_genre)
        self.layout_butons_genre.addStretch()
        self.layout_butons_genre.addWidget(self.btn_del_genre)

        # Titles
        self.layout_title.addWidget(self.text_title)
        self.layout_title.addWidget(self.lw_titles)
        self.layout_title.addLayout(self.layout_butons_title)
        self.layout_butons_title.addWidget(self.btn_add_title)
        self.layout_butons_title.addWidget(self.btn_del_title)

        # Note
        self.layout_note.addWidget(self.note)
        self.layout_note.addWidget(self.btn_save)

    def setup_connections(self):
        self.btn_add_author.clicked.connect(self.add_author)
        self.btn_del_author.clicked.connect(self.del_author)
        self.lw_authors.itemClicked.connect(self.get_genres)

        self.btn_add_genre.clicked.connect(self.add_genre)
        self.btn_del_genre.clicked.connect(self.del_genre)
        self.lw_genres.itemClicked.connect(self.get_titles)

        self.btn_add_title.clicked.connect(self.add_title)
        self.btn_del_title.clicked.connect(self.del_title)
        self.lw_titles.itemClicked.connect(self.get_note)

        self.btn_save.clicked.connect(self.save_note)

    def add_author(self):
        author_name, ok = QtWidgets.QInputDialog.getText(self,
                                                         "Ajouter un auteur",
                                                         "Auteur")
        if ok and author_name:
            book = Book(author_name)
            author_add_ok = book.add_to_book("author")
            if author_add_ok:
                lw_author = QtWidgets.QListWidgetItem(book.author)
                self.lw_authors.addItem(lw_author)
                return True
            msg_error = QtWidgets.QMessageBox(text="L'auteur est déjà dans la liste !")
            msg_error.exec_()
            return False

    def add_genre(self):
        selected_item = self.get_selected_lw_item_author()
        genre_name, ok = QtWidgets.QInputDialog.getText(self,
                                                        "Ajouter un genre",
                                                        "Genre")

        if ok and genre_name and selected_item:
            book = Book(selected_item.text(), genre_name)
            genre_add_ok = book.add_to_book("genre")
            if genre_add_ok:
                lw_genre = QtWidgets.QListWidgetItem(book.genre)
                self.lw_genres.addItem(lw_genre)
                return True
            msg_error = QtWidgets.QMessageBox(text="Le genre est déjà dans la liste !")
            msg_error.exec_()
            return False

    def add_title(self):
        selected_item_author = self.get_selected_lw_item_author()
        selected_item_genre = self.get_selected_lw_item_genre()
        title_name, ok = QtWidgets.QInputDialog.getText(self,
                                                        "Ajouter un titre",
                                                        "Titre")

        if ok and title_name and selected_item_genre and selected_item_author:
            book = Book(selected_item_author.text(),selected_item_genre.text(), title_name)
            title_add_ok = book.add_to_book("title")
            if title_add_ok:
                lw_title = QtWidgets.QListWidgetItem(book.title)
                self.lw_titles.addItem(lw_title)
                return True
            msg_error = QtWidgets.QMessageBox(text="Le titre est déjà dans la liste !")
            msg_error.exec_()
            return False

    def del_author(self):
        selected_item = self.get_selected_lw_item_author()
        books = get_books()
        if selected_item:
            answer = QtWidgets.QMessageBox.question(self, "Etes-vous sûr ?",
                                                    "Voulez vous vraiment supprimer cet auteur ?\nToutes les informations, genres, titres et notes seront supprimés également.",
                                                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                for book in books:
                    if selected_item.text() == book.author:
                        book.remove("author")
                        self.lw_authors.takeItem(self.lw_authors.row(selected_item))

    def del_genre(self):
        selected_item = self.get_selected_lw_item_genre()
        selectedAuthor = self.get_selected_lw_item_author()
        books = get_books()
        if selected_item:
            answer = QtWidgets.QMessageBox.question(self, "Etes-vous sûr ?",
                                                    "Voulez vous vraiment supprimer ce genre ?\nToutes les informations, titres et notes seront supprimés également.",
                                                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                for book in books:
                    if selected_item.text() == book.genre and selectedAuthor.text() == book.author:
                        book.remove("genre")
                        self.lw_genres.takeItem(self.lw_genres.row(selected_item))

    def del_title(self):
        selected_item = self.get_selected_lw_item_title()
        books = get_books()
        if selected_item:
            answer = QtWidgets.QMessageBox.question(self, "Etes-vous sûr ?",
                                                    "Voulez vous vraiment supprimer ce genre ?\nLe texte lié à ce titre sera supprimé également.",
                                                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                for book in books:
                    if selected_item.text() == book.title:
                        book.remove("title")
                        self.lw_titles.takeItem(self.lw_titles.row(selected_item))

    def get_selected_lw_item_author(self):
        selected_items = self.lw_authors.selectedItems()
        if selected_items:
            return selected_items[0]
        return None

    def get_selected_lw_item_genre(self):
        selected_items = self.lw_genres.selectedItems()
        if selected_items:
            return selected_items[0]
        return None

    def get_selected_lw_item_title(self):
        selected_items = self.lw_titles.selectedItems()
        if selected_items:
            return selected_items[0]
        return None

    def get_books_interface(self):
        books = get_books()
        for book in books:
            item = self.lw_authors.findItems(book.author, QtCore.Qt.MatchExactly)
            if not item:
                self.lw_authors.addItem(book.author)

    def get_genres(self):
        self.note.setText("")
        self.lw_genres.clear()
        self.lw_titles.clear()
        selectedAuthor = self.get_selected_lw_item_author()
        if selectedAuthor:
            books = get_books()
            print(books)
            for book in books:
                item = self.lw_genres.findItems(book.genre, QtCore.Qt.MatchExactly)
                if book.author == selectedAuthor.text() and not item:
                    self.lw_genres.addItem(book.genre)

    def get_titles(self):
        self.note.setText("")
        self.lw_titles.clear()
        selectedAuthor = self.get_selected_lw_item_author()
        selectedGenre = self.get_selected_lw_item_genre()
        if selectedGenre:
            books = get_books()
            for book in books:
                item = self.lw_genres.findItems(book.title, QtCore.Qt.MatchExactly)
                if book.author == selectedAuthor.text() and not item and book.genre == selectedGenre.text():
                    self.lw_titles.addItem(book.title)

    def get_note(self):
        selectedTitle = self.get_selected_lw_item_title()
        selectedAuthor = self.get_selected_lw_item_author()
        selectedGenre = self.get_selected_lw_item_genre()
        if selectedTitle:
            books = get_books()
            for book in books:
                if book.title == selectedTitle.text() and book.author==selectedAuthor.text() and book.genre==selectedGenre.text():
                    self.note.setText(book.note)

    def save_note(self):
        selectedAuthor = self.get_selected_lw_item_author()
        selectedGenre = self.get_selected_lw_item_genre()
        selectedTitle = self.get_selected_lw_item_title()
        if selectedAuthor and selectedGenre and selectedTitle :
            books = get_books()
            for book in books:
                if book.author == selectedAuthor.text() and book.genre == selectedGenre.text() and book.title == selectedTitle.text():
                   book.note = self.note.toPlainText()
                   book.add_to_book("note")