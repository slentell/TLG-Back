from django.conf import Settings, settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from auth_app.models import UserAccount

# Create your models here.
class Team(models.Model):
   
    # Choice Lists
    GENDER_CHOICES = [
        ("Boys", "Boys"),
        ("Girls", "Girls")
    ] 

    team_name = models.CharField(max_length=255)
    coach = models.ForeignKey('auth_app.UserAccount', on_delete=models.CASCADE)
    primary_color = models.CharField(max_length=255)
    secondary_color = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)

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
    def return_weightclass(gender, weight_input):
        weight_class = None
        print('checking weight')
        print(weight_input)

    
        # put this in an if based on gender

        # weight_classes = {
        #     range(0, 101) : '101',
        #     range(102, 110) : '110',
        #     range(111, 119) : '119',
        #     range(120, 129) : '129',
        #     range(130, 139) : '139',
        #     range(140, 154) : '154',
        #     range(155, 169) : '169',
        #     range(170, 183) : '183',
        #     range(184, 199) : '199',
        #     range(200, 1400) : 'Unlimited',
        # }
        # for k, v in weight_classes.items():
        #     print(k, v)
        #     if weight in k:
        #         print('me here')
        #         weight_class = v
        
        # return weight_class
        
        if int(weight_input) < 102:
            weight_class = '101'
        elif int(weight_input) < 111:
            weight_class = '110'
        elif int(weight_input) < 120:
            weight_class = '119'
        elif int(weight_input) < 130:
            weight_class = '129'
        elif int(weight_input) < 140:
            weight_class = '139'
        elif int(weight_input) < 155:
            weight_class = '154'
        elif int(weight_input) < 170:
            weight_class = '169'
        elif int(weight_input) < 184:
            weight_class = '183'
        elif int(weight_input) < 200:
            weight_class = '199'
        else:
            weight_class = 'unlimited'
        
        return weight_class

    athlete = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    grade = models.CharField(max_length=9, choices=GRADE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1400)])
    dob = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teammates', null=True)
    weightclass = models.CharField(max_length=255) 
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)

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

class ImageGallery(models.Model):
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_gallery')

class Calendar(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
    title = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    color = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
