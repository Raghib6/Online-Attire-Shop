from products.models import Category
from products.models import Product

def categories(request):
    parent_cat = Category.objects.filter(cat_parent=None)
    
    return {'parent_cat':parent_cat}