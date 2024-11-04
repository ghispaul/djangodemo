from shop.models import Category


def menu(request):
    c=Category.objects.all()
    return {'links':c}