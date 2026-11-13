# =================================================================
# Animation: Monatsumsatz je Kategorie als gestapelte Fläche,
# die von unten nach oben wächst.
#
# Ergebnis: ein GIF, das einmal abläuft und auf dem letzten Bild
# stehen bleibt (für Anhang A5 der CEO-Präsentation).
#
# Grundidee wie bei einem Daumenkino:
#   Wir zeichnen 121 einzelne Bilder. Auf jedem Bild sind die
#   Schichten ein kleines Stück weiter gewachsen. Hintereinander
#   abgespielt (alle 30 Millisekunden ein Bild) sieht das wie
#   eine flüssige Bewegung aus.
# =================================================================

import io                                    # damit wir Bilder im Arbeitsspeicher statt auf der Festplatte ablegen können
import numpy as np                           # Rechnen mit Zahlenreihen (z. B. Schichten aufaddieren)
import pandas as pd                          # Tabellen einlesen und gruppieren
import seaborn as sns                        # einheitlicher Grundstil für Diagramme
import matplotlib.pyplot as plt              # das eigentliche Zeichnen
import matplotlib.transforms as mt           # Umrechnung zwischen Koordinatensystemen (für die Legende)
from matplotlib.colors import LinearSegmentedColormap   # eigener Farbverlauf
from matplotlib.patches import Rectangle     # kleine Farbkästchen für die Legende
from PIL import Image                        # Bilder zu einem GIF zusammensetzen


# =================================================================
# 1. EINSTELLUNGEN
#
# Hier stehen alle Werte, die man vielleicht einmal ändern möchte:
# Dateinamen und Farben. Wer das Skript auf einem anderen Rechner
# laufen lässt, muss nur diese Zeilen anpassen.
# =================================================================

DATEI_ORDERLINES = "orderlines_cl.csv"                      # bereinigte Bestellpositionen (eine Zeile pro gekauftem Produkt)
DATEI_KATEGORIEN = "products_kategorie_vorlaeufig.csv"      # unsere eigene Zuordnung: welche SKU gehört zu welcher Kategorie
DATEI_GIF = "A5_Umsatz_Jahresverlauf_Animation.gif"         # so heißt die fertige Animation

BG = "#0A0A0C"        # Hintergrund: fast schwarz, wie in der ganzen Präsentation
FG = "#EDEDF0"        # Schrift: fast weiß
MUTE = "#8A8F99"      # gedämpftes Grau, z. B. für die Beschriftung der y-Achse


# =================================================================
# 2. DATEN VORBEREITEN
#
# Ziel: eine Tabelle mit einer Zeile pro Kategorie und einer
# Spalte pro Monat. In jeder Zelle steht der Umsatz in Mio. €.
#
#               Jan 17   Feb 17   ...   Nov 17   ...
#   Mac          0,46     0,22    ...    1,15    ...
#   Speicher     0,29     0,17    ...    0,55    ...
#   ...
#
# Danach legen wir die Farben fest und drehen die Reihenfolge um,
# damit beim Stapeln die kleinste Kategorie unten liegt und Mac
# ganz oben.
# =================================================================

# Beide Dateien einlesen und über die SKU (Artikelnummer) verbinden.
# So bekommt jede Bestellposition ihre Kategorie dazu.
kat = pd.read_csv(DATEI_KATEGORIEN)
ol = pd.read_csv(DATEI_ORDERLINES).merge(kat[["sku", "kategorie_vorl"]], on="sku")

# Echter Umsatz einer Position = Preis nach Rabatt × Menge.
# Beispiel: 2 Stück zu je 49,90 € ergeben 99,80 € Umsatz.
ol["umsatz"] = ol.unit_price * ol.product_quantity

# Aus dem Datum wird der Monat, z. B. 2017-11-24 → 2017-11.
ol["monat"] = pd.to_datetime(ol.date).dt.to_period("M")

# Umsatz je Kategorie und Monat aufsummieren und als Tabelle ausbreiten
# (Kategorien als Zeilen, Monate als Spalten). Fehlende Monate werden 0.
tabelle = ol.groupby(["kategorie_vorl", "monat"]).umsatz.sum().unstack(fill_value=0)

# Kategorien nach Gesamtumsatz sortieren: die größte (Mac) zuerst.
reihenfolge = tabelle.sum(axis=1).sort_values(ascending=False).index
tabelle = tabelle.loc[reihenfolge] / 1e6          # in Millionen Euro umrechnen: 1.150.000 € → 1,15

# Lesbare Monatsnamen für die x-Achse, z. B. "Nov 17".
monatsnamen = {1: "Jan", 2: "Feb", 3: "Mär", 4: "Apr", 5: "Mai", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Dez"}
beschriftung = [f"{monatsnamen[p.month]} {str(p.year)[2:]}" for p in tabelle.columns]
x = np.arange(len(beschriftung))                  # Positionen auf der x-Achse: 0, 1, 2, ... 14 (15 Monate)

# Gelber Farbverlauf: fünf Stützfarben von Hellgelb bis Dunkelrot.
# Daraus werden 12 gleichmäßig verteilte Farben, eine pro Kategorie.
# Die größte Kategorie bekommt das hellste Gelb, die kleinste das dunkelste Rot.
verlauf = LinearSegmentedColormap.from_list("flamme", ["#FFF0A0", "#FFC21A", "#FF7A0A", "#D93A10", "#5E1608"])
farben = [verlauf(i / (len(tabelle) - 1)) for i in range(len(tabelle))]

# Reihenfolge umdrehen: Beim Stapeln wird die erste Zeile ganz unten gezeichnet.
# Wir wollen aber die kleinste Kategorie unten und Mac oben.
schichten = tabelle.iloc[::-1]
farben = farben[::-1]
anzahl = len(schichten)                           # 12 Kategorien
nov = beschriftung.index("Nov 17")                # Spaltennummer der höchsten Spitze (Black Friday und Weihnachten)

# Wo stehen die Legendeneinträge? Wir verteilen sie gleichmäßig
# auf der Höhe der y-Achse, von 0,22 bis 2,78 Mio. €.
# Armbänder (unterste Schicht) steht bei 0,22, Mac ganz oben bei 2,78.
legende_y = [0.22 + k * (2.78 - 0.22) / (anzahl - 1) for k in range(anzahl)]


# =================================================================
# 3. EIN EINZELNES BILD ZEICHNEN
#
# Die Funktion bild() zeichnet einen Moment der Animation.
# Sie bekommt eine Liste "anteil" mit 12 Zahlen zwischen 0 und 1:
#   0   = diese Schicht ist noch gar nicht da
#   0,5 = diese Schicht ist halb so hoch wie am Ende
#   1   = diese Schicht ist vollständig gewachsen
#
# Beispiel: anteil = [1, 1, 1, 0.5, 0, 0, ...]
#   → die drei untersten Schichten sind fertig, die vierte ist
#     halb gewachsen, alle darüber fehlen noch.
# =================================================================

def stil():
    """Dunkler Grundstil wie in allen Diagrammen der Präsentation."""
    sns.set_theme(style="ticks")
    plt.style.use("dark_background")
    plt.rcParams.update({"font.family": "Inter", "figure.facecolor": BG, "axes.facecolor": BG,
                         "savefig.facecolor": BG, "axes.edgecolor": "#5A5F69", "xtick.color": FG,
                         "ytick.color": FG, "text.color": FG, "axes.labelcolor": MUTE})

def bild(anteil):
    stil()
    fig, ax = plt.subplots(figsize=(16.5, 7.2))   # Seitenverhältnis passend zur Folie

    # --- Die Flächen stapeln ---
    # Stell dir einen Turm aus Bauklötzen vor: Jeder Klotz liegt auf
    # dem, was darunter schon steht. "basis" ist die aktuelle Höhe
    # des Turms in jedem Monat. Jede neue Schicht beginnt dort und
    # erhöht die Basis um ihre eigene (gerade gewachsene) Höhe.
    # Deshalb entstehen keine Lücken, auch wenn mehrere Schichten
    # gleichzeitig wachsen.
    basis = np.zeros(len(x))                                   # am Anfang ist der Turm 0 hoch
    for k in range(anzahl):
        hoehe = schichten.values[k] * anteil[k]                # z. B. Mac im Nov: 1,15 × 0,5 = 0,575 Mio. €
        if anteil[k] > 0:
            ax.fill_between(x, basis, basis + hoehe, color=farben[k], linewidth=0.6, edgecolor=BG)
        basis = basis + hoehe                                  # der Turm wird höher

    # --- Achsen ---
    ax.set_xticks(x, beschriftung, fontsize=14)                # Monatsnamen unten
    ax.set_xlim(0, len(x) - 1)                                 # Fläche reicht genau von Jan 17 bis Mär 18
    ax.set_ylim(0, 3.1)                                        # feste Höhe, damit die Achse beim Wachsen nicht mitspringt
    ax.set_ylabel("Umsatz in Mio. €", fontsize=18)
    ax.tick_params(axis="y", labelsize=17)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))   # deutsches Komma: 2,5 statt 2.5

    # --- Legende, die mit der Spitze mitwächst ---
    # Zuerst berechnen wir, wie hoch die Novemberspitze gerade ist
    # (Summe aller Schichten im November, jeweils mal ihrem Anteil).
    spitze = sum(schichten.values[k][nov] * anteil[k] for k in range(anzahl))

    # Die Legende steht rechts neben dem Diagramm. Für ihre Position
    # mischen wir zwei Koordinatensysteme:
    #   x relativ zur Achse (1,0 = rechter Rand des Diagramms),
    #   y in Mio. €, also auf derselben Skala wie die Flächen.
    # So können wir sagen: "Eintrag bei 1,5 Mio. € Höhe".
    trafo = mt.blended_transform_factory(ax.transAxes, ax.transData)

    for k in range(anzahl):
        y = legende_y[k]
        # Ein Eintrag erscheint erst, wenn die Spitze seine Höhe erreicht.
        # Er blendet sanft ein über die letzten 0,12 Mio. € davor.
        # Beispiel: Eintrag bei 1,50 → unsichtbar bis Spitze 1,38,
        #           halb sichtbar bei 1,44, voll sichtbar ab 1,50.
        sichtbar = max(0.0, min(1.0, (spitze - (y - 0.12)) / 0.12))
        if sichtbar <= 0:
            continue
        ax.add_patch(Rectangle((1.025, y - 0.055), 0.035, 0.11, transform=trafo, color=farben[k],
                               alpha=sichtbar, clip_on=False, linewidth=0))           # Farbkästchen
        ax.text(1.075, y, schichten.index[k], transform=trafo, va="center", fontsize=19,
                color=FG, alpha=sichtbar, clip_on=False)                              # Name der Kategorie

    # --- Rahmen ---
    sns.despine(ax=ax)                                          # obere und rechte Achsenlinie weglassen
    # Fester Rand statt automatischem Layout: So bleibt das Diagramm
    # auf jedem Bild exakt an derselben Stelle und nichts wackelt.
    # rechts = 0,725 heißt: die rechten 27,5 % bleiben frei für die Legende.
    fig.subplots_adjust(left=0.065, right=0.725, top=0.97, bottom=0.08)

    # Bild im Arbeitsspeicher ablegen und zurückgeben.
    # 1600 Pixel breit: Bei größeren GIFs komprimiert Google Slides neu und es wird pixelig.
    puffer = io.BytesIO()
    fig.savefig(puffer, dpi=1600 / 16.5)
    plt.close(fig)                                              # Speicher freigeben, sonst sammeln sich 121 offene Diagramme
    puffer.seek(0)
    return Image.open(puffer).convert("RGB")


# =================================================================
# 4. ZEITACHSE: WANN WÄCHST WELCHE SCHICHT?
#
# Jede Schicht bekommt eine Startzeit und eine Dauer in Sekunden.
# Die Schichten starten versetzt (alle 0,17 Sekunden die nächste)
# und überlappen sich: Die nächste beginnt, bevor die vorige
# fertig ist. Dadurch wirkt es wie eine einzige fließende Bewegung.
#
#   Armbänder:  startet bei 0,25 s, wächst 0,75 s lang
#   Service:    startet bei 0,42 s, wächst 0,75 s lang
#   ...
#   Mac:        startet zuletzt und wächst 1,3 s lang (Höhepunkt)
#
# Dann gehen wir in 30-Millisekunden-Schritten durch die Zeit und
# zeichnen für jeden Zeitpunkt ein Bild.
# =================================================================

def weich(t):
    """Weicher Anlauf und weiches Abbremsen.
    t = Fortschritt von 0 bis 1. Werte außerhalb werden abgeschnitten.
    Wie ein Auto, das sanft anfährt und sanft bremst, statt ruckartig:
      weich(0) = 0, weich(0,25) ≈ 0,16, weich(0,5) = 0,5, weich(0,75) ≈ 0,84, weich(1) = 1"""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

start = [0.25 + 0.17 * k for k in range(anzahl - 1)] + [0.25 + 0.17 * (anzahl - 1) + 0.15]   # Mac startet mit kleiner Extrapause
dauer = [0.75] * (anzahl - 1) + [1.3]                     # alle 0,75 s, nur Mac 1,3 s
ende = max(s + d for s, d in zip(start, dauer)) + 0.05    # Zeitpunkt, an dem die letzte Schicht fertig ist
schritt = 0.03                                            # 30 ms pro Bild, also etwa 33 Bilder pro Sekunde

bilder, zeiten = [], []
t = 0.0
while t <= ende + 1e-9:
    # Für jede Schicht ausrechnen, wie weit sie zum Zeitpunkt t ist.
    # Beispiel: Startzeit 1,0 s, Dauer 0,75 s, jetzt t = 1,3 s
    #   → (1,3 − 1,0) / 0,75 = 0,4 → weich(0,4) ≈ 0,35 → Schicht ist zu 35 % gewachsen.
    anteil = [weich((t - start[k]) / dauer[k]) for k in range(anzahl)]
    bilder.append(bild(anteil))
    zeiten.append(int(schritt * 1000))                    # Anzeigedauer dieses Bildes in Millisekunden
    t += schritt

# Das letzte Bild bleibt etwa 11 Minuten stehen (das Maximum, das GIF zulässt).
# Sonst würde die Animation in Google Slides von vorn beginnen.
zeiten[-1] = 655000


# =================================================================
# 5. ALS GIF SPEICHERN
#
# Ein GIF kann nur 256 Farben gleichzeitig darstellen. Wir müssen
# also eine Palette aussuchen, die alle wichtigen Farben enthält.
# Nimmt man nur das erste Bild (fast leer), fehlen später die
# Gelbtöne. Deshalb legen wir Anfang, Mitte und Ende als Collage
# untereinander und bauen die Palette daraus.
# =================================================================

breite, hoehe = bilder[0].size
collage = Image.new("RGB", (breite, hoehe * 3))
for i, b in enumerate([bilder[0], bilder[len(bilder) // 2], bilder[-1]]):
    collage.paste(b, (0, i * hoehe))
palette = collage.convert("P", palette=Image.ADAPTIVE, colors=255)

# Jedes Bild auf diese Palette umrechnen. dither=NONE heißt: keine
# Punktmuster zum Vortäuschen von Zwischenfarben, damit die Flächen
# sauber und glatt bleiben.
gif = [b.quantize(palette=palette, dither=Image.Dither.NONE) for b in bilder]

# Speichern. Ohne "loop" läuft das GIF genau einmal ab.
gif[0].save(DATEI_GIF, save_all=True, append_images=gif[1:], duration=zeiten, optimize=True)
print(f"{len(bilder)} Bilder, {bilder[0].size[0]} × {bilder[0].size[1]} Pixel, {sum(zeiten[:-1]) / 1000:.1f} Sekunden")
