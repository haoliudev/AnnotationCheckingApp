from unicodedata import category
from django.shortcuts import render, redirect

from images.forms import XmlModelForm, XmlImgModelForm, UpdateImgModelForm
from .models import Annotation, Category, Image, Xml_img_files, Xmlfile
import xml.etree.ElementTree as ET
from PIL import Image as PILIMAGE
from PIL import ImageDraw as PILDRAW
import requests
from django.core.files import File
from pathlib import Path
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from io import StringIO
from io import BytesIO
from .next_prev import next_in_order, prev_in_order
from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.

def gallery(request):

    category = request.GET.get('category')
    print('category:', category)

    if category == None:
        imgs = Image.objects.all()
    else:
        imgs = Image.objects.filter(category__name__contains=category)
    
    files = Xml_img_files.objects.all()
    






    categories = Category.objects.all()
    # imgs = Image.objects.all()

    context = {'categories': categories, 'imgs': imgs, 'files': files}
    return render(request, 'images/gallery.html', context)

def viewImg(request, pk):
    img = Image.objects.get(id=pk)
    Imgs = Image.objects.all()
    files = Xml_img_files.objects.all()
    categories = Category.objects.all()

    first = Image.objects.first()
    last = prev_in_order(first, loop=True)
    count = 1
    current_count = 1
    
    while(first != last):
        first = next_in_order(first)
        count += 1
    
    first = Image.objects.first()
    while(first != img):
        first = next_in_order(first)
        current_count += 1
    
    FIRST = Image.objects.first()
    LAST = prev_in_order(first, loop=True)

    next = next_in_order(img, loop=True)
    previous = prev_in_order(img, loop=True)

    if request.method == "POST" :
        for oneCategory in categories:
            if str(oneCategory.name) in request.POST:
                data = request.POST
                new_category, created = Category.objects.get_or_create(name=data[str(oneCategory.pk)])
                Image.objects.filter(pk=img.pk).update(category=new_category)
                xmlpath = img.xmlfile
                new_xmin = int(img.xmin)
                with open(xmlpath, 'r') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    totalNum = 0
                    itemNum = 0
                    for child in root:
                        print(child.tag, child.attrib)
                        totalNum += 1
                    for j in range(6,totalNum):
                        if new_xmin == int(root[j][4][0].text):
                            itemNum = j

                    root[itemNum][0].text = data[str(oneCategory.pk)]
                    tree.write(xmlpath)

        if 'textEdit' in request.POST:
                data = request.POST
            
                if data['category_new'] != '':
                    new_category, created = Category.objects.get_or_create(name=data['category_new'])
                    Image.objects.filter(pk=img.pk).update(category=new_category)
                    xmlpath = img.xmlfile
                    new_xmin = int(img.xmin)
                    with open(xmlpath, 'r') as f:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        totalNum = 0
                        itemNum = 0
                        for child in root:
                            print(child.tag, child.attrib)
                            totalNum += 1
                        for i in range(6,totalNum):
                            if new_xmin == int(root[i][4][0].text):
                                itemNum = i

                        root[itemNum][0].text = str(data['category_new'])
                        tree.write(xmlpath)


        
   
        return HttpResponseRedirect(request.path_info)
            

       
    

    context = {'img':img,'categories': categories, 'count':count, 
    'current_count':current_count, 'next':next, 'previous':previous, 'Imgs':Imgs,
    'FIRST':FIRST, 'LAST':LAST, 'files': files,}


        
    return render(request, 'images/image.html', context)




def addLabel(request):
    categories = Category.objects.all()

    if request.method == "POST" :
        data = request.POST
    
        if data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])

        
   
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'images/addlabel.html', context)

def removeAnnotation(request,pk):
    categories = Category.objects.all()
    Imgs = Image.objects.all()
    im1 = Image.objects.get(id=pk)
    next = next_in_order(im1, loop=True)

    if request.method == "POST" :
        data = request.POST
        xmlpath = im1.xmlfile
        new_xmin = int(im1.xmin)
        with open(xmlpath, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            totalNum = 0
            itemNum = 0
            for child in root:
                print(child.tag, child.attrib)
                totalNum += 1
            for i in range(6,totalNum):
                if new_xmin == int(root[i][4][0].text):
                    itemNum = i

            root.remove(root[itemNum])
            tree.write(xmlpath)
        Image.objects.filter(id=pk).delete()
        return HttpResponseRedirect(reverse('image', args=(next.id,)))
            
    return render(request, 'images/removeannotation.html')
            
        



def editlabel(request,pk):
    categories = Category.objects.all()
    Imgs = Image.objects.all()
    category = Category.objects.get(id=pk)

    if request.method == "POST" :
        data = request.POST
    
        if data['category_new'] != '':
            new_category, created = Category.objects.get_or_create(name=data['category_new'])
        

        
   
        return redirect('gallery')

    context = {'categories': categories,'category':category}
    return render(request, 'images/editlabel.html', context)


def addImg(request):
    categories = Category.objects.all()

    if request.method == "POST" :
        data = request.POST
        img = request.FILES.get('img')
        print(img.size)
    

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        
        image = Image.objects.create(
        category=category,
        description=data['description'],
        img=img,)

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'images/add.html', context)




def cropper(original_image, xmin, ymin, xmax, ymax):
      img_io = StringIO.StringIO()
      original_image = PILIMAGE.open(original_image)
      cropped_img = original_image.crop((xmin,ymin,xmax,ymax))
      cropped_img.save(img_io, format='JPEG', quality=100)
      img_content = ContentFile(img_io.getvalue(), 'img5.jpg')
      return img_content


def clearfiles(request):
        if request.method == 'POST':

            # import function to run
            Xmlfile.objects.all().delete()
            Image.objects.all().delete()
            Category.objects.all().delete()
            Xml_img_files.objects.all().delete()

            # call function
        

    # return user to required page
            return redirect('gallery')
            
        return render(request, 'images/clearfiles.html')



def addFiles(request):

    categories = Category.objects.all()

    form = XmlImgModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = XmlImgModelForm()
        obj = Xml_img_files.objects.get(activated=False)
        print(obj.xml_file_name.path,'r')
        createItems(obj.xml_file_name.path,obj.img_file_name.path)
       
                
        
        return redirect('gallery')

    
    



    return render(request, 'images/uploadfile.html', {'form': form})

def bulkUpload(request):
    if request.method == "POST" :
        data = request.POST
        img = request.FILES.get('img')
    return render(request, 'images/bulkupload.html')

def createItems(xml_file_path,img_file_path):
    with open(xml_file_path, 'r') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        itemNum = 0
        for child in root:
            itemNum += 1
        myList = []
        im = PILIMAGE.open(img_file_path, 'r').convert("RGBA")
        source_width, source_height = im.size
            
        for i in range(6,itemNum):
            left=int(root[i][4][0].text)
            top=int(root[i][4][1].text)
            right=int(root[i][4][2].text)
            bottom=int(root[i][4][3].text)
            im1 = im.crop((left, top, right, bottom))
            width1, height1 = im1.size
            newsize = (width1*8,height1*8)
            im1 = im1.resize(newsize)


            background_url = "https://cdn.wallpapersafari.com/9/57/CKwAM5.jpg"
            background = PILIMAGE.open(requests.get(background_url, stream=True).raw).convert("RGBA")
            bgsize = (source_width/2,source_height/2)
            # background = background.resize(bgsize)


            bg_w, bg_h = background.size
            bgsize = (bg_w*2,bg_h*2)
            background = background.resize(bgsize)
            bg_w, bg_h = background.size
            img_w, img_h = im1.size

            
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

            background.paste(im1,offset,im1)    
            img_io = BytesIO()
                    
            
            background.save(img_io, format='PNG', quality=100)
            img_content = ContentFile(img_io.getvalue(), 'img'+str(i)+'.png')



            
            go, created = Category.objects.get_or_create(name=root[i][0].text)
            



            newimage = Image.objects.create(
                category=go,
                description=None,
                img = img_content,
                xmin = left,
                xmlfile = xml_file_path,
                )
