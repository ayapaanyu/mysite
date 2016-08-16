from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from cms.models import Category, Artist, Identification, Production, Location, Usage, Description, Item, \
    Entry, Exit, LoanIn, LoanOut, ItemPhoto, Page
from cms.forms import CategoryForm, PageForm, UserForm, UserProfileForm, ArtistForm, GeneralSearchForm, \
    IdentificationForm, ProductionForm, LocationForm, UsageForm, DescriptionForm, ItemForm, EntryForm, ExitForm, \
    LoanInForm, LoanOutForm, ItemPhotoForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q
import re
from django.forms import inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Get the number of visits to the sites.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit, update the last visit cookie now that we've updated the count.
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # update/set the visits cookie
    request.session['visits'] = visits


def index(request):
    request.session.set_test_cookie()
    # Request the context of the request.
    # The context contains information such as the client's machine details.

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    # Call function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # Obtain our Response object early so we can add cookie info.
    # Return response back to the user, updating any cookies that need changed.
    response = render(request, 'cms/index.html', context=context_dict)
    return response

#    Construct a dictionary to pass to the template engine as its context.
#    Note the key bold message is the same as {{ boldmessage }} in the template!
#    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # Return a rendered response to send to the client.
    # return render (request, 'rango/index.html', context_dict)
    # return HttpResponse ("Rango says hello world!")


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


def collection(request):
    # if request.session.test_cookie_worked():
        # print("TEST COOKIE WORKED!")
        # request.session.delete_test_cookie()

    category_list = Category.objects.all()
    artist_list = Artist.objects.all()

    general_form = GeneralSearchForm()

    if request.method == 'GET':
        if 'general' in request.GET:
            general_form = GeneralSearchForm(request.GET)
            if general_form.is_valid():
                words = request.GET['keywords']
                keys = re.compile(r'[^\s";,.:]+').findall(words)
                if keys:
                    entries = Item.objects.none()
                else:
                    entries = Item.objects.all()
                ents = []
                get_general_entries(keys, ents)

                for ent in ents:
                    if ent:
                        entries |= ent

                #results = {}
                #for item in entries:
                    #identification = Identification.objects.filter(item__item_id=item)
                    #production = Production.objects.filter(item__item_id=item)
                    #photos = ItemPhoto.objects.filter(item=item)
                    #results[item] = {'photos': photos} #'identification': identification, 'production': production, }

                items = Item.objects.filter(item_id__in=entries)
                usages = Usage.objects.filter(item__item_id__in=items).exclude(status="").exclude(status="EX")
                items = Item.objects.filter(usage__in=usages)
                paginator = Paginator(items, 5)
                page = request.GET.get('page')
                query_string = request.GET.urlencode()
                try:
                    paged_items = paginator.page(page)
                except PageNotAnInteger:
                    paged_items = paginator.page(1)
                except EmptyPage:
                    paged_items = paginator.page(paginator.num_pages)

                return render(request, 'cms/collection.html', {'general_form': general_form, 'paged_items': paged_items,
                                                               'query_string': query_string})

        else:
            context_dict = {'categories': category_list, 'artists': artist_list, 'general_form': general_form}
            return render(request, 'cms/collection.html', context_dict)


def show_item(request, item_id):
    context_dict = {}
    try:
        item = Item.objects.get(item_id=item_id)
        identification = Identification.objects.get(item__item_id=item_id)
        production = Production.objects.get(item__item_id=item_id)
        location = Location.objects.get(item__item_id=item_id)
        usage = Usage.objects.get(item__item_id=item_id)
        description = Description.objects.get(item__item_id=item_id)
        photos = ItemPhoto.objects.filter(item=item_id)

        context_dict['item'] = item
        context_dict['identification'] = identification
        context_dict['production'] = production
        context_dict['location'] = location
        context_dict['usage'] = usage
        context_dict['description'] = description
        context_dict['photos'] = photos

    except Category.DoesNotExist:
        context_dict['item'] = None
        context_dict['identification'] = None
        context_dict['production'] = None
        context_dict['location'] = None
        context_dict['usage'] = None
        context_dict['description'] = None
        context_dict['photos'] = None

    return render(request, 'cms/item.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        identifications = Identification.objects.filter(category=category)
        items = Item.objects.filter(identification__in=identifications)
        usages = Usage.objects.filter(item__item_id__in=items).exclude(status="").exclude(status="EX")
        items = Item.objects.filter(usage__in=usages)
        #productions = Production.objects.filter(item__item_id__in=items)
        #photos = ItemPhoto.objects.filter(item__in=items)
        context_dict['category'] = category
        #context_dict['identifications'] = identifications
        #context_dict['items'] = items
        #context_dict['productions'] = productions
        #context_dict['photos'] = photos

        paginator = Paginator(items, 5)
        page = request.GET.get('page')
        try:
            paged_items = paginator.page(page)
        except PageNotAnInteger:
            paged_items = paginator.page(1)
        except EmptyPage:
            paged_items = paginator.page(paginator.num_pages)
        context_dict['paged_items'] = paged_items

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template will display the "no category" message for us.
        context_dict['category'] = None
        #context_dict['identifications'] = None
        #context_dict['items'] = None
        #context_dict['productions'] = None
        #context_dict['photos'] = None
        context_dict['paged_items'] = None

    return render(request, 'cms/category.html', context_dict)


def show_artist(request, artist_name_slug):
    context_dict = {}
    try:
        artist = Artist.objects.get(slug=artist_name_slug)
        productions = Production.objects.filter(artist=artist)
        items = Item.objects.filter(production__in=productions)
        usages = Usage.objects.filter(item__item_id__in=items).exclude(status="").exclude(status="EX")
        items = Item.objects.filter(usage__in=usages)
        pages = Page.objects.filter(artist=artist)
        #identifications = Identification.objects.filter(item__item_id__in=items)
        #context_dict['items'] = items
        #context_dict['productions'] = productions
        context_dict['artist'] = artist
        context_dict['pages'] = pages
        #context_dict['identifications'] = identifications

        paginator = Paginator(items, 5)
        page = request.GET.get('page')
        try:
            paged_items = paginator.page(page)
        except PageNotAnInteger:
            paged_items = paginator.page(1)
        except EmptyPage:
            paged_items = paginator.page(paginator.num_pages)
        context_dict['paged_items'] = paged_items

    except Artist.DoesNotExist:
        #context_dict['items'] = None
        context_dict['artist'] = None
        context_dict['productions'] = None
        #context_dict['identifications'] = None
        context_dict['paged_items'] = None
        context_dict['pages'] = None

    return render(request, 'cms/artist.html', context_dict)


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab info from the raw form info. Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid, save the user's form data to the database.
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                # Now we save the UserProfile model instance.
                profile.save()
                # Update our variable to indicate that the template registration was successful.
                registered = True
        else:
            # Invalid form or forms - mistakes or something else? Print problems to the terminal.
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'cms/register.html',
                {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant info.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This info is obtained from the login form.
        # We use request.POST.get('<variable>')as opposed to request.POST.get['<variable>'],
        # because the former returns None if the value doesn't exist, while the latter will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/ password combination is valid.
        # A user object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None, no user with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

        # The request is not a HTTP POST, so display the login form.
        # This scenario would mot likely be a HTTP GET.

    else:
        # No context variables to pass to the template system, hence the blank dictionary object...
        return render(request, 'cms/login.html', {})


@login_required
def edit_item_search(request):
    # return HttpResponse("Since you're logged in, you can see this text!")
    general_form = GeneralSearchForm()

    if request.method == 'GET':
        if 'general' in request.GET:
            general_form = GeneralSearchForm(request.GET)
            if general_form.is_valid():
                words = request.GET['keywords']
                keys = re.compile(r'[^\s";,.:]+').findall(words)
                ents = []
                if keys:
                    entries = Item.objects.none()
                else:
                    entries = Item.objects.all()
                get_general_entries(keys, ents)
                for ent in ents:
                    if ent:
                        entries |= ent

                #results = {}
                #for item in entries:
                    #identification = Identification.objects.filter(item__item_id=item)
                    #production = Production.objects.filter(item__item_id=item)
                    #photos = ItemPhoto.objects.filter(item=item)
                    #results[item] = {'identification': identification, 'production': production, 'photos': photos}

                paginator = Paginator(entries, 5)
                page = request.GET.get('page')
                query_string = request.GET.urlencode()
                try:
                    paged_items = paginator.page(page)
                except PageNotAnInteger:
                    paged_items = paginator.page(1)
                except EmptyPage:
                    paged_items = paginator.page(paginator.num_pages)

                return render(request, 'cms/edit_item_search.html', {'general_form': general_form,
                                                                     'paged_items': paged_items,
                                                                     'query_string': query_string})

        else:
            context_dict = {'general_form': general_form}
            return render(request, 'cms/edit_item_search.html', context_dict)


@login_required
def edit_artist_search(request):
    artist_list = Artist.objects.all()
    context_dict = {'artists': artist_list}
    return render(request, 'cms/edit_artist_search.html', context_dict)


@login_required
def edit_category_search(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}
    return render(request, 'cms/edit_category_search.html', context_dict)


@login_required
def edit_item(request, item_id, template_name="cms/edit_item.html"):
    general_form = GeneralSearchForm()
    context_dict = {'general_form': general_form}
    item = Item.objects.get(item_id=item_id)
    photos = ItemPhoto.objects.filter(item=item_id)

    item_form = get_object_or_404(Item, item_id=item_id)
    identification_form = get_object_or_404(Identification, item__item_id=item_id)
    production_form = get_object_or_404(Production, item__item_id=item_id)
    location_form = get_object_or_404(Location, item__item_id=item_id)
    usage_form = get_object_or_404(Usage, item__item_id=item_id)
    description_form = get_object_or_404(Description, item__item_id=item_id)
    EntryInlineFormSet = inlineformset_factory(Item, Entry, form=EntryForm, extra=1)
    ExitInlineFormSet = inlineformset_factory(Item, Exit, form=ExitForm, extra=1)
    LoanInInlineFormSet = inlineformset_factory(Item, LoanIn, form=LoanInForm, extra=1)
    LoanOutInlineFormSet = inlineformset_factory(Item, LoanOut, form=LoanOutForm, extra=1)
    ItemPhotoInlineFormSet = inlineformset_factory(Item, ItemPhoto, fields=('picture',), extra=1)
    #ItemPhotoFormSet = modelformset_factory(ItemPhoto, fields=('picture',), extra=1)

    formA = ItemForm(request.POST or None, instance=item_form)
    formB = IdentificationForm(request.POST or None, instance=identification_form)
    formC = ProductionForm(request.POST or None, instance=production_form)
    formD = LocationForm(request.POST or None, instance=location_form)
    formE = UsageForm(request.POST or None, instance=usage_form)
    formF = DescriptionForm(request.POST or None, instance=description_form)
    formsetA = EntryInlineFormSet(request.POST or None, instance=item)
    formsetB = ExitInlineFormSet(request.POST or None, instance=item)
    formsetC = LoanInInlineFormSet(request.POST or None, instance=item)
    formsetD = LoanOutInlineFormSet(request.POST or None, instance=item)
    formsetE = ItemPhotoInlineFormSet(request.POST or None, request.FILES or None, instance=item)
    #formsetE = ItemPhotoFormSet(request.POST or None, request.FILES or None, queryset=ItemPhoto.objects.none())

    if formA.is_valid() and formB.is_valid() and formC.is_valid() and formD.is_valid() and formE.is_valid() \
            and formF.is_valid() and formsetA.is_valid() and formsetB.is_valid() and formsetC.is_valid() \
            and formsetD.is_valid() and formsetE.is_valid():
        formA.save(commit=True)
        formB.save(commit=True)
        formC.save(commit=True)
        formD.save(commit=True)
        formE.save(commit=True)
        formF.save(commit=True)
        formsetA.save(commit=True)
        formsetB.save(commit=True)
        formsetC.save(commit=True)
        formsetD.save(commit=True)
        formsetE.save()
        #for form in formsetE.cleaned_data:
            #image = form['picture']
            #photo = ItemPhoto(item=item_form, picture=image)
            #photo.save()
            #form.picture = edited_item
            #form.save()
        return render(request, 'cms/edit_item_search.html', context_dict)

    context_dict = {'formA': formA, 'formB': formB, 'formC': formC, 'formD': formD, 'formE': formE, 'formF': formF,
                    'formsetA': formsetA, 'formsetB': formsetB, 'formsetC': formsetC, 'formsetD': formsetD,
                    'item': item, 'photos': photos, 'formsetE': formsetE}

    return render(request, template_name, context_dict)


@login_required
def edit_artist(request, artist_name_slug, template_name="cms/edit_artist.html"):
    artist = Artist.objects.get(slug=artist_name_slug)
    artist_form = get_object_or_404(Artist, slug=artist_name_slug)
    form = ArtistForm(request.POST or None, instance=artist_form)
    #PageInlineFormSet = inlineformset_factory(Artist, Page, form=PageForm, extra=1)
    #formset = PageInlineFormSet(request.POST or None, instance=artist)
    if form.is_valid():
        form.save(commit=True)
        #formset.save()
        return redirect('edit_artist_search')

    context_dict = {'form': form, 'artist': artist}
    #context_dict = {}
    #try:
        #artist = Artist.objects.get(slug=artist_name_slug)
        #context_dict['artist'] = artist
    #except Artist.DoesNotExist:
        #context_dict['artist'] = None

    return render(request, template_name, context_dict)


@login_required
def edit_category(request, category_name_slug, template_name="cms/edit_category.html"):
    category = Category.objects.get(slug=category_name_slug)
    category_form = get_object_or_404(Category, slug=category_name_slug)
    form = CategoryForm(request.POST or None, instance=category_form)
    if form.is_valid():
        form.save(commit=True)
        return redirect('edit_category_search')

    context_dict = {'form': form, 'category': category}
    return render(request, template_name, context_dict)


@login_required
def add_item(request):
    item_form = ItemForm()
    identification_form = IdentificationForm()
    production_form = ProductionForm()
    location_form = LocationForm()
    usage_form = UsageForm()
    description_form = DescriptionForm()
    EntryFormSet = inlineformset_factory(Item, Entry, form=EntryForm, extra=1)
    ExitFormSet = inlineformset_factory(Item, Exit, form=ExitForm, extra=1)
    LoanInFormSet = inlineformset_factory(Item, LoanIn, form=LoanInForm, extra=1)
    LoanOutFormSet = inlineformset_factory(Item, LoanOut, form=LoanOutForm, extra=1)
    ItemPhotoInlineFormSet = inlineformset_factory(Item, ItemPhoto, fields=('picture',), extra=3)
    #ItemPhotoFormSet = formset_factory(ItemPhotoForm, extra=1)

    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        identification_form = IdentificationForm(request.POST)
        production_form = ProductionForm(request.POST)
        location_form = LocationForm(request.POST)
        usage_form = UsageForm(request.POST)
        description_form = DescriptionForm(request.POST)

        if item_form.is_valid() and identification_form.is_valid() and production_form.is_valid() \
                and location_form.is_valid() and usage_form.is_valid() and description_form.is_valid():
            new_item = item_form.save(commit=False)
            identification = identification_form.save(commit=True)
            production = production_form.save(commit=True)
            location = location_form.save(commit=True)
            usage = usage_form.save(commit=True)
            description = description_form.save(commit=True)
            new_item.identification = identification
            new_item.production = production
            new_item.location = location
            new_item.usage = usage
            new_item.description = description

            entry_formset = EntryFormSet(request.POST, instance=new_item)
            exit_formset = ExitFormSet(request.POST, instance=new_item)
            loan_in_formset = LoanInFormSet(request.POST, instance=new_item)
            loan_out_formset = LoanOutFormSet(request.POST, instance=new_item)
            #item_photo_formset = ItemPhotoFormSet(request.POST or None, request.FILES or None)
            item_photo_formset = ItemPhotoInlineFormSet(request.POST or None, request.FILES or None, instance=new_item)

            if entry_formset.is_valid() and exit_formset.is_valid() and loan_in_formset.is_valid()\
                    and loan_out_formset.is_valid() and item_photo_formset.is_valid():
                new_item.save()
                entry_formset.save()
                exit_formset.save()
                loan_in_formset.save()
                loan_out_formset.save()
                item_photo_formset.save()
                #for form in item_photo_formset.cleaned_data:
                    #image = form['picture']
                    #photo = ItemPhoto(item=new_item, picture=image)
                    #photo.save()
                return redirect('add_item')
        else:
            print(item_form.errors)

    return render(request, 'cms/add_item.html', {'item_form': item_form, 'identification_form': identification_form,
                                                 'production_form': production_form, 'location_form': location_form,
                                                 'usage_form': usage_form, 'description_form': description_form,
                                                 'entry_formset': EntryFormSet, 'exit_formset': ExitFormSet,
                                                 'loan_in_formset': LoanInFormSet, 'loan_out_formset': LoanOutFormSet,
                                                 'item_photo_formset': ItemPhotoInlineFormSet})


@login_required
def add_artist(request):
    form = ArtistForm()
    #PageInlineFormSet = inlineformset_factory(Artist, Page, form=PageForm, extra=1)

    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #formset = PageInlineFormSet(request.POST, instance=new_artist)
            #if formset.is_valid():
                #new_artist.save()
                #formset.save()
            return redirect('add_artist')
        else:
            print(form.errors)
    return render(request, 'cms/add_artist.html', {'form': form})


@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved. We could give a confirmation message.
            # But since the most recent category added is on the index page,
            # Then we can redirect the user back to the index page.
            return redirect('add_category')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

    return render(request, 'cms/add_category.html', {'form': form})


@login_required
def delete_item(request, template_name="cms/delete_confirmation.html"):
    general_form = GeneralSearchForm()
    context_dict = {'general_form': general_form}
    delete_items = request.GET.getlist('delete_items')

    if request.method == "POST":
        item = Item.objects.filter(item_id__in=delete_items)
        Identification.objects.filter(item__item_id__in=item).delete()
        Production.objects.filter(item__item_id__in=item).delete()
        Location.objects.filter(item__item_id__in=item).delete()
        Usage.objects.filter(item__item_id__in=item).delete()
        Description.objects.filter(item__item_id__in=item).delete()
        item.delete()
        return render(request, 'cms/edit_item_search.html', context_dict)
    else:
        return render(request, template_name, {'object': delete_items})


@login_required
def delete_artist(request, template_name="cms/delete_confirmation.html"):
    delete_artists = request.GET.getlist('delete_artists')

    if request.method == "POST":
        Artist.objects.filter(name__in=delete_artists).delete()
        return redirect('edit_artist_search')
    else:
        return render(request, template_name, {'object': delete_artists})


@login_required
def delete_category(request, template_name="cms/delete_confirmation.html"):
    delete_categories = request.GET.getlist('delete_categories')

    if request.method == "POST":
        Category.objects.filter(name__in=delete_categories).delete()
        return redirect('edit_category_search')
    else:
        return render(request, template_name, {'object': delete_categories})


#@login_required
#def add_page(request, category_name_slug):
    #try:
        #category = Category.objects.get(slug=category_name_slug)
    #except Category.DoesNotExist:
        #category = None

    #form = PageForm()
    #if request.method == "POST":
        #form = PageForm(request.POST)
        #if form.is_valid():
            #if category:
                #page = form.save(commit=False)
                #page.category = category
                #page.views = 0
                #page.save()
            #return show_category(request, category_name_slug)
        #else:
            #print(forms.errors)

    #context_dict = {'form': form, 'category': category}
    #return render(request, 'cms/add_page.html', context_dict)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))