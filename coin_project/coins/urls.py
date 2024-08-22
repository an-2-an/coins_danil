from django.urls import path
from . import views


app_name = 'coins'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sign/out/', views.signout, name='sign-out'),
    path('sign/in/', views.signin, name='sign-in'),
    path('coin/<int:pk>/', views.CoinDetailView.as_view(), name='coin-detail'),
    path('offer/detail/', views.offer_detail, name='offer-detail'),
    path('coin/<int:pk>/offer/', views.CoinMakeOfferView.as_view(), name='coin-make-offer'),
    path('make/offer/', views.make_offer, name='make-offer'),
    # path('user/offers/', views.OfferByUserListView.as_view(), name='user-offers'),
    # path('user/offers/', views.offers_by_user, name='user-offers'),
    path('user/offers/', views.multi_offers_by_user, name='user-offers'),
    path('offer/<int:pk>/cancel/', views.cancel_offer, name='remove-offer'),
    # path('offer/<int:pk>/accept/', views.accept_offer, name='accept-offer'),
    path('offer/<int:pk>/accept/', views.accept_multi_offer, name='accept-multi-offer'),
    path('create/account/page/', views.CreateUserView.as_view(), name='create-account-page'),
    path('create/account/new/', views.create_new_account, name='create-new-account'),
    path('user/cabinet/<int:pk>/', views.UserCabinetView.as_view(), name='user-cabinet'),
    path('coin/change/status/', views.coin_change_status, name='coin-change-status'),
    path('continent/<int:pk>/', views.ContinentDetailView.as_view(), name='continent-detail'),
    path('country/<int:pk>/', views.CountryDetailView.as_view(), name='country-detail'),
    path('coins/send/', views.CoinsToSendListView.as_view(), name='coins-to-send'),
    path('coin/sended/', views.coin_sended, name='coins-sended'),
    path('user/mailbox/<int:pk>/', views.MailBox.as_view(), name='user-mail-box'),
    path('message/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('message/create/<int:pk>/', views.create_new_message, name='create-new-message'),
    path('message/cabinet/create/<int:pk>/', views.message_from_cabinet, name='message-from-cabinet'),
    path('multi/offer/<int:pk>/', views.multi_offer_view, name='multi-offer'),
    path('multi/offer/create/', views.create_new_multi_offer, name='create-multi-offer'),
    path('multi_offer/cancel/<int:pk>/', views.cancel_multi_offer, name='cancel-multi-offer'),

]