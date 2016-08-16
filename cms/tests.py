from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from cms.models import Category, Artist, Identification, Production, Location, Usage, Description, Item, Entry
from cms.views import edit_item, edit_artist, edit_category, add_item, add_artist, add_category, delete_item, delete_artist, delete_category
from django.test.client import Client
from django.views.decorators.csrf import csrf_exempt
#from django_webtest import WebTest


class IndexTests(TestCase):
    def test_index(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    #def test_index_contains_title(self):
        # Check if there is the title 'Collection Management System'
        #resp = self.client.get(reverse('index'))
        #self.assertIn(b'Collection Management System', resp.content)

    def test_index_using_template(self):
        # Check the template used to render index page
        resp = self.client.get(reverse('index'))
        self.assertTemplateUsed(resp, 'cms/index.html')

    def test_index_displays_picture(self):
        # Check if is there an image called 'unsplash1.jpg' on the index page
        resp = self.client.get(reverse('index'))
        self.assertIn(b'img src="/static/unsplash1.jpg', resp.content)

    #def test_index_has_title(self):
        # Check to make sure that the title tag has been used
        # And that the template contains the HTML from Chapter 4
        #response = self.client.get(reverse('index'))
        #self.assertIn(b'<title>', response.content)
        #self.assertIn(b'</title>', response.content)


class CollectionTests(TestCase):
    def setUp(self):
        cat = Category.objects.get_or_create(name="cat1")[0]
        art = Artist.objects.get_or_create(name="art1")[0]
        item1 = Item.objects.get_or_create(item_id='item1')[0]
        item1.identification = Identification.objects.create(category=cat, title="title1", edition="edition1", series="series1", stock=1)
        item1.production = Production.objects.create(artist=art, production_year='1900', place='place1', technique='technique1')
        item1.location = Location.objects.create(location='location1', location_date='1900-01-01')
        item1.usage = Usage.objects.create(status='DP')
        item1.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition1', subject='subject1', note='note1')
        item1.save()
        entry1 = Entry.objects.get_or_create(item=item1, entry_id='entry1')[0]
        entry1.save()

        item2 = Item.objects.get_or_create(item_id='item2')[0]
        item2.identification = Identification.objects.create(category=cat, title="title2", edition="edition2", series="series2", stock=1)
        item2.production = Production.objects.create(artist=art, production_year='1900', place='place2', technique='technique2')
        item2.location = Location.objects.create(location='location2', location_date='1900-01-01')
        item2.usage = Usage.objects.create(status='EX')
        item2.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition2', subject='subject2', note='note2')
        item2.save()
        entry2 = Entry.objects.get_or_create(item=item2, entry_id='entry2')[0]
        entry2.save()

        item3 = Item.objects.get_or_create(item_id='item3')[0]
        item3.identification = Identification.objects.create(category=cat, title="title3", edition="edition3", series="series3", stock=1)
        item3.production = Production.objects.create(artist=art, production_year='1900', place='place3', technique='technique3')
        item3.location = Location.objects.create(location='location3', location_date='1900-01-01')
        item3.usage = Usage.objects.create(status='DP')
        item3.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition3', subject='subject3', note='note')
        item3.save()
        entry3 = Entry.objects.get_or_create(item=item3, entry_id='entry3')[0]
        entry3.save()

    def test_collection(self):
        resp = self.client.get('/cms/collection/')
        self.assertEqual(resp.status_code, 200)

    def test_collection_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4
        resp = self.client.get(reverse('collection'))
        self.assertTemplateUsed(resp, 'cms/collection.html')

    def test_collection_contains_category_list(self):
        # Check if in the collection page is there - and contains the category list
        cat1 = Category.objects.create(name="cat1")
        resp = self.client.get(reverse('collection'))
        self.assertTrue('categories' in resp.context)
        self.assertEqual(cat1.name, 'cat1')

    def test_collection_contains_artist_list(self):
        # Check if in the collection page is there - and contains the category list
        art1 = Artist.objects.create(name="art1", born='1900', died='2000', artist_description="art1_description")
        resp = self.client.get(reverse('collection'))
        self.assertTrue('artists' in resp.context)
        self.assertEqual(art1.name, 'art1')
        self.assertEqual(art1.born, '1900')
        self.assertEqual(art1.died, '2000')
        self.assertEqual(art1.artist_description, 'art1_description')

    def test_collection_search(self):
        self.setUp()
        item1 = Item.objects.get(item_id="item1")
        item2 = Item.objects.get(item_id="item2")
        item3 = Item.objects.get(item_id="item3")
        c = Client()
        resp = c.get('/cms/collection/', {'keywords': 'item', 'general': 'general'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['paged_items'][0].item_id, 'item1')
        self.assertEqual(resp.context['paged_items'][1].item_id, 'item3')
        self.failUnlessEqual(len(resp.context['paged_items']), 2)

    def test_show_item(self):
        self.setUp()
        item1 = Item.objects.get(item_id="item1")
        c = Client()
        resp = c.get('/cms/item/item1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['item'].item_id, 'item1')


class ShowCategoryTests(TestCase):
    def test_show_category(self):
        cat1 = Category.objects.create(name="cat1")
        resp = self.client.get('/cms/category/cat1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['category'].name, 'cat1')

    def test_show_category_item(self):
        self.setUp()
        item1 = Item.objects.get(item_id="item1")
        item2 = Item.objects.get(item_id="item2")
        item3 = Item.objects.get(item_id="item3")
        c = Client()
        resp = c.get('/cms/category/cat1/')
        self.assertEqual(resp.context['paged_items'][0].item_id, 'item1')
        self.assertEqual(resp.context['paged_items'][1].item_id, 'item3')
        self.failUnlessEqual(len(resp.context['paged_items']), 2)


class ShowArtistTests(TestCase):
    def test_show_artist(self):
        art1 = Artist.objects.create(name="art1", born=1900, died=2000, artist_description="art1_description")
        resp = self.client.get('/cms/artist/art1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['artist'].name, 'art1')

    def test_show_artist_item(self):
        self.setUp()
        item1 = Item.objects.get(item_id="item1")
        item2 = Item.objects.get(item_id="item2")
        item3 = Item.objects.get(item_id="item3")
        c = Client()
        resp = c.get('/cms/artist/art1/')
        self.assertEqual(resp.context['paged_items'][0].item_id, 'item1')
        self.assertEqual(resp.context['paged_items'][1].item_id, 'item3')
        self.failUnlessEqual(len(resp.context['paged_items']), 2)


class EditTests(TestCase):
    def setUp(self):
        cat = Category.objects.get_or_create(name="cat1")[0]
        art = Artist.objects.get_or_create(name="art1")[0]
        item1 = Item.objects.get_or_create(item_id='item1')[0]
        item1.identification = Identification.objects.create(category=cat, title="title1", edition="edition1",
                                                             series="series1", stock=1)
        item1.production = Production.objects.create(artist=art, production_year='1900', place='place1',
                                                     technique='technique1')
        item1.location = Location.objects.create(location='location1', location_date='1900-01-01')
        item1.usage = Usage.objects.create(status='DP')
        item1.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition1',
                                                       subject='subject1', note='note1')
        item1.save()
        entry1 = Entry.objects.get_or_create(item=item1, entry_id='entry1')[0]
        entry1.save()

        item2 = Item.objects.get_or_create(item_id='item2')[0]
        item2.identification = Identification.objects.create(category=cat, title="title2", edition="edition2",
                                                             series="series2", stock=1)
        item2.production = Production.objects.create(artist=art, production_year='1900', place='place2',
                                                     technique='technique2')
        item2.location = Location.objects.create(location='location2', location_date='1900-01-01')
        item2.usage = Usage.objects.create(status='EX')
        item2.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition2',
                                                       subject='subject2', note='note2')
        item2.save()
        entry2 = Entry.objects.get_or_create(item=item2, entry_id='entry2')[0]
        entry2.save()

        item3 = Item.objects.get_or_create(item_id='item3')[0]
        item3.identification = Identification.objects.create(category=cat, title="title3", edition="edition3",
                                                             series="series3", stock=1)
        item3.production = Production.objects.create(artist=art, production_year='1900', place='place3',
                                                     technique='technique3')
        item3.location = Location.objects.create(location='location3', location_date='1900-01-01')
        item3.usage = Usage.objects.create(status='DP')
        item3.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition3',
                                                       subject='subject3', note='note')
        item3.save()
        entry3 = Entry.objects.get_or_create(item=item3, entry_id='entry3')[0]
        entry3.save()

        self.client = Client(enforce_csrf_checks=True)
        self.factory = RequestFactory()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'testuser')

    def test_edit_search_view(self):
        self.client.login(username='testuser', password='testuser')
        resp = self.client.get(reverse('restricted'))
        self.assertEqual(resp.status_code, 200)

        item1 = Item.objects.get(item_id="item1")
        item2 = Item.objects.get(item_id="item2")
        item3 = Item.objects.get(item_id="item3")
        resp = self.client.get('/cms/edit_item/', {'keywords': 'item', 'general': 'general'})
        self.assertEqual(resp.context['paged_items'][0].item_id, 'item1')
        self.assertEqual(resp.context['paged_items'][1].item_id, 'item2')
        self.assertEqual(resp.context['paged_items'][2].item_id, 'item3')
        self.failUnlessEqual(len(resp.context['paged_items']), 3)

    def test_edit_item(self):
        self.client.login(username='testuser', password='testuser')
        item1 = Item.objects.get(item_id="item1")
        resp = self.client.get('/cms/edit_item/item1/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/edit_item/item1/')
        request.user = self.user
        resp = edit_item(request, 'item1')
        self.factory.post('/cms/edit_item/item1/', {'title': 'item1_edited'})
        self.assertEqual(resp.status_code, 200)

    def test_edit_artist(self):
        self.client.login(username='testuser', password='testuser')
        art = Artist.objects.get(name="art1")
        resp = self.client.get('/cms/edit_artist/art1/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/edit_artist/art1/')
        request.user = self.user
        resp = edit_artist(request, 'art1')
        self.factory.post('/cms/edit_artist/art1/', {'name': 'art1_edited'})
        self.assertEqual(resp.status_code, 200)

    def test_edit_category(self):
        self.client.login(username='testuser', password='testuser')
        cat = Category.objects.get(name="cat1")
        resp = self.client.get('/cms/edit_category/cat1/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/edit_artist/cat1/')
        request.user = self.user
        resp = edit_category(request, 'cat1')
        self.factory.post('/cms/edit_category/cat1/', {'name': 'cat1_edited'})
        self.assertEqual(resp.status_code, 200)


class AddTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.factory = RequestFactory()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'testuser')

    def test_add_item(self):
        self.client.login(username='testuser', password='testuser')
        resp = self.client.get('/cms/add_item/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/add_item/')
        request.user = self.user
        resp = add_item(request)
        self.factory.post('/cms/add_item/', {'item_id': 'item1_added'})
        self.assertEqual(resp.status_code, 200)

    def test_add_artist(self):
        self.client.login(username='testuser', password='testuser')
        resp = self.client.get('/cms/add_artist/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/add_artist/')
        request.user = self.user
        resp = add_artist(request)
        self.factory.post('/cms/add_artist/', {'name': 'art1_added'})
        self.assertEqual(resp.status_code, 200)

    def test_add_category(self):
        self.client.login(username='testuser', password='testuser')
        resp = self.client.get('/cms/add_category/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/add_category/')
        request.user = self.user
        resp = add_category(request)
        self.factory.post('/cms/add_category/', {'name': 'cat1_added'})
        self.assertEqual(resp.status_code, 200)


class DeleteTests(TestCase):
    def setUp(self):
        cat = Category.objects.get_or_create(name="cat1")[0]
        art = Artist.objects.get_or_create(name="art1")[0]
        item1 = Item.objects.get_or_create(item_id='item1')[0]
        item1.identification = Identification.objects.create(category=cat, title="title1", edition="edition1",
                                                             series="series1", stock=1)
        item1.production = Production.objects.create(artist=art, production_year='1900', place='place1',
                                                     technique='technique1')
        item1.location = Location.objects.create(location='location1', location_date='1900-01-01')
        item1.usage = Usage.objects.create(status='DP')
        item1.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition1',
                                                       subject='subject1', note='note1')
        item1.save()
        entry1 = Entry.objects.get_or_create(item=item1, entry_id='entry1')[0]
        entry1.save()

        item2 = Item.objects.get_or_create(item_id='item2')[0]
        item2.identification = Identification.objects.create(category=cat, title="title2", edition="edition2",
                                                             series="series2", stock=1)
        item2.production = Production.objects.create(artist=art, production_year='1900', place='place2',
                                                     technique='technique2')
        item2.location = Location.objects.create(location='location2', location_date='1900-01-01')
        item2.usage = Usage.objects.create(status='EX')
        item2.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition2',
                                                       subject='subject2', note='note2')
        item2.save()
        entry2 = Entry.objects.get_or_create(item=item2, entry_id='entry2')[0]
        entry2.save()

        item3 = Item.objects.get_or_create(item_id='item3')[0]
        item3.identification = Identification.objects.create(category=cat, title="title3", edition="edition3",
                                                             series="series3", stock=1)
        item3.production = Production.objects.create(artist=art, production_year='1900', place='place3',
                                                     technique='technique3')
        item3.location = Location.objects.create(location='location3', location_date='1900-01-01')
        item3.usage = Usage.objects.create(status='DP')
        item3.description = Description.objects.create(width=0, height=0, depth=0, weight=0, condition='condition3',
                                                       subject='subject3', note='note')
        item3.save()
        entry3 = Entry.objects.get_or_create(item=item3, entry_id='entry3')[0]
        entry3.save()

        self.client = Client(enforce_csrf_checks=True)
        self.factory = RequestFactory()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'testuser')

    def test_delete_item(self):
        self.client.login(username='testuser', password='testuser')
        resp = self.client.get('/cms/delete_item/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/delete_item/')
        request.user = self.user
        resp = delete_item(request)
        self.factory.post('/cms/delete_item/', {'item_id': 'item1'})
        self.assertEqual(resp.status_code, 200)

    def test_delete_artist(self):
        self.client.login(username='testuser', password='testuser')
        resp = self.client.get('/cms/delete_artist/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/delete_artist/')
        request.user = self.user
        resp = delete_artist(request)
        self.factory.post('/cms/delete_artist/', {'name': 'art1'})
        self.assertEqual(resp.status_code, 200)

    def test_delete_category(self):
        self.client.login(username='testuser', password='testuser')
        resp = self.client.get('/cms/delete_category/')
        self.assertEqual(resp.status_code, 200)

        request = self.factory.get('/cms/delete_category/')
        request.user = self.user
        resp = delete_category(request)
        self.factory.post('/cms/delete_category/', {'name': 'cat1'})
        self.assertEqual(resp.status_code, 200)


class ModelTests(TestCase):
    def test_category_slug_creation(self):
        cat1 = Category.objects.create(name="cat 1")
        self.assertEqual(cat1.slug, "cat-1")

    def test_artist_slug_creation(self):
        art1 = Artist.objects.create(name="art 1")
        self.assertEqual(art1.slug, "art-1")


    #def setUp(self):
        #try:
            #from populate_cms import populate
            #populate()
        #except ImportError:
            #print('The module populate_cms does not exist')
        #except NameError:
            #print('The function populate() does not exist or is not correct')
        #except:
            #print('Something went wrong in the populate() function :-(')

    #def get_category(self, name):
        #from cms.models import Category
        #try:
            #cat = Category.objects.get(name=name)
        #except Category.DoesNotExist:
            #cat = None
        #return cat

    #def test_python_cat_added(self):
        #cat = self.get_category('Python')
        #self.assertIsNotNone(cat)

    #def test_python_cat_with_views(self):
        #cat = self.get_category('Python')
        #self.assertEquals(cat.views, 128)

    #def test_python_cat_with_likes(self):
        #cat = self.get_category('Python')
        #self.assertEquals(cat.likes, 64)


class LoginTests(TestCase):
    def test_login(self):
        c = Client()
        resp = c.post('/accounts/login/', {'username': 'testuser', 'password': 'CrEm6s8ecaZ?'})
        self.assertEqual(resp.status_code, 200)


#class GeneralTests(TestCase):
    #def test_serving_static_files(self):
        # If using static media properly result is not NONE once it finds NoImage.jpg
        #result = finders.find('images/NoImage.jpg')
        #self.assertIsNotNone(result)
