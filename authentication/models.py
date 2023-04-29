from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            return ValueError("Email field is required!")
        elif not username:
            return ValueError("Username field is required!")

        email = self.normalize_email(email)

        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()

    def create_superuser(self, email, username, password=None):
        if not email:
            return ValueError("Email field is required!")
        elif not username:
            return ValueError("Username field is required!")

        email = self.normalize_email(email)

        user = self.model(email=email, username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class Account(AbstractBaseUser):
    username = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-id", )

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email
    

@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)