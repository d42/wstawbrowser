# Create your views here.
from django.shortcuts import render

from wstaw.utils import Wstaw, last_image, list_split


per_page = 12

def index(request):
    return page(request, page=0)


def page(request, page):
    page = int(page)
    images  = list_split(
      [Wstaw.get(x + (page*per_page)) for x in range(per_page)],
      4
    )
    return render(request, 
            "wstaw/dupa.html",
            {
                "images":images,
                "page":page
            }
            )
    pass

