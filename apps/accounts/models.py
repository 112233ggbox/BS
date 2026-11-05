from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class Department(models.Model):
    name = models.CharField("部门名称", max_length=80, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField("邮箱", unique=True)
    full_name = models.CharField("姓名", max_length=80)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.PROTECT)
    confirmed = models.BooleanField("管理员已确认", default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="accounts_email_ci_unique"),
            models.UniqueConstraint(Lower("username"), name="accounts_username_ci_unique"),
        ]
