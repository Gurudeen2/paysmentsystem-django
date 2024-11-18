from django.shortcuts import render, redirect
from goods.models import Goods
from addtocart.models import AddToCart
from payments.models import Payment
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.


def attotcart(request, id):
    product = Goods.objects.get(pk=id)
    addcart = AddToCart.objects.create(
        user=request.user, 
        product_name = product.name,
        price = product.price,
        image = product.image,
        ordered = False

        
        )
    addcart.save()


    return redirect('index')


@login_required(login_url='login')
def singlecart(request):
    addtocart = AddToCart.objects.filter(user=request.user).filter(ordered=True)
    totalprice = 0
    for item in addtocart:
        totalprice += item.price


    if request.method == 'POST':

        pk = settings.PAYSTACK_PUBLIC_KEY
        
        payment = Payment.objects.create(amount=totalprice, email=request.user.email, user=request.user)
        payment.save()

        orderedfilter =AddToCart.objects.filter(user=request.user).filter(ordered=False)
        orderedfilter.update(ordered=True)
        

        
        context = {
			'payment': payment,
			'field_values': request.POST,
			'paystack_pub_key': pk,
			'amount_value': payment.amount_value(),
		}
        return render(request, 'make_payment.html', context)
    

    return render(request, 'addtocart.html', {'carts': addtocart, 'totalprice':totalprice})

def deletecart(request, id):
    deleteaddtocart = AddToCart.objects.filter(user=request.user).filter(pk=id)
    deleteaddtocart.delete()
    return redirect('carts')