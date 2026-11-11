from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req


# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if not username or len(password) < 3:
            return render(request, "signup.html", {"form": SignUpForm, "message": "Username and password (at least 3 characters) are required."})
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"form": SignUpForm, "message": "user already exist"})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "signup.html", {"form": SignUpForm})


def index(request):
    return render(request, "index.html")


def songs(request):
    songs = [{"id": 1, "title": "duis faucibus accumsan odio curabitur convallis", "lyrics": "Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."}]
    return render(request, "songs.html", {"songs": songs})


def photos(request):
    photos = [{"id": 1, "pic_url": "https://dummyimage.com/136x100.png/5fa2dd/ffffff", "event_country": "United States", "event_state": "District of Columbia", "event_city": "Washington", "event_date": "11/16/2022"}]
    return render(request, "photos.html", {"photos": photos})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return HttpResponseRedirect(reverse("index"))
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def concerts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    rows = []
    for concert in Concert.objects.all():
        attendee = concert.attendee.filter(user=request.user).first()
        rows.append({"concert": concert, "status": attendee.attending if attendee else "-"})
    return render(request, "concerts.html", {"concerts": rows})


def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {"concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices})
    else:
        return HttpResponseRedirect(reverse("login"))
    pass


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
