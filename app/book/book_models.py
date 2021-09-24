class Book(object): 
    '''Book model'''
    def __init__(self) -> None:
        self.isbn = None
        self.title = None
        self.subtitle = None
        self.author = None
        self.published = None
        self.publisher = None
        self.pages = None
        self.description = None
        self.website = None