from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm, BookForm, SignUpForm
from .models import Book, Category, CustomUser
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'auth/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '新規登録に成功しました。')
            return redirect('search_app:search_book_list')
        return render(request, 'auth/signup.html', {'form': form})


class LoginView(AuthLoginView):
    template_name = 'auth/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'ログインに成功しました。')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'ログインに失敗しました。名前またはパスワードが間違っています。')
        return super().form_invalid(form)


@login_required
def book_create(request):
  if request.method == 'POST':
    form = BookForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('search_app:search_book_list')
    else:
      return render(request, 'book/book_form.html', {'form': form})
  else:
      form = BookForm()
      return render(request, 'book/book_form.html', {'form': form})


@login_required
def book_detail(request, pk):
  book = get_object_or_404(Book, pk=pk)
  return render(request, 'book/book_detail.html', {'book': book})


@login_required
def book_update(request, pk):
  book = get_object_or_404(Book, pk=pk)
  if request.method == 'POST':
    form = BookForm(request.POST, instance=book)
    if form.is_valid():
      form.save()
      return redirect('search_app:book_detail', pk=book.pk)
    else:
      return render(request, 'book/book_form.html', {'form': form, 'book': book})

  else:
      form = BookForm(instance=book)
      return render(request, 'book/book_form.html', {'form': form, 'book': book})


@login_required
def book_delete(request, pk):
  book = get_object_or_404(Book, pk=pk)
  if request.method == 'POST':
    book.delete()
    return redirect('search_app:search_book_list')
  return render(request, 'book/book_confirm_delete.html', {'book': book})


@login_required
def search_book_list_view(request):
    form = SearchForm(request.GET or None)
    results = Book.objects.all()

    # 検索条件
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query)
            )

    # カテゴリフィルタリング
    category_id = request.GET.get('category')
    if category_id and category_id != 'placeholder':
        try:
            category = Category.objects.get(id=category_id)
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = Book.objects.none()

    # 並び替え処理
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'title':
        results = results.order_by('title')
    elif sort_by == 'publication_date':
        results = results.order_by('-publication_date')

    # ページネーション
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj
    }

    return render(request, 'book/search_book_list.html', context)