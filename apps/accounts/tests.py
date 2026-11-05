from django.contrib.auth.models import Group
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase
from .models import Department, User


class IdentityFoundationTests(TestCase):
    def test_seed_is_repeatable_and_grants_no_permissions(self):
        call_command("seed_base", verbosity=0)
        call_command("seed_base", verbosity=0)
        self.assertEqual(Department.objects.count(), 3)
        self.assertEqual(Group.objects.count(), 5)
        self.assertFalse(Group.objects.filter(permissions__isnull=False).exists())
        self.assertEqual(User.objects.count(), 0)

    def test_email_uniqueness_is_case_insensitive(self):
        User.objects.create_user(username="alice", email="Alice@example.com", password="Example-Password-123")
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create_user(username="bob", email="alice@example.com", password="Example-Password-123")

    def test_new_user_has_no_enterprise_privileges_and_password_is_hashed(self):
        user = User.objects.create_user(username="staff", email="staff@example.com", password="Example-Password-123")
        self.assertTrue(user.check_password("Example-Password-123"))
        self.assertNotEqual(user.password, "Example-Password-123")
        self.assertFalse(user.confirmed)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.department)
