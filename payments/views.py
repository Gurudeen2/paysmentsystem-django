from django.shortcuts import render, redirect
from .models import Payment
from django.conf import settings
from django.contrib.auth.decorators import login_required
from goods.models import Goods
from django.core.paginator import Paginator



def index(request):
    goods = Goods.objects.all().order_by('-name')

    paginator = Paginator(goods, 10) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'products': page_obj})



@login_required(login_url='login')
def initiate_payment(request):
	if request.method == "POST":
		amount = request.POST['amount']
		email = request.POST['email']

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

	return render(request, 'payment.html')

@login_required(login_url='login')
def verify_payment(request, ref):
	payment = Payment.objects.get(ref=ref)
	verified = payment.verify_payment()

	if verified:
		# user_wallet = UserWallet.objects.get(user=request.user)
		# user_wallet.balance += payment.amount
		# user_wallet.save()
		# print(request.user.username, " funded wallet successfully")
		return render(request, "success.html")
	return render(request, "success.html")