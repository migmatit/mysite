from django.urls import path
#die in diesem Ordener befindliche Datei wird importiert
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('eingang', views.eingang, name='eingang'),
	path('vokabeltest', views.vokabeltest, name='vokabeltest'),
	path('sudoku', views.sudoku, name='sudoku'),
]