from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from .models import Whitelist
from .models import Blacklist
import random
import subprocess
import tempfile

def index(request):
    # Si le formulaire est soumis avec l'identifiant
    if request.method == 'POST' and 'identifiant' in request.POST:
        identifiant = request.POST.get('identifiant')
        print(f"Identifiant reçu : {identifiant}")
        request.session['identifiant'] = identifiant  # Stocker l'identifiant dans la session
        mail = identifiant + "@parisnanterre.fr"
        print(mail)
        request.session['mail'] = mail
        # Générer un code aléatoire et le stocker dans la session
        code = random.randint(100000, 999999)
        print(f"Code généré : {code}")

        # Passer le code et l'identifiant à la fonction d'envoi de mail
        request.session['code'] = code
        envoie_mail(code, identifiant)  # Ajout de identifiant ici

        # Rediriger vers l'étape 'code' pour permettre à l'utilisateur d'entrer son code
        return render(request, 'login.html', {'step': 'code'})
    
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
            ajouter_a_whitelist(mail, 'user')
            return redirect('calendar')  # Assurez-vous que l'URL 'calendar' existe
        else:
            print("Code incorrect")
            # Si le code est incorrect, redemander l'identifiant
            return render(request, 'login.html', {'step': 'identifiant', 'error_message': 'Code incorrect. Veuillez réessayer.'})

    # Par défaut, afficher la page avec l'étape d'identification si aucune requête POST n'est reçue
    return render(request, 'login.html', {'step': 'identifiant'})


def envoie_mail(code, identifiant):
    print(f"{code} envoyé par mail")
    
    # Configuration des variables pour l'e-mail
    sender_email = "franckzheng123@outlook.com"
    receiver_email = f"{identifiant}@parisnanterre.fr"  # Utilisation de identifiant passé en paramètre
    subject = "Code de vérification"
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    password = "fzraidenbeacon12375019"  # Évitez d'inclure les mots de passe dans le code

    # Construction du message
    message = f"""
From: {sender_email}
To: {receiver_email}
Subject: {subject}

Voici votre code de vérification : {code}
"""

    # Créer un fichier temporaire pour stocker le message
    with tempfile.NamedTemporaryFile(delete=False) as msg_file:
        msg_file.write(message.encode('utf-8'))
        msg_file.close()

        # Commande curl pour envoyer l'e-mail
        curl_command = [
            "curl",
            "--url", f"smtp://{smtp_server}:{smtp_port}",
            "--ssl-reqd",
            "--mail-from", sender_email,
            "--mail-rcpt", receiver_email,
            "--user", f"{sender_email}:{password}",
            "--upload-file", msg_file.name
        ]

        try:
            # Exécution de la commande avec subprocess
            result = subprocess.run(
                curl_command, 
                text=True, 
                capture_output=True
            )

            print(result.stdout)  # Affiche la sortie standard
            print(result.stderr)  # Affiche les erreurs éventuelles

        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail : {e}")
        finally:
            # Nettoyage du fichier temporaire
            import os
            os.remove(msg_file.name)

    return code



def calendrier(request):
    # Fonctionne mais est enregister dans les cookis de l'app
    if not request.session.get('code') or not request.session.get('identifiant'):
        print("Pas")
        return render(request, 'login.html', {'step': 'identifiant'})
    #____________________________________________________________________________________
    #debug : 
    # code = request.session.get('code')
    # identifiant = request.session.get('identifiant')
    # print(f"{identifiant} Oui")
    # print(f"{code} Oui")
    # print("Page du calendrier")
    #____________________________________________________________________________________
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

#____________________________________________________________________________________








#____________________________________________________________________________________
def admini(request):
    #securite : 
    # Fonctionne mais est enregister dans les cookis de l'app
    if not request.session.get('code') or not request.session.get('identifiant') and Whitelist.objects.filter(statut = admin):
        print("Pas")
        return render(request, 'login.html', {'step': 'identifiant'})
    return render(request, 'admini.html')