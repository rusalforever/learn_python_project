from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

class LibraryItemModel(BaseModel, ABC):
    """
    Pydantic model for the Book class
    """

    title: str = Field(..., min_length=1, description='The title of the book')
    author: str = Field(..., min_length=1, description='The author of the book')
    year: int = Field(..., description='The year of the book')

    @abstractmethod
    def get_publication_info(self) -> str:
        """
        Abstract method to return publication-specific information
        Must be implemented in subclasses
        """
        return f"'Was published in {self.year}"

    def __str__(self) -> str:
        """
        Returns a string representation of the book
        """
        return f"'{self.title}' by {self.author}, {self.year}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the book. Good for printing and
        debugging purposes
        """
        return f"BookModel(title='{self.title}', author='{self.author}', year={self.year}')"

class MagazineModel(LibraryItemModel):
    issue: int = Field(..., gt=0, description='Issue number of the magazine')
    month: str = Field(..., description='Month of publication')
    type: str = Field(..., description='Type of the magazine')

    def get_publication_info(self) -> str:
        return f"Issue {self.issue}, published in {self.month} {self.year}"

    def __str__(self):
        return f"'{self.title}' by {self.author}, {self.year} - Issue {self.issue}, {self.month}"

class BookModel(LibraryItemModel):
    type: str = Field(..., description='Type of the book')

    def get_publication_info(self) -> str:
        return f"Book {self.issue}, published in {self.month} {self.year}"

    def __str__(self):
        return f"'{self.title}' by {self.author}, {self.year}"

