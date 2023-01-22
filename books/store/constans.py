from django.db.models import TextChoices

class RatingChoises(TextChoices):
    AWFUL = 1
    BAD = 2
    OK = 3
    GOOD = 4
    PERFECT = 5

