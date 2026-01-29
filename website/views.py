import requests
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from .coinbase_client import get_coinbase_client
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from decimal import Decimal




# Create your views here.

def index(request):
    return render(request, 'website/index.html')




@login_required
def dashboard(request):
    # --- BUY TRANSACTIONS ---
    purchases = Purchase.objects.filter(user=request.user).order_by('-created_at')
    total_transactions = purchases.count()
    crypto_purchased = purchases.aggregate(total=Sum("usd_amount"))["total"] or 0
    pending_orders = purchases.filter(status="pending").count()
    sent_orders = purchases.filter(status="sent").count()
    delivered_orders = purchases.filter(status="delivered").count()
    purchases_initial = purchases[:5]  # Show only first 5 initially

    # --- SELL TRANSACTIONS ---
    sell_transactions = SellTransaction.objects.filter(user=request.user).order_by('-created_at')
    total_sell_transactions = sell_transactions.count()
    sell_transactions_initial = sell_transactions[:5]  # Show only first 5 initially

    context = {
        # Buy transactions
        "purchases": purchases_initial,
        "total_transactions": total_transactions,
        "crypto_purchased": crypto_purchased,
        "pending_orders": pending_orders,
        "sent_orders": sent_orders,
        "delivered_orders": delivered_orders,

        # Sell transactions
        "sell_transactions": sell_transactions_initial,
        "total_sell_transactions": total_sell_transactions,
    }

    return render(request, "website/dashboard/dashboard.html", context)






from django.http import JsonResponse

@login_required
def load_more_purchases(request):
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 5))

    purchases = Purchase.objects.filter(user=request.user).order_by('-created_at')[offset:offset+limit]

    data = [
        {
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"),
            "crypto": p.crypto.title(),
            "usd_amount": float(p.usd_amount),
            "status": p.status.title(),
        }
        for p in purchases
    ]
    return JsonResponse({"purchases": data})




# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SellTransaction

@login_required
def load_more_sell_transactions(request):
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 5))

    sells = SellTransaction.objects.filter(
        user=request.user
    ).order_by("-created_at")[offset:offset + limit]

    data = [
        {
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
            "crypto": s.crypto.title(),
            "usd_amount": float(s.usd_amount),
            "status": s.status.title(),
        }
        for s in sells
    ]

    return JsonResponse({"sell_transactions": data})




@login_required
def buy_crypto(request):
    if request.method == "POST":
        usd_amount = float(request.POST.get("usd_amount", 0))
        crypto_id = request.POST.get("crypto", "bitcoin")
        contact_method = request.POST.get("contact_method")
        whatsapp_number = request.POST.get("whatsapp_number")
        contact_email = request.POST.get("contact_email")
        new_contact_email = request.POST.get("new_contact_email")
        crypto_address = request.POST.get("crypto_address")

        final_email = new_contact_email if new_contact_email else contact_email

        # Validation
        if contact_method == "whatsapp" and not whatsapp_number:
            return render(request, "website/dashboard/buy_crypto.html", {
                "error": "WhatsApp number is required if you choose WhatsApp."
            })
        if contact_method == "email" and not final_email:
            return render(request, "website/dashboard/buy_crypto.html", {
                "error": "Email address is required if you choose Email."
            })
        if not crypto_address:
            return render(request, "website/dashboard/buy_crypto.html", {
                "error": "Wallet address is required to complete your purchase."
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

        # Save purchase
        Purchase.objects.create(
            user=request.user,
            crypto=crypto_id,
            usd_amount=usd_amount,
            fee=fee,
            total=total_charge,
            crypto_amount=crypto_amount,
            price_at_purchase=crypto_price,
            contact_method=contact_method,
            whatsapp_number=whatsapp_number if contact_method == "whatsapp" else None,
            email=False,
            status="pending",
            crypto_address=crypto_address
        )

        return render(request, "website/dashboard/buy_crypto.html", {
            "success": True,
            "final_email": final_email,
            "contact_method": contact_method,
            "whatsapp_number": whatsapp_number,
        })


    return render(request, "website/dashboard/buy_crypto.html")








@login_required
def sell_crypto(request):
    if request.method == "POST":
        # Get form data
        usd_amount = request.POST.get("usd_amount")
        crypto = request.POST.get("crypto")
        receive_method = request.POST.get("receive_method")

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        address = request.POST.get("address", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        moncash_number = request.POST.get("moncash_number", "").strip()
        screenshot = request.FILES.get("screenshot")

        errors = []

        # Validation
        try:
            usd_amount = Decimal(usd_amount)
            if usd_amount < 75:
                errors.append("Le montant minimum est de 75 $")
        except:
            errors.append("Montant invalide")

        if crypto not in ["bitcoin", "ethereum", "litecoin", "dogecoin", "solana", "tether"]:
            errors.append("Cryptomonnaie invalide")

        if receive_method not in ["western_union", "moncash"]:
            errors.append("Méthode de réception invalide")

        if receive_method == "western_union":
            if not (first_name and last_name and address and phone_number):
                errors.append("Tous les champs Western Union sont obligatoires")

        if receive_method == "moncash":
            if not (first_name and phone_number):
                errors.append("Tous les champs MonCash sont obligatoires")

        if not screenshot:
            errors.append("Veuillez téléverser la capture d’écran du transfert")

        # ❌ Validation errors
        if errors:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": errors}, status=400)

            return render(request, "website/dashboard/sell_crypto.html", {
                "errors": errors
            })

        # Fees
        EASY_PASS_FEE_RATE = Decimal("0.05")  # 5%
        TRANSFER_FEE = Decimal("8")

        easy_pass_fee = usd_amount * EASY_PASS_FEE_RATE
        net_usd = usd_amount - easy_pass_fee - TRANSFER_FEE
        net_htg = net_usd * Decimal("130.9")

        # Crypto price
        try:
            res = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price",
                params={"ids": crypto, "vs_currencies": "usd"},
                timeout=10
            )
            res.raise_for_status()
            price = Decimal(res.json()[crypto]["usd"])
        except Exception:
            price = Decimal("0")

        crypto_amount = usd_amount / price if price > 0 else Decimal("0")

        # Save transaction
        SellTransaction.objects.create(
            user=request.user,
            crypto=crypto,
            usd_amount=usd_amount,
            crypto_amount=crypto_amount,
            net_usd=net_usd,
            net_htg=net_htg,
            receive_method=receive_method,
            first_name=first_name,
            last_name=last_name,
            address=address if receive_method == "western_union" else "",
            phone_number=phone_number,
            moncash_number=moncash_number if receive_method == "moncash" else "",
            screenshot=screenshot,
            status="processing",
        )

        # ✅ AJAX SUCCESS
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})

        # Fallback (no JS)
        return redirect(f"{request.path}?success=true")

    return render(request, "website/dashboard/sell_crypto.html")





def terms_of_use(request):
    return render(request, 'website/terms-of-use.html')






def privacy_policy(request):
    return render(request, 'website/privacy_policy.html')







@login_required
def account_settings(request):
    user = request.user

    if request.method == "POST":
        try:
            # Basic info
            user.first_name = request.POST.get("first_name", "").strip()
            user.last_name = request.POST.get("last_name", "").strip()
            user.phone_number = request.POST.get("phone_number", "").strip()
            user.wallet_address = request.POST.get("wallet_address", "").strip()

            # Contact method
            contact_method = request.POST.get("contact_method")

            if contact_method == "email":
                email = request.POST.get("email", "").strip()
                if email:
                    user.email = email

            elif contact_method == "whatsapp":
                whatsapp_number = request.POST.get("whatsapp_number", "").strip()
                if whatsapp_number:
                    user.phone_number = whatsapp_number

            # Profile picture
            if "profile_picture" in request.FILES:
                user.profile_picture = request.FILES["profile_picture"]

            user.save()

            return redirect("website:account_settings_success")

        except Exception as e:
            return render(request, "website/dashboard/settings.html", {
                "error": "Une erreur est survenue lors de la mise à jour.",
            })

    return render(request, "website/dashboard/settings.html")
