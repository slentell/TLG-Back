from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from auth_app.models import UserAccount

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255)
    coach = models.ForeignKey('auth_app.UserAccount', on_delete=models.CASCADE)
    primary_color = models.CharField(max_length=255)
    secondary_color = models.CharField(max_length=255)

class Athlete(models.Model):
    # Choice Lists
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ] 

    GRADE_CHOICES = [
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior')
    ]

    # weightclass function 
    def return_weightclass(gender, weight):
        weight_class = None

        # put this in an if based on gender
        weight_classes = {
            range(0, 100) : 'Small'
        }

        return weight_class

    grade = models.CharField(max_length=9, choices=GRADE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1400)])
    dob = models.DateField(max_length=8)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teammates')
    weightclass = models.CharField(max_length=255, default=return_weightclass(gender, weight)) 


class Posts:
    pass

class Lifts:
    pass

class LiftHistory:
    pass

class MaxLift:
    pass
