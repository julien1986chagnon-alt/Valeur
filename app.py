import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="L'Échelle Juste — 20 Catégories, Calculatrice 4.10 & Modèle 3D",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ L'Échelle Juste : L'Économie Proportionnelle")
st.markdown(
    "Un manuscrit interactif créé par **Julien Chagnon** (Bruxelles) où chaque dépense vitale représente **exactement le même effort (%)** "
    "pour tout le monde, du minimex (400 €) jusqu'aux très hauts revenus (100 000 €)."
)

# --- PARAMÈTRES DE LA CALCULATRICE 4.10 ---
with st.sidebar:
    st.header("⚙️ Réglages Calculatrice 4.10")
    palier = st.radio(
        "Palier du Podium des Monnaies :",
        options=[
            "0,01 € (Actuel - Carte / Payconiq)",
            "0,05 € (Cash Belgique - Sans 1 & 2 cents)",
            "0,10 € (Futur - Recyclage pièces brunes)",
            "1,00 € (Unité Primaire - Sans virgule)",
            "5,00 € (Tout-Billet - Forfait minimum)"
        ],
        index=0
    )
    pas_map = {
        "0,01 € (Actuel - Carte / Payconiq)": 0.01,
        "0,05 € (Cash Belgique - Sans 1 & 2 cents)": 0.05,
        "0,10 € (Futur - Recyclage pièces brunes)": 0.10,
        "1,00 € (Unité Primaire - Sans virgule)": 1.00,
        "5,00 € (Tout-Billet - Forfait minimum)": 5.00
    }
    pas = pas_map[palier]

    st.divider()
    st.subheader("📊 Clé de répartition (100 %)")
    st.markdown("""
    - **🏠 Loyer :** 30 %
    - **⚡ Factures :** 15 %
    - **🛒 Courses (4 caddies à 5 %) :** 20 %
    - **🚇 Déplacements :** 10 %
    - **🩺 Soins & Santé :** 8 %
    - **🎬 Loisirs & Culture :** 10 %
    - **🏦 Épargne :** 7 %
    - **🍌 1 Banane :** 0,02 %
    """)

def arrondir_410(montant, pas_monnaie):
    if pas_monnaie >= 1.0:
        return max(pas_monnaie, math.ceil(montant / pas_monnaie) * pas_monnaie)
    return round(math.ceil(montant / pas_monnaie) * pas_monnaie, 2)

def fmt(val, pas_monnaie):
    if pas_monnaie >= 1.0:
        return f"{int(val):,} €".replace(",", " ")
    return f"{val:,.2f} €".replace(",", " ").replace(".", ",")

# --- LES 20 CATÉGORIES DE SALAIRES / REVENUS ---
categories_revenus = [
    ("01. Petit Minimex / Étudiant", 400),
    ("02. Demi-allocation / Temps très partiel", 800),
    ("03. Minimex / RIS Isolé (Belgique)", 1300),
    ("04. Incapacité de travail / Pension min.", 1500),
    ("05. Salaire minimum (RMMMG)", 2000),
    ("06. Salaire médian de référence", 2500),
    ("07. Employé / Ouvrier qualifié", 3000),
    ("08. Enseignant / Infirmier confirmé", 3500),
    ("09. Cadre intermédiaire / Tech", 4000),
    ("10. Ingénieur / Chef de projet", 5000),
    ("11. Profession libérale débutante", 6000),
    ("12. Directeur de service", 7500),
    ("13. Cadre supérieur / Médecin", 10000),
    ("14. Haut fonctionnaire / Député", 12500),
    ("15. Ministre / Dirigeant public", 15000),
    ("16. Directeur général (PME)", 20000),
    ("17. Chirurgien / Associé cabinet", 30000),
    ("18. Dirigeant grande entreprise", 50000),
    ("19. Top exécutif international", 75000),
    ("20. Très haut revenu / PDG", 100000),
]

# Génération du tableau des 20 catégories
lignes = []
for nom, rev in categories_revenus:
    loyer = arrondir_410(rev * 0.30, pas)
    factures = arrondir_410(rev * 0.15, pas)
    un_caddie = arrondir_410(rev * 0.05, pas)
    courses_mois = arrondir_410(rev * 0.20, pas)
    deplacements = arrondir_410(rev * 0.10, pas)
    soins = arrondir_410(rev * 0.08, pas)
    loisirs = arrondir_410(rev * 0.10, pas)
    epargne = arrondir_410(rev * 0.07, pas)
    banane = arrondir_410(rev * 0.0002, pas)

    lignes.append({
        "Catégorie de revenu": nom,
        "Revenu mensuel": f"{rev:,} €".replace(",", " "),
        "🏠 Loyer (30%)": fmt(loyer, pas),
        "⚡ Factures (15%)": fmt(factures, pas),
        "🛒 1 Caddie (5%)": fmt(un_caddie, pas),
        "🛍️ 4 Caddies/mois (20%)": fmt(courses_mois, pas),
        "🚇 Déplacements (10%)": fmt(deplacements, pas),
        "🩺 Soins (8%)": fmt(soins, pas),
        "🎬 Loisirs (10%)": fmt(loisirs, pas),
        "🏦 Épargne (7%)": fmt(epargne, pas),
        "🍌 1 Banane (0,02%)": fmt(banane, pas),
    })

df = pd.DataFrame(lignes)

# --- ONGLETS POUR UNE LECTURE CLAIRE ---
tab1, tab2, tab3 = st.tabs([
    "📋 Tableau des 20 Catégories",
    "🔍 Fiche Résumé par Catégorie",
    "🧊 Modèle 3D Interactif"
])

with tab1:
    st.subheader("Vue d'ensemble des 20 catégories de revenus (400 € → 100 000 €)")
    st.dataframe(df, use_container_width=True, hide_index=True, height=740)

with tab2:
    st.subheader("Détail complet pour une catégorie choisie")
    choix = st.selectbox(
        "Sélectionne une catégorie de revenu pour afficher sa fiche budget :",
        options=[f"{nom} — {rev:,} €".replace(",", " ") for nom, rev in categories_revenus],
        index=3
    )
    index_choisi = [f"{nom} — {rev:,} €".replace(",", " ") for nom, rev in categories_revenus].index(choix)
    nom_sel, rev_sel = categories_revenus[index_choisi]

    st.info(f"### {nom_sel} : **{rev_sel:,} € / mois**".replace(",", " "))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏠 Loyer (30 %)", fmt(arrondir_410(rev_sel * 0.30, pas), pas))
    c2.metric("⚡ Factures (15 %)", fmt(arrondir_410(rev_sel * 0.15, pas), pas))
    c3.metric("🛒 1 Caddie (5 %)", fmt(arrondir_410(rev_sel * 0.05, pas), pas))
    c4.metric("🛍️ Courses mois (20 %)", fmt(arrondir_410(rev_sel * 0.20, pas), pas))

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("🚇 Déplacements (10 %)", fmt(arrondir_410(rev_sel * 0.10, pas), pas))
    c6.metric("🩺 Soins & Santé (8 %)", fmt(arrondir_410(rev_sel * 0.08, pas), pas))
    c7.metric("🎬 Loisirs (10 %)", fmt(arrondir_410(rev_sel * 0.10, pas), pas))
    c8.metric("🏦 Épargne (7 %)", fmt(arrondir_410(rev_sel * 0.07, pas), pas))

    st.success(
        f"🍌 **Indice Banane (0,02 %) :** Avec ce revenu, une banane coûte **{fmt(arrondir_410(rev_sel * 0.0002, pas), pas)}** "
        f"(soit un pouvoir d'achat constant de **5 000 bananes/mois**, identique aux 19 autres catégories)."
    )

with tab3:
    st.subheader("🧊 Exploration en 3 Dimensions : Revenus × Postes × Coût (€)")
    st.markdown("Fais pivoter, zoome et survole le relief 3D à la souris pour voir comment les coûts évoluent proportionnellement sur les 3 axes.")

    postes_noms = [
        "Loyer (30%)",
        "Courses (20%)",
        "Factures (15%)",
        "Déplacements (10%)",
        "Loisirs (10%)",
        "Soins (8%)",
        "Épargne (7%)"
    ]
    postes_taux = [0.30, 0.20, 0.15, 0.10, 0.10, 0.08, 0.07]
    revenus_vals = [rev for _, rev in categories_revenus]

    z_matrix = []
    for rev in revenus_vals:
        z_matrix.append([arrondir_410(rev * t, pas) for t in postes_taux])

    fig = go.Figure(data=[go.Surface(
        z=z_matrix,
        x=postes_noms,
        y=revenus_vals,
        colorscale="Viridis",
        colorbar=dict(title="Montant (€)")
    )])

    fig.update_layout(
        title="Surface de L'Échelle Juste en 3D",
        scene=dict(
            xaxis_title="Poste Budgétaire",
            yaxis_title="Revenu Mensuel (€)",
            zaxis_title="Coût Proportionnel (€)",
        ),
        height=650,
        margin=dict(l=0, r=0, b=0, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

