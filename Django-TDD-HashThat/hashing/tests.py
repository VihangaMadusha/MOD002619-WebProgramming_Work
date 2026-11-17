import hashlib
import os
import shutil
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse

from .forms import HashForm
from .models import Hash

HELLO = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

# --- Selenium is optional: the functional tests are skipped if Chrome/Selenium are not installed ---
CHROME = os.environ.get("CHROME_BIN") or shutil.which("google-chrome") or shutil.which("chromium")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    HAVE_SELENIUM = True
except ImportError:  # pragma: no cover
    HAVE_SELENIUM = False


# ===================================================================== Functional tests (Selenium)
@unittest.skipUnless(HAVE_SELENIUM and CHROME, "Selenium and Chrome are required for functional tests")
class HomePageTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.binary_location = CHROME
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        cls.browser = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_home_page_exists(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Enter text here:", self.browser.page_source)

    def test_hash_hello(self):
        self.browser.get(self.live_server_url)
        text = self.browser.find_element(By.ID, "id_text")
        text.send_keys("hello")
        self.browser.find_element(By.NAME, "submit").click()
        self.assertIn(HELLO, self.browser.page_source)

    def test_hash_hello_ajax(self):
        self.browser.get(self.live_server_url)
        text = self.browser.find_element(By.ID, "id_text")
        text.send_keys("hello")
        # explicit wait is better than time.sleep(10): it returns as soon as the condition is met
        WebDriverWait(self.browser, 10).until(lambda driver: HELLO in driver.page_source)
        self.assertIn(HELLO, self.browser.page_source)


# ===================================================================== Unit tests
class UnitTests(TestCase):

    def storeHashOfHello(self):
        hashobj = Hash()
        hashobj.text = "hello"
        hashobj.hash = HELLO
        hashobj.save()
        return hashobj

    def test_hash_form(self):
        form = HashForm(data={"text": "hello"})
        self.assertTrue(form.is_valid())

    def test_blank_form_invalid(self):
        self.assertFalse(HashForm(data={"text": ""}).is_valid())

    def test_hash_function_works(self):
        text_hash = hashlib.sha256("hello".encode("utf-8")).hexdigest()
        self.assertEqual(HELLO, text_hash)

    def test_hash_object(self):
        hashobj = self.storeHashOfHello()
        hashpulled = Hash.objects.get(hash=HELLO)
        self.assertEqual(hashpulled.text, hashobj.text)


# ===================================================================== View tests (no browser needed)
class ViewTests(TestCase):

    def test_home_contains_label(self):
        r = self.client.get(reverse("hashing:home"))
        self.assertContains(r, "Enter text here:")

    def test_post_redirects_and_saves(self):
        r = self.client.post(reverse("hashing:home"), {"text": "hello"})
        self.assertRedirects(r, reverse("hashing:hash", args=[HELLO]))
        self.assertEqual(Hash.objects.get(hash=HELLO).text, "hello")

    def test_post_same_text_twice_stored_once(self):
        self.client.post(reverse("hashing:home"), {"text": "hello"})
        self.client.post(reverse("hashing:home"), {"text": "hello"})
        self.assertEqual(Hash.objects.count(), 1)

    def test_hash_page_shows_hash(self):
        Hash.objects.create(text="hello", hash=HELLO)
        r = self.client.get(reverse("hashing:hash", args=[HELLO]))
        self.assertContains(r, HELLO)

    def test_unknown_hash_404(self):
        self.assertEqual(self.client.get(reverse("hashing:hash", args=["nope"])).status_code, 404)

    def test_quickhash_json(self):
        r = self.client.get(reverse("hashing:quickhash"), {"text": "hello"})
        self.assertEqual(r.json(), {"hash": HELLO})
