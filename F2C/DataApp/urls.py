from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm
# from django.contrib.auth.decorators import user_passes_test
# from .views import is_dashboard_user
urlpatterns = [
    # path('', views.home),L
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
         form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(
        template_name='app/passwordchangedone.html'), name='passwordchangedone.html'),
    path('custlogin/', views.customerlogin, name='login'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
    #      authentication_form=LoginForm), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cust_logout/', views.cust_logout, name='logout'),
    path('search/',views.search,name='search'),
    

    
    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),





    # path('login/',auth_views.LoginView.as_view(template_name='app/flogin.html',authentication_form=FLoginForm), name='Farmerlogin'),
#     path('dashboard/', user_passes_test(is_dashboard_user)(views.dashboard), name='dashboard'),

    path('fhome/', views.farmerRegistration.as_view(), name='farmerRegistration'),
    path('flogin/', views.farmerlogin, name='farmerlogin'),
    path('sellerHome/', views.sellerHome, name='sellerHome'),
    path('farmhome/',views.farmerhome, name='farmerhome'),
    path('addproduct/', views.addproducts, name='addproducts'),
    path('flogout/', views.user_logout, name='user_logout'),
    path('custorders/', views.orderdproducts, name='orderdproducts'),
    path('dispatched/<int:id>/',views.dispatched, name = 'dispatched'),
    path('allorders/',views.all_orders, name = 'allorders'),
    path('<int:id>/', views.update_data, name='updatefarmer'),
    path('deletefarmer/<int:id>', views.delete_data, name='deletefarmer'),
    path('custfarm/', views.custandfarmregister, name='custfarm'),
    
    


    # payment
    path("continue/<totalamount>/", views.pay, name="continue"),
    path("payment/", views.order_payment, name="payment"),
    path("razorpay/callback/", views.callback, name="callback"),
    path("success/",views.callback),

   # path("feedback/",views.feedback_view,name="feedback"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
