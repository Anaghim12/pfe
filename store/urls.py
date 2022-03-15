from django.urls import path
from . import views
#viewsets
from rest_framework.routers import SimpleRouter
from pprint import pprint

#implémentation with viewsets
# router =SimpleRouter()
# router.register('products',views.ProductViewSet)
# router.register('collections',views.CollectionViewSet)
# pprint(router.urls)


# M1: implémentation with function based views voir ce qui est commentées + M2 : implémentation with class based views non pas commentées
urlpatterns =[
    # path('products/',views.product_list),
    path('products/',views.ProductList.as_view()),
    path('products/add/',views.ProductCreate.as_view()),
    path('products/<int:pk>',views.ProductRetreive.as_view()),
    path('products/destroy/<int:pk>',views.ProductDestroy.as_view()),
    path('products/update/<int:pk>',views.ProductUpdate.as_view()),     
    # path('collections/<int:pk>',views.collection_detail, name='collection_detail'),
    path('collections/',views.CollectionList.as_view()),
    path('collections/add/',views.CollectionCreate.as_view()),
    path('collections/<int:pk>',views.CollectionRetreive.as_view()),
    path('collections/destroy/<int:pk>',views.CollectionDestroy.as_view()),
    path('collections/update/<int:pk>',views.CollectionUpdate.as_view()), 
    #auth by sorra's method (not complete)
    path('customers/',views.CustomerCreateViewSet.as_view()),
    path('customers/<int:pk>',views.CustomerRetreiveUpdateViewSet.as_view()),
    #auth to get the current user(authorized)Get +Put
    path('customers/me',views.CustomerCurrent),
    #manage user 
    path('users/',views.CustomerList.as_view()),
    path('users/add/',views.CustomerCreate.as_view()),
    path('users/<int:pk>',views.CustomerRetrieve.as_view()),
    path('users/update/<int:pk>',views.CustomerUpdate.as_view()),  
    # manage product images
    path('products/<int:product_pk>/images/add',views.ProductImageCreateViewSet.as_view()),
    path('products/<int:product_pk>/images/update/<int:pk>',views.ProductImageUpdateViewSet.as_view()),
    path('products/<int:product_pk>/images/<int:pk>',views.ProductImageRetrieveViewSet.as_view()),
    path('products/<int:product_pk>/images/',views.ProductImageListViewSet),
    path('products/<int:product_pk>/images/destroy/<int:pk>',views.ProductDestroy.as_view()),
    #manage cart
    path('carts/add',views.CartCreateViewSet.as_view()),
    path('carts/<pk>',views.CartRetrieveViewSet.as_view()),
    path('carts/<pk>/destroy',views.CartDestroyViewSet.as_view()),
    #manage cartitem
    path('carts/<cart_pk>/items/<pk>',views.ItemCartRetreiveViewSet.as_view()),
    path('carts/<cart_pk>/items/<pk>/destroy',views.ItemCartDestroyViewSet.as_view()),
    path('carts/<cart_pk>/items/<pk>/update',views.ItemCartUpdateViewSet.as_view()),
    path('carts/<cart_pk>/items/',views.ItemCartListViewSet.as_view()),
    path('carts/items/add',views.ItemCartCreateViewSet.as_view()),
    #manage orders
    path('orders/',views.OrderListViewSet.as_view()),
    path('orders/add/',views.OrderCreateViewSet.as_view()),
    path('orders/<int:pk>/',views.OrderRetreiveViewSet.as_view()),
    path('orders/<int:pk>/destory/',views.OrderDestroyViewSet.as_view()),
    path('orders/<int:pk>/update/',views.OrderUpdateViewSet.as_view()),
    #manage slide
    path('slide/',views.SlideListViewSet.as_view()),
    path('slide/add/',views.SlideCreateViewSet.as_view()),
    path('slide/<int:pk>/destory/',views.SlideDestroyViewSet.as_view()),
    path('slide/<int:pk>/update/',views.SlideUpdateViewSet.as_view()),
    #manage reviews
    path('reviews/',views.ReviewListViewSet.as_view()),
    path('reviews/add/',views.ReviewCreateViewSet.as_view()),
    # path('reviews/<int:pk>/destory/',views.ReviewDestroyViewSet.as_view()),
    # path('reviews/<int:pk>/update/',views.ReviewUpdateViewSet.as_view()),








]