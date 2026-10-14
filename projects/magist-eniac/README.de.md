# Soll Eniac mit Magist nach Brasilien?

[English](README.md) · **Deutsch**

**Art:** Gruppenprojekt (Dreierteam), Weiterbildung Data Analytics & AI bei der WBS · **Dauer:** 2 Wochen · **Status:** Abgeschlossen

## Zusammenfassung

In diesem Projekt haben wir als Team die Rolle von Analysten für Eniac übernommen, einen europäischen Onlinehändler für Apple-kompatible Technik. Eniac überlegte, über eine Partnerschaft mit Magist, einem brasilianischen Marktplatz, in den brasilianischen Markt einzusteigen. Unsere Aufgabe war, mit Daten herauszufinden, ob Magist ein guter Partner ist, und der Geschäftsführung von Eniac eine klare Empfehlung zu präsentieren.

Wir haben die Geschäftsfrage in kleinere Fragen zerlegt, diese mit SQL beantwortet, die Ergebnisse in Tableau visualisiert, eine Marktrecherche ergänzt und unsere Empfehlung in einer kurzen Präsentation vorgestellt: Brasilien ist ein attraktiver Markt, aber Magist ist nicht der richtige Partner für eine Premium-Marke.

## Wie wir vorgegangen sind

1. **Das Geschäftsproblem verstehen.** Eniac hatte zwei Bedenken: Liefert Magist schnell genug für Premium-Kunden? Und passt Magist zu hochwertigen Tech-Produkten?
2. **Fragenbaum.** Wir haben diese Bedenken in fünf Bereiche zerlegt (Sortiment, Verkäufer, Lieferung, Kundenzufriedenheit, Markt), jeweils mit nummerierten Unterfragen. Jede Frage hatte eine zuständige Person, einen Status und eine Kurzantwort, sodass immer klar war, was noch offen ist.
3. **Gemeinsame Annahmen.** Vor den Abfragen haben wir festgelegt, welche Produktkategorien als Tech zählen und wie Umsatz definiert ist, damit unsere Ergebnisse vergleichbar sind.
4. **Datenanalyse mit SQL.** Wir haben die Magist-Datenbank in MySQL Workbench untersucht: Produktkategorien, Preise, Verkäufer, Lieferzeiten, Pünktlichkeit und Bewertungen.
5. **Visualisierung in Tableau.** Die wichtigsten Ergebnisse haben wir in Diagramme übersetzt, die auch ein nicht-technisches Publikum auf einen Blick versteht.
6. **Marktrecherche.** Weil die Daten allein nicht jede Frage beantworten konnten, haben wir öffentliche Quellen zu E-Commerce in Brasilien, Wettbewerbern, Apple-Preisen und Logistik ergänzt.
7. **Präsentation.** Wir haben alles auf zwei Fragen, zwei klare Antworten und eine Empfehlung verdichtet und sie im Rollenspiel der „Geschäftsführung“ präsentiert.

## Meine Rolle

- Die Analyse als Fragenbaum strukturiert und offene Fragen im Blick behalten
- Analysiert, welche Produktkategorien für Eniac relevant sind (SQL)
- Die Marktrecherche zu Wachstum, Wettbewerb, Apple-Preisen und Logistik übernommen, mit Quellen
- Die Präsentation eröffnet und abgeschlossen sowie den Marktkontext und die Empfehlung vorgestellt

Team: Julia, Matías und Tim

## Sprachen, Bibliotheken und Tools

- **SQL** (MySQL Workbench): Joins, Aggregationen, CASE WHEN, Window Functions
- **Tableau**: Balkendiagramme, berechnete Felder, Farbcodierung für Schwellenwerte
- **Google Docs und Slides**: Fragenbaum, gemeinsame Notizen, Präsentation
- **Marktrecherche** in portugiesischsprachigen Quellen

## Wichtigste Erkenntnisse

- **Ein Fragenbaum hält das Team fokussiert.** Eine Geschäftsfrage in nummerierte Unterfragen mit Zuständigkeiten aufzuteilen, hat klar gemacht, wer woran arbeitet und welche Antworten noch fehlen.
- **Daten brauchen Kontext.** Die Zahlen zeigten, dass Magist kaum teure Technik verkauft. Die Marktrecherche erklärte, warum: In Brasilien sind Premium-Apple-Produkte Luxusgüter mit kleiner Zielgruppe.
- **Mein Psychologie-Hintergrund hilft.** Forschung zum Statusstreben (Walasek & Brown, 2015) lieferte eine plausible Erklärung für die Apple-Nachfrage in Brasilien und machte die Geschichte für ein nicht-technisches Publikum leichter nachvollziehbar.
- **Eine Empfehlung braucht eine klare Antwort.** Entscheider wollen Ja, Nein oder Ja unter Bedingungen, gestützt auf zwei oder drei starke Punkte, nicht jedes Query-Ergebnis.
- **Unterschiedliche Arbeitsweisen können sich ergänzen.** Wir sind Aufgaben recht unterschiedlich angegangen, aber alle konnten ihre Stärken einbringen, und gemeinsam ist eine Präsentation entstanden, die keiner von uns allein so gemacht hätte.

## Herausforderungen

- **Arbeiten im Team.** Bisher habe ich meist eigenständig gearbeitet. Mir war wichtig, meinem Team respektvoll zu begegnen und Raum für die Beiträge der anderen zu lassen. Eine klare Struktur von Anfang an hat mir geholfen, mich auf meine Aufgaben zu konzentrieren und den anderen bei ihren zu vertrauen.
- **Einheitliche Definitionen im Team.** Jede und jeder von uns schrieb eigene Queries. Kleine Unterschiede, etwa welche Kategorien als Tech zählen oder ein Tippfehler in einem Kategorienamen, können Ergebnisse verändern, ohne dass es jemand merkt. Gemeinsame Annahmen zu Beginn aufzuschreiben, hat geholfen; beim nächsten Mal würde ich zusätzlich eine gemeinsame Basis-Query teilen.
- **Währung.** Magists Preise sind in brasilianischen Real, Eniacs in Euro. Für einen korrekten Vergleich muss jeder Wert einheitlich umgerechnet und die Währung auf jedem Diagramm angegeben werden.
- **Auf eine Empfehlung einigen.** Unterwegs hatten wir drei mögliche Empfehlungen: einen regionalen Start, einen befristeten Test und einen alternativen Partner. Uns auf eine Botschaft für die Abschlusspräsentation zu einigen, erforderte eine bewusste Diskussion.

## Nächste Schritte

- Öfter präsentieren, weil Ergebnisse verständlich zu erklären eine Kernfähigkeit im Job als Data Analyst ist.
- In Tableau schneller und selbstständiger werden.
- Gezieltere SQL-Abfragen schreiben.
- Der Frage, die dieses Projekt offen gelassen hat – ob verspätete Lieferungen Kundentreue kosten –, gehe ich in meinem eigenen Projekt [Delivery & Loyalty](../delivery-loyalty/README.de.md) nach.

## Dateien

- [`presentation/Team_Jaguar_Magist.pdf`](presentation/Team_Jaguar_Magist.pdf): Abschlusspräsentation (Deutsch)
- [`sql/`](sql/): alle SQL-Queries des Teams, nach Frage nummeriert; die Autorin bzw. der Autor steht in jeder Datei (meine: [`01_tech_categories.sql`](sql/01_tech_categories.sql))

## Daten und Quellen

- **Magist-Datenbank (MySQL):** im Kurs bereitgestellte Datenbank auf Basis des öffentlichen [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), lizenziert unter [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Rund 99.000 Bestellungen, September 2016 bis Oktober 2018.
- **Marktrecherche:** Ebit Webshoppers 38 (2018); Tribuna PR (2019); Gazeta do Povo (2017); Tecnoblog (2017); Olhar Digital (2018, 2019) mit Deutsche Bank Research (2019); Diário do Comércio (2018); MercadoLibre Earnings Call Q4 2018; Walasek, L. & Brown, G. D. A. (2015). Income Inequality and Status Seeking. *Psychological Science*.
