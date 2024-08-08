from pydantic import BaseModel


class BookModel(BaseModel):
    title: str
    author: str
    year: int


class Book:
    def __init__(self, model: BookModel):
        self._model = model

    @property
    def title(self) -> str:
        return self._model.title

    @property
    def author(self) -> str:
        return self._model.author

    @property
    def year(self) -> int:
        return self._model.year

    def get_ribbon(self) -> str:
        return f"{self.title} by {self.author}, published in {self.year}"

    def __str__(self):
        return f"Book(title={self.title}, author={self.author}, year={self.year})"


class Magazine(Book):
    def __init__(self, model: BookModel):
        super().__init__(model)

    def get_ribbon(self) -> str:
        return f"The {self.title} magazine by {self.author}, published in {self.year}"