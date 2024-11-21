from django.shortcuts import render, redirect
from .forms import UtilisateurFormulaire
from .models import Utilisateur

def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurFormulaire(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('liste_utilisateurs')
    else:
        form = UtilisateurFormulaire()
    return render(request, 'utilisateurs/ajouter.html', {'form': form})

def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()  # Récupère tous les utilisateurs
    return render(request, 'utilisateurs/liste.html', {'utilisateurs': utilisateurs})