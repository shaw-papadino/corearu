import requests
from domain.Book import Book 

class GetBookService:
    """
    Input : title / (author / isbn)
    Output : isbn
    """
    query_type = ["intitle", "inauthor", "inpublisher", "subject", "isbn", "lccn", "oclc"]
    gurl = "https://www.googleapis.com/books/v1/volumes?q="
    def get(self, title):
        #googlebooksapi
        book = Book(title = title)
        query = self.query_type[0] + ":" + book.title
        response = requests.get(self.gurl + query)
        if (response.status_code == 200):
            book_info = response.json()
            # print(book_info)
            if (book_info["totalItems"] > 0):
                book.authors = book_info["items"][0]["volumeInfo"]["authors"]
                book.isbn = book_info["items"][0]["volumeInfo"]["industryIdentifiers"][1]["identifier"]
            else:
                # ない場合 {'kind': 'books#volumes', 'totalItems': 0}
                # rakutenapi
                pass


        return book.isbn

