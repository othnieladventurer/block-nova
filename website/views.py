from django.shortcuts import render, redirect
from django.contrib import messages
from .coinbase_client import get_coinbase_client
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    return render(request, 'website/index.html')




@login_required
def dashboard(request):
    return render(request, 'website/dashboard/dashboard.html')





@login_required
def buy_crypto(request):
    # Build absolute callback URL dynamically
    callback_url = request.build_absolute_uri("/coinbase/callback/")

    return render(request, "website/dashboard/buy_crypto.html", {
        "callback_url": callback_url
    })




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


