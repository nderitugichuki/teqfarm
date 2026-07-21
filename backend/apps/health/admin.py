from django.contrib import admin
from .models import DiseaseRecord, MedicationRecord, Vaccination, VetVisit
admin.site.register((Vaccination, MedicationRecord, DiseaseRecord, VetVisit))
