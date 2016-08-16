import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

#from django.conf import settings
#settings.configure(DEBUG=True)

from cms.models import Category, Page

def populate():

#    python_cat = add_cat('Python')

#    add_page (cat=python_cat, title="Official Python Tutorial", url="http://docs.python.org/2/tutorial/")
#    add_page (cat=python_cat, title="How to Think like a Computer Scientist", url="http://www.greenteapress.com/thinkpython/")
#    add_page (cat=python_cat, title="Learn Python in 10 Minutes", url="http://korokithakis.net/tutorials/python/")

#    django_cat = add_cat ("Django")

#    add_page (cat=django_cat, title="Official Django Tutorial",
#             url="http://docs.djangoproject.com/en/1.5/intro/tutorial01/")
#    add_page (cat=django_cat, title="Django Rocks",
#             url="http://www.djangorocks.com/")
#    add_page (cat=django_cat, title="How to Tango with Django", url="http://www.tangowithdjango.com/")

#    frame_cat = add_cat ("Other Frameworks")

#    add_page (cat=frame_cat, title="Bottle", url="http://bottlepy.org/docs/dev/")
#    add_page (cat=frame_cat, title="Flask", url="http://flask.pocoo.org")

#    add_viewlikeCat('Python', 128, 64)
#    add_viewlikeCat('Django', 64, 32)
#    add_viewlikeCat('Other Frameworks', 32, 16)

    add_viewsPage('Official Python Tutorial', 868)
    add_viewsPage('How to Think like a Computer Scientist', 774)
    add_viewsPage('Learn Python in 10 Minutes', 697)
    add_viewsPage('Official Django Tutorial', 538)
    add_viewsPage('Django Rocks', 471)
    add_viewsPage('How to Tango with Django', 320)
    add_viewsPage('Bottle', 218)
    add_viewsPage('Flask', 164)

    # Print out what we have added to the user.

#    for c in Category.objects.all():
#        for p in Page.objects.filter(category=c):
#            print ("- {0} - {1}".format(str(c), str(p)))

#    for vl in Category.objects.all():
#        print(vl.name, vl.views, vl.likes)

    for v in Page.objects.all():
        print(v.title, v.views)


#def add_page(cat, title, url, views=0):
#    p = Page.objects.get_or_create(category=cat, title=title)[0]
#    p.url = url
#    p.views = views
#    p.save()
#    return p

#def add_cat(name):
#    c = Category.objects.get_or_create(name=name)[0]
#    return c

#def add_viewlikeCat(name, views, likes):
#    vl = Category.objects.get(name=name)
#    vl.views=views
#    vl.likes=likes
#    vl.save()
#    return vl

def add_viewsPage(title, views):
    v = Page.objects.get(title=title)
    v.views=views
    v.save()
    return v

# Start execution here!
if __name__ == '__main__':
    print ("Starting Rango population script ...")
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    #from rango.models import Category, Page
    populate()