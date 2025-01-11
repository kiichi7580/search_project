from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import SearchForm, BookForm
from .models import Book, Category
from .utils import get_cover_image_url
from django.db.models import Q

def book_create(request):
  if request.method == 'POST':
    form = BookForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('search_book_list')
    else:
      return render(request, 'book_form.html', {'form': form})
  else:
      form = BookForm()
      return render(request, 'book_form.html', {'form': form})


def book_detail(request, pk):
  book = get_object_or_404(Book, pk=pk)
  return render(request, 'book_detail.html', {'book': book})


def book_update(request, pk):
  book = get_object_or_404(Book, pk=pk)
  if request.method == 'POST':
    form = BookForm(request.POST, instance=book)
    if form.is_valid():
      form.save()
      return redirect('book_detail', pk=book.pk)
    else:
      return render(request, 'book_form.html', {'form': form, 'book': book})

  else:
      form = BookForm(instance=book)
      return render(request, 'book_form.html', {'form': form, 'book': book})


def book_delete(request, pk):
  book = get_object_or_404(Book, pk=pk)
  if request.method == 'POST':
    book.delete()
    return redirect('search_book_list')
  return render(request, 'book_confirm_delete.html', {'book': book})


def search_book_list(request):
  form = SearchForm(request.GET or None)
  results = Book.objects.all()
  if form.is_valid():
    query = form.cleaned_data['query']
    print(f"query: {query}")

    if query:
      results = results.filter(Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query))
      print(f"results: {results}")
  # カテゴリフィルタリング
  category_id = request.GET.get('category')
  print(f"category_id: {category_id}")
  if category_id == 'placeholder':
    pass
  elif category_id:
    try:
      category = Category.objects.get(id=category_id)
      print(f"category: {category}")
      results = results.filter(category_id=category.id)
      print(f"results: {results}")
    except Category.DoesNotExist:
      results = results.none()
      category = None

  # 並び替え処理
  sort_by = request.GET.get('sort', 'name')
  print(f"sort_by: {sort_by}")
  if sort_by == 'title':
    results = results.order_by('title')
  elif sort_by == 'publication_date':
    results = results.order_by('-publication_date')

  # クエリセットをリストに変換せず、直接Paginatorに渡す
  paginator = Paginator(results, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'search_book_list.html', {'form': form, 'page_obj': page_obj, 'results': results})
