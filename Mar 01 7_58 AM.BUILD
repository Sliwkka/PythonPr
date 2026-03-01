
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")
# cos napisane
# dzieki
:D
  
# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.models import Car, Reservation

# Create your views here.

def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")


# reservations/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
"""
model_db Brand 
- name
- logo (opcjonalnie)
- kraj pochodzenia (opcjonalne)
- sidziba (opcjonalne)
"""
class Brand(models.Model):
    name = models.CharField(verbose_name="nazwa marki", max_length=32)

    def __str__(self):
        return f"{self.name}"
"""
model_db Model
- name
- generacja 
- segment
- opis
- klucz obcy (Brand)
- cena/dobe
"""

class Model(models.Model):
    SEGMENT_CHOICES = {
        "A": "budget",
        "B": "basic",
        "C": "compact",
        "D": "delux",
        "E": "executive",
    }

    name = models.CharField(verbose_name="nazwa modelu", max_length=32)
    generation = models.IntegerField(verbose_name="generacja modelu")
    segment = models.CharField(verbose_name="segment modelu", choices=SEGMENT_CHOICES)
    description = models.TextField(verbose_name="opis modelu")
    brand = models.ForeignKey(Brand, related_name="models", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand.name}:{self.name}"




"""
model_db Car
- klucz obcy (Model)
- nr rejestracyjny (CharField)
- cena/dobe (DecimalField)
- opis (wraz z wyposazeniem) (TextField)
- rok produkcji (DateField)
- przebieg (    mileage = models.PositiveIntegerField(verbose_name="przebieg"))
"""
from django.utils import timezone
class Car(models.Model):
    model = models.ForeignKey(Model, related_name="cars", on_delete=models.PROTECT)
    plate_number = models.CharField(verbose_name="numer rejestracyjny", max_length=16)
    # 999,99  
    # 9999,99 <- wybrane
    # max_digits laczna liczba cyfr
    # decimal_places <- liczba cyfr po przecinku
    price_per_day = models.DecimalField(verbose_name="cena za dobe",max_digits=6, decimal_places=2)
    description = models.TextField(verbose_name="opis samochodu")
    mileage = models.PositiveIntegerField(verbose_name="przebieg")
    production_date = models.DateField(verbose_name="data produkcji")

    def __str__(self):
        return f"{self.model.brand.name}:{self.model.name}:{self.plate_number}"
    

    # stworzyc pomocnicza funkcje is_reserved
    @property
    def is_reserved(self):
        now = timezone.now()
        # set -> zbiór
        # self -> samochod
        return self.reservation_set.filter(start_date__lte=now, end_date__gte=now).exists()
    
    # jak mialoby to dzialac?
    def is_reserved_in_selected_dates(self, new_start_date, new_end_date):
        from django.db.models import Q
        # przypadek pierwszy nowa rezerwajcja po trwajacej
        #self.reservation_set.filter(w Q piszemy tak jakbysmy byli w tym miejscu)
        # lt <- less than
        assert new_start_date <= new_end_date
        case_one = Q(end_date__lt=new_start_date)
        case_two = Q(start_date__gt=new_end_date)
        # | <- lub/or
        # & <- i/and
        # ~ <- not
        is_free = case_one | case_two
        is_reserved = ~is_free
        queryset = self.reservation_set.filter(is_reserved)
        print(queryset)
        print(queryset.query)
        """
        SELECT "reservations_reservation"."id", "reservations_reservation"."car_id", "reservations_reservation"."user_id", "reservations_reservation"."start_date", "reservations_reservation"."end_date" FROM "reservations_reservation" WHERE ("reservations_reservation"."car_id" = 2 AND NOT ("reservations_reservation"."end_date" < 2026-04-02 OR "reservations_reservation"."start_date" > 2026-04-03))"""
        return queryset.exists()


    #bez property
    #car.is_reserved()
    #z property
    #car.is_reserved

"""
Stworzyc model Reservation
- ForeignKey do Car
- ForeignKey do User
- start_date (DateField)
- end_date (DateField)
"""

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="poczatek rezerwacji")
    end_date = models.DateField(verbose_name="koniec rezerwacji")

    def __str__(self):
        return f"Rezerwacja {self.car} dla {self.user.username}"
    
    # do poprawy w przypadku aktualizacji
    def save(self, *args, **kwargs):
        if self.car.is_reserved_in_selected_dates(self.start_date, self.end_date):
            raise ValueError("MODELS Car is already reserved")
        else:
            super().save(*args, **kwargs)
            
            
# reservations/templates/reservation_list.html
<a href="{% url 'car_list_view' %}">HOME</a>
{% if reservations_from_context %}
    <ul>
        {% for reservation in reservations_from_context %}
        <li>
            <p>{{ reservation.car}} {{ reservation.start_date }} {{ reservation.end_date }}</p>
        </li>
        {% endfor %}
    </ul>
{% else %}
    <p>No reservations are available</p>
{% endif %}
        
    
    
# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)


def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")



# stworzyc plik forms w folderze reservations
# reservations/forms.py
from django import forms

class CarListForm(forms.Form):
    brand = forms.CharField(max_length=32)
    segment = forms.CharField(max_length=32)
    price = forms.DecimalField(max_digits=6, decimal_places=2)


# reservations/templates/index.html
{{ form }}

{% if cars_from_context %}
    <ul>
        {% for car in cars_from_context %}
        <li>
            <a href="{% url 'car_detail_view' car.id %}"> {{ car.model.brand.name }} {{ car.model.name }}</a>
        </li>
        {% endfor %}
    </ul>
{% else %}
    <p>No cars are available</p>
{% endif %}



<a href="{% url 'reservation_list_view' %}">TWOJE REZERWACJE</a>

# reservations/urls.py
"""
URL configuration for car_reservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from reservations.views import CarListView, car_detail_view, reservation_list_view, reserve

urlpatterns = [
    path('', CarListView.as_view(), name='car_list_view'),
    path('car/<int:car_id>', car_detail_view, name='car_detail_view'),
    path('reservations/', reservation_list_view, name="reservation_list_view"),
    path('reserve/<int:car_id>', reserve, name="reserve")
]
# "" -> widok listy samochodow
# "car/<id>" -> widok szczegolowy samochodu


# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        data = request.POST
        form = CarListForm(data)
        if form.is_valid():
            print(form.cleaned_data)
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")


# reservations/templates/index.html
<form method="post" action="{% url 'car_list_view' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit">
</form>

{% if cars_from_context %}
    <ul>
        {% for car in cars_from_context %}
        <li>
            <a href="{% url 'car_detail_view' car.id %}"> {{ car.model.brand.name }} {{ car.model.name }} {{ car.price_per_day }}</a>
        </li>
        {% endfor %}
    </ul>
{% else %}
    <p>No cars are available</p>
{% endif %}



<a href="{% url 'reservation_list_view' %}">TWOJE REZERWACJE</a>

# reservations/forms.py
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator

class CarListForm(forms.Form):
    brand = forms.CharField(max_length=32, required=False)
    segment = forms.CharField(max_length=32, required=False)
    price = forms.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], required=False)
    
# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        data = request.POST
        form = CarListForm(data)
        if form.is_valid():
            price = form.cleaned_data["price"]
            qs = self.get_queryset()
            qs = qs.filter(price_per_day__lte=price)
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:CharField
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")


# reservations/views.py
    def post(self, request):
        qs = self.get_queryset()
        data = request.POST
        form = CarListForm(data)
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price:
                qs = qs.filter(price_per_day__lte=price)
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)

# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        qs = self.get_queryset()
        data = request.POST
        form = CarListForm(data)
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price is not None:
                qs = qs.filter(price_per_day__lte=price)
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")

# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        qs = self.get_queryset()
        data = request.POST
        form = CarListForm(data)
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price is not None:
                qs = qs.filter(price_per_day__lte=price)
            segment = form.cleaned_data["segment"]
            if segment:
                qs = qs.filter(model__segment=segment)
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:B
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")

# reservations/templates/index.html
<form method="post" action="{% url 'car_list_view' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit">
</form>

{% if cars_from_context %}
    <ul>
        {% for car in cars_from_context %}
        <li>
            <a href="{% url 'car_detail_view' car.id %}"> {{ car.model.brand.name }} {{ car.model.name }} {{ car.price_per_day }} {{ car.model.segment }}</a>
        </li>
        {% endfor %}
    </ul>
{% else %}
    <p>No cars are available</p>
{% endif %}



<a href="{% url 'reservation_list_view' %}">TWOJE REZERWACJE</a>

#reservations/forms.py
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator

from reservations.models import Model


CarListSegmentChoices = {
    "":"-------"
}
CarListSegmentChoices.update(Model.SEGMENT_CHOICES)
"""
{
        "":"-------",
        "A": "budget",
        "B": "basic",
        "C": "compact",
        "D": "delux",
        "E": "executive",
}
"""
class CarListForm(forms.Form):
    brand = forms.CharField(max_length=32, required=False)
    segment = forms.ChoiceField(choices=CarListSegmentChoices, required=False) # jesli mamy choices zdefiniowane w modelu
    price = forms.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))], required=False)

# reservations/templates/index.html
<form method="post" action="{% url 'car_list_view' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit">
    <input type="button" value="Clear" onclick="window.location.href='{% url 'car_list_view' %}'">
</form>


{% if cars_from_context %}
    <ul>
        {% for car in cars_from_context %}
        <li>
            <a href="{% url 'car_detail_view' car.id %}"> {{ car.model.brand.name }} {{ car.model.name }} {{ car.price_per_day }} {{ car.model.segment }}</a>
        </li>
        {% endfor %}
    </ul>
{% else %}
    <p>No cars are available</p>
{% endif %}



<a href="{% url 'reservation_list_view' %}">TWOJE REZERWACJE</a>
    

# reservations/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
"""
model_db Brand 
- name
- logo (opcjonalnie)
- kraj pochodzenia (opcjonalne)
- sidziba (opcjonalne)
"""
class Brand(models.Model):
    name = models.CharField(verbose_name="nazwa marki", max_length=32, unique=True)

    def __str__(self):
        return f"{self.name}"
"""
model_db Model
- name
- generacja 
- segment
- opis
- klucz obcy (Brand)
- cena/dobe
"""

class Model(models.Model):
    SEGMENT_CHOICES = {
        "A": "budget",
        "B": "basic",
        "C": "compact",
        "D": "delux",
        "E": "executive",
    }

    name = models.CharField(verbose_name="nazwa modelu", max_length=32)
    generation = models.IntegerField(verbose_name="generacja modelu")
    segment = models.CharField(verbose_name="segment modelu", choices=SEGMENT_CHOICES)
    description = models.TextField(verbose_name="opis modelu")
    brand = models.ForeignKey(Brand, related_name="models", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand.name}:{self.name}"




"""
model_db Car
- klucz obcy (Model)
- nr rejestracyjny (CharField)
- cena/dobe (DecimalField)
- opis (wraz z wyposazeniem) (TextField)
- rok produkcji (DateField)
- przebieg (    mileage = models.PositiveIntegerField(verbose_name="przebieg"))
"""
from django.utils import timezone
class Car(models.Model):
    model = models.ForeignKey(Model, related_name="cars", on_delete=models.PROTECT)
    plate_number = models.CharField(verbose_name="numer rejestracyjny", max_length=16)
    # 999,99  
    # 9999,99 <- wybrane
    # max_digits laczna liczba cyfr
    # decimal_places <- liczba cyfr po przecinku
    price_per_day = models.DecimalField(verbose_name="cena za dobe",max_digits=6, decimal_places=2)
    description = models.TextField(verbose_name="opis samochodu")
    mileage = models.PositiveIntegerField(verbose_name="przebieg")
    production_date = models.DateField(verbose_name="data produkcji")

    def __str__(self):
        return f"{self.model.brand.name}:{self.model.name}:{self.plate_number}"
    

    # stworzyc pomocnicza funkcje is_reserved
    @property
    def is_reserved(self):
        now = timezone.now()
        # set -> zbiór
        # self -> samochod
        return self.reservation_set.filter(start_date__lte=now, end_date__gte=now).exists()
    
    # jak mialoby to dzialac?
    def is_reserved_in_selected_dates(self, new_start_date, new_end_date):
        from django.db.models import Q
        # przypadek pierwszy nowa rezerwajcja po trwajacej
        #self.reservation_set.filter(w Q piszemy tak jakbysmy byli w tym miejscu)
        # lt <- less than
        assert new_start_date <= new_end_date
        case_one = Q(end_date__lt=new_start_date)
        case_two = Q(start_date__gt=new_end_date)
        # | <- lub/or
        # & <- i/and
        # ~ <- not
        is_free = case_one | case_two
        is_reserved = ~is_free
        queryset = self.reservation_set.filter(is_reserved)
        print(queryset)
        print(queryset.query)
        """
        SELECT "reservations_reservation"."id", "reservations_reservation"."car_id", "reservations_reservation"."user_id", "reservations_reservation"."start_date", "reservations_reservation"."end_date" FROM "reservations_reservation" WHERE ("reservations_reservation"."car_id" = 2 AND NOT ("reservations_reservation"."end_date" < 2026-04-02 OR "reservations_reservation"."start_date" > 2026-04-03))"""
        return queryset.exists()


    #bez property
    #car.is_reserved()
    #z property
    #car.is_reserved

"""
Stworzyc model Reservation
- ForeignKey do Car
- ForeignKey do User
- start_date (DateField)
- end_date (DateField)
"""

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="poczatek rezerwacji")
    end_date = models.DateField(verbose_name="koniec rezerwacji")

    def __str__(self):
        return f"Rezerwacja {self.car} dla {self.user.username}"
    
    # do poprawy w przypadku aktualizacji
    def save(self, *args, **kwargs):
        if self.car.is_reserved_in_selected_dates(self.start_date, self.end_date):
            raise ValueError("MODELS Car is already reserved")
        else:
            super().save(*args, **kwargs)
        
    

  ### przyklad comprahension
jakas_lista = []
for k in range(5):
    jakas_lista.append(k)

print(jakas_lista)

# [ wartosc for wartosc in dane]
inna_lista = [str(k) for k in range(5)]
print(inna_lista)

jakis_slownik = {}
for k in range(5):
    jakis_slownik[k]=k
print(jakis_slownik)

inny_slownik = {k:str(k) for k in range(5)}
print(inny_slownik)


# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Brand, Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        brands = list(Brand.objects.all().values_list("name", flat=True))
        brands_choices = {name: name for name in brands}
        form.fields["brand"].choices = brands_choices
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        qs = self.get_queryset()
        data = request.POST
        form = CarListForm(data)
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price is not None:
                qs = qs.filter(price_per_day__lte=price)
            segment = form.cleaned_data["segment"]
            if segment:
                qs = qs.filter(model__segment=segment)
            brand = form.cleaned_data["brand"]
            if brand:
                qs = qs.filter(model__brand__name=brand)
        # form["brand"].choices = 
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")
    
    
# reservation/forms.py
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator

from reservations.models import Model


CarListSegmentChoices = {
    "":"-------"
}
CarListSegmentChoices.update(Model.SEGMENT_CHOICES)
"""
{
        "":"-------",
        "A": "budget",
        "B": "basic",
        "C": "compact",
        "D": "delux",
        "E": "executive",
}
"""
class CarListForm(forms.Form):
    brand = forms.ChoiceField(required=False)
    segment = forms.ChoiceField(choices=CarListSegmentChoices, required=False) # jesli mamy choices zdefiniowane w modelu
    price = forms.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))], required=False)
    

# reservations/views.py   
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Brand, Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        brands = list(Brand.objects.all().values_list("name", flat=True))
        choices = {"":"-------"}
        brands_choices = {name: name for name in brands}
        choices.update(brands_choices)
        form.fields["brand"].choices = choices
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        qs = self.get_queryset()
        data = request.POST
        form = CarListForm(data)
        brands = list(Brand.objects.all().values_list("name", flat=True))
        choices = {"":"-------"}
        brands_choices = {name: name for name in brands}
        choices.update(brands_choices)
        form.fields["brand"].choices = choices
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price is not None:
                qs = qs.filter(price_per_day__lte=price)
            segment = form.cleaned_data["segment"]
            if segment:
                qs = qs.filter(model__segment=segment)
            brand = form.cleaned_data["brand"]
            if brand:
                qs = qs.filter(model__brand__name=brand)
        # form["brand"].choices = 
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")

#reservation/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Brand, Car, Reservation
from django.views.generic.list import ListView

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        brands = list(Brand.objects.all().values_list("name", flat=True))
        choices = {"":"-------"}
        brands_choices = {name: name for name in brands}
        choices.update(brands_choices)
        form.fields["brand"].choices = choices
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        qs = self.get_queryset()
        data = request.POST
        form = CarListForm(data)
        brands = list(Brand.objects.all().values_list("name", flat=True))
        choices = {"":"-------"}
        brands_choices = {name: name for name in brands}
        choices.update(brands_choices)
        form.fields["brand"].choices = choices
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price is not None:
                qs = qs.filter(price_per_day__lte=price)
            segment = form.cleaned_data["segment"]
            if segment:
                qs = qs.filter(model__segment=segment)
            brand = form.cleaned_data["brand"]
            if brand:
                qs = qs.filter(model__brand__name=brand)
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            print(start_date, end_date)
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")

#reservations/forms.py
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator

from reservations.models import Model


CarListSegmentChoices = {
    "":"-------"
}
CarListSegmentChoices.update(Model.SEGMENT_CHOICES)
"""
{
        "":"-------",
        "A": "budget",
        "B": "basic",
        "C": "compact",
        "D": "delux",
        "E": "executive",
}
"""
class CarListForm(forms.Form):
    brand = forms.ChoiceField(required=False)
    segment = forms.ChoiceField(choices=CarListSegmentChoices, required=False) # jesli mamy choices zdefiniowane w modelu
    price = forms.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))], required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    
  
# reservation/forms.py
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator

from reservations.models import Model


CarListSegmentChoices = {
    "":"-------"
}
CarListSegmentChoices.update(Model.SEGMENT_CHOICES)
"""
{
        "":"-------",
        "A": "budget",
        "B": "basic",
        "C": "compact",
        "D": "delux",
        "E": "executive",
}
"""
class CarListForm(forms.Form):
    brand = forms.ChoiceField(required=False)
    segment = forms.ChoiceField(choices=CarListSegmentChoices, required=False) # jesli mamy choices zdefiniowane w modelu
    price = forms.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))], required=False)
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    
    
    
    
# reservations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reservations.forms import CarListForm
from reservations.models import Brand, Car, Reservation
from django.views.generic.list import ListView
from django.db.models import Exists, OuterRef

# Create your views here.
class CarListView(ListView):
    model = Car
    context_object_name = "cars_from_context"
    template_name = "index.html"

    def get(self, request):
        form = CarListForm()
        brands = list(Brand.objects.all().values_list("name", flat=True))
        choices = {"":"-------"}
        brands_choices = {name: name for name in brands}
        choices.update(brands_choices)
        form.fields["brand"].choices = choices
        # self.get_queryset -> self.model.objects.all()
        context = {"cars_from_context": self.get_queryset(), "form": form}
        print(context)
        return render(request, self.template_name, context)
    
    def post(self, request):
        qs = self.get_queryset()
        data = request.POST
        form = CarListForm(data)
        brands = list(Brand.objects.all().values_list("name", flat=True))
        choices = {"":"-------"}
        brands_choices = {name: name for name in brands}
        choices.update(brands_choices)
        form.fields["brand"].choices = choices
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price is not None:
                qs = qs.filter(price_per_day__lte=price)
            segment = form.cleaned_data["segment"]
            if segment:
                qs = qs.filter(model__segment=segment)
            brand = form.cleaned_data["brand"]
            if brand:
                qs = qs.filter(model__brand__name=brand)
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            print(start_date, end_date)
            print(qs)
            if start_date is not None and end_date is not None:
                print("filtr dat")
                qs = qs.annotate(
                    has_reservations=Exists(
                        Reservation.objects.filter(
                        car=OuterRef('pk'), start_date__lte=end_date, end_date__gte=start_date)
                            )
                    ).filter(has_reservations=False)
                print(qs.query)
                """
                SELECT "reservations_car"."id", "reservations_car"."model_id", "reservations_car"."plate_number", "reservations_car"."price_per_day", "reservations_car"."description", "reservations_car"."mileage", "reservations_car"."production_date", EXISTS(SELECT 1 AS "a" FROM "reservations_reservation" U0 WHERE (U0."car_id" = ("reservations_car"."id") AND U0."end_date" >= 2026-03-08 AND U0."start_date" <= 2026-03-16) LIMIT 1) AS "has_reservations" FROM "reservations_car" WHERE NOT EXISTS(SELECT 1 AS "a" FROM "reservations_reservation" U0 WHERE (U0."car_id" = ("reservations_car"."id") AND U0."end_date" >= 2026-03-08 AND U0."start_date" <= 2026-03-16) LIMIT 1)
                """
        context = {"cars_from_context": qs, "form": form}
        return render(request, self.template_name, context)



def car_list_view(request):
    cars = Car.objects.all()
    context = {"cars_from_context": cars}
    return render(request, "index.html", context)


# #ListView
# def index(request):
#     questions = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"questions_from_context": questions}
#     return render(request, "index.html", context)

def car_detail_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "car_detail.html", {"car": car})

# def detail(request, question_id):
#     # shortcut, ktory pozwala nam szybciej upewnic sie ze obiekt istnieje
#     # jesli uzytkownik odpyta sie po nieistniejacy element to funkcja zwroci nam kod 404
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})

def reservation_list_view(request):
    user = request.user
    if user.is_authenticated:
        reservations = Reservation.objects.filter(user=user)
        context = {"reservations_from_context": reservations}
        return render(request, "reservation_list.html", context)
    else:
        return HttpResponse("USER IS NOT AUTHENTICATED", status=403)
    

def reserve(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.POST:
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        if not car.is_reserved_in_selected_dates(start_date, end_date):
            user = request.user
            # if user.is_authenticated
            Reservation.objects.create(car=car, user=user, start_date=start_date, end_date=end_date)
        else:
            raise ValueError("VIEW CAR IS RESERVED")
        return redirect("reservation_list_view")
    else:
        return HttpResponse(f"Rezerwujesz samochod {car_id}")
        
        
    




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # METODY HTTP
#     # GET - to pobieranie informacji
#     # POST - to wysylanie informacji
#     # PUT 
#     # DELETE
#     if request.POST:
#         try:
#             choice_id = request.POST["choice"]
#             # choice = get_object_or_404(Choice, pk=choice_id)
#             # znaszego pytania, z jego zbioru odpowiedzi, wez odpowiedz o kluczu glownym rownym choice_id
#             selected_choice = question.choice_set.get(pk=choice_id)
#         #Choice.DoesNotExist pojawi sie kiedy albo: 
#         # a) odpowiedz o podanym id w ogole nie istnieje
#         # b) odpowiedz nie jest do danego pytania
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, "detail.html", {"question": question, "error_message": "Nie wybrałeś odpowiedzi"})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)
        
#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")
    
    
    
    
    
    
    

