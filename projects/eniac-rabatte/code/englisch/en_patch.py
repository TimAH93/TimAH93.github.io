# Englische Beschriftungen für alle Diagramme: übersetzt jeden Text beim Setzen und leitet Dateien nach img2_en um
import re, matplotlib.text, matplotlib.figure
from PIL import Image as _I
PH=[('unter 50 €','under €50'),('50–100 €','€50–100'),('100–500 €','€100–500'),('500–1,000 €','€500–1,000'),('über 1,000 €','over €1,000'),
 ('Umsatz gegen verkaufte Stück je Marke (Top 10 nach Umsatz)','Revenue vs. units sold by brand (top 10 by revenue)'),
 ('Rabatt in Euro: Top 10 Umsatzmarken','Discount in euros: top 10 brands by revenue'),
 ('Rabatt in Euro je Kategorie','Discount in euros by category'),('Ø Rabatt je Preisklasse','Avg. discount by price range'),
 ('Umsatz je Preisklasse','Revenue by price range'),('Ø Rabatt je Kategorie','Avg. discount by category'),('Umsatz je Kategorie','Revenue by category'),
 ('Ø Rabatt in Prozent','Avg. discount in percent'),('Ø Rabatt in %','Avg. discount in %'),('Rabatt in Mio. €','Discount in € million'),('Umsatz in Mio. €','Revenue in € million'),
 ('Bestellungen in Tsd.','Orders in thousands'),('Anteil an\nverkauften Stück','Share of\nunits sold'),('Anteil am\nUmsatz','Share of\nrevenue'),('Anteil am\nRabattgeld','Share of\ndiscount money'),
 ('Anteil rabattierter Positionen','Share of discounted items'),('Anteil der Bestellpositionen in %','Share of items in %'),('Mit Rabatt','With discount'),('Ohne Rabatt','Without discount'),
 ('Anteil in %','Share in %'),('Rabatt in Euro','Discount in euros'),('Ø Rabatt','Avg. discount'),('Andere','Others'),
 ('Pack (Bundles und\nKonfigurationen)','Pack (bundles and\nconfigurations)'),('Pack (Konfigurationen)','Pack (configurations)'),
 ('Armbänder','Watch bands'),('Hüllen und Taschen','Cases and bags'),('Kabel und Strom','Cables and power'),('Monitore und Eingabe','Monitors and input'),
 ('Netzwerk und Smart Home','Networking and smart home'),('Sonstiges','Other'),('Speicher','Storage'),('iPhone und iPad','iPhone and iPad'),('Alle anderen','All others'),
 (' Rabatt',' discount')]
MON={'Mär':'Mar','Mai':'May','Okt':'Oct','Dez':'Dec'}
def tr(s):
    if not isinstance(s,str) or not s: return s
    s=re.sub(r"(?<=\d)[.,](?=\d)",lambda m:'§' if m.group(0)=='.' else '.',s).replace('§',',')
    for a,b in PH: s=s.replace(a,b)
    s=re.sub(r"\b(Mär|Mai|Okt|Dez)\b",lambda m:MON[m.group(1)],s)
    s=re.sub(r"(\+?)([\d.,]+) Mio\. €",lambda m:f"{m.group(1)}€{m.group(2)}M",s)
    return s.replace(' %','%')
_st=matplotlib.text.Text.set_text
matplotlib.text.Text.set_text=lambda self,s:_st(self,tr(s) if isinstance(s,str) else s)
def _p(p): return p.replace('/gs/img2/','/gs/img2_en/') if isinstance(p,str) else p
_sf=matplotlib.figure.Figure.savefig
matplotlib.figure.Figure.savefig=lambda self,f,*a,**k:_sf(self,_p(f),*a,**k)
_is=_I.Image.save
_I.Image.save=lambda self,f,*a,**k:_is(self,_p(f),*a,**k)
