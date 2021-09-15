from products.models import Category
from products.models import Product

def categories(request):
    parent_cat = Category.objects.filter(cat_parent=None)
    men = Product.objects.filter(product_cat__cat_parent__cat_name='Men')
    women = Product.objects.filter(product_cat__cat_parent__cat_name='Women')
    
    return {'parent_cat':parent_cat,'men':men,'women':women}