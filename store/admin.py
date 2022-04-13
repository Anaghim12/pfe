from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from tags.models import TaggedItem
from . import models 
from django.contrib.contenttypes.admin import GenericTabularInline

#costom filter
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'  #tiitre de filtre
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low') #on voit <10 fil filter 
        ]
	#logic filtering (we want to see product with low inventory)
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

class TagInline(GenericTabularInline):
    model = TaggedItem
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inline =[TagInline]
    autocomplete_fields = ['collection','store']
    #le slug est auto-generated
    # prepopulated_fields = {
    #     'slug': ['title']
    # }
    #this a custom action we added
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status','store','inventory','is_active']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
#creating custom actions: this action will reset the inventory of the selected product to 0
    @admin.action(description='Clear inventory')
    #request represent the current http request, queryset contain the object the user has selected 
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        # to show a message to a user
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS
        )
# @admin.register(models.StoreWishList)
# class StoreWishListAdmin(admin.ModelAdmin):
#     list_display = ['user','note']

@admin.register(models.ProdWishList)
class ProdWishListAdmin(admin.ModelAdmin):
    list_display = ['username','created_at']
    autocomplete_fields = ['user']
    list_select_related =['user']
    search_fields = ['user']
    # def user_first_name(self, ProdWishList):
    #     return ProdWishList.user.first_name

@admin.register(models.ProdItemWishList)
class ProdItemWishListAdmin(admin.ModelAdmin):
    list_display = ['username','products','note']
    autocomplete_fields = ['user','products']
    list_select_related =['user']
    search_fields = ['user']

# store wishlist
@admin.register(models.StoreWishList)
class StoreWishListAdmin(admin.ModelAdmin):
    list_display = ['username','created_at']
    autocomplete_fields = ['user']
    list_select_related =['user']
    search_fields = ['user']


@admin.register(models.StoreItemWishList)
class StoreItemWishListAdmin(admin.ModelAdmin):
    list_display = ['username','store','note']
    autocomplete_fields = ['user','store']
    list_select_related =['user']
    search_fields = ['user']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title']
    search_fields = ['title']
    # prepopulated_fields = {
    #     'slug': ['title']
    # }


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name','user','order_count','membership']
    search_fields = ['store_name']
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id']
#orders
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    #inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','product','quantity','unit_price']


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']
@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image']

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership', 'order_count',]
    list_editable = ['membership']
    list_per_page = 10
    # auth : customer profile
    list_select_related =['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

   
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
# reviews
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product','name','description','date']

#store Reviews
@admin.register(models.StoreReview)
class StoreReviewAdmin(admin.ModelAdmin):
    list_display = ['store','description','date']
#store Reviews
@admin.register(models.SubCollection)
class SubCollectionAdmin(admin.ModelAdmin):
    list_display = ['title','slug','is_active','collection']
    # prepopulated_fields = {
    #     'slug': ['title']
    # }