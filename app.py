import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Segments clients", layout="wide")


@st.cache_data
def charger():
    return pd.read_csv("data/marketing_segmented.csv", parse_dates=["Dt_Customer"])


df = charger()
mnt_cols = [c for c in df.columns if c.startswith("Mnt")]
canaux = ["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]

st.title("Segmentation clients : quels segments sont les plus rentables ?")
st.caption("Dataset : Customer Personality Analysis (2 051 clients après nettoyage)")

# Filtres
st.sidebar.header("Filtres")
tous_seg = sorted(df["Segment"].unique())
tous_edu = sorted(df["Education"].unique())
segments = st.sidebar.multiselect("Segments", tous_seg, default=tous_seg)
educ = st.sidebar.multiselect("Éducation", tous_edu, default=tous_edu)
rmin, rmax = int(df["Income"].min()), int(df["Income"].max())
revenu = st.sidebar.slider("Revenu", rmin, rmax, (rmin, rmax))

f = df[
    df["Segment"].isin(segments)
    & df["Education"].isin(educ)
    & df["Income"].between(*revenu)
]
if f.empty:
    st.warning("Aucun client avec ces filtres.")
    st.stop()

# Indicateurs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Clients", f"{len(f):,}")
c2.metric("Dépense moyenne", f"{f['TotalSpent'].mean():.0f}")
c3.metric("Taux de réponse", f"{f['Response'].mean() * 100:.1f} %")
c4.metric("Chiffre d'affaires", f"{f['TotalSpent'].sum():,.0f}")

# Part des clients vs part du CA
st.subheader("Part des clients et du chiffre d'affaires par segment")
part = f.groupby("Segment").agg(Clients=("ID", "count"), CA=("TotalSpent", "sum"))
part = (part / part.sum() * 100).round(1).reset_index()
part = part.melt(id_vars="Segment", var_name="Indicateur", value_name="Part (%)")
st.plotly_chart(px.bar(part, x="Segment", y="Part (%)", color="Indicateur", barmode="group"))

# Réponse aux campagnes et canaux
g1, g2 = st.columns(2)
with g1:
    st.subheader("Taux de réponse (dernière campagne)")
    rep = (f.groupby("Segment")["Response"].mean() * 100).round(1).reset_index()
    rep.columns = ["Segment", "Taux de réponse (%)"]
    st.plotly_chart(px.bar(rep, x="Segment", y="Taux de réponse (%)", color="Segment"))
with g2:
    st.subheader("Canaux d'achat (moyenne par client)")
    can = f.groupby("Segment")[canaux].mean().reset_index()
    can = can.melt(id_vars="Segment", var_name="Canal", value_name="Achats moyens")
    st.plotly_chart(px.bar(can, x="Segment", y="Achats moyens", color="Canal", barmode="group"))

# Dépenses par catégorie
st.subheader("Dépenses moyennes par catégorie de produit")
mnt = f.groupby("Segment")[mnt_cols].mean().reset_index()
mnt = mnt.melt(id_vars="Segment", var_name="Catégorie", value_name="Dépense moyenne")
st.plotly_chart(px.bar(mnt, x="Segment", y="Dépense moyenne", color="Catégorie"))

# Revenu vs dépenses
st.subheader("Revenu vs dépenses totales")
st.plotly_chart(px.scatter(f, x="Income", y="TotalSpent", color="Segment", opacity=0.6))

# Tableau récapitulatif
st.subheader("Résumé par segment")
resume = f.groupby("Segment").agg(
    Clients=("ID", "count"),
    Depense_moyenne=("TotalSpent", "mean"),
    Recence_jours=("Recency", "mean"),
    Revenu_moyen=("Income", "mean"),
    Taux_reponse=("Response", "mean"),
).round(2)
st.dataframe(resume)