from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager) :
    def create_user(self, student_id, password=None, **extra_fields) :
        if not student_id :
            raise ValueError('The student ID must be set')
        user = self.models(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, student_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(student_id, password, **extra_fields)
    
def validate_student_id(value) :
    if len(value) != 10 or not value.isdigit() :
        raise ValidationError('Student ID must be exactly 10 digits.')

class CustomUser(AbstractBaseUser, PermissionsMixin) :
    student_id = models.CharField(
        max_length=10, 
        unique=True, 
        validators=[validate_student_id]  # 10자리 숫자 검증
    )
    nickname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # 가입 날짜 혹시몰라서 넣어둠

    objects = CustomUserManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.student_id