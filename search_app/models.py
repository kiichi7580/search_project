from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import get_cover_image_url

class CustomUser(AbstractUser):
  email = models.EmailField('メールアドレス', unique=True)


class Category(models.Model):
  name = models.CharField(max_length=255, unique=True)


  def __str__(self):
    return self.name
  
  @staticmethod
  def create_default_categories():
    default_categories = [
      'IT・テクノロジー', '金融', '製造', '小売', 'サービス', '医療', '建設', 'エネルギー', '農業', 'その他'
    ]
    for category_name in default_categories:
      Category.objects.get_or_create(name=category_name)


class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100)
  publisher = models.CharField(max_length=100)
  publication_date = models.DateField()
  description = models.TextField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
  isbn = models.CharField(max_length=13, unique=True)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)


  def __str__(self):
    return self.title

  # def cover_url(self):
  #   ISBNからOpen Libraryの画像URLを生成する
  #   return f"https://covers.openlibrary.org/b/isbn/{self.isbn}-M.jpg"

  def cover_url(self):
    cover_url = get_cover_image_url(self.isbn)
    return cover_url
    

