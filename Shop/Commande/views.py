from django.shortcuts import render

def vue_panier(request):
    return render(request,"Commande/panier_view.html")
