from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Books with Dummies
    num_dummies_books = Book.objects.filter(title__icontains='dummies').count()

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_dummies_books': num_dummies_books,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksLibrarianListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to users."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
