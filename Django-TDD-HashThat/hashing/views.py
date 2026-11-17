import hashlib

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from .forms import HashForm
from .models import Hash


def home(request):
    if request.method == "POST":
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            clearText = filled_form.cleaned_data["text"]
            hashText = hashlib.sha256(clearText.encode("utf-8")).hexdigest()
            # only store it if we have not seen this hash before
            if not Hash.objects.filter(hash=hashText).exists():
                Hash.objects.create(text=clearText, hash=hashText)
            return redirect("hashing:hash", hash=hashText)

    form = HashForm()
    return render(request, "home.html", {"form": form})


def hash(request, hash):
    hashobj = Hash.objects.filter(hash=hash).first()
    if hashobj is None:
        raise Http404("Hash not found")
    return render(request, "hash.html", {"hash": hashobj})


def quickhash(request):
    text = request.GET.get("text", "")
    return JsonResponse({"hash": hashlib.sha256(text.encode("utf-8")).hexdigest()})
