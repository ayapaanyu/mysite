import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from cms.models import Artist

def populate():

#### Add Artist here ####
    add_artist('Katsushika Hokusai', 1760, 1849, "Katsushika Hokusai (1760-1849) is perhaps Japan's most famous artist. He is best known for his designs for prints and printed books, although later in life he focused increasingly on paintings.")
    add_artist('Kubo Shunman', 1757, 1820, "Shunman (1757-1820) was a celebrated painter, print-maker and author of the Edo period (1615-1868). As a print-maker, he specialised in surimono.")
    add_artist('Muneyoshi Yamada Chozaburo', 0, 0, "")
    add_artist('Kohosai', 0, 0, "")
    add_artist('Aorenraju', 1920, 0, "")

    for k in Artist.objects.all():
        print(k)


def add_artist(name, born, died, description):
    a = Artist.objects.get_or_create(name=name)[0]
    a.born = born
    a.died = died
    a.description = description
    a.save()
    return a

# Start execution here!
if __name__ == '__main__':
    print("Starting CMS population script ...")
    populate()





def search(keys, fields, search_model):
    if keys:
        query = None
        for key in keys:
            for field in fields:
                qry = Q(**{'%s__icontains' % field: key})
                if query is None:
                    query = qry
                else:
                    query = query | qry
        key_ids = search_model.objects.filter(query)
        return key_ids


def get_item_id(key_ids, field):
    if key_ids:
        query = None
        for key_id in key_ids:
            qry = Q(**{'%s__exact' % field: key_id})
            if query is None:
                query = qry
            else:
                query = query | qry
        results = Item.objects.filter(query)
        return results


def get_general_entries(keys, ents):
    # search keys in item_id of Item
    item = get_item_id(search(keys, ['item_id'], Item), 'item_id')
    ents.append(item)
    # search keys in title, edition, series of Identification and get item_id
    identification = get_item_id(search(keys, ['title', 'edition', 'series'], Identification), 'identification')
    ents.append(identification)
    # search keys in production_year, place and technique of Production and get item_id
    production = get_item_id(search(keys, ['production_year', 'place', 'technique'], Production), 'production')
    ents.append(production)
    # search keys in location and location_date of Location and get item_id
    location = get_item_id(search(keys, ['location', 'location_date'], Location), 'location')
    ents.append(location)
    # search keys in status of Usage and get item_id
    usage = get_item_id(search(keys, ['status'], Usage), 'usage')
    ents.append(usage)
    # search keys in subject of Description and get item_id
    description = get_item_id(search(keys, ['subject'], Description), 'description')
    ents.append(description)
    # searching keys in name of Artist and get item_id
    artist_keys = search(keys, ['name', 'born', 'died'], Artist)
    artist = get_item_id(search(artist_keys, ['artist__name'], Production), 'production')
    ents.append(artist)
    # searching keys in name of Category and get item_id
    category_keys = search(keys, ['name'], Category)
    category = get_item_id(search(category_keys, ['category__name'], Identification), 'identification')
    ents.append(category)

    return ents


def get_advanced_entries(keys, ents, field):
    if field == 'id':
        item = get_item_id(search(keys, ['item_id'], Item), 'item_id')
        if item:
            ents.append(item)
    elif field == 'title':
        identification = get_item_id(search(keys, ['title', 'edition', 'series'], Identification), 'identification')
        if identification:
            ents.append(identification)
    elif field == 'category':
        category_keys = search(keys, ['name'], Category)
        category = get_item_id(search(category_keys, ['category__name'], Identification), 'identification')
        if category:
            ents.append(category)
    elif field == 'date':
        production_year = get_item_id(search(keys, ['production_year'], Production), 'production')
        if production_year:
            ents.append(production_year)
    elif field == 'artist':
        artist_keys = search(keys, ['name'], Artist)
        artist = get_item_id(search(artist_keys, ['artist__name'], Production), 'production')
        if artist:
            ents.append(artist)
    elif field == 'place_of_origin':
        place_of_origin = get_item_id(search(keys, ['place'], Production), 'production')
        if place_of_origin:
            ents.append(place_of_origin)
    elif field == 'technique':
        technique = get_item_id(search(keys, ['technique'], Production), 'production')
        if technique:
            ents.append(technique)
    elif field == 'subject':
        subject = get_item_id(search(keys, ['subject'], Description), 'description')
        if subject:
            ents.append(subject)

    return ents


def collection(request):
    # if request.session.test_cookie_worked():
        # print("TEST COOKIE WORKED!")
        # request.session.delete_test_cookie()

    category_list = Category.objects.all()
    artist_list = Artist.objects.all()

    general_form = GeneralSearchForm()
    advanced_form = AdvancedSearchForm()

    if request.method == 'GET':
        if 'general' in request.GET: #request.GET is a dictionary-like object containing all GET request parameters
            general_form = GeneralSearchForm(request.GET)
            if general_form.is_valid():
                entries = Item.objects.none()
                ents = []
                words = request.GET['words']
                keys = re.compile(r'[^\s";,.:]+').findall(words)
                get_general_entries(keys, ents)

                for ent in ents:
                    if ent:
                        entries |= ent

                return render(request, 'cms/results.html', {'general_form': general_form, 'advanced_form': advanced_form, 'entries': entries})
            advanced_form = AdvancedSearchForm()

        elif 'advanced' in request.GET:
            advanced_form = AdvancedSearchForm(request.GET)
            if advanced_form.is_valid():
                ents = []
                fields = ['id', 'title', 'category', 'date', 'artist', 'place_of_origin', 'technique', 'subject']
                for field in fields:
                    if request.GET[field]:
                        words = request.GET[field]
                        keys = re.compile(r'[^\s";,.:]+').findall(words)
                        get_advanced_entries(keys, ents, field)

                q_objects = Q()
                for ent in ents:
                    q_objects.add(Q(item_id=ent), Q.AND)
                entries = Item.objects.filter(q_objects)

                return render(request, 'cms/results.html', {'general_form': general_form, 'advanced_form': advanced_form, 'ents': ents, 'q_objects': q_objects, 'entries': entries})
            general_form = GeneralSearchForm()

    else:
        general_form = GeneralSearchForm()
        advanced_form = AdvancedSearchForm()

    context_dict = {'categories': category_list, 'artists': artist_list, 'general_form': general_form, 'advanced_form': advanced_form}
    return render(request, 'cms/collection.html', context_dict)


#results.html
< div


class ="container" >

< form
id = "general"
method = "get"
action = "{% url 'collection' %}" >
{ % csrf_token %}
{ % bootstrap_form
general_form %}
< button


class ="btn btn-primary" type="submit" name="general" value="general" > Search < / button >

< / form >

< form
id = "advanced"
method = "get"
action = "{% url 'collection' %}" >
{ % csrf_token %}
{ % bootstrap_form
advanced_form %}
< br / >
< button


class ="btn btn-primary" type="submit" name="advanced" value="advanced" > Search < / button >

< / form >
< / div >

< div


class ="container" >


{ % if entries %}
{{entries}}
{ % endif %}
< / div >


#collection.html
< div


class ="container" >

< form
id = "general"
method = "get"
action = "" >
{ % bootstrap_form
general_form %}
< button


class ="btn btn-primary" type="submit" name="general" value="general" > Search < / button >

< / form >

< form
id = "advanced"
method = "get"
action = "" >
{ % bootstrap_form
advanced_form %}
< br / >
< button


class ="btn btn-primary" type="submit" name="advanced" value="advanced" > Search < / button >

< / form >



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^collection/', views.collection, name='collection'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^artist/(?P<artist_name_slug>[\w\-]+)/$', views.show_artist, name='show_artist'),
    url(r'^item/(?P<item_id>[\w\-]+)/$', views.show_item, name='show_item'),
    url(r'^edit/$', views.edit, name='restricted'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_artist/$', views.add_artist, name='add_artist'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),



url(r'^collection/$', Collection.as_view(), name='collection'),
class MultiFormMixin(ContextMixin):
    form_classes = {}

    # 使用するFormクラスを取得する
    def get_form_classes(self):
        return self.form_classes

    # Formクラスのインスタンスを取得する
    def get_forms(self, form_classes):
        return dict([(key, klass(**self.get_form_kwargs())) for key, klass in form_classes.items()])

    # Formクラスに渡す引数を取得する
    def get_form_kwargs(self, form_name, bind_form=False):
        kwargs = {}
        kwargs.update({'initial': self.get_initial(form_name)})
        kwargs.update({'prefix': self.get_prefix(form_name)})

        if bind_form:
            kwargs.update(self._bind_form_data())

        return kwargs

    # 正常時の処理
    def forms_valid(self, forms, form_name):
        return super(MultiFormMixin, self).form_valid(forms)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

    # Formの初期値を設定する
    def get_initial(self, form_name):
        initial_method = 'get_%s_initial' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        else:
            return self.initial.copy()

    # Formのprefixを設定する
    def get_prefix(self, form_name):
        return self.prefixes.get(form_name, self.prefix)


class MultiFormView(FormView):
    # if request.session.test_cookie_worked():
        # print("TEST COOKIE WORKED!")
        # request.session.delete_test_cookie()

    # GETメソッドでアクセス時に呼ばれる
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        form_name = request.GET.get('submit')
        if form_name:
            forms = self.get_forms(form_classes, form_name)
            form = forms[form_name]
            if form.is_valid:
                return self.forms_valid(forms, form_name)
        else:
            form_classes = self.get_form_classes()
            forms = self.get_forms(form_classes)
            return self.render_to_response(self.get_context_data(forms=forms))


     #def get(self, request, *args, **kwargs):  # GETメソッドでアクセス時に呼ばれる
    #def get_initial(self):  # Formの初期値を設定する
    #def get_prefix(self):  # Formのprefixを設定する
     #def get_form_class(self):  # 使用するFormクラスを取得する
    #def get_form_kwargs(self):  # Formクラスに渡す引数を取得する
     #def get_form(self, form_class=None):  # Formクラスのインスタンスを取得する
    #def get_success_url(self):  # 正常終了時にリダイレクトするURL
     #def form_valid(self, form):  # 正常時の処理
    #def form_invalid(self, form):  # データが不正な場合の処理
    #def get_context_data(self, **kwargs):  # templateに渡すcontextを取得する
    #def render_to_response(self, context, **response_kwargs):  # responseを作成する
    #def get_template_names(self):  # レンダリングに使用するテンプレート名を取得する


class BaseSearch (MultiFormMixin, MultiFormView):
    pass


class Collection (BaseSearch):
    template_name = 'cms/collection.html'
    form_classes = {'general': GeneralSearchForm, 'advanced': AdvancedSearchForm}
    success_url = reverse_lazy('collection')

    category_list = Category.objects.all()
    artist_list = Artist.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Collection, self).get_context_data(**kwargs)
        context.update({'categories': self.category_list, 'artists': self.artist_list})
        return context