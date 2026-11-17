from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .filters import StudentFilter
from .forms import StudentEditForm
from .models import Module, Student


def home(request):
    """Hero page (Week 05)."""
    return render(request, "home.html")


def student_detail(request, student_id):
    """Week 04 - details for a single student."""
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise Http404(f"Student {student_id} not found!")
    return render(request, "student_detail.html", {"student": student})


def studentlist(request, page):
    """Weeks 05/06 - paginated, filterable list of students."""
    students = Student.objects.all().order_by("lastName", "firstName")
    filter = StudentFilter(request.GET, queryset=students)

    paginator = Paginator(filter.qs, 20)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )

    # keep the filter arguments when the user moves between pages
    query_string = urlencode(request.GET.copy())

    context = {"filter": filter, "page_obj": page_obj, "query_string": query_string}
    return render(request, "studentlist.html", context)


def modulelist(request):
    """Week 05 - list of modules with number of students enrolled."""
    modules = Module.objects.all().order_by("code")
    return render(request, "modulelist.html", {"modules": modules})


def student_edit(request, student_id):
    """Week 06 - edit a student using a ModelForm."""
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        # request.FILES is needed for the image upload, instance= makes it an UPDATE not an INSERT
        studentForm = StudentEditForm(request.POST, request.FILES, instance=student)
        if studentForm.is_valid():
            studentForm.save()
            return redirect("myApp:student_detail", student_id=student_id)
    else:
        studentForm = StudentEditForm(instance=student)
    context = {"studentForm": studentForm, "student_id": student_id}
    return render(request, "student_edit.html", context)
