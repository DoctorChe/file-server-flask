import unittest

from pathlib import Path

from services.web.project.utils import get_file_name, get_full_path


class UtilsTests(unittest.TestCase):
    def test_get_file_name(self):
        file_name = get_file_name(b"hello world")
        self.assertTrue(file_name == "5eb63bbbe01eeed093cb22bb8f5acdc3")

    def test_get_full_path(self):
        upload_folder = "store"
        file_name = "5eb63bbbe01eeed093cb22bb8f5acdc3"
        full_path = get_full_path(upload_folder, file_name)
        self.assertTrue(full_path == Path("/store/5e/5eb63bbbe01eeed093cb22bb8f5acdc3"))
