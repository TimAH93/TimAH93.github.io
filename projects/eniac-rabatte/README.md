# Eniac · Do the Discounts Pay Off?

**English** · [Deutsch](README.de.md)

### Discount analysis for an online retailer of Apple products

**Do Eniac's discounts pay off?**
A data-driven answer for the CEO: Python → charts → presentation → recommendation

![Python](https://img.shields.io/badge/Python-pandas%20%C2%B7%20matplotlib-F28E2B)
![Pillow](https://img.shields.io/badge/Pillow-animated%20charts-F28E2B)
![JavaScript](https://img.shields.io/badge/JavaScript-pptxgenjs-E15759)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-E15759)

[![The presentation at a glance](video/teaser_en.gif)](video/Eniac_Presentation_Video_EN.mp4)

*The presentation at a glance, at double speed. Click to open the full video (2:30 minutes, no sound); the slides are also available [as a PDF](presentation/Eniac_CEO_Presentation_EN.pdf).*

[Project](#project) · [Question](#question) · [Key Numbers](#key-numbers) · [Approach](#approach) · [Findings](#findings) · [Recommendation](#recommendation) · [My Contribution](#my-contribution) · [Files](#files) · [Team](#team)

---

## Project

Eniac is an online retailer of Apple products and accessories in Spain. Almost everything is sold at a discount. The CEO wanted to know whether this pays off. Our task as a team: analyse the sales data from January 2017 to March 2018 and present the answer in a five-minute presentation, with an appendix for follow-up questions.

> Group project in the "Data Analysis and AI" training at WBS Coding School, presented on 13 November 2026. Eniac is a case study provided by the course.

## Question

> **Do Eniac's discounts pay off?**

| # | Sub-question | Perspective | Answer |
|---|---|---|---|
| 1 | Do discounts drive revenue? | Marketing | Yes, but not everywhere. |
| 2 | Do discounts cost us revenue and reputation? | Board | Not our reputation, but money in the wrong place. |

**Overall answer:** We're not losing money. But we're missing out on money we could be earning.

## Key Numbers

**Data**

| Metric | Value |
|---|---|
| Period | 437 days (January 2017 to March 2018) |
| Completed orders | 46,605 (of 226,909 before cleaning) |
| Products in the catalogue | 9,992 (of 19,326 before cleaning) |
| Revenue | €15.9M |

**Discounts**

| Metric | Value |
|---|---|
| Discounted items | 93% (56,203 of 60,375) |
| Strongest month | November 2017: €2.89M revenue, 21.5% avg. discount |
| Macs | 41% of revenue, only 10.3% discount, but €0.77M in discount money |
| Apple overall | about 11% discount, but €1.17M in discount money, almost half of all discount money |
| Other brands | about 18% discount, three times as many units sold, but less revenue |

## Approach

```mermaid
flowchart LR
    A[Raw data<br/>4 tables] --> B[Cleaning<br/>pandas]
    B --> C[Analysis<br/>2 sub-questions]
    C --> D[Charts<br/>matplotlib + Pillow]
    D --> E[Presentation<br/>pptxgenjs]
    E --> F[Recommendation<br/>with test plan]
```

1. **Clean the data.** Only completed orders count as revenue. 36,169 unit prices were stored as text in the format `1.234.56`. Because all of them follow this format, the first dot is clearly a thousands separator; we removed it instead of deleting the rows (deleting would have cost about 46% of revenue). In the product catalogue the format was ambiguous, so we deleted 542 prices there: a missing price is visible, a wrongly repaired one silently distorts the discount. We also removed duplicates and rows with missing values.
2. **Build a working table.** Every item sold, with revenue, list-price revenue, discount in percent and in euros, category and brand.
3. **Answer the two sub-questions.** Monthly trend, categories, brands, price classes, and a direct comparison of Apple against all other brands.
4. **Calculate the recommendation.** What one percentage point of Apple discount is worth, how many sales could drop without losing revenue, and what shifting the discount would bring.
5. **Present.** One main question, two sub-questions with short answers, one recommendation with numbers. Everything for follow-up questions goes into an appendix with a linked overview (A1 to A7).

## Findings

Click a chart to open the notebook. Below each chart you can expand the code that produced it.

### Discounts are standard, but November sells itself

93% of all items are sold at a discount. The strongest month is November 2017, with Black Friday and €2.89M in revenue.

[![Monthly trend of revenue and discount](images/en/monthly_trend.png)](code/analyse/Eniac_Rabattanalyse.ipynb)

<details>
<summary>Show the code for this chart</summary>

Excerpt from the [notebook](code/analyse/Eniac_Rabattanalyse.ipynb), section T1.3 (variable names in German). It uses the working table `basis` and the helper functions `de()` and `balken_abrunden()` from the first cell. The animated version is built the same way in [`code/diagramme/bestell_linien.py`](code/diagramme/bestell_linien.py).

```python
monate = basis.groupby("monat").agg(umsatz=("umsatz", "sum"),
                                    bestellungen=("id_order", "nunique"),
                                    rabatt=("rabatt", "mean"))

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(monate))
farben = [ORANGE if str(m) == "2017-11" else "#8F5420" for m in monate.index]
ax.bar(x, monate["umsatz"] / 1e6, color=farben, width=0.65)
ax.set_xticks(x, [m.strftime("%b %y") for m in monate.index], fontsize=10)
ax.set_ylabel("Umsatz in Mio. €")
ax.set_ylim(0, 3.4)

ax2 = ax.twinx()
ax2.plot(x, monate["rabatt"] * 100, color=ROT, lw=2.5, marker="o")
ax2.set_ylim(0, 30); ax2.set_ylabel("Ø Rabatt in %", color=ROT)
ax2.spines["right"].set_visible(True); ax2.tick_params(axis="y", colors=ROT)

ax.set_title("Umsatz und Ø Rabatt pro Monat · November 2017 ist der stärkste Monat")
balken_abrunden(ax, 6)
plt.tight_layout(); plt.show()

nov = monate.loc["2017-11"]
print(f"November 2017: {de(nov['umsatz'] / 1e6, 2)} Mio. € Umsatz, "
      f"{de(nov['bestellungen'], 0)} Bestellungen, Ø Rabatt {de(nov['rabatt'] * 100)} %")
print(f"Ø Rabatt über alle Monate: {de(basis['rabatt'].mean() * 100)} %")
```

</details>

### Macs carry the revenue

Macs bring in 41% of revenue.

[![Revenue by category](images/en/revenue_by_category.png)](code/analyse/Eniac_Rabattanalyse.ipynb)

<details>
<summary>Show the code for this chart</summary>

Excerpt from the [notebook](code/analyse/Eniac_Rabattanalyse.ipynb), section T1.4 (variable names in German). It uses the working table `basis` and the helper functions `de()` and `balken_abrunden()` from the first cell. The animated version is built the same way in [`code/diagramme/gifs2.py`](code/diagramme/gifs2.py).

```python
kategorien = (basis.groupby("kategorie")
              .agg(umsatz=("umsatz", "sum"), rabatt_eur=("rabatt_eur", "sum"),
                   listenumsatz=("listenumsatz", "sum"), rabatt_mittel=("rabatt", "mean"))
              .sort_values("umsatz"))
kategorien["anteil_umsatz"] = kategorien["umsatz"] / kategorien["umsatz"].sum() * 100

fig, ax = plt.subplots(figsize=(12, 6))
farben = [ORANGE if k == "Mac" else "#6B4A2A" for k in kategorien.index]
ax.barh(kategorien.index, kategorien["umsatz"] / 1e6, color=farben, height=0.62)
for i, (u, a) in enumerate(zip(kategorien["umsatz"], kategorien["anteil_umsatz"])):
    ax.text(u / 1e6 + 0.06, i, f"{de(u / 1e6, 2)} Mio. € · {de(a)} %", va="center", fontsize=11)
ax.set_xlim(0, 7.6); ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.set_title("Umsatz je Kategorie · Macs bringen rund 41 % des Umsatzes")
balken_abrunden(ax, 8, "rechts")
plt.tight_layout(); plt.show()

kategorien.sort_values("umsatz", ascending=False)[["umsatz", "anteil_umsatz"]].round(1).head(4)
```

</details>

### Apple: low discount rate, but almost half of all discount money

Apple gets about 11% discount on average, other brands about 18%. Because Apple devices are expensive, €1.17M in discount money still goes to Apple, almost half of the total.

[![Apple vs. other brands](images/en/apple_vs_others.png)](code/analyse/Eniac_Rabattanalyse.ipynb)

<details>
<summary>Show the code for this chart</summary>

Excerpt from the [notebook](code/analyse/Eniac_Rabattanalyse.ipynb), section T2.3 (variable names in German). It uses the working table `basis` and the helper functions `de()` and `balken_abrunden()` from the first cell. The animated version is built the same way in [`code/diagramme/welten3.py`](code/diagramme/welten3.py).

```python
vergleich = basis.groupby("ist_apple").agg(stueck=("product_quantity", "sum"), umsatz=("umsatz", "sum"),
                                           rabatt_eur=("rabatt_eur", "sum"), listenumsatz=("listenumsatz", "sum"))
vergleich.index = vergleich.index.map({True: "Apple", False: "Andere"})

kennzahlen = pd.DataFrame({
    "Anteil Stück": vergleich["stueck"] / vergleich["stueck"].sum() * 100,
    "Anteil Umsatz": vergleich["umsatz"] / vergleich["umsatz"].sum() * 100,
    "Ø Rabatt": vergleich["rabatt_eur"] / vergleich["listenumsatz"] * 100,
    "Anteil Rabattgeld": vergleich["rabatt_eur"] / vergleich["rabatt_eur"].sum() * 100,
}).T[["Apple", "Andere"]]
beschriftung = ["Anteil an\nverkauften Stück", "Anteil am\nUmsatz", "Ø Rabatt", "Anteil am\nRabattgeld"]

fig, ax = plt.subplots(figsize=(12, 5.5))
x = np.arange(4); b = 0.38
apple_farben = [BLAU, ORANGE, ROT, ROT]
andere_farben = ["#2A5E86", "#8F5420", "#8C3A3B", "#8C3A3B"]
ax.bar(x - b / 2, kennzahlen["Apple"], width=b, color=apple_farben)
ax.bar(x + b / 2, kennzahlen["Andere"], width=b, color=andere_farben)
for i, (a, n) in enumerate(zip(kennzahlen["Apple"], kennzahlen["Andere"])):
    ax.text(i - b / 2, a + 1.5, f"{de(a, 0)} %", ha="center", fontsize=15, fontweight="bold")
    ax.text(i + b / 2, n + 1.5, f"{de(n, 0)} %", ha="center", fontsize=15, fontweight="bold")
    ax.text(i - b / 2, 1.5, "Apple", ha="center", fontsize=10, color=BG, fontweight="bold")
    ax.text(i + b / 2, 1.5, "Andere", ha="center", fontsize=10, color=FG, fontweight="bold")
ax.set_xticks(x, beschriftung, fontsize=12); ax.set_yticks([]); ax.set_ylim(0, 90)
ax.spines["left"].set_visible(False)
ax.set_title("Apple: wenig Stück, viel Umsatz, wenig Rabatt – aber fast die Hälfte des Rabattgelds")
balken_abrunden(ax, 8)
plt.tight_layout(); plt.show()

print("Rabattgeld Apple:", de(vergleich.loc["Apple", "rabatt_eur"] / 1e6, 2), "Mio. €")
kennzahlen.round(1)
```

</details>

### Low percentage, high amount

Macs get only 10.3% discount, but in euros that is €0.77M (31% of all discount money). Cases and bags are the opposite: 32.7% discount, but only €0.15M.

[![Discount by category in percent and in euros](images/en/discount_by_category.png)](code/analyse/Eniac_Rabattanalyse.ipynb)

<details>
<summary>Show the code for this chart</summary>

Excerpt from the [notebook](code/analyse/Eniac_Rabattanalyse.ipynb), section A5 (variable names in German). It uses the working table `basis` and the helper functions `de()` and `balken_abrunden()` from the first cell. The animated version is built the same way in [`code/diagramme/a4_kombi.py`](code/diagramme/a4_kombi.py).

```python
k = kategorien.sort_values("rabatt_eur")
k["anteil_rabattgeld"] = k["rabatt_eur"] / k["rabatt_eur"].sum() * 100

fig, (links, rechts) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
links.barh(k.index, k["rabatt_mittel"] * 100, color=ROT, height=0.62)
rechts.barh(k.index, k["rabatt_eur"] / 1e6, color=ROT, height=0.62)
for i, (p, e) in enumerate(zip(k["rabatt_mittel"] * 100, k["rabatt_eur"] / 1e6)):
    links.text(p + 0.4, i, f"{de(p)} %", va="center", fontsize=10)
    rechts.text(e + 0.01, i, f"{de(e, 2)} Mio. €", va="center", fontsize=10)
links.set_title("Ø Rabatt in %"); rechts.set_title("Rabatt in Euro")
links.set_xlim(0, 40); rechts.set_xlim(0, 0.95)
for achse in (links, rechts):
    achse.set_xticks([]); achse.spines["bottom"].set_visible(False)
    balken_abrunden(achse, 6, "rechts")
plt.tight_layout(); plt.show()

k.loc[["Mac", "Hüllen und Taschen"], ["rabatt_mittel", "rabatt_eur", "anteil_rabattgeld"]].round(3)
```

</details>

## Recommendation

| # | Lever | Reason |
|---|---|---|
| 1 | **Lower the Apple discount** | Each percentage point is worth about €105,000. |
| 2 | **Target discounts at other brands** | There, discounts work as a purchase incentive. |
| 3 | **Discount outside the peak season** | In November, customers buy anyway. |

**Example calculation (January 2017 to March 2018):** With the money saved on the Apple discount, the discount on other brands could rise from 18% to up to 25% at the same budget. Or Eniac keeps the money: up to €0.54M more revenue at the same unit sales.

[![Shifting the discount](images/en/shift_discount.png)](code/analyse/Eniac_Rabattanalyse.ipynb)

<details>
<summary>Show the code for this chart</summary>

Excerpt from the [notebook](code/analyse/Eniac_Rabattanalyse.ipynb), section E.3 (variable names in German). It uses the working table `basis` and the helper functions `de()` and `balken_abrunden()` from the first cell. The animated version is built the same way in [`code/diagramme/regler_balken.py`](code/diagramme/regler_balken.py).

```python
stufen = [10, 9, 8, 7, 6]
szenario = pd.DataFrame({"apple_rabatt": stufen})
szenario["frei_mio"] = listen_apple * (rabatt_apple - szenario["apple_rabatt"]) / 100 / 1e6
szenario["andere_rabatt"] = rabatt_andere + szenario["frei_mio"] * 1e6 / listen_andere * 100

fig, ax = plt.subplots(figsize=(12, 5.5))
x = np.arange(len(stufen))
ax.bar(x, szenario["frei_mio"], color=ORANGE, width=0.58)
for i, f in enumerate(szenario["frei_mio"]):
    ax.text(i, f + 0.015, f"+{de(f, 2)} Mio. €", ha="center", fontsize=13, fontweight="bold")
ax.set_xticks(x, [f"Apple {s} %" for s in stufen], fontsize=12)
ax.set_ylim(0, 0.8); ax.set_yticks([]); ax.spines["left"].set_visible(False)

ax2 = ax.twinx()
ax2.plot(x, szenario["andere_rabatt"], color=ROT, lw=3, marker="o", ms=8)
for i, r in enumerate(szenario["andere_rabatt"]):
    ax2.text(i, r + 1.2, f"{de(r)} %", ha="center", color=ROT, fontsize=12, fontweight="bold")
ax2.set_ylim(-8, 32); ax2.axis("off")

ax.set_title("Beispielrechnung · Einbehalten (Balken) oder auf andere Marken umschichten (Linie)")
balken_abrunden(ax, 8)
plt.tight_layout(); plt.show()

print(f"Andere Marken heute: {de(rabatt_andere)} % Rabatt")
szenario.round(2)
```

</details>

**Buffer and test plan:** At 7% instead of 11.1% Apple discount, up to 4.5% fewer Apple devices could be sold without losing revenue. Proposed test: offer iPads at 7% instead of 11% discount for six weeks, not in November, and compare with the same weeks of the previous year. If sales drop by less than 4.5%, roll the change out.

### Limits of the data

- **No purchase prices:** margins can only be estimated in scenarios (appendix A4).
- **No customer ID:** new customers and loyalty cannot be measured.

That is why we do not claim that discounts lose money, and propose tests instead.

## My Contribution

The three of us presented together. Organisation, code and design were mostly my part.

#### What I built

- **Project organisation:** set up the group document with a question tree: main question, sub-questions F1 to F6, owners and a consistent template for the answers
- **Cleaning orders and orderlines:** repaired 36,169 prices with two dots instead of deleting them, because otherwise about 46% of revenue would have been missing
- **Analysis of prices and price classes** (sub-question F4)
- **Final code:** revised and unified based on Walter's and Miguel's first versions; one notebook that recalculates every number in the presentation from the raw data
- **Storyline and structure of the presentation:** main question, two sub-questions, answer, recommendation
- **Design:** designed and built all slides, charts and animations; the team adopted this style for the whole presentation
- **Recommendation with example calculation:** €105,000 per percentage point, 4.5% buffer, shifting the discount
- **Preparing for questions:** collected and prioritised likely questions, built the appendix with a linked overview

Walter did the first analyses of revenue and discounts and made the broken price formats in the catalogue visible. We agreed on the cleaning rules together.

#### Presentation

| | Part of the presentation |
|---|---|
| Walter | Data basis, share of discounted items, monthly trend, Macs |
| Miguel | Brand distribution, price classes, Apple vs. other brands |
| Tim | Opening and agenda, interim conclusions, answer, recommendation, appendix |

The only follow-up question on content after the presentation, how we would test the recommendation, could be answered with a prepared appendix slide (calculation and test plan).

### Key Learnings

- **Preparing for questions pays off.** I had collected and prioritised likely questions. The question about testing came up, and slide A2 answered it.
- **Percent and euros tell different stories.** The smallest discount in percent was the largest amount in euros.
- **Cleaning means making decisions.** Repair where the pattern is unambiguous, delete where it is not, and document both openly.

## Files

| File | Content |
|---|---|
| [`presentation/Eniac_CEO_Presentation_EN.pdf`](presentation/Eniac_CEO_Presentation_EN.pdf) | Presentation with appendix (English) |
| [`presentation/Eniac_CEO_Praesentation.pdf`](presentation/Eniac_CEO_Praesentation.pdf) | Original German presentation |
| [`video/Eniac_Presentation_Video_EN.mp4`](video/Eniac_Presentation_Video_EN.mp4) | Video of the presentation (2:30 minutes, no sound) |
| [`code/analyse/Eniac_Rabattanalyse.ipynb`](code/analyse/Eniac_Rabattanalyse.ipynb) | Final notebook (German): cleaning, both sub-questions, recommendation, appendix and check against the slides |
| [`code/`](code/) | Further scripts: charts and animations, slide builder, video, English version (overview in [`CODE.md`](code/CODE.md), German) |
| [`images/`](images/) | Charts on this page |

The notebook recalculates every number in the presentation from the four raw files and compares them with the slides at the end. Its outputs are saved, so it can be read directly on GitHub. The raw course data is not included in this repository. The scripts in `code/` are the original scripts behind the presentation and serve as reference; they still contain local paths.

## Team

**Team Discount Detectives:** Walter, Miguel and Tim Aßmann
