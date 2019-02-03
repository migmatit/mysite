import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()
from django.db.models import Max

from marcador.models import Vokabel

vokabeln = Vokabel.objects.filter(kapitel=4)
print(vokabeln)
input()