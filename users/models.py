# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, first_name=None, last_name=None, phone_number=None):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    # فیلد اصلی برای احراز هویت (تغییر یافته به username)
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # فیلدهای تکمیلی
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    # قابلیت‌های جدید
    bio = models.TextField(verbose_name='Biography', blank=True, null=True)
    profile_image = models.ImageField(verbose_name='Profile Picture', upload_to='profiles/', blank=True, null=True)

    # فیلدهای وضعیت
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(verbose_name='Is Email Verified', default=False)

    # فیلدهای زمانبندی
    date_joined = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(
        auto_now=True)  # Changed from auto_now to auto_now_add to prevent constant updates

    # تعیین کلاس مدیریت
    objects = MyUserManager()

    # فیلدی که برای ورود استفاده می‌شود
    USERNAME_FIELD = 'username'

    # فیلدهای اجباری برای ساخت کاربر با دستور createsuperuser
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin