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
    price_per_day = models.DecimalField(verbose_name="cena za dobe", max_digits=6, decimal_places=2)
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
        # self.reservation_set.filter(w Q piszemy tak jakbysmy byli w tym miejscu)
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
        SELECT "reservations_reservation"."id",
               "reservations_reservation"."car_id",
               "reservations_reservation"."user_id",
               "reservations_reservation"."start_date",
               "reservations_reservation"."end_date"
        FROM "reservations_reservation"
        WHERE ("reservations_reservation"."car_id" = 2 AND
               NOT ("reservations_reservation"."end_date" < 2026 - 04 - 02 OR
                    "reservations_reservation"."start_date" > 2026 - 04 - 03))"""
        return queryset.exists()

    # bez property
    # car.is_reserved()
    # z property
    # car.is_reserved


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