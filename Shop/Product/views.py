from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse, HttpResponseBadRequest


"""def index(request):
    products = Produit.objects.prefetch_related('imageproduit_set').all()
    for product in products:
        for image in product.imageproduit_set.all():
            print(image.image.url)  # Imprime l'URL de chaque image associée
    return render(request, 'Product/index.html', {'products': products})"""

def index(request):
    categories = Categorie.objects.prefetch_related(
        'produit_set__imageproduit_set'
    ).all()

    # Gestion du panier
    panier = request.session.get('panier', {})
    produits_panier = []
    total = 0

    for produit_id, quantite in panier.items():
        try:
            produit = Produit.objects.get(id=produit_id)
            total_item = produit.prix * quantite
            total += total_item
            produits_panier.append({
                'produit': produit,
                'quantite': quantite,
                'total': total_item,
            })
        except Produit.DoesNotExist:
            continue  # si produit supprimé, ignorer

    context = {
        'categories': categories,
        'produits_panier': produits_panier,
        'quantite_panier': sum(panier.values()),
        'total_panier': total,
    }

    return render(request, 'Product/index.html', context)



def ajouter_au_panier(request, product_slug):
    print(f"Produit Slug reçu: {product_slug}")
    produit = get_object_or_404(Produit, slug=product_slug)

    panier = request.session.get('panier', {})
    panier[str(produit.id)] = panier.get(str(produit.id), 0) + 1
    request.session['panier'] = panier

    return JsonResponse({'success': True, 'quantite': panier[str(produit.id)]})