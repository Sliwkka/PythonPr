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
        choices = {"": "-------"}
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
        choices = {"": "-------"}
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
                SELECT "reservations_car"."id",
                       "reservations_car"."model_id",
                       "reservations_car"."plate_number",
                       "reservations_car"."price_per_day",
                       "reservations_car"."description",
                       "reservations_car"."mileage",
                       "reservations_car"."production_date",
                       EXISTS(SELECT 1 AS "a"
                              FROM "reservations_reservation" U0
                              WHERE (U0."car_id" = ("reservations_car"."id") AND U0."end_date" >= 2026 - 03 - 08 AND
                                     U0."start_date" <= 2026 - 03 - 16) LIMIT 1) AS "has_reservations"
                FROM "reservations_car"
                WHERE NOT EXISTS(SELECT 1 AS "a"
                                 FROM "reservations_reservation" U0
                                 WHERE (U0."car_id" = ("reservations_car"."id") AND U0."end_date" >= 2026 - 03 - 08 AND
                                        U0."start_date" <= 2026 - 03 - 16) LIMIT 1)
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