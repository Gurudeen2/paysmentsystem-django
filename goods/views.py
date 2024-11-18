from django.shortcuts import render
from django.conf import settings
from payments.models import Payment
from goods.models import Goods
from addtocart.models import AddToCart
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



# Create your views here.
@login_required(login_url='login')
def addtocart(request, id):
    product = Goods.objects.get(pk=id)
    addcart = AddToCart.objects.create(
        user=request.user, 
        product_name = product.name,
        price = product.price,
        image = product.image,
        ordered = True

        
        )
    addcart.save()



    return render(request, 'index.html')



def index(request):
    goods = Goods.objects.all().order_by('-name')
  
    paginator = Paginator(goods, 10) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'products': page_obj})

@login_required(login_url='login')
def order(request):
    goods = Goods.objects.all()
    if request.method == "POST":
        email = request.POST['email']
        id = request.POST['mytext']
        price = Goods.objects.get(pk=id)
        amount = price.price

        
      
        pk = settings.PAYSTACK_PUBLIC_KEY
        
        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()
        
        context = {
			'payment': payment,
			'field_values': request.POST,
			'paystack_pub_key': pk,
			'amount_value': payment.amount_value(),
		}
        return render(request, 'make_payment.html', context)
    return render(request, 'goods.html', {'goods':goods})