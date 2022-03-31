from django.contrib import admin

# Register your models here.

from .models import Category, Image, Xml_img_files, Xmlfile

admin.site.register(Category)

admin.site.register(Image)

admin.site.register(Xmlfile)

admin.site.register(Xml_img_files)