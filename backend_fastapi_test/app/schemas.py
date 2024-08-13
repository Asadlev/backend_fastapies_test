from pydantic import BaseModel, constr, validator


class ArticleBase(BaseModel):
    title: constr(min_length=3, max_length=100)
    content: str

    @validator('title', 'content')
    def validate_no_special_chars(cls, v):
        if not v.isalpha():
            raise ValueError('Only alphabetic characters are allowed')
        return v


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    username: constr(min_length=1, pattern='^[a-zA-Z]+$')


class AuthorCreate(AuthorBase):
    password: str


class Author(AuthorBase):
    articles: list[Article] = []

    class Config:
        orm_mode = True
