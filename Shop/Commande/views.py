from itertools import product

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Product.models import Produit
from .models import *


def vue_panier(request):
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
        'produits_panier': produits_panier,
        'quantite_panier': sum(panier.values()),
        'total_panier': total,
    }
    return render(request,"Commande/panier_view.html",context)


def supprimer_panier(request):

    if 'panier' in request.session:
        del request.session['panier']

        return JsonResponse({'success':True})


def enregistrer_commande(request):
    # Vérifie si l'utilisateur est connecté et a un panier
    if request.method == "POST" and 'panier' in request.session:
        # Récupère les informations de la commande depuis le formulaire ou les données de session
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        tel = request.POST.get('tel')
        ville = request.POST.get('ville')
        quartier = request.POST.get('quartier')
        total_panier = request.POST.get('total_panier')

        print("nom:", nom)
        nom_client = nom + " " + prenom
        adresse = ville + "/" + quartier

        # Crée la commande
        commande = Commande.objects.create(
            nom_client=nom_client,
            adresse=adresse,
            telephone = tel,
            montant_total = total_panier
        )

        # Récupère les produits du panier depuis la session
        panier = request.session['panier']

        # Pour chaque produit dans le panier, crée une entrée dans ProduitCommande
        for produit_id, quantite in panier.items():  # Parcours chaque produit et sa quantité
            try:
                produit = Produit.objects.get(id=produit_id)  # Récupère le produit

                montant = produit.prix * quantite
                # Crée une ligne dans ProduitCommande

                ProduitCommande.objects.create(
                    commande=commande,
                    produit=produit,
                    quantite=quantite,
                    montant = montant
                )
            except Produit.DoesNotExist:
                print(f"Produit avec id {produit_id} non trouvé.")
                return HttpResponse(f"Produit avec id {produit_id} non trouvé.", status=404)

        # Une fois la commande enregistrée, vide le panier
        del request.session['panier']

        # Redirige l'utilisateur vers une page de confirmation
        messages.success(request, "Commande passée avec succès, Vous serez contacter pour confirmation de votre commande")

        return redirect('index')
    else:
        return redirect('vue_panier')  # Redirige vers la page panier si pas de panier



def show_video(request, slug):
    product = get_object_or_404(Produit.objects.prefetch_related('imageproduit_set'),slug=slug)

    return render(request, 'Commande/show_video.html', {'product': product})


def single_commande(request, slug):
    print(request.session['video_finished'])
    if not request.session.get('video_finished'):
        return redirect('show_video', slug=slug)

    product = get_object_or_404(Produit.objects.prefetch_related("imageproduit_set"),slug=slug)
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        adresse = request.POST.get('adresse')
        tel = request.POST.get('telephone')
        quantite = request.POST.get('quantite')
        montant_total = float(request.POST.get("montant_total", 0))
        nom_client = nom + " " + prenom

        commande = Commande.objects.create(
            nom_client=nom_client,
            adresse=adresse,
            telephone=tel,
            montant_total=montant_total
        )
        ProduitCommande.objects.create(
            commande=commande,
            produit=product,
            quantite=quantite,
            montant=product.prix
        )

        messages.success(request, "Commande passée avec succès, Vous serez contacter pour confirmation de votre commande")
        request.session['video_finished'] = False

        return redirect('index')

    return render(request, "Commande/single_commande.html",{"product":product})


def mark_video_finished(request):
    print("appel de fonction")
    if request.method == "POST":
        request.session['video_finished'] = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

