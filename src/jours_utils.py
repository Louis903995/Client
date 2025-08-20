import datetime
import calendar


def jour_cible(jour_cible, date_ref=None):
    # date_ref = date de référence, par défaut aujourd'hui
    if date_ref is None:
        date_ref = datetime.date.today()
    annee = date_ref.year
    mois = date_ref.month
    jour_auj = date_ref.day

    # Dictionnaires français
    jours_fr = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    mois_fr = [
        "",
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ]

    # Cas 1 : le jour cible existe ce mois ET est dans le passé
    nb_jours_courant = calendar.monthrange(annee, mois)[1]
    if jour_cible <= jour_auj and jour_cible <= nb_jours_courant:
        date_resultat = datetime.date(annee, mois, jour_cible)
    else:
        # Sinon, on regarde le mois précédent
        if mois == 1:
            annee_prec = annee - 1
            mois_prec = 12
        else:
            annee_prec = annee
            mois_prec = mois - 1
        nb_jours_prec = calendar.monthrange(annee_prec, mois_prec)[1]
        if jour_cible <= nb_jours_prec:
            date_resultat = datetime.date(annee_prec, mois_prec, jour_cible)
        else:
            # Si le jour cible n'existe pas, prendre le 1er du mois courant
            date_resultat = datetime.date(annee, mois, 1)

    nom_jour = jours_fr[date_resultat.weekday()]
    nom_mois = mois_fr[date_resultat.month]
    jour_str = (
        f"{date_resultat.day}er" if date_resultat.day == 1 else str(date_resultat.day)
    )
    return f"{nom_jour} {jour_str} {nom_mois} {date_resultat.year}"
