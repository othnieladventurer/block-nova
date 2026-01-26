from django.shortcuts import render, redirect
from django.contrib import messages
from .coinbase_client import generate_onramp_url



# Create your views here.

def index(request):
    return render(request, 'website/index.html')





def dashboard(request):
    return render(request, 'website/dashboard/dashboard.html')





def buy_crypto(request):
    if request.method == "POST":
        asset = request.POST.get("asset")
        amount = request.POST.get("amount")

        if not asset or not amount:
            messages.error(request, "Invalid form submission.")
            return redirect("website:buy")

        onramp_url = generate_onramp_url(asset, amount)
        return redirect(onramp_url)

    return render(request, "website/dashboard/buy_crypto.html")


def sell_crypto(request):
    return render(request, 'website/dashboard/sell_crypto.html')







def withdraw_crypto(request):
    return render(request, 'website/dashboard/withdraw_crypto.html')


