# Eniac · Lohnen sich die Rabatte?

[English](README.md) · **Deutsch**

### Rabattanalyse für einen Onlinehändler für Apple-Produkte

**Lohnen sich Eniacs Rabatte?**
Eine datengestützte Antwort für den CEO: Python → Diagramme → Präsentation → Empfehlung

![Python](https://img.shields.io/badge/Python-pandas%20%C2%B7%20matplotlib-F28E2B)
![Pillow](https://img.shields.io/badge/Pillow-animierte%20Diagramme-F28E2B)
![JavaScript](https://img.shields.io/badge/JavaScript-pptxgenjs-E15759)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-E15759)

[Projekt](#projekt) · [Frage](#frage) · [Kernzahlen](#kernzahlen) · [Vorgehen](#vorgehen) · [Ergebnisse](#ergebnisse) · [Empfehlung](#empfehlung) · [Mein Beitrag](#mein-beitrag) · [Dateien](#dateien) · [Team](#team)

---

## Projekt

Eniac ist ein Onlinehändler für Apple-Produkte und Zubehör in Spanien. Fast alles wird dort mit Rabatt verkauft. Der CEO wollte wissen, ob sich das lohnt. Unsere Aufgabe als Team: die Verkaufsdaten von Januar 2017 bis März 2018 auswerten und die Antwort in einer 5-Minuten-Präsentation vortragen, mit einem Anhang für Rückfragen.

> Gruppenprojekt der Weiterbildung „Data Analysis and AI“ der WBS Coding School, präsentiert am 13. November 2026. Eniac ist ein Fallbeispiel des Kurses.

**Ergebnis:** Die Instructor bewerteten unsere Präsentation als die beste des Kurses. Die einzige inhaltliche Rückfrage, wie wir die Empfehlung testen würden, konnten wir mit einer vorbereiteten Anhangfolie (Rechenweg und Testplan) vollständig beantworten.

## Frage

> **Lohnen sich Eniacs Rabatte?**

| # | Teilfrage | Sicht | Antwort |
|---|---|---|---|
| 1 | Bringen Rabatte Umsatz? | Marketing | Ja, aber nicht überall. |
| 2 | Kosten Rabatte uns Umsatz und Ruf? | Vorstand | Den Ruf nicht, aber Geld an der falschen Stelle. |

**Gesamtantwort:** Wir verlieren kein Geld. Aber wir verpassen Geld, das wir noch nicht verdienen.

## Kernzahlen

**Datengrundlage**

| Kennzahl | Wert |
|---|---|
| Zeitraum | 437 Tage (Januar 2017 bis März 2018) |
| Abgeschlossene Bestellungen | 46.605 (von 226.909 vor der Bereinigung) |
| Produkte im Katalog | 9.992 (von 19.326 vor der Bereinigung) |
| Umsatz | 15,9 Mio. € |

**Rabatt**

| Kennzahl | Wert |
|---|---|
| Rabattierte Positionen | 93 % (56.203 von 60.375) |
| Stärkster Monat | November 2017: 2,89 Mio. € Umsatz, 21,5 % Ø Rabatt |
| Macs | 41 % des Umsatzes, nur 10,3 % Rabatt, aber 0,77 Mio. € Rabattgeld |
| Apple gesamt | rund 11 % Rabatt, aber 1,17 Mio. € Rabattgeld, fast die Hälfte des gesamten Rabattgelds |
| Andere Marken | rund 18 % Rabatt, dreimal so viele verkaufte Geräte, aber weniger Umsatz |

## Vorgehen

```mermaid
flowchart LR
    A[Rohdaten<br/>4 Tabellen] --> B[Bereinigung<br/>pandas]
    B --> C[Analyse<br/>2 Teilfragen]
    C --> D[Diagramme<br/>matplotlib + Pillow]
    D --> E[Präsentation<br/>pptxgenjs]
    E --> F[Empfehlung<br/>mit Testplan]
```

1. **Daten bereinigen.** Nur abgeschlossene Bestellungen zählen als Umsatz. 36.169 Stückpreise standen als Text im Format `1.234.56`. Weil alle dieses Format haben, ist der erste Punkt eindeutig ein Tausenderpunkt; wir haben ihn entfernt, statt die Zeilen zu löschen (das hätte rund 46 % des Umsatzes gekostet). Im Katalog war das Format nicht eindeutig, deshalb haben wir dort 542 Preise gelöscht: Ein fehlender Preis ist sichtbar, ein falsch reparierter verfälscht den Rabatt unbemerkt. Dazu kamen Duplikate und Zeilen mit fehlenden Werten.
2. **Arbeitstabelle aufbauen.** Jede verkaufte Position mit Umsatz, Listenumsatz, Rabatt in Prozent und in Euro, Kategorie und Marke.
3. **Die zwei Teilfragen beantworten.** Monatsverlauf, Kategorien, Marken, Preisklassen und der direkte Vergleich Apple gegen andere Marken.
4. **Empfehlung durchrechnen.** Was ein Prozentpunkt Apple-Rabatt wert ist, wie viele Käufe wegfallen dürften, und was ein Umschichten des Rabatts bringen würde.
5. **Präsentieren.** Eine Hauptfrage, zwei Teilfragen mit kurzen Antworten, eine Empfehlung mit Zahlen. Alles für Rückfragen in einen Anhang mit verlinkter Übersicht (A1 bis A7).

## Ergebnisse

### Rabatt ist Standard, aber der November verkauft sich von selbst

93 % aller Positionen werden mit Rabatt verkauft. Der stärkste Monat ist der November 2017 mit Black Friday und 2,89 Mio. € Umsatz.

![Monatsverlauf von Umsatz und Rabatt](images/de/g25_linien.gif)

### Macs tragen den Umsatz

Macs bringen 41 % des Umsatzes.

![Umsatz je Kategorie](images/de/g33.gif)

### Apple: wenig Rabatt in Prozent, aber fast die Hälfte des Rabattgelds

Apple bekommt im Schnitt rund 11 % Rabatt, andere Marken rund 18 %. Weil Apple-Geräte teuer sind, gehen trotzdem 1,17 Mio. € Rabattgeld an Apple, fast die Hälfte des gesamten Rabattgelds.

![Apple gegen andere Marken](images/de/g_paare2.gif)

### Wenig Prozent, viel Geld

Bei Macs sind es nur 10,3 % Rabatt, in Euro aber 0,77 Mio. € (31 % des gesamten Rabattgelds). Bei Hüllen und Taschen ist es umgekehrt: 32,7 % Rabatt, aber nur 0,15 Mio. €.

![Rabatt je Kategorie in Prozent und in Euro](images/de/a4_kombi.png)

## Empfehlung

| # | Hebel | Begründung |
|---|---|---|
| 1 | **Apple-Rabatt senken** | Jeder Prozentpunkt sind rund 105.000 €. |
| 2 | **Andere Marken gezielt rabattieren** | Dort wirkt Rabatt als Kaufanreiz. |
| 3 | **Rabatt außerhalb der Saison** | Im November kaufen die Kunden ohnehin. |

**Beispielrechnung (Januar 2017 bis März 2018):** Mit dem eingesparten Apple-Rabatt ließe sich bei gleichem Budget der Rabatt auf andere Marken von 18 % auf bis zu 25 % erhöhen. Oder Eniac behält das Geld ein: bis zu 0,54 Mio. € mehr Umsatz bei gleicher Stückzahl.

![Rabatt umschichten](images/de/g_regler_balken.gif)

**Puffer und Testplan:** Bei 7 statt 11,1 % Apple-Rabatt dürften bis zu 4,5 % weniger Apple-Geräte verkauft werden, ohne dass Umsatz verloren geht. Vorschlag zum Testen: iPads sechs Wochen lang mit 7 statt 11 % Rabatt anbieten, nicht im November, und mit denselben Wochen im Vorjahr vergleichen. Geht der Absatz um weniger als 4,5 % zurück, wird die Änderung ausgeweitet.

### Grenzen der Daten

- **Keine Einkaufspreise:** Margen lassen sich nur in Szenarien schätzen (Anhang A4).
- **Keine Kunden-ID:** Neukunden und Kundenbindung sind nicht messbar.

Deshalb behaupten wir nicht, dass Rabatte Verlust machen, sondern schlagen Tests vor.

## Mein Beitrag

Präsentiert haben wir zu dritt. Organisation, Code und Gestaltung lagen überwiegend bei mir.

#### Was ich umgesetzt habe

- **Projektorganisation:** Gruppendokument mit Fragenbaum aufgebaut: Leitfrage, Teilfragen F1 bis F6, Zuständigkeiten und eine einheitliche Vorlage für die Antworten
- **Bereinigung von orders und orderlines:** 36.169 Preise mit zwei Punkten repariert statt gelöscht, weil sonst rund 46 % des Umsatzes gefehlt hätten
- **Analyse der Preise und Preisklassen** (Teilfrage F4)
- **Finaler Code:** auf Basis der ersten Fassungen von Walter und Miguel überarbeitet und vereinheitlicht; ein Notebook, das alle Zahlen der Präsentation aus den Rohdaten nachrechnet
- **Storyline und Aufbau der Präsentation:** Hauptfrage, zwei Teilfragen, Antwort, Empfehlung
- **Gestaltung:** alle Folien, Diagramme und Animationen entworfen und umgesetzt; das Team hat diesen Stil für die gesamte Präsentation übernommen
- **Empfehlung mit Beispielrechnung:** 105.000 € pro Prozentpunkt, 4,5 % Puffer, Umschichtung des Rabatts
- **Vorbereitung auf Rückfragen:** Fragen gesammelt und priorisiert, Anhang mit verlinkter Übersicht gebaut

Walter hat die ersten Analysen zu Umsatz und Rabatten gemacht und die fehlerhaften Preisformate im Katalog sichtbar gemacht. Die Regeln für die Bereinigung haben wir gemeinsam festgelegt.

#### Vortrag

| | Teil der Präsentation |
|---|---|
| Walter | Datengrundlage, Anteil rabattierter Positionen, Monatsverlauf, Macs |
| Miguel | Markenverteilung, Preisklassen, Apple gegen andere Marken |
| Tim | Einstieg und Agenda, Zwischenfazits, Antwort, Empfehlung, Anhang |

Die Präsentation wurde im Kurs als beste bewertet; die einzige Rückfrage, wie wir die Empfehlung testen würden, ließ sich mit einer vorbereiteten Anhangfolie beantworten.

### Wichtigste Erkenntnisse

- **Rückfragen vorbereiten zahlt sich aus.** Ich hatte mögliche Rückfragen gesammelt und priorisiert. Genau die Frage nach dem Test kam, und Folie A2 hat sie beantwortet.
- **Prozent und Euro erzählen verschiedene Geschichten.** Der kleinste Rabatt in Prozent war der größte Betrag in Euro.
- **Bereinigen heißt entscheiden.** Reparieren, wo das Muster eindeutig ist, löschen, wo es das nicht ist, und beides offen dokumentieren.

## Dateien

| Datei | Inhalt |
|---|---|
| [`presentation/Eniac_CEO_Praesentation.pdf`](presentation/Eniac_CEO_Praesentation.pdf) | Präsentation mit Anhang (Deutsch) |
| [`presentation/Eniac_CEO_Presentation_EN.pdf`](presentation/Eniac_CEO_Presentation_EN.pdf) | Englische Fassung der Präsentation |
| [`code/analyse/Eniac_Rabattanalyse.ipynb`](code/analyse/Eniac_Rabattanalyse.ipynb) | Finales Notebook: Bereinigung, beide Teilfragen, Empfehlung, Anhang und Abgleich mit den Folien |
| [`code/`](code/) | Weitere Skripte: Diagramme und Animationen, Folien-Builder, Video, englische Fassung (Übersicht in [`CODE.md`](code/CODE.md)) |
| [`images/`](images/) | Diagramme dieser Seite |

Das Notebook rechnet alle Zahlen der Präsentation aus den vier Rohdateien nach und vergleicht sie am Ende mit den Folien. Die Ausgaben sind gespeichert, sodass es sich direkt auf GitHub lesen lässt. Die Rohdaten aus dem Kurs liegen nicht in diesem Repository. Die Skripte in `code/` sind die Originalskripte der Präsentation und dienen als Referenz; sie enthalten noch lokale Pfade.

## Team

**Team Discount Detectives:** Walter, Miguel und Tim Aßmann
