from django.test import SimpleTestCase


class CITest(SimpleTestCase):
    def test_ci_pipeline(self):
        self.assertEqual(1 + 1, 2)
