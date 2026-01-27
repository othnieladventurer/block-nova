import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .coinbase_client import get_coinbase_client
from django.contrib.auth.decorators import login_required
from .models import Purchase



# Create your views here.

def index(request):
    return render(request, 'website/index.html')




@login_required
def dashboard(request):
    return render(request, 'website/dashboard/dashboard.html')







@login_required
def buy_crypto(request):
    if request.method == "POST":
        usd_amount = float(request.POST.get("usd_amount", 0))
        crypto_id = request.POST.get("crypto", "bitcoin")
        contact_method = request.POST.get("contact_method")
        whatsapp_number = request.POST.get("whatsapp_number")

        # Validation: if WhatsApp chosen, number must be provided
        if contact_method == "whatsapp" and not whatsapp_number:
            return render(request, "website/dashboard/buy_crypto.html", {
                "error": "WhatsApp number is required if you choose WhatsApp."
            })

        # Call CoinGecko API
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": crypto_id, "vs_currencies": "usd"}
        response = requests.get(url, params=params)
        data = response.json()

        crypto_price = data[crypto_id]["usd"]
        crypto_amount = usd_amount / crypto_price
        fee = 6
        total_charge = usd_amount + fee

        # Save purchase in DB
        Purchase.objects.create(
            user=request.user,
            crypto=crypto_id,
            usd_amount=usd_amount,
            fee=fee,
            total=total_charge,
            crypto_amount=crypto_amount,
            price_at_purchase=crypto_price,
            contact_method=contact_method,
            whatsapp_number=whatsapp_number if contact_method == "whatsapp" else None
        )

        return render(request, "website/dashboard/buy_crypto.html", {
            "success": True
        })

    return render(request, "website/dashboard/buy_crypto.html")





@login_required
def coinbase_callback(request):
    # Coinbase will redirect here with query params like ?status=success&transaction_id=123
    status = request.GET.get("status")
    tx_id = request.GET.get("transaction_id")

    if status == "success":
        # TODO: Save transaction to DB, update user balance, etc.
        return render(request, "website/dashboard/coinbase_success.html", {"tx_id": tx_id})
    else:
        return render(request, "website/dashboard/coinbase_failed.html")





@login_required
def sell_crypto(request):
    return render(request, 'website/dashboard/sell_crypto.html')






@login_required
def withdraw_crypto(request):
    return render(request, 'website/dashboard/withdraw_crypto.html')







def terms_of_use(request):
    return render(request, 'website/terms-of-use.html')






def privacy_policy(request):
    return render(request, 'website/privacy_policy.html')



