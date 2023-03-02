from . import models


def main_categories(request):
    categories = models.Category.objects.filter(type='M')
    return {'main_categories': categories}

