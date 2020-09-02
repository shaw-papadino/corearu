import requests
from domain.Book import Book 

class GetBookService:
    """
    Input : title / (author / isbn)
    Output : isbn
    """
    query_type = ["intitle", "inauthor", "inpublisher", "subject", "isbn", "lccn", "oclc"]
    gurl = "https://www.googleapis.com/books/v1/volumes?q="
    def put(self, index):
        for i in range(index):
            isbn = self.book_info["items"][i]["volumeInfo"].get("industryIdentifiers")
            title = self.book_info["items"][i]["volumeInfo"].get("title")
            image_link = self.book_info["items"][i]["volumeInfo"].get("imageLinks").get("thumbnail", "")
            if isbn is not None:
                isbn = isbn[1]["identifier"]
            self.books.append(Book(title, isbn, image_link))
    def get(self, title):
        #googlebooksapi
        # [{isbn: sss, title:sss,imagelink:sss},{},{}]
        self.books = []
        query = self.query_type[0] + ":" + title
        response = requests.get(self.gurl + query)
        if response.status_code == 200:
            self.book_info = response.json()
            book_length = book_info["totalItems"]
            if book_length >= 3:
                self.put(3)
            elif book_length > 0:
                self.put(book_length)
            else:
                pass
        else:
            pass

        return self.books

