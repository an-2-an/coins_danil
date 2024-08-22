from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth import logout, login, authenticate

from .models import *
from .forms import *

class IndexView(TemplateView):
    template_name = 'coins/index.html'
    extra_context = {
        "coin_list": Coin.objects.filter(status='a'),
        "continent_list": Continent.objects.order_by("name"),
    }
    
class CoinDetailView(DetailView):
    model = Coin
    extra_context = {
        'form': MessageForm(),

    }

    

def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        login(request, user) 
    return HttpResponseRedirect(reverse('coins:index'))

       
def signout(request):
    # add_countries()
    logout(request) 
    return HttpResponseRedirect(reverse('coins:index'))


def offer_detail(request):
    coin_id = request.POST.get('coin_id')
    return HttpResponseRedirect(reverse('coins:coin-make-offer', kwargs={"pk": coin_id}))

def user_cabinet_view(request, pk):
    owner = get_object_or_404(User, id=pk)
    user_offers = Offer.objects.filter(author=owner)
    multi_offers = MultiOffer.objects.filter(author=owner)

    context = {
        'owner': owner,
        'user_offers': user_offers,
        'multi_offers': multi_offers,
    }

    return render(request, 'coins/user_cabinet.html', context)

class CoinMakeOfferView(DetailView):
    model = Coin
    template_name = 'coins/coin_make_offer.html'

def make_offer(request):
    coin_to_get_id = request.POST.get('coin_to_get_id')
    coin_to_give_id = request.POST.get('coin_to_give_id')
    if coin_to_get_id and coin_to_give_id:        
        coin_to_get = Coin.objects.get(id=coin_to_get_id)
        coin_to_give = Coin.objects.get(id=coin_to_give_id)          
        new_offer = Offer(
            coin_to_get=coin_to_get,
            coin_to_give=coin_to_give,
            author = coin_to_give.owner,
            responder=coin_to_get.owner,
            )
        new_offer.save()

       
    return HttpResponseRedirect(reverse('coins:index'))

# class OfferByUserListView(ListView):
#     model = Offer
#     template_name = 'coins/ofers_by_user.html'
    
def offers_by_user(request):
    context = {
        'object_list': Offer.objects.filter(responder=request.user, status='c')
    }
    return render(request=request, template_name="coins/ofers_by_user.html", context=context)

def multi_offers_by_user(request):
    context = {
        'object_list': MultiOffer.objects.filter(responder=request.user, status='c')
    }
    return render(request=request, template_name="coins/ofers_by_user.html", context=context)

def accept_multi_offer(request, pk):
    multi_offer = MultiOffer.objects.get(id=pk)
    coins_to_get = multi_offer.coins_to_get.all()
    coins_to_give = multi_offer.coins_to_give.all()
    for coin_to_get in coins_to_get:        
        coin_to_get.owner = multi_offer.author
        coin_to_get.status = 'e'
        coin_to_get.save()
    for coin_to_give in coins_to_give:   
        coin_to_give.owner = multi_offer.responder
        coin_to_give.status = 'e'  
        coin_to_give.save() 
    multi_offer.status = 'd'    
    multi_offer.save()
    return HttpResponseRedirect(reverse('coins:index'))

def cancel_multi_offer(request, pk):
    multi_offer = get_object_or_404(MultiOffer, pk=pk)
    if request.method == 'POST':
        multi_offer.delete()
    return redirect('coins:user-cabinet', pk=request.user.id)
    # return render(request, 'coins/cancel_multi_offer.html', {'multi_offer': multi_offer})
    
def cancel_offer(request, pk):
    offer = Offer.objects.get(id=pk)
    offer.delete()
    return HttpResponseRedirect(reverse('coins:index'))

def accept_offer(request, pk):
    offer = Offer.objects.get(id=pk)
    coin_to_get = offer.coin_to_get
    coin_to_give = offer.coin_to_give
    coin_to_get.owner = offer.author
    coin_to_get.status = 'e'
    coin_to_get.save()
    coin_to_give.owner = offer.responder
    coin_to_give.status = 'e'  
    coin_to_give.save()     
    offer.status = 'd'    
    offer.save()
    return HttpResponseRedirect(reverse('coins:index'))

class CreateUserView(TemplateView):
    template_name = 'coins/create_account.html'
    extra_context = {
        'form': MyUserCreationForm(),

    }

def create_new_account(request):
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    postcode = request.POST.get('postcode')
    addres = request.POST.get('addres')
    city =  request.POST.get('city')

    if password1 == password2:
        new_user = User.objects.create_user(username=username, password=password2)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()        
        UserProfile.objects.create(user=new_user, phone=phone, postcode=postcode, addres=addres, city=city, user_pic=request.FILES.get('user_picture'))
        login(request, new_user)


    return HttpResponseRedirect(reverse('coins:index'))

class UserCabinetView(DetailView):
    model = User
    template_name = 'coins/user_cabinet.html'
    context_object_name = 'owner'
    extra_context = {
        'form': MessageForm(),
    }


def coin_change_status(request):
    pk = request.POST.get('pk')
    status = request.POST.get('status')
    coin = Coin.objects.get(id=pk)
    if status == 'a' or status == 'w':        
        coin.status = status
        coin.save()
    return HttpResponseRedirect(reverse('coins:user-cabinet', kwargs={"pk":coin.owner.id}))

class ContinentDetailView(DetailView):
    model = Continent

class CountryDetailView(DetailView):
    model = Country

class CoinsToSendListView(ListView):
    model = Coin
    queryset = Coin.objects.filter(status='w')
    template_name = 'coins/coins_to_send.html'

def coin_sended(request):
    pk = request.POST.get('pk')
    coin = Coin.objects.get(id=pk)
    coin.status = 's'
    coin.save()
    new_message = Message(
        text = f'Coin(s) have been sent to you: {coin}\nthis message was generated automatically' ,
        author = User.objects.get(id=1),
        recipient = coin.owner
    )
    new_message.save()
    return HttpResponseRedirect(reverse('coins:coins-to-send'))

class MailBox(DetailView):
    model = User
    template_name = 'coins/mail_box.html'
    context_object_name = 'owner'

class MessageDetailView(DetailView):
    model = Message
    
    def get_object(self, queryset=None):
        object = super().get_object(queryset=queryset)
        if self.request.user == object.recipient:
            object.is_read = True
            object.save()
        return object

def create_new_message(request, pk):
    author_id = request.POST.get('author_id')
    recipient_id = request.POST.get('recipient_id')    
    f = MessageForm(request.POST)
    new_message = f.save(commit=False)
    new_message.author_id = author_id
    new_message.recipient_id = recipient_id
    new_message.save()
    return HttpResponseRedirect(reverse('coins:coin-detail', args=[pk]))

def message_from_cabinet(request, pk):
    author_id = request.POST.get('author_id')
    recipient_id = request.POST.get('recipient_id')    
    f = MessageForm(request.POST)
    new_message = f.save(commit=False)
    new_message.author_id = author_id
    new_message.recipient_id = recipient_id
    new_message.save()
    return HttpResponseRedirect(reverse('coins:user-cabinet', args=[pk]))

def multi_offer_view(request, pk):
    recipient = User.objects.get(id=pk)
    author = request.user
    context = {
        'recipient': recipient,
    }
    return render(
        request=request, 
        template_name='coins/multi_offer.html',
        context=context
    )

def create_new_multi_offer(request):
    coins_to_get_ids = request.POST.getlist('coins_to_get_ids')
    coins_to_get = Coin.objects.filter(id__in=coins_to_get_ids)
    coins_to_give_ids = request.POST.getlist('coins_to_give_ids')
    coins_to_give = Coin.objects.filter(id__in=coins_to_give_ids)
    responder_id = request.POST.get('recipient_id')
    responder = User.objects.get(id=responder_id)
    new_multi_offer = MultiOffer(
        author=request.user,
        responder=responder,
    )
    new_multi_offer.save()
    new_multi_offer.coins_to_get.add(*coins_to_get)
    new_multi_offer.coins_to_give.add(*coins_to_give)
    return HttpResponseRedirect(reverse('coins:index'))