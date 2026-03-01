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
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return redirect("results", question_id=question.id)

#     else:
#         return HttpResponse(f"Odpowiadasz na pytanie: {question_id}")
