from django.contrib import admin

from healthcareapp.models import *
# Register your models here.

admin.site.register(contact_model)
admin.site.register(register_model)
admin.site.register(drug_model)
admin.site.register(supplement_model)
admin.site.register(BodyPart)
admin.site.register(Symptom)
admin.site.register(Disease)
admin.site.register(Blogs)
admin.site.register(Pill)