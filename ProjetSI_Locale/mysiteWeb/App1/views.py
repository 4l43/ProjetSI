from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from .models import Whitelist
from .models import Blacklist
from .models import Appointment
from datetime import datetime , date , time , timedelta
import random
import subprocess
import tempfile
from calendar import Calendar
from django.contrib import messages
import calendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
from django.conf import settings



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
    subject = "Code de vérification"
    message = f"Voici votre code de vérification : {code}"
    recipient = f"{identifiant}@parisnanterre.fr"

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
        print(f"Code {code} envoyé par mail à {recipient}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")



def calendrier(request):
    current_date = datetime.now()
    current_year = int(request.GET.get('year', current_date.year))
    current_month = int(request.GET.get('month', current_date.month))
    month_name = calendar.month_name[current_month]

    # Calcul des mois précédent et suivant
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year

    # Liste des jours par mois (prend en compte les années bissextiles)
    days_in_month = [
        31,
        28 + (1 if current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0) else 0),
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ]

    # Calculer le premier jour du mois
    first_day_of_month = datetime(current_year, current_month, 1)
    start_day = first_day_of_month.weekday()  # 0 = Lundi, 6 = Dimanche

    # Générer le tableau du calendrier
    calendar_days = []
    day = 1
    for week in range(6):
        week_days = []
        for d in range(7):
            if (week == 0 and d < start_day) or day > days_in_month[current_month - 1]:
                week_days.append('')  # Jour vide
            else:
                week_days.append(day)
                day += 1
        calendar_days.append(week_days)

    # Récupérer les rendez-vous déjà réservés pour le mois
    reserved_slots = Appointment.objects.filter(date__year=current_year, date__month=current_month)

    # Créer un dictionnaire pour les créneaux réservés (jour -> heure)
    reserved_times = {}
    for appointment in reserved_slots:
        day = appointment.date.day
        entry_time = appointment.entry_time.hour
        if day not in reserved_times:
            reserved_times[day] = []
        reserved_times[day].append(entry_time)

    # Gérer les données soumises (réservation)
    if request.method == 'POST':
        # Récupérer le mois et l'année soumis dans le formulaire
        current_year = int(request.POST.get('year', current_year))
        current_month = int(request.POST.get('month', current_month))

        selected_slots = request.POST.getlist('time_slots')
        user_email = request.session.get('mail')  # Récupérer l'email de l'utilisateur connecté
        for slot in selected_slots:
            try:
                # Extraire la date et l'heure du slot
                day, time = slot.split('-')
                date = datetime(current_year, current_month, int(day)).date()
                entry_time = datetime.strptime(time, '%H:%M').time()
                exit_time = (datetime.combine(date, entry_time) + timedelta(hours=1)).time()

                # Vérifier le nombre de créneaux réservés pour l'utilisateur sur ce jour
                appointments_today = Appointment.objects.filter(mail=user_email, date=date)
                if appointments_today.count() >= 2:
                    # Afficher un message d'erreur si l'utilisateur a déjà 2 créneaux
                    messages.error(request, f"Vous ne pouvez pas réserver plus de 2 créneaux pour le {date}.")
                    return redirect('calendar')  # Rediriger vers le calendrier

                # Créer un nouvel enregistrement dans la base de données
                Appointment.objects.create(
                    mail=user_email,
                    date=date,
                    entry_time=entry_time,
                    exit_time=exit_time
                )
            except Exception as e:
                print(f"Erreur lors de l'insertion : {e}")

    context = {
        'current_year': current_year,
        'current_month': current_month,
        'calendar_days': calendar_days,
        'month_name': month_name,
        'reserved_times': reserved_times,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
    }

    return render(request, 'calendrier.html', context)
#____________________________________________________________________________________

def reservation(request):
    # Récupérer toutes les entrées de la table Appointment
    #appointments = Appointment.objects.all()
    # Récupérer l'email de l'utilisateur connecté ou du paramètre de la requête
    user_email = request.session.get('mail')  # Si l'utilisateur est authentifié

    # Si l'email est passé dans la requête, utiliser cette valeur
    # user_email = request.GET.get('email')

    # Filtrer les réservations par e-mail
    appointments = Appointment.objects.filter(mail=user_email)
    
    # Passer les données au template
    return render(request, 'reservation.html', {'appointments': appointments})



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
def admini(request):
    #securite : 
    # Fonctionne mais est enregister dans les cookis de l'app
    if not request.session.get('code') or not request.session.get('identifiant') and Whitelist.objects.filter(statut = admin):
        print("Pas")
        return render(request, 'login.html', {'step': 'identifiant'})
    return render(request, 'admini.html')
