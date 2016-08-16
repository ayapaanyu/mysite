from django.contrib import admin
from cms.models import Category, UserProfile, Artist, Identification, Production, Location, Usage, Description, \
    Item, Entry, Exit, LoanIn, LoanOut, ItemPhoto, Page


class CategoryAdmin (admin.ModelAdmin):
    #list_display = ('name', 'views', 'likes', 'slug')
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)


class PageAdmin (admin.ModelAdmin):
    #list_display = ('title', 'category', 'url')
    list_display = ('title', 'artist', 'url')
admin.site.register(Page, PageAdmin)


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'born', 'died', 'slug')
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Artist, ArtistAdmin)


class IdentificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'edition', 'series', 'category', 'stock')
admin.site.register(Identification, IdentificationAdmin)


class ProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'artist', 'production_year', 'place', 'technique')
admin.site.register(Production, ProductionAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'location_date')
admin.site.register(Location, LocationAdmin)


class UsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
admin.site.register(Usage, UsageAdmin)


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'width', 'height', 'depth', 'weight', 'condition', 'subject')
admin.site.register(Description, DescriptionAdmin)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('entry_id', 'item', 'entry_date', 'owner', 'entry_note')
admin.site.register(Entry, EntryAdmin)


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 1


class ExitAdmin(admin.ModelAdmin):
    list_display = ('exit_id', 'item', 'exit_date', 'exit_destination', 'exit_note')
admin.site.register(Exit, ExitAdmin)


class ExitInline(admin.StackedInline):
    model = Exit
    extra = 1


class LoanInAdmin(admin.ModelAdmin):
    list_display = ('loan_in_id', 'item', 'loan_in_date', 'lender', 'return_out_date', 'loan_in_note')
admin.site.register(LoanIn, LoanInAdmin)


class LoanInInline(admin.StackedInline):
    model = LoanIn
    extra = 1


class LoanOutAdmin(admin.ModelAdmin):
    list_display = ('loan_out_id', 'item', 'loan_out_date', 'borrower', 'return_in_date', 'loan_out_note')
admin.site.register(LoanOut, LoanOutAdmin)


class LoanOutInline(admin.StackedInline):
    model = LoanOut
    extra = 1


class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('picture', 'item')


class ItemPhotoInline(admin.StackedInline):
    model = ItemPhoto
    extra = 1
admin.site.register(ItemPhoto)


admin.site.register(UserProfile)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'identification', 'production', 'location', 'usage', 'description')
    inlines = [EntryInline, ExitInline, LoanInInline, LoanOutInline, ItemPhotoInline]
admin.site.register(Item, ItemAdmin)