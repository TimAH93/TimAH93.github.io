# -*- coding: utf-8 -*-
"""
Fallstudie 02 · Eniac – Lohnt es sich, Rabatte zu geben?
=========================================================
Alle Zahlen des Berichts entstehen in dieser Datei, Schritt für Schritt.
Jeder Abschnitt ist eine Zelle (# %%), sodass die Datei auch in Colab /
VS Code zellenweise läuft.

Daten: vier CSV-Dateien von Eniac (Januar 2017 bis März 2018)
  orders.csv      eine Zeile pro Bestellung (Datum, bezahlte Summe, Status)
  orderlines.csv  eine Zeile pro Artikel in einer Bestellung (SKU, Menge, Stückpreis)
  products.csv    der Produktkatalog (SKU, Name, Listenpreis)
  brands.csv      Markenkürzel → Markenname
"""

# %% 1 · Laden --------------------------------------------------------------
import pandas as pd
import numpy as np
import json, sys, os, re

pd.set_option("display.width", 110)
pd.set_option("display.max_columns", 12)
pd.set_option("display.float_format", lambda x: f"{x:,.3f}" if abs(x) < 10 else f"{x:,.1f}")

# Ordner mit den vier CSV-Dateien (in Colab: Dateien hochladen oder Drive einbinden)
DATEN = os.environ.get("ENIAC_DATEN", "./")

orders     = pd.read_csv(DATEN + "orders.csv")
orderlines = pd.read_csv(DATEN + "orderlines.csv")
products   = pd.read_csv(DATEN + "products.csv")
brands     = pd.read_csv(DATEN + "brands.csv")

for name, df in {"orders": orders, "orderlines": orderlines,
                 "products": products, "brands": brands}.items():
    print(f"{name:<11} {df.shape[0]:>8,} Zeilen  {df.shape[1]} Spalten")

# %% 2 · Erster Blick: Was taugen die Daten? --------------------------------
# Zeitraum
orders["created_date"] = pd.to_datetime(orders["created_date"])
print("Zeitraum:", orders.created_date.min().date(), "bis", orders.created_date.max().date())

# Status der Bestellungen: Nur „Completed“ ist ein echter Kauf
status = orders["state"].value_counts()
print(status)
print("Anteil Completed:", round(status["Completed"] / len(orders), 3))

# Preise stehen als Text in der Tabelle – mit zwei Punkten bei Tausendern
print(orderlines["unit_price"].dtype)                       # object = Text
print(orderlines["unit_price"].str.count(r"\.").value_counts())   # 1 Punkt normal, 2 Punkte kaputt

# Der Produktkatalog hat doppelte Zeilen
print("doppelte Zeilen in products:", products.duplicated().sum())
print("doppelte SKUs in products:  ", products["sku"].duplicated().sum())
print("fehlende Preise:            ", products["price"].isna().sum())

# %% 3 · Bereinigung: orders -----------------------------------------------
# Nur abgeschlossene Bestellungen zählen als Umsatz.
orders_c = orders[orders["state"] == "Completed"].copy()
print(f"{len(orders_c):,} abgeschlossene Bestellungen "
      f"({len(orders_c) / len(orders):.1%} aller Bestellungen)")

# %% 4 · Bereinigung: orderlines -------------------------------------------
# Stückpreise wie "1.137.99" sind 1137.99 – der erste Punkt ist ein
# Tausenderpunkt. Alle Werte mit zwei Punkten haben genau dieses Muster:
zwei_punkte = orderlines["unit_price"].str.count(r"\.") == 2
muster_ok   = orderlines.loc[zwei_punkte, "unit_price"].str.match(r"^\d{1,3}\.\d{3}\.\d{2}$").all()
print("zwei Punkte:", zwei_punkte.sum(), "| alle nach dem Muster 1.234.56:", muster_ok)

# Tausenderpunkt entfernen, dann in Zahlen umwandeln
orderlines["unit_price"] = pd.to_numeric(
    orderlines["unit_price"].str.replace(r"^(\d{1,3})\.(\d{3})\.(\d{2})$", r"\1\2.\3", regex=True)
)
orderlines["date"] = pd.to_datetime(orderlines["date"])
print("unit_price ist jetzt", orderlines["unit_price"].dtype)

# Nur Zeilen abgeschlossener Bestellungen
lines = orderlines[orderlines["id_order"].isin(orders_c["order_id"])].copy()
lines["umsatz"] = lines["unit_price"] * lines["product_quantity"]
print(f"{len(lines):,} Bestellzeilen, {lines['umsatz'].sum():,.0f} € Umsatz")

# %% 5 · Nachmessen: Stimmt die Preis-Reparatur? ---------------------------
# Probe: Summe der Zeilen einer Bestellung gegen die tatsächlich bezahlte Summe.
# Die Differenz sollte den Versandkosten entsprechen (0 bis ca. 15 €).
summe_zeilen = lines.groupby("id_order")["umsatz"].sum()
probe = orders_c.set_index("order_id")[["total_paid"]].join(summe_zeilen, how="inner")
probe["differenz"] = probe["total_paid"] - probe["umsatz"]
anteil_passt = probe["differenz"].between(-0.01, 15).mean()
print(f"Bei {anteil_passt:.1%} der Bestellungen liegt die Differenz zwischen 0 und 15 € (Versand).")
print(probe["differenz"].describe().round(2))

# %% 6 · Bereinigung: products ---------------------------------------------
# 6a  Exakte Kopien entfernen
vorher = len(products)
products = products.drop_duplicates()
print(f"Duplikate entfernt: {vorher - len(products):,}  →  {len(products):,} Produkte")

# 6b  Produkte ohne Preis entfernen (darunter der doppelte iMac APP1197)
products = products.dropna(subset=["price"])
print("ohne Preis entfernt → doppelte SKUs:", products["sku"].duplicated().sum())

# 6c  Preise mit drei Nachkommastellen ("599.918", "1.639.792") sind kaputt:
#     Die Produkte wurden tatsächlich für rund ein Zehntel verkauft (59,99 €).
#     Da der echte Listenpreis nicht sicher rekonstruierbar ist, fliegen sie raus.
drei_stellen = products["price"].str.match(r"^(\d{1,3}\.)?\d+\.\d{3}$")
print("Preise mit drei Nachkommastellen:", drei_stellen.sum())
products = products[~drei_stellen].copy()
products["price"] = pd.to_numeric(products["price"])
print(f"{len(products):,} Produkte mit brauchbarem Listenpreis")

# 6d  Marke aus der SKU: die ersten drei Zeichen sind das Markenkürzel
products["marke_kuerzel"] = products["sku"].str[:3]
products = products.merge(brands, left_on="marke_kuerzel", right_on="short", how="left")
products = products.rename(columns={"long": "marke"}).drop(columns=["short"])

# %% 7 · Kategorien aus dem Produktnamen ------------------------------------
# Der Katalog kennt keine Kategorien ("type" ist nur ein Zahlencode). Ich lese
# sie aus dem Produktnamen. Die Reihenfolge der Regeln zählt: der erste Treffer
# gewinnt. Zuerst die Apple-Geräte, damit ein "MacBook Pro | 512GB SSD" nicht
# bei "Speicher" landet. Zubehör-Wörter (Hülle, Kabel …) schließen ein Gerät aus.
ZUBEHOER = r"(case|cover|funda|carcasa|sleeve|cable|adapter|adaptador|charger|cargador|dock|glass|protector|keyboard|teclado|pencil|stylus|stand|support|soporte|hub|skin|mount|holder|bumper|folio)"
regeln = [
    ("Apple-Geräte",           r"apple (iphone|ipad|macbook|imac|mac mini|mac pro)\b(?!.*" + ZUBEHOER + ")"),
    ("Apple-Geräte",           r"apple watch.*(series|gps|nike)"),
    ("Service & Reparatur",    r"\b(applecare|repair|replacement|reparaci|reparación)\b"),
    ("Speicher",               r"\b(ssd|hdd|hard drive|hard disk|disco duro|nas|memory|memoria|ram|microsd|sd card|usb stick|pendrive|flash drive|storage|raid|\d+\s?tb)\b"),
    ("Eingabe & Tabletts",     r"\b(keyboard|teclado|mouse|ratón|trackpad|pencil|stylus|cintiq|intuos|wacom|graphics tablet|tablet gráfica|mobilestudio)\b"),
    ("Bildschirme",            r"\b(monitor|display|pantalla|projector|proyector)\b"),
    ("Hüllen & Schutz",        r"\b(case|cover|funda|carcasa|sleeve|protector|glass|folio|bumper|skin|shell|band|strap|correa)\b"),
    ("Kabel, Adapter & Docks", r"\b(cable|adapter|adaptador|hub|dock|docking|charger|cargador|lightning|thunderbolt|hdmi|usb-c|usb c|displayport|connector|power bank|powerbank|battery)\b"),
    ("Audio",                  r"\b(headphone|headphones|headset|earphone|earphones|earbuds|airpods|speaker|speakers|altavoz|auricular|auriculares|soundbar|beats|homepod|microphone|micrófono|bose|sonos)\b"),
    ("Smart Home & Gadgets",   r"\b(hue|nest|eve|smart|wifi|router|airport|drone|dron|gopro|camera|cámara|watch|fitbit|withings|garmin|tracker|scale|báscula|thermostat|scooter|osmo|gimbal|stabilizer)\b"),
    ("Halterungen",            r"\b(stand|support|soporte|mount|holder|arm|tripod|trípode|bracket)\b"),
]
regeln = [(kat, re.compile(muster)) for kat, muster in regeln]

def kategorie(name):
    n = str(name).lower()
    for kat, muster in regeln:
        if muster.search(n):
            return kat
    return "Sonstiges"

def geraet(name):
    """Feiner: Welches Apple-Gerät? (nur für Apple-Geräte)"""
    n = str(name).lower()
    for g, wort in [("iPhone", "iphone"), ("iPad", "ipad"), ("Mac", "mac"), ("Watch", "watch")]:
        if wort in n:
            return g
    return "andere"

products["kategorie"]    = products["name"].apply(kategorie)
products["apple_geraet"] = products["kategorie"] == "Apple-Geräte"
products["geraet"]       = np.where(products["apple_geraet"], products["name"].apply(geraet), "")
print(products["kategorie"].value_counts())

# %% 8 · Zusammenführen und Rabatt berechnen --------------------------------
verkauf = lines.merge(products[["sku", "name", "price", "marke", "kategorie", "apple_geraet", "geraet"]],
                      on="sku", how="inner", validate="many_to_one")
verloren = len(lines) - len(verkauf)
print(f"{len(verkauf):,} Bestellzeilen mit Produktdaten "
      f"({verloren:,} Zeilen ohne passendes Produkt verworfen, "
      f"{1 - verkauf['umsatz'].sum() / lines['umsatz'].sum():.1%} des Umsatzes)")

# Rabatt = Listenpreis minus bezahlter Preis, als Anteil des Listenpreises.
# Liegt der bezahlte Preis über dem Listenpreis (alte Modelle, der Listenpreis
# wurde später gesenkt), gilt: kein Rabatt (0).
verkauf["rabatt"] = (1 - verkauf["unit_price"] / verkauf["price"]).clip(lower=0)
verkauf["rabatt_eur"] = (verkauf["price"] - verkauf["unit_price"]).clip(lower=0) * verkauf["product_quantity"]
verkauf["monat"] = verkauf["date"].dt.to_period("M")
verkauf["woche"] = verkauf["date"].dt.to_period("W")

print("Median-Rabatt:", f"{verkauf['rabatt'].median():.1%}",
      "| Quartile:", f"{verkauf['rabatt'].quantile(.25):.0%} – {verkauf['rabatt'].quantile(.75):.0%}")
print("Anteil verkaufter Artikel mit Rabatt:", f"{(verkauf['rabatt'] > 0.001).mean():.1%}")
# Wie viele Produkte wurden überhaupt mal rabattiert verkauft?
je_produkt = verkauf.groupby("sku")["rabatt"].max()
print("Anteil Produkte, die mindestens einmal mit Rabatt verkauft wurden:", f"{(je_produkt > 0.001).mean():.1%}")

# %% 9 · Rabattstufen: Wo kommt der Umsatz her? ------------------------------
stufen = pd.cut(verkauf["rabatt"], bins=[-0.001, 0.001, 0.10, 0.20, 0.30, 1.0],
                labels=["kein Rabatt", "bis 10 %", "10–20 %", "20–30 %", "über 30 %"])
nach_stufe = verkauf.groupby(stufen, observed=True).agg(
    zeilen=("umsatz", "size"), stueck=("product_quantity", "sum"),
    umsatz=("umsatz", "sum"), nachlass=("rabatt_eur", "sum"))
nach_stufe["umsatz_anteil"] = nach_stufe["umsatz"] / nach_stufe["umsatz"].sum()
nach_stufe["stueck_anteil"] = nach_stufe["stueck"] / nach_stufe["stueck"].sum()
print(nach_stufe.round(3))

# %% 10 · Apple-Geräte gegen den Rest -----------------------------------------
apple = verkauf.groupby("apple_geraet").agg(
    umsatz=("umsatz", "sum"), stueck=("product_quantity", "sum"),
    rabatt_median=("rabatt", "median"), preis_median=("unit_price", "median"))
apple["umsatz_anteil"] = apple["umsatz"] / apple["umsatz"].sum()
# gewichteter Rabatt: Nachlass in Euro geteilt durch den Listenwert
apple["rabatt_gewichtet"] = verkauf.groupby("apple_geraet").apply(
    lambda g: g["rabatt_eur"].sum() / (g["price"] * g["product_quantity"]).sum(), include_groups=False)
print(apple.round(3))

# Innerhalb der Apple-Geräte: iPhone, iPad, Mac, Watch
geraete = verkauf[verkauf["apple_geraet"]].groupby("geraet").agg(
    umsatz=("umsatz", "sum"), stueck=("product_quantity", "sum"), rabatt_median=("rabatt", "median"))
geraete["rabatt_gewichtet"] = verkauf[verkauf["apple_geraet"]].groupby("geraet").apply(
    lambda g: g["rabatt_eur"].sum() / (g["price"] * g["product_quantity"]).sum(), include_groups=False)
geraete["umsatz_anteil_gesamt"] = geraete["umsatz"] / verkauf["umsatz"].sum()
print(geraete.sort_values("umsatz", ascending=False).round(3))

# Wie viel vom Umsatz jeder Gruppe läuft über tiefe Rabatte (über 30 %)?
tief = verkauf.assign(tief=verkauf["rabatt"] > 0.30).groupby("apple_geraet").apply(
    lambda g: g.loc[g["tief"], "umsatz"].sum() / g["umsatz"].sum(), include_groups=False)
print("Umsatzanteil mit über 30 % Rabatt – Apple-Geräte / Rest:", tief.round(3).to_dict())

# %% 11 · Kategorien: Umsatz und Rabatt --------------------------------------
kat = verkauf.groupby("kategorie").agg(
    umsatz=("umsatz", "sum"), stueck=("product_quantity", "sum"),
    rabatt_median=("rabatt", "median"), produkte=("sku", "nunique")).sort_values("umsatz", ascending=False)
kat["umsatz_anteil"] = kat["umsatz"] / kat["umsatz"].sum()
kat["rabatt_gewichtet"] = verkauf.groupby("kategorie").apply(
    lambda g: g["rabatt_eur"].sum() / (g["price"] * g["product_quantity"]).sum(), include_groups=False)
print(kat.round(3))

# %% 12 · Preisverteilung der verkauften Artikel -----------------------------
preisklassen = pd.cut(verkauf["unit_price"], bins=[0, 25, 100, 300, 1000, 1e9],
                      labels=["bis 25 €", "25–100 €", "100–300 €", "300–1.000 €", "über 1.000 €"])
nach_preis = verkauf.groupby(preisklassen, observed=True).agg(
    stueck=("product_quantity", "sum"), umsatz=("umsatz", "sum"), rabatt_median=("rabatt", "median"))
nach_preis["stueck_anteil"] = nach_preis["stueck"] / nach_preis["stueck"].sum()
nach_preis["umsatz_anteil"] = nach_preis["umsatz"] / nach_preis["umsatz"].sum()
print(nach_preis.round(3))

# %% 13 · Saison: Umsatz und Rabatt pro Monat --------------------------------
monat = verkauf.groupby("monat").agg(
    umsatz=("umsatz", "sum"), stueck=("product_quantity", "sum"),
    rabatt=("rabatt", "mean"), bestellungen=("id_order", "nunique"))
monat["rabatt_gewichtet"] = verkauf.groupby("monat").apply(
    lambda g: g["rabatt_eur"].sum() / (g["price"] * g["product_quantity"]).sum(), include_groups=False)
print(monat.round(3))
print("Korrelation Rabatt (gewichtet) ↔ Stück pro Monat:",
      round(monat["rabatt_gewichtet"].corr(monat["stueck"]), 2))

# %% 14 · Black Friday und Weihnachten ---------------------------------------
# Black Friday 2017 war am 24. November. Ich vergleiche die Woche (Mo–So)
# mit dem Durchschnitt aller anderen Wochen.
woche = verkauf.groupby("woche").agg(umsatz=("umsatz", "sum"), stueck=("product_quantity", "sum"),
                                     rabatt=("rabatt", "mean"))
woche["rabatt_gewichtet"] = verkauf.groupby("woche").apply(
    lambda g: g["rabatt_eur"].sum() / (g["price"] * g["product_quantity"]).sum(), include_groups=False)
bf_woche = pd.Period("2017-11-24", freq="W")
normal = woche.drop(index=bf_woche)
print("Black-Friday-Woche:", woche.loc[bf_woche].round(3).to_dict())
print("andere Wochen (Durchschnitt):", normal.mean().round(3).to_dict())
print("Faktor Umsatz:", round(woche.loc[bf_woche, "umsatz"] / normal["umsatz"].mean(), 1))

# Top-Wochen nach Umsatz
print(woche.sort_values("umsatz", ascending=False).head(6).round(3))

# Was wurde in der Black-Friday-Woche gekauft? Rabattstufen im Vergleich
bf_lines = verkauf[verkauf["woche"] == bf_woche]
rest_lines = verkauf[verkauf["woche"] != bf_woche]
bf_stufen = pd.DataFrame({
    "black_friday": bf_lines.groupby(pd.cut(bf_lines["rabatt"], bins=[-0.001, 0.001, 0.10, 0.20, 0.30, 1.0],
                                            labels=nach_stufe.index), observed=True)["umsatz"].sum() / bf_lines["umsatz"].sum(),
    "andere_wochen": rest_lines.groupby(pd.cut(rest_lines["rabatt"], bins=[-0.001, 0.001, 0.10, 0.20, 0.30, 1.0],
                                               labels=nach_stufe.index), observed=True)["umsatz"].sum() / rest_lines["umsatz"].sum()})
print(bf_stufen.round(3))
print("Apple-Anteil am Umsatz – Black-Friday-Woche:",
      f"{bf_lines.loc[bf_lines['apple_geraet'], 'umsatz'].sum() / bf_lines['umsatz'].sum():.1%}",
      "| sonst:", f"{rest_lines.loc[rest_lines['apple_geraet'], 'umsatz'].sum() / rest_lines['umsatz'].sum():.1%}")

# Dezember (Weihnachten) gegen den Durchschnitt der übrigen Monate
dez = monat.loc[pd.Period("2017-12", freq="M"), "umsatz"]
print("Dezember 2017 gegenüber dem Mittel der anderen Monate (ohne Nov):",
      round(dez / monat.drop(index=[pd.Period("2017-11", freq="M"), pd.Period("2017-12", freq="M")])["umsatz"].mean(), 2))

# %% 15 · Wirkt der Rabatt beim einzelnen Produkt? ---------------------------
# Vergleich innerhalb desselben Produkts: Wochen, in denen es stärker
# rabattiert war als in seinem eigenen Durchschnitt, gegen die übrigen Wochen.
# So vergleiche ich nicht Äpfel mit Kabeln, sondern jedes Produkt mit sich selbst.
sw = verkauf.groupby(["sku", "woche"]).agg(stueck=("product_quantity", "sum"), umsatz=("umsatz", "sum"),
                                           rabatt=("rabatt", "mean")).reset_index()
wochen_pro_sku = sw.groupby("sku")["woche"].nunique()
dauerbrenner = wochen_pro_sku[wochen_pro_sku >= 20].index          # in mindestens 20 Wochen verkauft
sw = sw[sw["sku"].isin(dauerbrenner)].copy()
sw["rabatt_mittel_sku"] = sw.groupby("sku")["rabatt"].transform("mean")
sw["hoch"] = sw["rabatt"] > sw["rabatt_mittel_sku"] + 0.05          # mind. 5 Punkte über dem eigenen Schnitt
vergleich = sw.groupby(["sku", "hoch"]).agg(stueck=("stueck", "mean"), umsatz=("umsatz", "mean"),
                                            rabatt=("rabatt", "mean")).unstack()
vergleich = vergleich.dropna()
vergleich["faktor_stueck"] = vergleich[("stueck", True)] / vergleich[("stueck", False)]
vergleich["faktor_umsatz"] = vergleich[("umsatz", True)] / vergleich[("umsatz", False)]
vergleich["mehr_rabatt"]   = vergleich[("rabatt", True)] - vergleich[("rabatt", False)]
print(f"{len(dauerbrenner)} Dauerbrenner, davon {len(vergleich)} mit Wochen in beiden Gruppen")
print("Median: zusätzlicher Rabatt in den 'hohen' Wochen:", f"{vergleich['mehr_rabatt'].median():.1%} Punkte")
print("Median-Faktor Stück/Woche  (hoher Rabatt ÷ normal):", round(vergleich["faktor_stueck"].median(), 2))
print("Median-Faktor Umsatz/Woche (hoher Rabatt ÷ normal):", round(vergleich["faktor_umsatz"].median(), 2))
print("Anteil Produkte, die mit hohem Rabatt mehr Stück verkaufen:", f"{(vergleich['faktor_stueck'] > 1).mean():.0%}")
print("Anteil Produkte, die mit hohem Rabatt mehr Umsatz machen:  ", f"{(vergleich['faktor_umsatz'] > 1).mean():.0%}")

# Dasselbe getrennt nach Apple-Geräten und Zubehör
vergleich.columns = ["_".join(map(str, c)).rstrip("_") for c in vergleich.columns]
vergleich = vergleich.join(products.set_index("sku")["apple_geraet"])
print(vergleich.groupby("apple_geraet")[["faktor_stueck", "faktor_umsatz", "mehr_rabatt"]].median().round(2))
print(vergleich.groupby("apple_geraet").size())

# %% 16 · Was kostet der Rabatt? ---------------------------------------------
nachlass_gesamt = verkauf["rabatt_eur"].sum()
listenwert = (verkauf["price"] * verkauf["product_quantity"]).sum()
print(f"Umsatz: {verkauf['umsatz'].sum():,.0f} €  |  Nachlass: {nachlass_gesamt:,.0f} €  "
      f"({nachlass_gesamt / listenwert:.1%} des Listenwerts)")
print("Nachlass nach Stufe (Anteil):", (nach_stufe["nachlass"] / nachlass_gesamt).round(3).to_dict())

# %% 17 · Ergebnisse für den Bericht sichern ---------------------------------
ergebnis = {
    "orders_gesamt": int(len(orders)), "orders_completed": int(len(orders_c)),
    "anteil_completed": float(len(orders_c) / len(orders)),
    "status": status.to_dict(),
    "zeitraum": [str(orders.created_date.min().date()), str(orders.created_date.max().date())],
    "zwei_punkte": int(zwei_punkte.sum()), "probe_passt": float(anteil_passt),
    "products_roh": int(vorher), "products_sauber": int(len(products)), "drei_stellen": int(drei_stellen.sum()),
    "lines_completed": int(len(lines)), "lines_mit_produkt": int(len(verkauf)), "lines_verloren": int(verloren),
    "umsatz": float(verkauf["umsatz"].sum()), "umsatz_lines": float(lines["umsatz"].sum()), "nachlass": float(nachlass_gesamt), "listenwert": float(listenwert),
    "rabatt_median": float(verkauf["rabatt"].median()),
    "rabatt_q25": float(verkauf["rabatt"].quantile(.25)), "rabatt_q75": float(verkauf["rabatt"].quantile(.75)),
    "anteil_mit_rabatt": float((verkauf["rabatt"] > 0.001).mean()),
    "anteil_produkte_mit_rabatt": float((je_produkt > 0.001).mean()),
    "stufen": nach_stufe.reset_index().rename(columns={"rabatt": "stufe"}).astype({"stufe": str}).to_dict(orient="records"),
    "apple": apple.reset_index().to_dict(orient="records"),
    "kategorien": kat.reset_index().to_dict(orient="records"),
    "preisklassen": nach_preis.reset_index().rename(columns={"unit_price": "klasse"}).astype({"klasse": str}).to_dict(orient="records"),
    "monate": monat.reset_index().astype({"monat": str}).to_dict(orient="records"),
    "korr_monat": float(monat["rabatt_gewichtet"].corr(monat["stueck"])),
    "bf": {"woche": woche.loc[bf_woche].to_dict(), "normal": normal.mean().to_dict(),
           "faktor": float(woche.loc[bf_woche, "umsatz"] / normal["umsatz"].mean())},
    "top_wochen": woche.sort_values("umsatz", ascending=False).head(6).reset_index().astype({"woche": str}).to_dict(orient="records"),
    "geraete": geraete.reset_index().to_dict(orient="records"),
    "tief_anteil": {str(k): float(v) for k, v in tief.items()},
    "bf_stufen": bf_stufen.reset_index().rename(columns={"rabatt": "stufe"}).astype({"stufe": str}).to_dict(orient="records"),
    "bf_apple_anteil": [float(bf_lines.loc[bf_lines['apple_geraet'], 'umsatz'].sum() / bf_lines['umsatz'].sum()),
                        float(rest_lines.loc[rest_lines['apple_geraet'], 'umsatz'].sum() / rest_lines['umsatz'].sum())],
    "elastisch": {"dauerbrenner": int(len(dauerbrenner)), "mit_beiden": int(len(vergleich)),
                  "mehr_rabatt_median": float(vergleich["mehr_rabatt"].median()),
                  "rabatt_normal_median": float(vergleich["rabatt_False"].median()),
                  "rabatt_hoch_median": float(vergleich["rabatt_True"].median()),
                  "faktor_stueck_median": float(vergleich["faktor_stueck"].median()),
                  "faktor_umsatz_median": float(vergleich["faktor_umsatz"].median()),
                  "anteil_mehr_stueck": float((vergleich["faktor_stueck"] > 1).mean()),
                  "anteil_mehr_umsatz": float((vergleich["faktor_umsatz"] > 1).mean()),
                  "nach_gruppe": vergleich.groupby("apple_geraet")[["faktor_stueck", "faktor_umsatz", "mehr_rabatt"]].median().reset_index().to_dict(orient="records"),
                  "n_gruppe": {str(k): int(v) for k, v in vergleich.groupby("apple_geraet").size().items()}},
}
with open(os.environ.get("ENIAC_ERGEBNIS", "ergebnis_eniac.json"), "w", encoding="utf-8") as f:
    json.dump(ergebnis, f, ensure_ascii=False, indent=1, default=str)
print("gespeichert.")
