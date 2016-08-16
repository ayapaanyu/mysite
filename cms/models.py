from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    #views = models.IntegerField(default=0)
    #likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=128, unique=True)
    born = models.CharField(max_length=128, blank=True)
    died = models.CharField(max_length=128, blank=True)
    artist_description = models.CharField(max_length=3000, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Artist, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Identification(models.Model):
    title = models.CharField(max_length=128, blank=True)
    edition = models.CharField(max_length=128, blank=True)
    series = models.CharField(max_length=128, blank=True)
    category = models.ForeignKey(Category)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Production(models.Model):
    artist = models.ForeignKey(Artist)
    production_year = models.CharField(max_length=10, null=True, blank=True)
    place = models.CharField(max_length=128, blank=True)
    technique = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return str(self.id)


class Location(models.Model):
    location = models.CharField(max_length=128, blank=True)
    location_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Usage(models.Model):
    STATUS_CHOICES = (
        ('DP', 'On Display'),
        ('SR', 'In Storage'),
        ('LN', 'On Loan'),
        ('EX', 'Exit'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return str(self.id)


class Description(models.Model):
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    condition = models.CharField(max_length=128, blank=True)
    subject = models.CharField(max_length=128, blank=True)
    note = models.CharField(max_length=3000, blank=True)

    def __str__(self):
        return str(self.id)


class Item(models.Model):
    item_id = models.CharField(max_length=128, primary_key=True)
    identification = models.ForeignKey(Identification, default=None, null=True, blank=True)
    production = models.ForeignKey(Production, default=None, null=True, blank=True)
    location = models.ForeignKey(Location, default=None, null=True, blank=True)
    usage = models.ForeignKey(Usage, default=None, null=True, blank=True)
    description = models.ForeignKey(Description, default=None, null=True, blank=True)

    def __str__(self):
        return self.item_id


class Entry(models.Model):
    item = models.ForeignKey(Item, related_name='entries', default=None, null=True, blank=True)
    entry_id = models.CharField(max_length=128, unique=True, blank=True)
    entry_date = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=128, blank=True)
    entry_note = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.entry_id


class Exit(models.Model):
    item = models.ForeignKey(Item, related_name='exits', default=None, null=True, blank=True)
    exit_id = models.CharField(max_length=128, unique=True, blank=True)
    exit_date = models.DateField(blank=True, null=True)
    exit_destination = models.CharField(max_length=128, blank=True)
    exit_note = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.exit_id


class LoanIn(models.Model):
    item = models.ForeignKey(Item, related_name='loan_ins', default=None, null=True, blank=True)
    loan_in_id = models.CharField(max_length=128, unique=True, blank=True)
    loan_in_date = models.DateField(blank=True, null=True)
    lender = models.CharField(max_length=128, blank=True)
    return_out_date = models.DateField(blank=True, null=True)
    loan_in_note = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.loan_in_id


class LoanOut(models.Model):
    item = models.ForeignKey(Item, related_name='loan_outs', default=None, null=True, blank=True)
    loan_out_id = models.CharField(max_length=128, unique=True, blank=True)
    loan_out_date = models.DateField(blank=True, null=True)
    borrower = models.CharField(max_length=128, blank=True)
    return_in_date = models.DateField(blank=True, null=True)
    loan_out_note = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.loan_out_id


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return str(self.picture)


class Page (models.Model):
    #category = models.ForeignKey(Category)
    artist = models.ForeignKey(Artist, related_name='page_artist', default=None, null=True, blank=True)
    title = models.CharField(max_length=128)
    url = models.URLField()
    #views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username