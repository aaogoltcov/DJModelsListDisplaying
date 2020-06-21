from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse

from books.models import Book


def index(request):
    return redirect(reverse(books_view))


def get_sorted_list_of_books(object): # получение данныз из БД
    book_list = object.objects.all().values('name', 'author', 'pub_date')
    return sorted(book_list, key=lambda k: k['pub_date'])


def books_view(request): # просмотр всего каталога
    template = 'books/books_list.html'
    context = {
        'book_list': get_sorted_list_of_books(Book),
    }
    return render(request, template, context)


def get_date(date): # string to date
    try:
        return datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        try:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()
        except ValueError:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
    except TypeError:
        return ''


def get_list_of_books(request, pub_date=None): # просмотр книг по дате, а также ссылки на предыдующую и следующие даты
    template_name = 'books/book.html'
    current_page = str()
    next_page = str()
    prev_page = str()
    set_of_dates = sorted(list(set(list['pub_date'] for list in get_sorted_list_of_books(Book) if list)))
    for i, item in enumerate(set_of_dates):
        if get_date(pub_date) == item:
            current_page = get_date(pub_date)
            if i == 0:
                prev_page = ''
                next_page = set_of_dates[i + 1]
                break
            elif i == len(set_of_dates) - 1:
                prev_page = set_of_dates[i - 1]
                next_page = ''
                break
            else:
                prev_page = set_of_dates[i - 1]
                next_page = set_of_dates[i + 1]
                break
    context = {
        'book_list': (list for list in get_sorted_list_of_books(Book)
                      if (pub_date == '' or list['pub_date'] == get_date(pub_date))), # список книг за конкретную дату
        'date': get_date(pub_date),
        'current_page': current_page,
        'next_page': next_page,
        'prev_page': prev_page,
    }
    return render(request, template_name, context)