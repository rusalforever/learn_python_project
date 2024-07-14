from book import Book

class Comics(Book):
    def __init__(self, title, author, illustrator, series, *args, **kwargs):
        super().__init__(title, author, *args, **kwargs)
        self.illustrator = illustrator
        self.series = series

    def __str__(self):
        return f"{self.title} by {self.author}, illustrated by {self.illustrator} (Series: {self.series})"
    