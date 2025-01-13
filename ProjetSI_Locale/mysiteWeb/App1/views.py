from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from .models import Whitelist
from .models import Blacklist
import random

def index(request):
    # Si le formulaire est soumis avec l'identifiant
    if request.method == 'POST' and 'identifiant' in request.POST:
        identifiant = request.POST.get('identifiant')
        print(f"Identifiant reçu : {identifiant}")
        request.session['identifiant'] = identifiant  # Stocker l'identifiant dans la session
        mail = identifiant+"@parisnanterre.fr"
        print(mail)
        request.session['mail'] = mail
        # Générer un code aléatoire et le stocker dans la session
        code = random.randint(100000, 999999)
        print(f"Code généré : {code}")

        # Ici, tu pourrais envoyer le code par mail (à implémenter si nécessaire)
        request.session['code'] = code

        # Rediriger vers l'étape 'code' pour permettre à l'utilisateur d'entrer son code
        return render(request, 'login.html', {'step': 'code'})

    
    
    #_______________________________________________________________________________________
    # Si le formulaire est soumis avec un code
    elif request.method == 'POST' and 'code' in request.POST:
        entered_code = request.POST.get('code')
        print(f"Code reçu : {entered_code}")

        # Vérifier si le code soumis correspond à celui stocké dans la session
        stored_code = str(request.session.get('code'))
        print(f"Code stocké dans la session : {stored_code}")
        if entered_code == stored_code:
            print("Code correct")
            # Rediriger vers la page calendrier si le code est correct
            mail = request.session.get('mail')
            ajouter_a_whitelist( mail, 'user')
            return redirect('calendar')  # Assurez-vous que l'URL 'calendar' existe
        else:
            print("Code incorrect")
            # Si le code est incorrect, redemander l'identifiant
            return render(request, 'login.html', {'step': 'identifiant', 'error_message': 'Code incorrect. Veuillez réessayer.'})

    # Par défaut, afficher la page avec l'étape d'identification si aucune requête POST n'est reçue
    return render(request, 'login.html', {'step': 'identifiant'})


def calendrier(request):
    if mail = request.session.get('code') == null: 
         return redirect('calendar')
    print("Page du calendrier")
    # Récupérer tous les éléments de la table whitelist
    whitelist_items = Whitelist.objects.all()
    # Passer les éléments de la whitelist au template
    return render(request, 'calendrier.html', {'whitelist_items': whitelist_items})

def ajouter_a_whitelist(mail, statut):
    if Blacklist.objects.filter(mail=mail).exists():
        print(f"Le mail {mail} existe dans la blacklist.")
        return render(request, 'login.html', {'step': 'identifiant'})
    # Vérifie si l'email existe déjà dans la table
    if not Whitelist.objects.filter(mail=mail).exists():
        # Si l'email n'existe pas, crée une nouvelle entrée
        Whitelist.objects.create(mail=mail, statut=statut)
        print(f"Le mail {mail} a été ajouté à la whitelist.")
    else:
        print(f"Le mail {mail} existe déjà dans la whitelist.")
