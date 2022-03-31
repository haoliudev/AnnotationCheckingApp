from pyexpat.errors import XML_ERROR_INCOMPLETE_PE
from tokenize import triple_quoted
from django.db import models
import xml.etree.ElementTree as ET

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100, null = False, blank = False)
    def __str__(self):
        return self.name

class Image(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    img = models.ImageField()
    description = models.TextField(null=True, blank=True)
    xmin = models.IntegerField(default=None)
    xmlfile = models.FilePathField(null=True, blank=True)

    def __str__(self):
        return f"File id: {self.id}"
class Annotation(models.Model):
    name = models.CharField(max_length = 100, null = False, blank = False)
    xmlfile = models.FileField(null = False, blank = False)
    imgfile = models.ImageField(null = False, blank = False)
    def __str__(self):
        return self.name

class Xmlfile(models.Model):
    file_name = models.FileField(upload_to='xml')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"File id: {self.id}"

# class Onepiece(models.Model):
#     label = models.CharField(max_length=200)
#     imageurl = models.URLField()
#     display = models.ImageField()
#     xmin = models.IntegerField()
#     ymin = models.IntegerField()
#     xmax = models.IntegerField()
#     ymax = models.IntegerField()

class Xml_img_files(models.Model):

    xml_file_name = models.FileField(upload_to='xml')
    img_file_name = models.FileField(upload_to='source_img')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def file_link(self):
        if self.xml_file_name:
            return "<a href='%s'>download</a>" % (self.xml_file_name.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True

    def __str__(self):
        return f"File id: {self.id}"

class BulkUploadFiles(models.Model):
    file_name = models.FileField(upload_to='bulk_files')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"File id: {self.id}"

