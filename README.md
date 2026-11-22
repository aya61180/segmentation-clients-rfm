# Segmentation clients : quels segments sont les plus rentables ?

Analyse exploratoire et segmentation RFM (K-Means) du dataset
[Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)
(Kaggle, Akash Patel), suivie d'un dashboard Streamlit interactif.

## Problématique
Quels segments de clients génèrent le plus de chiffre d'affaires,
et lesquels répondent le mieux aux campagnes marketing ?

## Méthode
1. Nettoyage des données (2 240 → 2 051 clients)
2. Analyse exploratoire (corrélations, distributions, canaux d'achat)
3. Segmentation RFM (Recency, Frequency, Monetary), standardisée
4. K-Means avec K = 4 : coude à k = 4, silhouette = 0,392,
   et k = 2 trop grossier pour une lecture business
5. Dashboard Streamlit avec filtres (segment, éducation, revenu)

## Résultats

| Segment | Clients | Dépense moyenne | Récence (jours) | Taux de réponse |
|---|---|---|---|---|
| Premium actifs | 431 | 1 188 | 23 | 29 % |
| Gros clients à relancer | 478 | 1 175 | 73 | 15 % |
| Petits clients actifs | 566 | 154 | 24 | 15 % |
| Clients à risque | 576 | 145 | 73 | 4 % |

### Insights
- Les deux segments à fortes dépenses représentent environ 86 % du CA.
- À dépenses égales, la récence change fortement la réponse aux campagnes
  (29 % vs 15 % chez les gros clients, 15 % vs 4 % chez les petits).
- Les « gros clients à relancer » pèsent environ 45 % du CA mais n'ont
  rien acheté depuis 73 jours en moyenne : principal risque et principale
  opportunité.

### Recommandations
- **Premium actifs** : fidélité et offres exclusives (vins, viande).
- **Gros clients à relancer** : campagne de réactivation prioritaire.
- **Petits clients actifs** : promotions pour augmenter fréquence et panier.
- **Clients à risque** : éviter les campagnes coûteuses, canal peu cher.

## Limites
- La récence est peu corrélée aux dépenses : la segmentation repose
  surtout sur la fréquence et le montant.
- Les clusters décrivent des profils, pas des causes.
- Taux de réponse basé sur une seule campagne.

## Dashboard

**Démo en ligne** : https://segmentation-clients-rfm.streamlit.app


## Lancer le projet
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Structure
```
├── data/            # marketing_segmented.csv
├── notebooks/       # 01 nettoyage, 02 EDA, 03 RFM, 04 segmentation
├── images/          # captures d'écran
├── app.py           # dashboard Streamlit
└── requirements.txt
```