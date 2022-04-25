from django.urls import path
from . import views

# M1: implémentation with function based views voir ce qui est commentées + M2 : implémentation with class based views non pas commentées
urlpatterns =[
    # path('products/',views.product_list),
    path('products/',views.ProductList.as_view(),name="product_list"),
    path('products/add/',views.ProductCreate.as_view()),
    path('products/<int:pk>',views.ProductRetreive.as_view(),name='product-detail'),
    path('products/destroy/<int:pk>',views.ProductDestroy.as_view()),
    path('products/update/<int:pk>',views.ProductUpdate.as_view()),     
    # path('collections/<int:pk>',views.collection_detail, name='collection_detail'),
    path('collections/',views.CollectionList.as_view()),
    path('collections/add/',views.CollectionCreate.as_view()),
    path('collections/<int:pk>',views.CollectionRetreive.as_view()),
    path('collections/destroy/<int:pk>',views.CollectionDestroy.as_view()),
    path('collections/update/<int:pk>',views.CollectionUpdate.as_view()), 
    # manage subcollection
    path('subcollections/add/',views.SubCollectionCreate.as_view()),
    path('subcollections/<int:pk>',views.SubCollectionRetreive.as_view()),
    path('subcollections/update/<int:pk>',views.SubCollectionUpdate.as_view()), 
    #auth to get the current user profile(authorized)Get +Put
    path('customers/me',views.CustomerCurrent),
    #manage user 
    path('users/',views.CustomerList.as_view()),
    # path('users/add/',views.CustomerCreate.as_view()),
    path('users/<int:pk>',views.CustomerRetrieve.as_view()),
    path('users/update/<int:pk>',views.CustomerUpdate.as_view()),
    path('users/destroy/<int:pk>',views.CustomerDestroy.as_view()),  
    # manage product images
    path('products/<int:product_pk>/images/add',views.ProductImageCreateViewSet.as_view()),
    path('products/<int:product_pk>/images/update/<int:pk>',views.ProductImageUpdateViewSet.as_view()),
    path('products/<int:product_pk>/images/<int:pk>',views.ProductImageRetrieveViewSet.as_view()),
    # path('products/<int:product_pk>/images/',views.ProductImageListViewSet),#problème ici
    path('products/<int:product_pk>/images/destroy/<int:pk>',views.ProductImageDestroyViewSet.as_view()),
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
    #manage the user reviews of product
    path('products/<int:product_pk>/reviews/add',views.ReviewCreateViewSet.as_view()),
    path('products/<int:product_pk>/reviews/update/<int:pk>',views.ReviewUpdateViewSet.as_view()),
    path('products/reviews/',views.ReviewListViewSet.as_view()),
    path('products/<int:product_pk>/reviews/destroy/<int:pk>',views.ReviewDestroyViewSet.as_view()),
    #manage the user reviews of store
    path('stores/<int:store_pk>/reviews/add',views.StoreCreateViewSet.as_view()),
    path('stores/<int:store_pk>/reviews/update/<int:pk>',views.StoreUpdateViewSet.as_view()),
    path('stores/reviews/',views.StoreListViewSet.as_view()),
    path('stores/<int:store_pk>/reviews/destroy/<int:pk>',views.StoreDestroyViewSet.as_view()),
    #search and filters 
    path('products/search/',views.SearchProduct.as_view()),
    #manage productWishList
    path('wishprod/add',views.ProdWishListCreateViewSet.as_view()),
    path('wishprod/',views.ProdWishListListViewSet.as_view()),
    path('wishprod/<int:pk>',views.ProdWishListRetreiveViewSet.as_view()),
    path('wishprod/destroy/<int:pk>',views.ProdWishListDestroyViewSet.as_view()),
    #manage productItemWishList
    #path('wishprod/items/<pk>',views.ItemCartRetreiveViewSet.as_view()),
    path('wishprod/items/<pk>/destroy',views.ProdItemWishListDestroyViewSet.as_view()),
    path('wishprod/items/<pk>/update',views.ProdItemWishListUpdateViewSet.as_view()),
    path('wishprod/items/',views.ProdItemWishListListViewSet.as_view()),
    path('wishprod/items/add',views.ProdItemWishListCreateViewSet.as_view()),
    #manage storeWishList
    path('wishstore/add',views.StoreWishListCreateViewSet.as_view()),
    path('wishstore/',views.StoreWishListListViewSet.as_view()),
    path('wishstore/<int:pk>',views.StoreWishListRetreiveViewSet.as_view()),
    path('wishstore/destroy/<int:pk>',views.StoreWishListDestroyViewSet.as_view()),
    #manage storeItemWishList
    path('wishstore/items/<pk>/destroy',views.StoreItemWishListDestroyViewSet.as_view()),
    path('wishstore/items/<pk>/update',views.StoreItemWishListUpdateViewSet.as_view()),
    path('wishstore/items/',views.StoreItemWishListListViewSet.as_view()),
    path('wishstore/items/add',views.StoreItemWishListCreateViewSet.as_view()),
    #manage store
    path('stores/',views.StoreList.as_view()),
    # path('stores/add/',views.StoreCreate.as_view()),
    path('stores/<int:pk>',views.StoreRetreive.as_view()),
    path('stores/destroy/<int:pk>',views.StoreDestroy.as_view()),
    path('stores/update/<int:pk>',views.StoreUpdate.as_view()),     
    # manage store images
    path('stores/<int:store_pk>/images/add',views.StoreImageCreateViewSet.as_view()),
    path('stores/<int:store_pk>/images/update/<int:pk>',views.StoreImageUpdateViewSet.as_view()),
    #path('stores/<int:store_pk>/images/<int:pk>',views.StoreImageRetrieveViewSet.as_view()),
    path('stores/<int:store_pk>/images/',views.StoreImageListViewSet),#problème ici
    path('stores/<int:store_pk>/images/destroy/<int:pk>',views.StoreDestroy.as_view()),
    # le vendeur peut voir ces produits
    path('myproducts/',views.MyProductList.as_view()),

    # manage Aprod
    path('products/<int:product_pk>/aprod/add',views.AprodCreateViewSet.as_view()),
    path('products/<int:product_pk>/aprod/update/<int:pk>',views.AprodUpdateViewSet.as_view()),
    path('products/<int:product_pk>/aprod/<int:pk>',views.AprodRetreiveViewSet.as_view()),
    path('products/<int:product_pk>/aprod/',views.AprodListViewSet.as_view()),
    path('products/<int:product_pk>/aprod/destroy/<int:pk>',views.AprodDestroyViewSet.as_view()),




]