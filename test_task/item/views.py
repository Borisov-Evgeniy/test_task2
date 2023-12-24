from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import stripe
from .models import Item, Order, Discount, Tax
from decouple import config

stripe.api_key = config('STRIPE_SECRET_KEY')


def item_list(request):
    items = Item.objects.all()
    discounts = Discount.objects.all()
    taxes = Tax.objects.all()
    return render(request, 'test_task/item_detail.html', {'items': items, 'discounts': discounts, 'taxes': taxes})


def get_checkout_session_id(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),  # Amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(item.get_absolute_url()),
        cancel_url=request.build_absolute_uri(item.get_absolute_url()),
    )

    return JsonResponse({'session_id': session.id})


def get_item_page(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    discounts = Discount.objects.all()
    taxes = Tax.objects.all()
    session_id_url = reverse('get_checkout_session_id', args=[item_id])
    return render(request, 'test_task/item_detail.html',
                  {'item': item, 'discounts': discounts, 'taxes': taxes, 'session_id_url': session_id_url})


def create_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    order = Order.objects.create(user=request.user)
    order.items.add(item)

    order.discount = Discount.objects.first()
    order.tax = Tax.objects.first()

    order.save()

    return redirect('order_detail', order_id=order.id)


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'test_task/order_detail.html', {'order': order})