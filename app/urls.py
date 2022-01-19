from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, CustomerRegistrationForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    # path for class based view
    path('', views.ProductView.as_view(), name='home'),

    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='product-detail'),

    path('cart/', views.show_cart, name='showcart'),

    path('preorder/', views.preorder, name='preorder'),

    path('search/', views.search, name='search'),

    path('pluscart/', views.plus_cart),

    path('minuscart/', views.minus_cart), 

    path('removecart/', views.remove_cart),

    path('removepreorder/', views.remove_preorder),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('add-to-preorder/', views.add_to_preorder, name='add-to-preorder'),

    path('buy/', views.buy_now, name='buy-now'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),

    path('orders/', views.orders, name='orders'),

    path('trousers/', views.trousers, name='trousers'),

    path('jackets/', views.jackets, name='jackets'),


    path('shoes/', views.shoes, name='shoes'),

    path('onepiece/', views.onepiece, name='onepiece'),
    path('ladies_pants/', views.ladies_pants, name='ladies_pants'),
    path('ladies_shoes/', views.ladies_shoes, name='ladies_shoes'),
    path('tops/', views.tops, name='tops'),

#     path('mobile/<slug:data>', views.mobile, name='mobiledata'),

#     path('laptop/<slug:data>', views.laptop, name='laptopdata'),

     path('checkout/', views.checkout, name='checkout'),
     path('paymentdone/', views.payment_done, name='paymentdone'),

    # view is not created for login, in built authentication consists of login and logout as well
    path('accounts/login/', auth_views.LoginView.as_view
         (template_name='app/login.html', authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # success url is given to redirect to given url after success
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
                                                                  form_class=MyPasswordChangeForm, success_url="/passwordchangedone/"), name='passwordchange'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="app/password_reset.html", form_class=MyPasswordResetForm), name="password_reset"),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name="app/password_reset_done.html"), name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
         template_name="app/password_reset_confirm.html", form_class=MySetPasswordForm), name="password_reset_confirm"),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name="app/password_reset_complete.html"), name="password_reset_complete"),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
         template_name="app/passwordchangedone.html"), name="passwordchangedone"),

    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),


    path('tshirts/', views.tshirts, name='tshirts'),
    path('jeans/', views.jeans, name='jeans'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
