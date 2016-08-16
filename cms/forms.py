from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from cms.models import Category, UserProfile, Artist, Identification, Production, Location, Usage, Description,\
    Item, Entry, Exit, LoanIn, LoanOut, ItemPhoto, Page


class CategoryForm(forms.ModelForm):
    #name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class ArtistForm(forms.ModelForm):
    #name = forms.CharField(max_length=128, help_text="Please enter the artist name.")
    #born = forms.IntegerField(min_value=0, required=False, help_text="Please enter the born year.")
    #died = forms.IntegerField(min_value=0, required=False, help_text="Please enter the died year.")
    #artist_description = forms.CharField(max_length=300, required=False, help_text="Please enter the artist description.")
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Artist
        fields = ('name', 'born', 'died', 'artist_description')


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'url')


class GeneralSearchForm(forms.Form):
    keywords = forms.CharField(required=False)


class IdentificationForm(forms.ModelForm):
    class Meta:
        model = Identification
        fields = ('title', 'edition', 'series', 'category', 'stock')


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ('artist', 'production_year', 'place', 'technique')


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('location', 'location_date')


class UsageForm(ModelForm):
    class Meta:
        model = Usage
        fields = ['status']


class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ('width', 'height', 'depth', 'weight', 'condition', 'subject', 'note')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_id',)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('entry_id', 'entry_date', 'owner', 'entry_note')


class ExitForm(forms.ModelForm):
    class Meta:
        model = Exit
        fields = ('exit_id', 'exit_date', 'exit_destination', 'exit_note')


class LoanInForm(forms.ModelForm):
    class Meta:
        model = LoanIn
        fields = ('loan_in_id', 'loan_in_date', 'lender', 'return_out_date', 'loan_in_note')


class LoanOutForm(forms.ModelForm):
    class Meta:
        model = LoanOut
        fields = ('loan_out_id', 'loan_out_date', 'borrower', 'return_in_date', 'loan_out_note')


class ItemPhotoForm(forms.ModelForm):
    picture = forms.ImageField(label='Image')

    class Meta:
        model = ItemPhoto
        fields = ('picture',)

#class AdvancedSearchForm(forms.Form):
    #id = forms.CharField(required=False)
    #title = forms.CharField(required=False)
    #category = forms.CharField(required=False)
    #date = forms.IntegerField(required=False)
    #artist = forms.CharField(required=False)
    #place_of_origin = forms.CharField(required=False)
    #technique = forms.CharField(required=False)
    #subject = forms.CharField(required=False)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', then prepend 'http://'
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them.
        # Here, we are hiding the foreign key.
        # We can either exclude the category field from the form,
        #exclude = ('category',)

        # or specify the fields to include
        fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.") # <- help_text added after bootstrap)
    # === Added after bootstrap
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    # =========================

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    # ===== Added after bootstrap
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    # ===========================

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
