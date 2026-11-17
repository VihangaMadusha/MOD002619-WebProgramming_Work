from datetime import datetime, timezone

from django.test import TestCase
from django.urls import reverse

from .filters import StudentFilter
from .models import Module, Student


def make_student(first="alice", last="smith", age=20, modules=()):
    s = Student.objects.create(firstName=first, lastName=last, age=age,
                               email=f"{first}@example.com",
                               enrolmentDate=datetime(2025, 9, 1, tzinfo=timezone.utc))
    for m in modules:
        s.modules.add(m)
    return s


class ModelTests(TestCase):
    def test_str_methods(self):
        m = Module.objects.create(code="mod1", name="web programming")
        s = make_student()
        self.assertEqual(str(s), "Alice, SMITH")
        self.assertEqual(str(m), "MOD1 Web Programming")

    def test_many_to_many(self):
        m = Module.objects.create(code="MOD1", name="Web")
        s = make_student(modules=[m])
        self.assertEqual(s.modules.count(), 1)
        self.assertEqual(m.student_set.count(), 1)


class ViewTests(TestCase):
    def setUp(self):
        self.mod = Module.objects.create(code="MOD002619", name="Web Programming")
        self.s1 = make_student("alice", "smith", 18, [self.mod])
        self.s2 = make_student("bob", "jones", 30)

    def test_home(self):
        self.assertEqual(self.client.get(reverse("myApp:home")).status_code, 200)

    def test_student_detail(self):
        r = self.client.get(reverse("myApp:student_detail", args=[self.s1.id]))
        self.assertContains(r, "SMITH")
        self.assertContains(r, "Web Programming")

    def test_student_detail_404(self):
        self.assertEqual(self.client.get(reverse("myApp:student_detail", args=[9999])).status_code, 404)

    def test_list_pagination(self):
        for i in range(45):
            make_student(f"s{i}", f"z{i}")
        r = self.client.get(reverse("myApp:studentlist", args=[1]))
        self.assertEqual(len(r.context["page_obj"]), 20)
        r = self.client.get(reverse("myApp:studentlist", args=[3]))
        self.assertEqual(r.context["page_obj"].number, 3)

    def test_list_filter_and_query_string_kept(self):
        r = self.client.get(reverse("myApp:studentlist", args=[1]), {"firstName__icontains": "ali"})
        self.assertEqual(r.context["page_obj"].paginator.count, 1)
        self.assertIn("firstName__icontains=ali", r.context["query_string"])

    def test_list_no_records(self):
        r = self.client.get(reverse("myApp:studentlist", args=[1]), {"firstName__icontains": "zzzz"})
        self.assertContains(r, "No Records Returned.")

    def test_module_list(self):
        r = self.client.get(reverse("myApp:modulelist"))
        self.assertContains(r, "MOD002619")

    def test_edit_get_and_post(self):
        url = reverse("myApp:student_edit", args=[self.s1.id])
        self.assertEqual(self.client.get(url).status_code, 200)
        r = self.client.post(url, {
            "firstName": "Alicia", "lastName": "Smith", "age": 21, "email": "a@example.com",
            "enrolmentDate": "2025-09-01T10:00", "modules": [self.mod.id],
        })
        self.assertRedirects(r, reverse("myApp:student_detail", args=[self.s1.id]))
        self.s1.refresh_from_db()
        self.assertEqual(self.s1.firstName, "Alicia")
        self.assertEqual(Student.objects.count(), 2)   # updated, not duplicated


class FilterTests(TestCase):
    def test_age_filters(self):
        make_student("a", "a", 18)
        make_student("b", "b", 40)
        qs = Student.objects.all()
        self.assertEqual(StudentFilter({"age__gt": 30}, queryset=qs).qs.count(), 1)
        self.assertEqual(StudentFilter({"age__lt": 30}, queryset=qs).qs.count(), 1)
