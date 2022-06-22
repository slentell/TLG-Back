from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from auth_app.models import UserAccount

# Create your models here.
class Team(models.Model):
   
    # Choice Lists
    GENDER_CHOICES = [
        ("M", "Boy's"),
        ("F", "Girl's")
    ] 

    team_name = models.CharField(max_length=255)
    coach = models.ForeignKey('auth_app.UserAccount', on_delete=models.CASCADE)
    primary_color = models.CharField(max_length=255)
    secondary_color = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    

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
            range(0, 101) : '101',
            range(102, 110) : '110',
            range(111, 119) : '119',
            range(120, 129) : '129',
            range(130, 139) : '139',
            range(140, 154) : '154',
            range(155, 169) : '169',
            range(170, 183) : '183',
            range(184, 199) : '199',
            range(200, 1400) : 'Unlimited',
        }
        
        return weight_class

    athlete = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    grade = models.CharField(max_length=9, choices=GRADE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1400)])
    dob = models.DateField(max_length=8)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teammates')
    weightclass = models.CharField(max_length=255, default=return_weightclass(gender, weight)) 

# Future DB for Lift DB for building/logging workout
# class Lifts:
#     pass

class LiftHistory(models.Model):
    athlete = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    lift = models.CharField(max_length=255)
    weight = models.IntegerField()
    date_of_lift = models.DateField()

class MaxLift(models.Model):
    athlete = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    max_lift = models.ForeignKey(LiftHistory, on_delete=models.CASCADE)

class Posts(models.Model):
    
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_pictures', blank=True, null=True)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
