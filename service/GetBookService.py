import requests_async as requests
from domain.Book import Book 

class GetBookService:
    """
    Input : title / (author / isbn)
    Output : isbn
    """
    query_type = ["intitle", "inauthor", "inpublisher", "subject", "isbn", "lccn", "oclc"]
    gurl = "https://www.googleapis.com/books/v1/volumes?q="
    async def get(self, title):
        #googlebooksapi
        book = Book(title = title)
        query = query_type[0] + ":" + book.title
        response = await requests.get(gurl + query)
        if (response.status_code == 200):
            book_info = response.getjson()
            book.authors = book_info["authors"]
            book.isbn = book_info["industryIdentifiers"][1]["identifier"]
        print(book)

        return book.isbn

        #rakutenapi
