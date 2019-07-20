from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."

        if len(postData['last_name']) < 2:
            errors['description'] = "Last name must be at least 2 characters."

        if len(postData['email']) < 3:
            errors['email'] = "Email must follow appropriate format."
        
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."

        if postData['password_confirm'] != postData['password']:
            errors['password_confirm'] = "Passwords do not match."

        return errors

class User(models.Model):
    alpha_only = RegexValidator(r'^[A-Za-z]*$')


    first_name = models.CharField(max_length=55, validators=[alpha_only])
    last_name = models.CharField(max_length=55, validators=[alpha_only])
    email = models.EmailField(max_length=55)
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name = "messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name="comments")
    user = models.ForeignKey(User, related_name = "comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def str_comment(self):
    #     return f'{self.comment}'