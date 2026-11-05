from unittest.mock import patch
from django.db import OperationalError
from django.test import TestCase


class HealthTests(TestCase):
    def test_database_readiness(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "reachable"})

    def test_database_failure_does_not_leak_connection_details(self):
        with patch("apps.core.views.connection.cursor", side_effect=OperationalError("secret connection details")):
            response = self.client.get("/health/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})
