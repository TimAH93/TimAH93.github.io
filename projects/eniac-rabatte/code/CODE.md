# Code des Eniac-Projekts

Die Skripte sind die Originalskripte der Präsentation. Sie enthalten noch lokale Pfade aus der Arbeitsumgebung (z. B. `/tmp/...`, `/mnt/user-data/...`) und brauchen die bereinigten CSV-Dateien (`orders_cl.csv`, `orderlines_cl.csv`, `products_kategorie_vorlaeufig.csv`). Fürs Portfolio sind sie Referenz; als lauffähige Fassung dient `analyse/Eniac_Rabattanalyse.ipynb`.

## analyse/
| Datei | Inhalt |
|---|---|
| `Eniac_Rabattanalyse.ipynb` | **Finales Notebook:** Bereinigung, Arbeitstabelle, beide Teilfragen, Empfehlung, Anhang und Abgleich mit den Folien – alles aus den vier Rohdateien, mit Ausgaben und Diagrammen |
| `eniac_fallstudie.py` / `.ipynb` | Meine eigene durchgehende Analyse: Laden, Bereinigen, alle Zahlen des Berichts Schritt für Schritt (Zellen mit `# %%`, läuft in Colab oder VS Code) |
| `F4_Preise_Tim.ipynb` | Mein Notebook zur Teilfrage Preise: Preise je Kategorie, Preisklassen, Umsatz und Rabatt je Preisklasse |

## diagramme/ (Python: pandas, matplotlib, seaborn, Pillow)
| Datei | Erzeugt |
|---|---|
| `rund.txt` | Hilfsfunktion `balken_abrunden` (Balken oben abgerundet), wird per `exec` geladen |
| `gifs2.py` | `g33` (Umsatz je Kategorie), `g43`/`g44` (Umsatz und Rabatt je Preisklasse); enthält `save()` für GIF, Start- und Endbild |
| `bestell_linien.py` | `g25_linien` (Monatsverlauf Umsatz und Rabatt) |
| `miguel_gifs.py` | `g_vergleich` (Markenverteilung), `g_rabattmarke` (Rabattgeld je Marke) |
| `welten3.py` | `g_paare1`/`g_paare2` (Apple gegen andere Marken, gepaarte Säulen) |
| `regler_zwei.py`, `regler_balken.py` | `g_regler_linie`/`g_regler_balken` (Rabatt umschichten) |
| `a4_kombi.py` | Rabatt je Kategorie in Prozent und Euro (Anhang A5) |
| `a5_mac_oben.py` | Umsatz im Jahresverlauf, Mac oben (Anhang A6) |
| `a5_animation_umsatz_jahresverlauf.py`, `a5_smooth.py` | Animierte Fassung des Jahresverlaufs (kommentiert) |

## folien/ (JavaScript + Python)
| Datei | Inhalt |
|---|---|
| `build_ceo8.js` | Setzt die Präsentation mit pptxgenjs zusammen: Master, Agenda, Diagrammfolien, Empfehlung, Fortschrittsbalken, verlinkter Anhang, Urheberschafts-Vermerk. `PDF=1` erzeugt die PDF-Fassung mit Standbildern statt GIFs |
| `sizes.json` | Bildgrößen für das Einpassen der Diagramme |
| `anim.py` + `anim_de.json` | Schreibt Einblende-Animationen (Fade, auf Klick oder automatisch) direkt in die PPTX |

Ablauf: `node build_ceo8.js` → `python3 anim.py Eniac_CEO_Praesentation_v62.pptx anim_de.json`

## video/
| Datei | Inhalt |
|---|---|
| `build_video.py` | Rendert das Video: Folienbilder, Aufbau-Zustände mit Überblendung und GIF-Bilder werden mit PIL zusammengesetzt und per ffmpeg (H.264, 30 fps) zu einem MP4 verbunden |

## englisch/
| Datei | Inhalt |
|---|---|
| `en_patch.py` | Übersetzt Diagrammtexte beim Zeichnen (Wörterbuch, Zahlenformat 1,000.5) und speichert in einen eigenen Ordner |
| `en_dict.py` + `build_ceo8_en.js` | Englische Folien (Stand vor den letzten deutschen Änderungen) |
