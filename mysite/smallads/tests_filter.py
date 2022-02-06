from django.test import TestCase
from models import Smallad, SmalladFav

# Create your tests here.

smalladfav_list = list(SmalladFav.objects.all().order_by(-'smallad_id'))

for i in smalladfav_list:
    fav_number_per_smallad_id = int(i.filter('smallad_id').count())