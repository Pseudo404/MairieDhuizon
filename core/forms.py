from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from core.models import News, QuickLink, AdminAccount, InscriptionCentreLoisirs

class IconSelectWidget(forms.Widget):    
    def __init__(self, icons_choices=None, attrs=None):
        super().__init__(attrs)
        self.icons_choices = icons_choices or []
    
    def render(self, name, value, attrs=None, renderer=None):
        widget_attrs = self.build_attrs(attrs or {}, {'name': name})
        widget_id = widget_attrs.get('id', f'id_{name}')
        html = f'<div class="icon-grid" id="{widget_id}" data-field="{name}">\n'
        
        for icon_value, icon_label in self.icons_choices:
            checked = 'checked' if value == icon_value else ''
            html += (
                f'  <label class="icon-option" data-value="{icon_value}">\n'
                f'    <input type="radio" name="{name}" value="{icon_value}" {checked} style="display:none;">\n'
                f'    <span class="material-symbols-outlined">{icon_value}</span>\n'
                f'  </label>\n'
            )
        
        html += '</div>\n'
        html += '''
            <style>
            .icon-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
                gap: 12px;
                margin-bottom: 16px;
                padding: 12px;
                background: #f9fafb;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }

            .icon-option {
                display: flex;
                align-items: center;
                justify-content: center;
                aspect-ratio: 1;
                border: 2px solid #d1d5db;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
                background: white;
                padding: 8px;
            }

            .icon-option:hover {
                border-color: #22c55e;
                background: #f0fdf4;
                transform: scale(1.05);
            }

            .icon-option input:checked + span,
            .icon-option:has(input:checked) {
                background: #22c55e;
                border-color: #16a34a;
                color: white;
            }

            .icon-option input:checked + span {
                color: white;
            }

            .icon-option span {
                font-size: 40px;
                color: #374151;
                font-weight: 400;
                display: block;
                line-height: 1;
            }
            </style>

            <script>
            document.addEventListener('DOMContentLoaded', function() {
                document.querySelectorAll('.icon-grid').forEach(grid => {
                    grid.querySelectorAll('.icon-option').forEach(label => {
                        label.addEventListener('click', function(e) {
                            e.preventDefault();
                            const input = this.querySelector('input');
                            input.checked = true;
                        });
                    });
                });
            });
            </script>
            '''
        return mark_safe(html)

class ContactForm(forms.Form):
    nom = forms.CharField(
        max_length=100,
        label="Nom",
        widget=forms.TextInput(attrs={
            'placeholder': 'Turing',
            'class': 'w-full px-5 py-4 rounded-2xl border border-gray-200 '
                     'focus:outline-none focus:ring-4 focus:ring-green-100 '
                     'focus:border-green-600 transition',
        }),
    )
    prenom = forms.CharField(
        max_length=100,
        label="Prénom",
        widget=forms.TextInput(attrs={
            'placeholder': 'Alan',
            'class': 'w-full px-5 py-4 rounded-2xl border border-gray-200 '
                     'focus:outline-none focus:ring-4 focus:ring-green-100 '
                     'focus:border-green-600 transition',
        }),
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'alan.turing@domaine.com',
            'class': 'w-full px-5 py-4 rounded-2xl border border-gray-200 '
                     'focus:outline-none focus:ring-4 focus:ring-green-100 '
                     'focus:border-green-600 transition',
        }),
    )
    telephone = forms.CharField(
        max_length=20,
        required=False,
        label="Numéro de téléphone",
        validators=[
            RegexValidator(
                regex=r'^[\d\s\+\-\.()]{0,20}$', #les chiffres, espaces, +, -, ., et parenthèses jusqu'à 20 caractères 
                message="Numéro de téléphone invalide.",
            ),
        ],
        widget=forms.TextInput(attrs={
            'placeholder': '06 12 34 56 78',
            'class': 'w-full px-5 py-4 rounded-2xl border border-gray-200 '
                     'focus:outline-none focus:ring-4 focus:ring-green-100 '
                     'focus:border-green-600 transition',
        }),
    )
    objet = forms.CharField(
        max_length=200,
        label="Objet",
        widget=forms.TextInput(attrs={
            'placeholder': 'Objet de votre demande',
            'class': 'w-full px-5 py-4 rounded-2xl border border-gray-200 '
                     'focus:outline-none focus:ring-4 focus:ring-green-100 '
                     'focus:border-green-600 transition',
        }),
    )
    message = forms.CharField(
        max_length=5000,
        label="Message",
        widget=forms.Textarea(attrs={
            'rows': 7,
            'placeholder': 'Écrivez votre message...',
            'class': 'w-full px-5 py-4 rounded-2xl border border-gray-200 '
                     'focus:outline-none focus:ring-4 focus:ring-green-100 '
                     'focus:border-green-600 transition resize-none',
        }),
    )

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'short_description', 'content', 'image', 'event_date', 'author', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Titre de l'actualité",
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                     'focus:border-green-600 transition',
            }),
            'short_description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Résumé court affiché dans la liste...',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                     'focus:border-green-600 transition resize-none',
            }),
            'content': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': "Contenu complet de l'actualité...",
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                     'focus:border-green-600 transition resize-none',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 '
                     'file:bg-green-700 file:text-white file:cursor-pointer hover:file:bg-green-800 transition',
            }),
            'event_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                         'focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                         'focus:border-green-600 transition',
            }),
            'author': forms.TextInput(attrs={
                'placeholder': "Nom de l'auteur (optionnel)",
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                     'focus:border-green-600 transition',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-gray-300 text-green-600 focus:ring-green-500 cursor-pointer',
            }),
        }
        labels = {
            'title': 'Titre',
            'short_description': 'Description courte',
            'content': 'Contenu',
            'image': 'Image principale',
            'event_date': "Date de l'événement",
            'author': 'Auteur',
            'is_published': 'Publier immédiatement',
        }

class AdminLoginForm(AuthenticationForm):
    """
    héritage du systeme de connexion de django
    changement de l'apparence
    """
    username = forms.CharField(
        max_length=254,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur",
            'class': 'w-full px-5 py-3 rounded-2xl bg-white border border-gray-300 '
                     'text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 '
                     'focus:ring-green-500 focus:border-transparent transition',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'placeholder': "Mot de passe",
            'class': 'w-full px-5 py-3 rounded-2xl bg-white border border-gray-300 '
                     'text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 '
                     'focus:ring-green-500 focus:border-transparent transition',
            'autocomplete': 'current-password',
        }),
    )

class QuickLinkForm(forms.ModelForm):
    class Meta:
        model = QuickLink
        fields = ['label', 'icon', 'url', 'order']
        widgets = {
            'label': forms.TextInput(attrs={
                'placeholder': "Ex: École, Pharmacie, Sports...",
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                     'focus:border-green-600 transition',
            }),
            'url': forms.TextInput(attrs={
                'placeholder': "Ex: /loisirs/#sport ou https://google.com",
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                     'focus:border-green-600 transition',
            }),
            'order': forms.NumberInput(attrs={
                'placeholder': "Ordre d'affichage",
                'min': '0',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
                     'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
                     'focus:border-green-600 transition',
            }),
        }
        labels = {
            'label': 'Libellé',
            'icon': 'Choisir une icône',
            'url': 'Lien de destination',
            'order': "Ordre d'affichage",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icon'].widget = IconSelectWidget(icons_choices=QuickLink.ICONS_CHOICES)

_INPUT_CLASS = (
    'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 '
    'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500/30 '
    'focus:border-green-600 transition'
)

class AdminAccountForm(forms.Form):
    """Création / modification d'un compte administrateur classique (employé mairie)."""

    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={'class': _INPUT_CLASS, 'autocomplete': 'username'}),
    )
    email = forms.EmailField(
        label='E-mail',
        required=False,
        widget=forms.EmailInput(attrs={'class': _INPUT_CLASS, 'autocomplete': 'email'}),
    )
    first_name = forms.CharField(
        label='Prénom',
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={'class': _INPUT_CLASS}),
    )
    last_name = forms.CharField(
        label='Nom',
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={'class': _INPUT_CLASS}),
    )
    password = forms.CharField(
        label='Mot de passe',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': _INPUT_CLASS,
            'autocomplete': 'new-password',
        }),
        help_text='Minimum 8 caractères.',
    )
    password_confirm = forms.CharField(
        label='Confirmer le mot de passe',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': _INPUT_CLASS,
            'autocomplete': 'new-password',
        }),
    )
    is_centre_loisirs = forms.BooleanField(
        label='Admin Centre de Loisirs uniquement',
        required=False,
        help_text="Accès restreint au centre de loisirs seulement (pas de panel général)."
    )
    can_access_centre_loisirs = forms.BooleanField(
        label='Accès Centre de Loisirs (en plus du panel)',
        required=False,
        help_text="Cet admin garde l'accès au panel général ET peut aussi gérer le centre de loisirs."
    )

    def __init__(self, *args, admin_account=None, **kwargs):
        self.admin_account = admin_account
        super().__init__(*args, **kwargs)
        if admin_account:
            user = admin_account.user
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['is_centre_loisirs'].initial = admin_account.is_centre_loisirs
            self.fields['can_access_centre_loisirs'].initial = admin_account.can_access_centre_loisirs
            self.fields['password'].help_text = 'Laisser vide pour conserver le mot de passe actuel.'
        else:
            self.fields['password'].required = True
            self.fields['password_confirm'].required = True

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        qs = User.objects.filter(username__iexact=username)
        if self.admin_account:
            qs = qs.exclude(pk=self.admin_account.user_id)
        if qs.exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password') or ''
        password_confirm = cleaned.get('password_confirm') or ''
        is_create = self.admin_account is None

        if is_create or password:
            if len(password) < 8:
                self.add_error('password', 'Le mot de passe doit contenir au moins 8 caractères.')
            elif password != password_confirm:
                self.add_error('password_confirm', 'Les mots de passe ne correspondent pas.')
        elif password_confirm:
            self.add_error('password', 'Saisissez le nouveau mot de passe.')

        return cleaned

    def save(self):
        data = self.cleaned_data
        if self.admin_account:
            user = self.admin_account.user
            user.username = data['username']
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            if data.get('password'):
                user.set_password(data['password'])
            user.save()
            self.admin_account.is_centre_loisirs = data.get('is_centre_loisirs', False)
            self.admin_account.can_access_centre_loisirs = data.get('can_access_centre_loisirs', False)
            self.admin_account.save()
            return self.admin_account

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_staff=True,
            is_superuser=False,
        )
        return AdminAccount.objects.create(
            user=user,
            is_super_admin=False,
            is_centre_loisirs=data.get('is_centre_loisirs', False),
            can_access_centre_loisirs=data.get('can_access_centre_loisirs', False),
        )

class InscriptionCentreLoisirsForm(forms.ModelForm):
    class Meta:
        model = InscriptionCentreLoisirs
        exclude = ['token', 'nom_enfant', 'prenom_enfant', 'date_naissance', 'pai_sante', 'vaccins', 'assurance_scolaire']
        widgets = {
            'nom_responsable_1': forms.TextInput(attrs={
                'placeholder': 'Nom de famille',
                'class': _INPUT_CLASS,
            }),
            'prenom_responsable_1': forms.TextInput(attrs={
                'placeholder': 'Prénom',
                'class': _INPUT_CLASS,
            }),
            'adresse_responsable_1': forms.TextInput(attrs={
                'placeholder': '12 Rue de la Mairie',
                'class': _INPUT_CLASS,
            }),
            'code_postal_1': forms.TextInput(attrs={
                'placeholder': '41220',
                'class': _INPUT_CLASS,
            }),
            'ville_1': forms.TextInput(attrs={
                'placeholder': 'Dhuizon',
                'class': _INPUT_CLASS,
            }),
            'telephone_1': forms.TextInput(attrs={
                'placeholder': '02 54 XX XX XX',
                'class': _INPUT_CLASS,
            }),
            'portable_1': forms.TextInput(attrs={
                'placeholder': '06 XX XX XX XX',
                'class': _INPUT_CLASS,
            }),
            'email_1': forms.EmailInput(attrs={
                'placeholder': 'parent@exemple.fr',
                'class': _INPUT_CLASS,
            }),
            'nom_responsable_2': forms.TextInput(attrs={
                'placeholder': 'Nom de famille',
                'class': _INPUT_CLASS,
            }),
            'prenom_responsable_2': forms.TextInput(attrs={
                'placeholder': 'Prénom',
                'class': _INPUT_CLASS,
            }),
            'adresse_responsable_2': forms.TextInput(attrs={
                'placeholder': '12 Rue de la Mairie',
                'class': _INPUT_CLASS,
            }),
            'code_postal_2': forms.TextInput(attrs={
                'placeholder': '41220',
                'class': _INPUT_CLASS,
            }),
            'ville_2': forms.TextInput(attrs={
                'placeholder': 'Dhuizon',
                'class': _INPUT_CLASS,
            }),
            'telephone_2': forms.TextInput(attrs={
                'placeholder': '02 54 XX XX XX',
                'class': _INPUT_CLASS,
            }),
            'portable_2': forms.TextInput(attrs={
                'placeholder': '06 XX XX XX XX',
                'class': _INPUT_CLASS,
            }),
            'email_2': forms.EmailInput(attrs={
                'placeholder': 'parent2@exemple.fr',
                'class': _INPUT_CLASS,
            }),
            'coefficient_familial': forms.TextInput(attrs={
                'placeholder': 'Ex : 800',
                'class': _INPUT_CLASS,
            }),
            'livret_famille': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-gray-300 text-green-600 focus:ring-green-500 cursor-pointer',
            }),
            'personnes_habilitees_texte': forms.Textarea(attrs={
                'placeholder': 'Noms et prénoms des personnes',
                'class': _INPUT_CLASS + ' h-24',
                'rows': 3
            }),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Formulaire d'inscription périscolaire (Garderie / Cantine) - Version PDF Exacte
# ──────────────────────────────────────────────────────────────────────────────

PHONE_VALIDATOR = RegexValidator(
    regex=r'^[\d\s\+\-\.()]{0,20}$',
    message="Numéro de téléphone invalide.",
)

class InscriptionPeriscolaireForm(forms.Form):
    # ── Enfant ──
    nom_enfant = forms.CharField(max_length=100, label="Nom", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    prenom_enfant = forms.CharField(max_length=100, label="Prénom", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    date_naissance_enfant = forms.DateField(label="Date de naissance", widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT_CLASS}))
    classe_enfant = forms.CharField(max_length=100, label="Classe", required=False, widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))

    # ── Responsables légaux ──
    responsable_1_nom_prenom = forms.CharField(max_length=200, label="Responsable 1", widget=forms.TextInput(attrs={'placeholder': 'Nom et Prénom', 'class': _INPUT_CLASS}))
    responsable_1_adresse = forms.CharField(max_length=300, label="Adresse", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    responsable_1_telephone = forms.CharField(max_length=20, label="Téléphone", validators=[PHONE_VALIDATOR], widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    responsable_1_courriel = forms.EmailField(label="Courriel", widget=forms.EmailInput(attrs={'class': _INPUT_CLASS}))

    responsable_2_nom_prenom = forms.CharField(max_length=200, required=False, label="Responsable 2", widget=forms.TextInput(attrs={'placeholder': 'Nom et Prénom', 'class': _INPUT_CLASS}))
    responsable_2_adresse = forms.CharField(max_length=300, required=False, label="Adresse", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    responsable_2_telephone = forms.CharField(max_length=20, required=False, label="Téléphone", validators=[PHONE_VALIDATOR], widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    responsable_2_courriel = forms.EmailField(required=False, label="Courriel", widget=forms.EmailInput(attrs={'class': _INPUT_CLASS}))

    # ── Responsable financier ──
    responsable_financier = forms.CharField(max_length=200, required=False, label="Nom et Prénom", widget=forms.TextInput(attrs={'placeholder': '', 'class': _INPUT_CLASS}))
    responsable_financier_adresse = forms.CharField(max_length=300, required=False, label="Adresse", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))

    # ── Service demandé (Grille) ──
    # Garderie du matin
    gm_lundi = forms.BooleanField(required=False)
    gm_mardi = forms.BooleanField(required=False)
    # gm_mercredi = forms.BooleanField(required=False)
    gm_jeudi = forms.BooleanField(required=False)
    gm_vendredi = forms.BooleanField(required=False)
    gm_regulier = forms.BooleanField(required=False)
    gm_occasionnel = forms.BooleanField(required=False)

    # Cantine
    can_lundi = forms.BooleanField(required=False)
    can_mardi = forms.BooleanField(required=False)
    # can_mercredi = forms.BooleanField(required=False)
    can_jeudi = forms.BooleanField(required=False)
    can_vendredi = forms.BooleanField(required=False)
    can_regulier = forms.BooleanField(required=False)
    can_occasionnel = forms.BooleanField(required=False)

    # Garderie du soir
    gs_lundi = forms.BooleanField(required=False)
    gs_mardi = forms.BooleanField(required=False)
    # gs_mercredi = forms.BooleanField(required=False)
    gs_jeudi = forms.BooleanField(required=False)
    gs_vendredi = forms.BooleanField(required=False)
    gs_regulier = forms.BooleanField(required=False)
    gs_occasionnel = forms.BooleanField(required=False)

    # ── Précisions horaires ──
    heure_arrivee = forms.TimeField(required=False, label="Heure habituelle d'arrivée le matin", widget=forms.TimeInput(attrs={'type': 'time', 'class': _INPUT_CLASS}))
    heure_depart = forms.TimeField(required=False, label="Heure habituelle de départ le soir", widget=forms.TimeInput(attrs={'type': 'time', 'class': _INPUT_CLASS}))

    # ── Santé et restauration ──
    PAI_CHOICES = [('Oui', 'Oui'), ('Non', 'Non')]
    pai_en_cours = forms.ChoiceField(choices=PAI_CHOICES, widget=forms.RadioSelect(attrs={'class': 'peer sr-only'}), label="PAI en cours", required=False)
    allergies = forms.CharField(max_length=1000, required=False, label="Allergies / intolérances / consignes particulières", widget=forms.Textarea(attrs={'rows': 4, 'class': _INPUT_CLASS}))

    # ── Personnes à prévenir en cas d'urgence ──
    urgence_nom_prenom = forms.CharField(max_length=200, required=False, label="Nom et prénom", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    urgence_lien = forms.CharField(max_length=100, required=False, label="Lien avec l'enfant", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    urgence_telephone = forms.CharField(max_length=20, required=False, label="Téléphone", validators=[PHONE_VALIDATOR], widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))

    # ── Assurance extra-scolaire ──
    assurance_coordonnees = forms.CharField(max_length=300, required=False, label="Coordonnées de l'assurance", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    assurance_souscripteur = forms.CharField(max_length=200, required=False, label="Souscripteur", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    assurance_numero = forms.CharField(max_length=100, required=False, label="Numéro de contrat", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))

    # ── Personnes autorisées (hors responsables légaux) ──
    auth_1 = forms.CharField(max_length=300, required=False, label="Nom, prénom et lien avec l'enfant", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    auth_2 = forms.CharField(max_length=300, required=False, label="Nom, prénom et lien avec l'enfant", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))

    # ── Engagement ──
    soussigne = forms.CharField(max_length=200, required=True, label="Je soussigné(e)", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    fait_a = forms.CharField(max_length=100, required=True, label="Fait à", widget=forms.TextInput(attrs={'class': _INPUT_CLASS}))
    le_date = forms.DateField(required=True, label="Le", widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT_CLASS}))
    engagement_certifie = forms.BooleanField(required=True, label="Je certifie exacts les renseignements portés sur cette fiche et m'engage à signaler toute modification à la mairie.")
    engagement_cantine = forms.BooleanField(required=True, label="Je reconnais avoir pris connaissance du règlement et des règles de vie de la cantine scolaire.")
    engagement_garderie = forms.BooleanField(required=True, label="Je reconnais avoir pris connaissance du règlement et des règles de vie de la garderie périscolaire.")

