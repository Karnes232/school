from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    telephone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Courses(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="professor")
    subject = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.subject}, {self.teacher}"


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    telephone = models.CharField(max_length=10)
    courses = models.ManyToManyField(Courses, blank = True, related_name="courses")

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Grades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="course")
    t1_p1 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t1_p2 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t1_p3 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t2_p1 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t2_p2 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t2_p3 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t3_p1 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t3_p2 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    t3_p3 = models.IntegerField(
            blank=True,
            default=0,
            validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    def __str__(self):
        return f"{self.student}, {self.course}"

    @property
    def avg1(self):
        count = 0
        total = 0
        if self.t1_p1 > 0:
            count += 1
            total += self.t1_p1
        if self.t1_p2 > 0:
            count += 1
            total += self.t1_p2
        if self.t1_p3 > 0:
            count += 1
            total += self.t1_p3
        if count > 0:
            average = total / count
            avg = round(average, 1)
            return avg
        else:
            return 0

    @property
    def avg2(self):
        count = 0
        total = 0
        if self.t2_p1 > 0:
            count += 1
            total += self.t2_p1
        if self.t2_p2 > 0:
            count += 1
            total += self.t2_p2
        if self.t2_p3 > 0:
            count += 1
            total += self.t2_p3
        if count > 0:
            average = total / count
            avg = round(average, 1)
            return avg
        else:
            return 0

    @property
    def avg3(self):
        count = 0
        total = 0
        if self.t3_p1 > 0:
            count += 1
            total += self.t3_p1
        if self.t3_p2 > 0:
            count += 1
            total += self.t3_p2
        if self.t3_p3 > 0:
            count += 1
            total += self.t3_p3
        if count > 0:
            average = total / count
            avg = round(average, 1)
            return avg
        else:
            return 0

    @property
    def grand(self):
        count = 0
        total = 0
        if self.t1_p1 > 0:
            count += 1
            total += self.t1_p1
        if self.t1_p2 > 0:
            count += 1
            total += self.t1_p2
        if self.t1_p3 > 0:
            count += 1
            total += self.t1_p3
        if self.t2_p1 > 0:
            count += 1
            total += self.t2_p1
        if self.t2_p2 > 0:
            count += 1
            total += self.t2_p2
        if self.t2_p3 > 0:
            count += 1
            total += self.t2_p3
        if self.t3_p1 > 0:
            count += 1
            total += self.t3_p1
        if self.t3_p2 > 0:
            count += 1
            total += self.t3_p2
        if self.t3_p3 > 0:
            count += 1
            total += self.t3_p3       
        if count > 0:
            average = total / count
            avg = round(average, 1)
            return avg
        else:
            return 0

