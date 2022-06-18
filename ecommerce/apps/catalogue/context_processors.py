from . import models


def categories(request):
    return {"categories": models.Category.objects.filter(level=0)}
