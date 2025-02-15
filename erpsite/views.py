from django.shortcuts import render
from django.http import Http404

def custom_page_not_found_view(request, exception):
    return render(request,'404.html',status=404)

def test_404(request):
    raise Http404('Page Not found!')
