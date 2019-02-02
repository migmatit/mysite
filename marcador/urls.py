from django.urls import path
#die in diesem Ordener befindliche Datei wird importiert
from . import views

urlpatterns = [
	#in view-Datei ist die Funktion 'hallo', sie bekommt
	# den namen hallo
	path('eingang', views.eingang, name='eingang'),
	path('vokabeltest', views.vokabeltest, name='vokabeltest')
]