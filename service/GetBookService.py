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
            if isbn is not None and "ISBN" in isbn[0]["type"]:
                isbn = isbn[0]["identifier"]
            else:
                continue
            title = self.book_info["items"][i]["volumeInfo"].get("title")
            image_link = self.book_info["items"][i]["volumeInfo"].get("imageLinks").get("thumbnail", "")
            try:
                self.books.append(Book(title = title, isbn = isbn, image_link = image_link))
            except ValidationError as e:
                print(f"[ERROR]{e}")

    def get(self, title):
        #googlebooksapi
        # [{isbn: sss, title:sss,imagelink:sss},{},{}]
        self.books = []
        query = self.query_type[0] + ":" + title
        try:
            response = requests.get(self.gurl + query)
            if response.status_code == 200:
                self.book_info = response.json()
                book_length = self.book_info["totalItems"]
                if book_length >= 3:
                    self.put(3)
                elif book_length > 0:
                    self.put(book_length)
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(f"[ERROR]{e}")

        finally:
            pass
        return self.books

