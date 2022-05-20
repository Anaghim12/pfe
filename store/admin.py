from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from tags.models import TaggedItem
from . import models 
from django.contrib.contenttypes.admin import GenericTabularInline

#costom filter

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
                    'store','is_active']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update']
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
    ordering=['created_at']
    # def user_first_name(self, ProdWishList):
    #     return ProdWishList.user.first_name

@admin.register(models.ProdItemWishList)
class ProdItemWishListAdmin(admin.ModelAdmin):
    list_display = ['username','products','note']
    autocomplete_fields = ['user','products']
    list_select_related =['user']
    search_fields = ['user']
    list_filter=['products__title','note']

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
    list_filter=['store__store_name','note']

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'  #tiitre de filtre
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('>1000','élevé'),
            ('<3', 'faible'), #on voit <10 fil filter 
            ('=0','en rupture de stock!')
        ]
	#logic filtering (we want to see product with low inventory)
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '>1000':
            return queryset.filter(inventory__gt=1000)
        elif self.value() == '<3':
            return queryset.filter(inventory__lt=3)
        elif self.value() == '=0':
            return queryset.filter(inventory=0)
@admin.register(models.Aprod)
class AprodAdmin(admin.ModelAdmin):
    list_display = ['slug','inventory','product']
    list_filter = ['product__title','size',InventoryFilter]
    search_fields = ['slug']
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title','slug']
    search_fields = ['title','slug']
    # prepopulated_fields = {
    #     'slug': ['title']
    # }
@admin.register(models.Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['id','slide_image']
    search_fields = ['id','slide_image']

@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name','user','order_count','membership']
    search_fields = ['store_name']
    list_filter=['membership']
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','created_at']
    search_fields = ['id']
    list_filter = ['created_at']
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
    ordering=['placed_at']
    # list_filter=['customer__user__username']

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','product','quantity','unit_price']

@admin.register(models.DemandeRetour)
class DemandeRetourAdmin(admin.ModelAdmin):
    list_display = ['placed_at','num_order','user','date_order','accept','refuse']
    list_filter=['accept','refuse']
    ordering=['placed_at']
@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','quantity']
    list_filter = ['cart__id']
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
    list_filter = ['name', 'note','product__title']
    ordering = ['date']

#store Reviews
@admin.register(models.StoreReview)
class StoreReviewAdmin(admin.ModelAdmin):
    list_display = ['store','description','date']
    list_filter = ['name', 'note','store__store_name']
    ordering = ['date']
#store Reviews
@admin.register(models.SubCollection)
class SubCollectionAdmin(admin.ModelAdmin):
    list_display = ['title','slug','is_active','collection']
    search_fields = ['title','slug']
    # prepopulated_fields = {
    #     'slug': ['title']
    # }