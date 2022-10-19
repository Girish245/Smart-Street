from .models import Category

def get_category_url(request):
    links = Category.objects.all()
    return {
        'links': links
    }