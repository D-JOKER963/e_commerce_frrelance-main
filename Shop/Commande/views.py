from itertools import product
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Product.models import Produit, Avis
from .models import *
from django.core.mail import send_mail


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
    return render(request, "Commande/panier_view.html", context)


def supprimer_panier(request):
    if 'panier' in request.session:
        del request.session['panier']

        return JsonResponse({'success': True})


def enregistrer_commande(request):
    if request.method == "POST" and 'panier' in request.session:
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        tel = request.POST.get('tel')
        ville = request.POST.get('ville')
        quartier = request.POST.get('quartier')
        total_panier = request.POST.get('total_panier')

        nom_client = f"{nom} {prenom}"
        adresse = f"{ville}, {quartier}"

        # Création de la commande
        commande = Commande.objects.create(
            nom_client=nom_client,
            adresse=adresse,
            telephone=tel,
            montant_total=total_panier
        )

        panier = request.session['panier']
        liste_produits = ""  # Préparer la liste des produits à afficher dans l'email

        for produit_id, quantite in panier.items():
            try:
                produit = Produit.objects.get(id=produit_id)
                montant = produit.prix * quantite
                ProduitCommande.objects.create(
                    commande=commande,
                    produit=produit,
                    quantite=quantite,
                    montant=montant
                )
                liste_produits += f"- {produit.nom} (x{quantite}) - {montant} FCFA\n"
            except Produit.DoesNotExist:
                return HttpResponse(f"Produit avec id {produit_id} non trouvé.", status=404)

        # Vider le panier
        del request.session['panier']

        # Format de date
        date_commande = timezone.now().strftime("%d/%m/%Y à %Hh%M")

        # Préparation du message d’email
        message_email = f"""
Nouvelle commande reçue !

Client : {nom_client}
Téléphone : {tel}
Adresse : {adresse}
Date : {date_commande}

Produits commandés :
{liste_produits}
Montant total : {total_panier} FCFA

Veuillez traiter cette commande dès que possible.
"""

        # Envoi de l’email
        send_mail(
            subject="Nouvelle Commande Client",
            message=message_email,
            from_email="boutique@site.com",
            recipient_list=["kossibalogou83@gmail.com", "urbainbalogou19@gmail.com"],
            fail_silently=False,
        )

        messages.success(request, "Commande passée avec succès, vous serez contacté pour confirmation.")
        return redirect('index')
    else:
        return redirect('vue_panier')


def show_video(request, slug):
    product = get_object_or_404(Produit.objects.prefetch_related('imageproduit_set'), slug=slug)

    return render(request, 'Commande/show_video.html', {'product': product})


def single_commande(request, slug):
    print(request.session['video_finished'])
    if not request.session.get('video_finished'):
        return redirect('show_video', slug=slug)

    product = get_object_or_404(Produit.objects.prefetch_related("imageproduit_set"), slug=slug)
    avis = product.avis.all()
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
        print("Envoi d'email")
        # Envoi de l'email
        send_mail(
            subject="Nouvelle Commande",
            message=f"Une nouvelle commande a été effectuée par {nom_client} pour la commande {slug}.",
            from_email="boutique@site.com",
            recipient_list=["kossibalogou83@gmail.com", "urbainbalogou19@gmail.com"],
            fail_silently=False,
        )

        messages.success(request,
                         "Commande passée avec succès, Vous serez contacter pour confirmation de votre commande")
        request.session['video_finished'] = False

        return redirect('index')

    return render(request, "Commande/single_commande.html", {"product": product, "avis": avis})


def mark_video_finished(request):
    print("appel de fonction")
    if request.method == "POST":
        request.session['video_finished'] = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def ajout_avis(request, slug):
    print("................................")
    product = get_object_or_404(Produit.objects.all(), slug=slug)
    if request.method == "POST":
        commentaire = request.POST.get('commentaire')
        utilisateur = request.POST.get('utilisateur')
        Avis.objects.create(
            produit=product,
            commentaire=commentaire,
            utilisateur=utilisateur
        )
        messages.success(request, "Votre avis est posté")
        return redirect('index')
