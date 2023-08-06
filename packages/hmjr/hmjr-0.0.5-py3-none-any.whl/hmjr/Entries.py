from python_graphql_client import GraphqlClient
import numpy as np

def splitIntoWords(str, badChars):
    return np.array(str.translate(str.maketrans( '', '', badChars)).split(" "))

def validateBook(book):
    strBook = str(book)
    while len(strBook) < 3:
        strBook = "0" + strBook
    return strBook

BAD_CHARS = "\""
DEFAULT_MAX = 50

class Entries:
    def __init__(self):
       self.client = GraphqlClient(endpoint="https://hmjrapi-prod.herokuapp.com/")

    # Sort the current entries with the given key function.
    # This mutates the order of stored entries.
    def sorted(self, key):
        try:
            self.results = sorted(self.results, key=key)
            return self
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of the result entry dictionaries.
    def entries(self):
        try:
            return np.array(self.results);
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of the result header strings.
    def headers(self):
        try:
            return np.array([i["header"] for i in self.results])
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of the result content strings.
    def content(self):
        try:
            return np.array([i["content"] for i in self.results])
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of the result date dictionaries.
    def dates(self):
        try:
            return np.array([d for i in self.results for d in i["dates"]])
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of the result index dictionaries.
    def indexes(self):
        try:
            return np.array([d for i in self.results for d in i["indexes"]])
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of all the words in all headers. Repetitions are allowed.
    def headerWords(self, badChars=BAD_CHARS):
        try:
            return splitIntoWords(' '.join(self.headers()), badChars)
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of all the words in all headers. Repetitions are allowed.
    def contentWords(self, badChars=BAD_CHARS):
        try:
            return splitIntoWords(' '.join(self.content()), badChars)
        except:
            print("No results found. Try running a query first.")

    # Return a numpy array of all the words in each entry. Equivalent to headerWords + contentWords
    def words(self, badChars=BAD_CHARS):
        try:
            return np.concatenate((self.headerWords(badChars),self.contentWords(badChars)))
        except:
            print("No results found. Try running a query first.")

    def associate(self, words):
        indexes = self.indexes()
        if indexes.any():
            containedStrs = [s["content"] for s in indexes for word in words if s["content"] is not None if word in s["content"]]
            words = [word for s in containedStrs for word in s.split(" ") ]
            return {word:words.count(word) for word in words}

    # Make a raw GQL query to the hmjrapi backend.
    def query(self, query, variables, name):
        try:
            self.results = self.client.execute(query=query,variables=variables)["data"][name]
        except:
            print("Query resulted in error: ")

    # Query entries with no criteria.
    def all(self, offset=0, max=DEFAULT_MAX):
        query = """
            query ($max: Float!, $offset: Float!) {
                entries(max: $max, offset: $offset) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max,"offset": offset}
        self.query(query, variables, "entries")
        return self;

    # Query entries that surround a specific date.
    def withDate(self, date, max=DEFAULT_MAX):
        query = """
            query ($max: Float!, $date: DateInput!) {
                entriesByDate(max: $max, date: $date) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max,"date": date}
        self.query(query, variables, "entriesByDate")
        return self;

    # Query entries that contain a specific keyword in their header/content.
    def withKeyword(self, keyword, max=DEFAULT_MAX):
        query = """
            query ($max: Float!, $keyword: [String!]!) {
                entriesByKeyword(max: $max, keyword: $keyword) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max,"keyword": keyword}
        self.query(query, variables, "entriesByKeyword")
        return self


    # Query entries with a specific volume of the diaries.
    def withBook(self, book, max=DEFAULT_MAX):
        query = """
            query ($max: Float!, $book: [String!]!) {
                entriesByBook(max: $max, book: $book) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        pag
                        content
                    }
                }
            }
        """
        variables = {"max": max,"book": [validateBook(x) for x in book]}
        self.query(query, variables, "entriesByBook")
        return self

    def withBookBetween(self, minBook, maxBook, max=DEFAULT_MAX):
        return self.withBook([x for x in range(minBook, maxBook, 1)], max)



