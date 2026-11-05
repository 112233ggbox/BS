from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.accounts.models import Department


class Command(BaseCommand):
    help = "Idempotently create base departments and role labels; grants no permissions."

    @transaction.atomic
    def handle(self, *args, **options):
        for name in ("研发部", "市场部", "财务部"):
            Department.objects.get_or_create(name=name)
        for name in ("普通员工", "部门负责人", "财务审批人", "企业负责人", "系统管理员"):
            Group.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Base departments and role labels initialized."))
