from dataclasses import field
from django import forms
from django.forms import ModelForm
from .models import Image, Xml_img_files, Xmlfile

class XmlModelForm(forms.ModelForm):
    class Meta:
        model = Xmlfile
        fields = ('file_name',)

class XmlImgModelForm(forms.ModelForm):
    class Meta:
        model = Xml_img_files
        fields = ('xml_file_name','img_file_name')
        help_texts = {
        'field_name': '<span class="my-class">Some useful help text.</span>',
    }

class UpdateImgModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('category',)