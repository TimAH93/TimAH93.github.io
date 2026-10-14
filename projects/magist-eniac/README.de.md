# Soll Eniac mit Magist nach Brasilien?

[English](README.md) · **Deutsch**

**Empfehlung: Brasilien ja, aber nicht über Magist.** Magist liefert nur in wenigen Bundesstaaten im Südosten schnell und zuverlässig, und das Tech-Geschäft der Plattform ist im Vergleich zu Eniacs Premium-Apple-Zubehör klein und preislich niedrig.

**Art:** Gruppenprojekt (Dreierteam), Weiterbildung Data Analytics & AI bei der WBS
**Status:** Abgeschlossen

## Fragestellung

Eniac, ein europäischer Onlinehändler für Apple-kompatible Technik, prüfte eine Partnerschaft mit Magist, einem brasilianischen Marktplatz, um in den brasilianischen Markt einzusteigen. Vor der Unterschrift waren zwei Bedenken zu klären:

1. **Lieferung:** Liefert Magist schnell genug für eine Premium-Marke?
2. **Passung:** Ist Magist ein guter Partner für hochwertige Tech-Produkte?

## Daten

- **Magist-Datenbank (MySQL):** im Kurs bereitgestellte Datenbank auf Basis des öffentlichen [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) ([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)). Rund 99.000 Bestellungen, September 2016 bis Oktober 2018. Die Daten sind nicht in diesem Repository enthalten.
- **Marktrecherche:** öffentliche Quellen zum brasilianischen Onlinehandel 2017 bis 2019 (siehe unten).

## Vorgehen

1. Die Leitfrage in einen Fragenbaum mit fünf Bereichen zerlegt: Sortiment, Verkäufer, Lieferung, Kundenzufriedenheit und Markt. Jede Unterfrage hatte eine zuständige Person, einen Status und eine Kurzantwort.
2. Gemeinsame Annahmen festgelegt: sechs Tech-Kategorien, Umsatz = Artikelpreis ohne Fracht und ohne stornierte Bestellungen.
3. Die Datenfragen mit SQL in MySQL Workbench beantwortet und die Ergebnisse in Tableau visualisiert.
4. Die Daten durch eine Marktrecherche in einen Kontext gesetzt.
5. Alles zu einer kurzen Entscheidungspräsentation zusammengeführt.

## Ergebnisse

**Lieferung (Ergebnis des Teams):** Nur drei Bundesstaaten (São Paulo, Paraná, Minas Gerais) liefern im Schnitt in unter 12 Tagen und sind dabei zu über 94 % pünktlich. Bei hochpreisigen Tech-Bestellungen erfüllten nur zwei Städte alle Kriterien für Geschwindigkeit, Pünktlichkeit und Bewertungen.

**Sortiment (Ergebnis des Teams):** Technik macht nur etwa 12 % von Magists Umsatz aus, und die Durchschnittspreise liegen weit unter Eniacs Preisniveau.

**Tech-Kategorien im Katalog (meine Analyse):** 3.387 von 32.951 Produkten (10,3 %) gehören zu sechs Tech-Kategorien. Aus den Kategorien allein geht nicht hervor, ob die Produkte High-End oder Apple-kompatibel sind; die Passung ließ sich mit den Daten also nicht belegen.

| Kategorie | Produkte |
|---|---|
| computers_accessories | 1.639 |
| telephony | 1.134 |
| electronics | 517 |
| audio | 58 |
| computers | 30 |
| tablets_printing_image | 9 |

Query: [`sql/01_tech_categories.sql`](sql/01_tech_categories.sql)

**Marktkontext (meine Recherche):**

- **Wachstum:** Der brasilianische Onlinehandel wuchs 2018 um etwa 12 %, die Wirtschaft insgesamt nur um etwa 1 %.
- **Apple als Luxusgut:** Das iPhone XS startete in Brasilien bei 7.300 BRL, dem höchsten Preis unter 40 verglichenen Ländern. Forschung zu Einkommensungleichheit und Statusstreben (Walasek & Brown, 2015) erklärt, warum die Nachfrage trotzdem da ist: In sehr ungleichen Gesellschaften werden Statussymbole wichtiger.
- **Anfällige Logistik:** Ein elftägiger Lkw-Fahrerstreik im Mai 2018 kostete den Onlinehandel rund 407 Mio. BRL, und die Beschwerden über verspätete Postzustellungen stiegen von 2016 bis 2018 jedes Jahr.
- **Wettbewerb:** B2W war Marktführer, Mercado Livre wuchs stark und verkürzte 2018 seine mittlere Lieferzeit in Brasilien um zwei Tage, und Amazon verkauft seit 2017 Elektronik in Brasilien.

## Empfehlung

Brasilien ist ein attraktiver, wachsender Markt, aber Magist ist nicht der richtige Partner für Eniac. Ein größerer Marktplatz mit stärkerer Logistik, etwa Mercado Livre, passt besser zu einer Premium-Marke.

## Tools

- SQL (MySQL Workbench)
- Tableau
- Google Docs und Slides für Teamorganisation und Präsentation

## Meine Rolle

- Die Analyse als Fragenbaum strukturiert und offene Fragen im Blick behalten
- Die Tech-Kategorien mit SQL ermittelt (Katalog-Analyse)
- Die Marktrecherche zu Wachstum, Wettbewerb, Apple-Preisen und Logistik übernommen
- Die Präsentation eröffnet und abgeschlossen sowie den Marktkontext und die Empfehlung vorgestellt

Team: Julia, Matías und Tim

## Quellen (Marktrecherche)

- Ebit, Webshoppers 38 (via PagBrasil), Sep. 2018
- Tribuna PR, E-Commerce-Umsatz 2018, Feb. 2019
- Gazeta do Povo, Mercado Livre vs. B2W, Jul. 2017
- Tecnoblog, Amazon verkauft Elektronik in Brasilien, Okt. 2017
- Olhar Digital, iPhone-Preise in Brasilien, Okt. 2018, und Ländervergleich von Deutsche Bank Research, Jul. 2019
- Walasek, L. & Brown, G. D. A. (2015). Income Inequality and Status Seeking. *Psychological Science*
- Diário do Comércio, Umsatzverluste im E-Commerce durch den Lkw-Streik, Jun. 2018
- Olhar Digital, Beschwerden über Verspätungen der Correios, Feb. 2019
- MercadoLibre, Earnings Call Q4 2018

---

## Reflexion

### Wichtigste Erkenntnisse

- **Ein Fragenbaum hält das Team fokussiert.** Eine Geschäftsfrage in nummerierte Unterfragen mit Zuständigkeiten aufzuteilen, hat klar gemacht, wer woran arbeitet und welche Antworten noch fehlen.
- **Daten brauchen Kontext.** Die Zahlen zeigten, dass Magist kaum teure Technik verkauft. Die Marktrecherche erklärte, warum: In Brasilien sind Premium-Apple-Produkte Luxusgüter mit kleiner Zielgruppe.
- **Mein Psychologie-Hintergrund hilft.** Forschung zum Statusstreben lieferte eine plausible Erklärung für die Apple-Nachfrage in Brasilien und machte die Geschichte für ein nicht-technisches Publikum leichter nachvollziehbar.
- **Eine Empfehlung braucht eine klare Antwort.** Entscheider wollen Ja, Nein oder Ja unter Bedingungen, gestützt auf zwei oder drei starke Punkte, nicht jedes Query-Ergebnis.
- **Unterschiedliche Arbeitsweisen können sich ergänzen.** Wir sind Aufgaben recht unterschiedlich angegangen, aber alle konnten ihre Stärken einbringen, und gemeinsam ist eine Präsentation entstanden, die keiner von uns allein so gemacht hätte.

### Herausforderungen

- **Arbeiten im Team.** Bisher habe ich meist eigenständig gearbeitet. Mir war wichtig, meinem Team respektvoll zu begegnen und Raum für die Beiträge der anderen zu lassen. Eine klare Struktur von Anfang an hat mir geholfen, mich auf meine Aufgaben zu konzentrieren und den anderen bei ihren zu vertrauen.
- **Einheitliche Definitionen im Team.** Jede und jeder von uns schrieb eigene Queries. Kleine Unterschiede, etwa welche Kategorien als Tech zählen oder ein Tippfehler in einem Kategorienamen, können Ergebnisse verändern, ohne dass es jemand merkt. Gemeinsame Annahmen zu Beginn aufzuschreiben, hat geholfen; beim nächsten Mal würde ich zusätzlich eine gemeinsame Basis-Query teilen.
- **Währung.** Magists Preise sind in brasilianischen Real, Eniacs in Euro. Für einen korrekten Vergleich muss jeder Wert einheitlich umgerechnet und die Währung auf jedem Diagramm angegeben werden.
- **Auf eine Empfehlung einigen.** Unterwegs hatten wir drei mögliche Empfehlungen: einen regionalen Start, einen befristeten Test und einen alternativen Partner. Uns auf eine Botschaft für die Abschlusspräsentation zu einigen, erforderte eine bewusste Diskussion.

### Nächste Schritte

- Öfter präsentieren, weil Ergebnisse verständlich zu erklären eine Kernfähigkeit im Job als Data Analyst ist.
- In Tableau schneller und selbstständiger werden.
- Gezieltere SQL-Abfragen schreiben.

### Offene Frage

Ob verspätete Lieferungen tatsächlich zu schlechteren Bewertungen und weniger Wiederholungskäufen führen, blieb in diesem Projekt offen. Dem gehe ich in meinem eigenen Projekt [Delivery & Loyalty](../delivery-loyalty/README.de.md) nach.
