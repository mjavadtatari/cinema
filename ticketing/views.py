from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from accounts.models import Profile
from ticketing.forms import ShowTimeSearchForm
from ticketing.models import Movie, Cinema, ShowTime, Ticket


def movie_list(request):
    movies = Movie.objects.all()
    movie = Movie.objects.all().count()
    cinema = Cinema.objects.all().count()
    show = ShowTime.objects.filter(status=2).count()
    user = request.user.is_authenticated
    context = {
        'movie_list': movies,
        'movie': movie,
        'cinema': cinema,
        'show': show,
        'user': user,
    }

    return render(request, 'ticketing/movie_list.html', context)


def cinema_list(request):
    cinemas = Cinema.objects.all()
    movie = Movie.objects.all().count()
    cinema = Cinema.objects.all().count()
    show = ShowTime.objects.filter(status=2).count()
    user = request.user.is_authenticated
    context = {
        'cinema_list': cinemas,
        'movie': movie,
        'cinema': cinema,
        'show': show,
        'user': user,
    }

    return render(request, 'ticketing/cinema_list.html', context)


def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    available_shows = ShowTime.objects.filter(movie=movie).order_by('status')
    user = request.user.is_authenticated
    context = {
        'movie': movie,
        'available_shows': available_shows,
        'user': user,
    }
    return render(request, 'ticketing/movie_details.html', context)


def cinema_details(request, cinema_id):
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    available_shows = ShowTime.objects.filter(cinema=cinema).order_by('status')
    user = request.user.is_authenticated
    context = {
        'cinema': cinema,
        'available_shows': available_shows,
        'user': user,
    }
    return render(request, 'ticketing/cinema_details.html', context)


def showtime_list(request):
    # Search Form -----------------------------------------------
    search_form = ShowTimeSearchForm(request.GET)
    showtime = ShowTime.objects.all()
    if search_form.is_valid():
        showtime = showtime.filter(movie__name__contains=search_form.cleaned_data['movie_name'])
        if search_form.cleaned_data['sale_is_open']:
            showtime = showtime.filter(status=ShowTime.SALE_OPEN)
        if search_form.cleaned_data['movie_length_min'] is not None:
            showtime = showtime.filter(movie__length__gte=search_form.cleaned_data['movie_length_min'])
        if search_form.cleaned_data['movie_length_max'] is not None:
            showtime = showtime.filter(movie__length__lte=search_form.cleaned_data['movie_length_max'])
        if search_form.cleaned_data['cinema'] is not None:
            showtime = showtime.filter(cinema=search_form.cleaned_data['cinema'])

        min_price, max_price = search_form.get_price_boundaries()
        if min_price is not None:
            showtime = showtime.filter(price__gte=min_price)
        if max_price is not None:
            showtime = showtime.filter(price__lte=max_price)
    showtime = showtime.order_by('status')
    # End of Search Form -----------------------------------------------
    movie = Movie.objects.all().count()
    cinema = Cinema.objects.all().count()
    show = ShowTime.objects.filter(status=2).count()
    user = request.user.is_authenticated
    context = {
        'showtime': showtime,
        'movie': movie,
        'cinema': cinema,
        'show': show,
        'user': user,
        'search_form': search_form,
    }
    return render(request, 'ticketing/showtime_list.html', context)


@login_required
def showtime_details(request, showtime_id):
    showtime = ShowTime.objects.get(pk=showtime_id)
    profile = request.user.profile
    # Generate Options for DropDown Menu -----------------------------------------------
    salable_list = []
    salable = 10
    if showtime.free_seats < 10:
        salable = showtime.free_seats
    for i in range(1, salable + 1):
        salable_list.append(i)
    # End of Generate Options for DropDown Menu -----------------------------------------------
    context = {
        'showtime': showtime,
        'profile': profile,
        'salable_list': salable_list,
    }
    # Buying Tickets -----------------------------------------------
    if request.method == 'POST':
        try:
            seat_count = int(request.POST['seat_count'])
            assert showtime.status == ShowTime.SALE_OPEN, 'فروش برای این سانس غیرفعال است'
            assert showtime.free_seats >= seat_count, 'به اندازه کافی صندلی خالی وجود ندارد'
            total_price = showtime.price * seat_count
            assert request.user.profile.spend(total_price), 'موجودی  کافی نیست'
            showtime.reserve_seats(seat_count=seat_count)
            ticket = Ticket.objects.create(showtime=showtime, customer=request.user.profile, seat_counter=seat_count)
        except Exception as e:
            context['error'] = str(e)
        else:
            return HttpResponseRedirect(reverse('ticketing:ticket_details', kwargs={'ticket_id': ticket.id}))
    # End of Buying Tickets -----------------------------------------------
    return render(request, 'ticketing/showtime_details.html', context)


def home_page(request):
    movie = Movie.objects.all().count()
    cinema = Cinema.objects.all().count()
    show = ShowTime.objects.filter(status=2).count()
    user = request.user.is_authenticated
    context = {
        'movie': movie,
        'cinema': cinema,
        'show': show,
        'user': user,
    }
    return render(request, 'ticketing/index.html', context)


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(customer=request.user.profile).order_by('-order_time')
    context = {
        'tickets': tickets,
    }
    return render(request, 'ticketing/ticket_list.html', context)


@login_required
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    context = {
        'ticket': ticket,
    }
    return render(request, 'ticketing/ticket_details.html', context)
