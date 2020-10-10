from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .models import Item, OrderItem, Order, User, Payment, Checkout
from django.http import HttpResponseRedirect
from .forms import CheckoutForm
import stripe
from django.contrib.auth.decorators import login_required

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


# Create your views here.
def homepage(request):
	items = Item.objects.all()
	if request.user.is_authenticated:
		orders = Order.objects.filter(user = request.user, ordered = False)
		if orders:
			order = orders[0]
			sadrzaj = {'items':items,'order':order}
		else:
			sadrzaj = {'items':items}
	else:
		sadrzaj = {'items':items}
		
			
	return render(request, 'core/index.html',sadrzaj)
	
def shop(request):
	items = Item.objects.all()
	if request.user.is_authenticated:
		orders = Order.objects.filter(user = request.user, ordered = False)
		if orders:
			order = orders[0]
			sadrzaj = {'items':items,'order':order}
		else:
			sadrzaj = {'items':items}
	else:
		sadrzaj = {'items':items}
	return render(request, 'core/shop.html', sadrzaj)

def shop_category(request,category):
	items = Item.objects.filter(category = category)
	if request.user.is_authenticated:
		orders = Order.objects.filter(user = request.user, ordered = False)
		if orders:
			order = orders[0]
			sadrzaj = {'items':items,'order':order}
		else:
			sadrzaj = {'items':items}
	else:
		sadrzaj = {'items':items}
		
	return render(request, 'core/shop.html',sadrzaj)
	
@login_required
def cart(request):
	orders = Order.objects.filter(user = request.user, ordered = False)
	if orders:
		order = orders[0]
		sadrzaj = {'order':order}
	else:
		sadrzaj = {}
	return render(request, 'core/cart.html',sadrzaj)
	
@login_required
def add_to_cart(request,slug):
	item = Item.objects.get(slug = slug)
	orders = Order.objects.filter(user = request.user, ordered = False)
	if orders:
		order = orders[0]
		qty = request.POST.get('quantity')
		orderitem = OrderItem.objects.create(item = item, user = request.user,quantity = qty)
		order.items.add(orderitem)
		return HttpResponseRedirect(reverse('core:product-details',args=[item.slug]))
	else:
		order = Order.objects.create(user = request.user, ordered = False)
		qty = request.POST.get('quantity')
		orderitem = OrderItem.objects.create(item = item, user = request.user,quantity = qty)
		order.items.add(orderitem)
		return HttpResponseRedirect(reverse('core:product-details',args=[item.slug]))
		
	return render(request, 'core/product-details.html')
@login_required
def remove_from_cart(request, slug):
	item = Item.objects.get(slug=slug)
	orderitems = OrderItem.objects.filter(item = item, user = request.user)
	if orderitems:
		orderitem = orderitems[0]
		if orderitem.quantity > 0:
			orderitem.quantity -= 1
			orderitem.save()
		if orderitem.quantity == 0:
			orderitem.delete()
		return HttpResponseRedirect(reverse('core:product-details', args=[item.slug]))
	else:
		return HttpResponseRedirect(reverse('core:product-details', args=[item.slug]))
	
	return render(request, 'core/product-details.html')
		
		

def product_details(request,slug):
	item = Item.objects.get(slug = slug)

	sadrzaj = {'item':item}
	return render(request, 'core/product-details.html',sadrzaj)
	
@login_required	
def checkout(request):
	form = CheckoutForm()
	orders = Order.objects.filter(user = request.user, ordered = False)
	if orders:
		order = orders[0]
		if request.method == 'POST':
			form = CheckoutForm(request.POST)
			if form.is_valid():
				billing = form.save()
				order.billing = billing
				order.save()
				if order.billing.payment_method == 'S':
					messages.success(request, 'Your payment with Stripe was successful.')
					return redirect('core:payment', payment_option = 'stripe')
				else:
					order.ordered  = True
					order.save()
					for item in order.items.all():
						item.ordered = True
						item.save()
					messages.success(request, 'Your order was successful.')
					return redirect('core:index')
		sadrzaj = {'order':order,'form':form}
	else:
		sadrzaj = {'form':form}
		
	return render(request, 'core/checkout.html',sadrzaj)

def search(request):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('core:homepage'))
	else:
		query = request.POST.get('search')
		articles = Item.objects.filter(title__icontains = query)
		if articles:
			sadrzaj = {'articles':articles}
		else:
			sadrzaj = {}
	
	return render(request, 'core/search.html',sadrzaj)
	
@login_required	
def add_to_favourite(request,slug):
	item = Item.objects.get(slug = slug)
	if item:
		user = request.user
		user.favourite_products.add(item)
		user.save()
		return HttpResponseRedirect(reverse('core:product-details', args=[item.slug]))
	else:
		return HttpResponseRedirect(reverse('core:shop'))
	sadrzaj = {'item':item}
	return render(request, 'core/product-details.html',sadrzaj)
@login_required	
def favourite_products(request):
	user = request.user
	if user:
		items = user.favourite_products.all()
		sadrzaj = {'items':items}
	else:
		sadrzaj = {}
	
	return render(request, 'core/favourite-products.html',sadrzaj)

def new_products(request):
	items = Item.objects.filter(new = True)
	if items:
		sadrzaj = {'items':items}
	else:
		sadrzaj = {}
	
	return render(request, 'core/new-products.html',sadrzaj)
@login_required	
def subscribe(request):
	info = request.POST.get('email')
	user = request.user
	if user:
		if user.has_discount == True:
			messages.error(request, "You already have a discount")
			return HttpResponseRedirect(reverse('core:index'))
		else:
			if user.email:
				email = user.email
				if email == info:
					order = Order.objects.get(user = request.user, id = 1, ordered = False)
					if order:
						order.total_fee -= (0.25 * order.total_fee)
						order.save()
						user.has_discount = True
						user.save()
						messages.success(request, 'On first order you have 25% off.')
						return HttpResponseRedirect(reverse('core:index'))
					else:
						user.has_discount = True
						user.save()
						messages.success(request, 'On first order you have 25% off')
						return HttpResponseRedirect(reverse('core:index'))
				else:
					messages.info(request, 'Email address you entered is not the same with the one you registered with')
					return HttpResponseRedirect(reverse('core:index'))
			else:
				user.email = info
				user.has_discount = True
				user.save()
				orders = Order.objects.filter(user = request.user, ordered = False)
				messages.info(request, "Congratulations, you got 25% on your first order")
				return HttpResponseRedirect(reverse('core:index'))
	else:
		return HttpResponseRedirect(reverse('accounts:login'))
		
	return render(request, 'core/index.html')
	
@login_required
def payment(request, payment_option):
	order = Order.objects.filter(user = request.user, ordered = False)[0]
	token = request.POST.get('stripeToken')	
	if request.method == 'POST':
		if request.user.has_discount == True:
			charge = stripe.Charge.create(
				amount=int(order.discount_price()) * 100,
				currency="usd",
				source=token,
				metadata={'order_id': '6735'}
				)
			payment = Payment()
			payment.stripe_charge_id = charge.id
			payment.user = request.user
			payment.amount = charge.amount
			payment.save()
			order.payment = payment
			order.ordered = True
			order.save()
			for item in order.items.all():
				item.ordered = True
				item.save()
			messages.success(request, 'Your order was successful')
			return HttpResponseRedirect(reverse('core:index'))					
		else:
			charge = stripe.Charge.create(
				amount=int(order.total_fee()) * 100,
				currency="usd",
				source=token,
				metadata={'order_id': '6735'}
				)
			payment = Payment()
			payment.stripe_charge_id = charge.id
			payment.user = request.user
			payment.amount = charge.amount
			payment.save()
			order.payment = payment
			order.ordered = True
			order.save()
			for item in order.items.all():
				item.ordered = True
				item.save()	
			messages.success(request, 'Your order was successful')
			return HttpResponseRedirect(reverse('core:index'))				
	
	return render(request, 'core/payment.html')
	
				
			
			
	
