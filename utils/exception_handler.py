from rest_framework.views import exception_handler
def _handle_authentification_error(exc,context,response):
    response.data={
        'error':'Veuillez vous connecter à votre compte pour continuer!!',
        'status_code': response.status_code
    }
    return response
def custom_exception_handler(exc, context):
    handlers={
        'NotAuthenticated':_handle_authentification_error
    }
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    exception_class=exc.__class__.__name__
    # list_pas_vendeur=["StoreImageCreateViewSet" , "AprodCreateViewSet", "AprodUpdateViewSet" , "AprodRetreiveViewSet" , "AprodListViewSet" , "AprodDestroyViewSet"]
    # list_ne_pas_son_magasin=["StoreImageUpdateViewSet" , "StoreImageDestroyViewSet" , "StoreDestroy" , "ProductImageCreateViewSet" , "ProductImageUpdateViewSet"  , "ProductUpdate" ,"ProductDestroy" , "ProductImageDestroyViewSet"]

    
    # Now add the HTTP status code to the response.
    if response is not None:
        print(context)
        print("***********************")
        print(str(exception_class))
        # print(exception_class)
        # if str(exception_class) =='NotAuthenticated':
        #     return handlers['NotAuthenticated'](exc,context,response)

        if "StoreImageUpdateViewSet" or "StoreImageDestroyViewSet" or "ProductImageCreateViewSet"or "ProductImageUpdateViewSet" or "ProductUpdate" or "ProductDestroy" or "ProductImageDestroyViewSet" in  str(context['view']):
            print("*********** 2 * *******")
            print(str(exception_class))
            print(context)
            response.data={
            'message':"Vous ne pouvez pas accéder à cette page puisque vous ne possédez pas ce magasin!",
            'status_code':response.status_code
            }
        if str(exception_class) =='NotAuthenticated':
            print("*********** 5 * *******")
            return handlers['NotAuthenticated'](exc,context,response)
        elif "OrderCreateViewSet" in str(context['view']):
            print("*********** 3 * *******")
            print(str(exception_class))
            print(context)
            response.data={
            'message':"Cher client, vous devez créer un profil pour que vous puissiez passer une commande!",
            'status_code':response.status_code
            }
        elif "CreateDemandeRetour" in str(context['view']):
            print("*********** 4 * *******")
            print(str(exception_class))
            print(context)
            response.data={
            'message':"Cher client pour que vous puissiez passer une demande de retour d'un ou plusieurs produits vous devez au minimum passer une commande!",
            'status_code':response.status_code
            }


    return response

    


