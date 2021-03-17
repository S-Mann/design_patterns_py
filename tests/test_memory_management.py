from unittest import TestCase
from design_patterns.memory_management.initialize_cleanup import Counter


class TestMemoryManagement(TestCase):

    def setUp(self, *args, **kwargs):
        self.x = Counter("first")

    def test_bro(self, *args, **kwargs):
        self.assertIsNotNone(self.x)
