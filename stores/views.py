from django.shortcuts import render, get_object_or_404
from accounts.models import SellerProfile

def seller_profile(request, seller_id):
    seller = get_object_or_404(SellerProfile, id=seller_id)
    return render(request, "stores/seller_profile.html", {"seller": seller})
