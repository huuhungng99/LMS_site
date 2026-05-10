from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/StudentProfilePic')  
    address = models.CharField(max_length=100)  
    mobile_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Format number: '+999999999'.")
    mobile = models.CharField(max_length=20, validators=[mobile_validator])  
    enrollment_number = models.CharField(max_length=30, unique=True)  
    date_of_birth = models.DateField() 
    age = models.PositiveIntegerField()  
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_id(self):
        return self.user.id

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=200)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)  # 'A', 'B', 'C', hoặc 'D'

    def __str__(self):
        return self.question_text

class Subject(models.Model):
    name = models.CharField(max_length=100)  # Tên môn học
    grade_level = models.CharField(max_length=50)  # Khối lớp
    description = models.TextField()  # Mô tả môn học
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)  # Ảnh mô tả

    def __str__(self):
        return self.name


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, related_name='lessons', on_delete=models.CASCADE)  # Liên kết với môn học
    lesson_number = models.PositiveIntegerField()  # Số thứ tự bài học
    description = models.TextField()  # Mô tả bài học
    youtube_link = models.URLField(blank=True, null=True)  # Link video YouTube

    class Meta:
        ordering = ['lesson_number']  # Sắp xếp theo số thứ tự bài học

    def __str__(self):
        return f"{self.subject.name} - Lesson {self.lesson_number}"


class Material(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='materials', on_delete=models.CASCADE)  # Liên kết với bài học
    description = models.TextField()  # Mô tả tài liệu
    file = models.FileField(upload_to='materials/')  # Tệp tài liệu

    def __str__(self):
        return f"Documentation {self.lesson.subject.name} - Lesson {self.lesson.lesson_number}"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0)  # Thêm trường score

    def __str__(self):
        return f"Result {self.quiz}"