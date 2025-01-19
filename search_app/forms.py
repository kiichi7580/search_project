from django import forms
from .models import Book

class SearchForm(forms.Form):
  query = forms.CharField(
    label='検索キーワード',
    max_length=100,
    required=False,
    widget=forms.TextInput(attrs={'placeholder': 'キーワードを入力'})
  )


class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = ['title', 'author', 'publisher', 'publication_date', 'description', 'category', 'isbn']
    labels = {
            'title': '書籍名',
            'author': '著者',
            'publisher': '出版社',
            'publication_date': '出版日',
            'description': '概要',
            'category': 'カテゴリー',
            'isbn': 'ISBNコード',
        }
    widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'タイトルを入力'}),
            'author': forms.TextInput(attrs={'placeholder': '著者を入力'}),
            'publisher': forms.TextInput(attrs={'placeholder': '出版社を入力'}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': '書籍の概要を入力'}),
            'category': forms.Select(attrs={'class': 'custom-select'}),
            'isbn': forms.TextInput(attrs={'placeholder': '13桁のISBNコードを入力'})
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) != 13:
            raise forms.ValidationError('ISBNは13桁である必要があります。')
        return isbn