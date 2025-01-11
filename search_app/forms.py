from django import forms
from .models import Book

class SearchForm(forms.Form):
  query = forms.CharField(
    label='検索キーワード',
    max_length=100,
    required=False,
    widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})
  )


class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = ['title', 'author', 'publisher', 'publication_date', 'description', 'category', 'isbn'] 