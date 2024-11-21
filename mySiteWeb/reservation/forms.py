from django import forms
from .models import Utilisateur

class UtilisateurFormulaire(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'mot_de_passe']
        widgets = {
            'mot_de_passe': forms.PasswordInput(),  # Champ masqué
        }