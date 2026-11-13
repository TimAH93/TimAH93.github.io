const pptxgen = require('pptxgenjs'); const fs=require('fs');
const SZ=JSON.parse(fs.readFileSync('sizes.json'));
const PDF=!!process.env.PDF;
const pres=new pptxgen(); pres.layout='LAYOUT_16x9';
pres.title='Eniac\'s Discount Strategy'; pres.author='Team Discount Detectives';
pres.theme={headFontFace:'Antonio',bodyFontFace:'Barlow'};
const BG='0A0A0C',FG='EDEDF0',MUTE='8A8F99',CYAN='00E5FF',GOLD='F28E2B',ROT='E15759',CARD='15161A',LINE='2A2D35';
const FOOT=[{image:{path:'img2/logo_team.png',x:0.35,y:5.17,w:0.39,h:0.3}},
];
const NUM={x:9.1,y:5.21,w:0.4,h:0.24,fontFace:'Barlow',fontSize:9,color:MUTE,align:'right',valign:'middle'};
pres.defineSlideMaster({title:'BILD',background:{color:BG},objects:FOOT,slideNumber:NUM});
pres.defineSlideMaster({title:'TITEL',background:{color:BG},objects:[]});
const FARBE={Walter:'E15759',Miguel:'4FA3E0',Tim:'F28E2B'}; let SP='';
function fuss(s){const r=[{text:'Team Discount Detectives · ',options:{color:MUTE}}];
  ['Walter','Miguel','Tim'].forEach((n,i)=>{r.push({text:n,options:{color:SP===n?FARBE[n]:MUTE,bold:SP===n}}); if(i<2) r.push({text:' · ',options:{color:MUTE}});});
  s.addText(r,{x:0.82,y:5.21,w:5,h:0.24,fontFace:'Barlow',fontSize:9,margin:0,valign:'middle',isTextBox:true});}
const neu=()=>{const s=pres.addSlide({masterName:'BILD'}); fuss(s); return s;};
const T=(s,t,o)=>s.addText(t,Object.assign({fontFace:'Barlow',margin:0,isTextBox:true},o));
const kick=(s,t)=>T(s,t,{x:0.5,y:0.28,w:9,h:0.25,fontSize:11,bold:true,color:CYAN,charSpacing:2});
const cap=(s,t)=>T(s,t,{x:0.5,y:0.6,w:9,h:0.4,fontSize:18,bold:true,color:FG});
const card=(s,x,y,w,h)=>s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:CARD},line:{color:LINE,width:0.75},rectRadius:0.12});
function img(s,p,box,alt){const [W,H]=SZ[p]; const ar=W/H; let w=box.w,h=w/ar; if(h>box.h){h=box.h;w=h*ar;}
  s.addImage({path:p,x:box.x+(box.w-w)/2,y:box.y,w,h,altText:alt});}
// Legende oben rechts (Farbe = Bedeutung)
function legende(s,items,yy){let x=0.5; yy=yy||0.32;   // linksbündig unter der Überschrift
  items.forEach(([txt,farbe])=>{const w=0.15+txt.length*0.095;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:yy+0.04,w:0.16,h:0.16,fill:{color:farbe},line:{color:farbe,width:0},rectRadius:0.03});
    T(s,txt,{x:x+0.24,y:yy,w:w,h:0.24,fontSize:12,color:FG,valign:'middle',wrap:false}); x+=0.24+w+0.15;});}
// Diagramm: erst Standbild, dann GIF (Klick = nächste Folie startet die Animation)
function chart(bilder,kicker,caption,alt,notes,leg){
  if(PDF){ bilder=[bilder[bilder.length-1].replace('.gif','_ende.png')]; notes=[notes[notes.length-1]]; }
  bilder.forEach((p,i)=>{const s=neu();
    kick(s,kicker); let top=0.65; if(caption){cap(s,caption); top=1.1;} if(leg){ legende(s,leg,top+0.08); top+=0.45; }
    img(s,p,{x:0.4,y:top,w:9.2,h:5.12-top},alt); s.addNotes(notes[i]||notes[notes.length-1]);});
}
// Zwischenfolie für die Moderation
function zwischen(label,frage,vorher,notes){
  const s=neu(); let y=1.55;
  if(vorher){ // vorher = [Label, Frage, Antwort, Erklärung]
    T(s,vorher[0],{x:0.6,y:0.35,w:8.8,h:0.28,fontSize:12,bold:true,color:CYAN,charSpacing:3,align:'center'});
    T(s,vorher[1],{x:0.6,y:0.65,w:8.8,h:0.35,fontSize:17,color:MUTE,align:'center'});
    T(s,vorher[2],{x:0.6,y:1.02,w:8.8,h:0.5,fontFace:'Antonio',fontSize:24,bold:true,color:FG,align:'center'});
    T(s,vorher[3],{x:0.8,y:1.52,w:8.4,h:0.7,fontSize:18,color:FG,align:'center',valign:'top'});
    s.addShape(pres.shapes.LINE,{x:3.5,y:2.4,w:3,h:0,line:{color:LINE,width:1}}); y=2.65; }
  T(s,label,{x:0.6,y,w:8.8,h:0.3,fontSize:12,bold:true,color:CYAN,charSpacing:3,align:'center'});
  T(s,frage,{x:0.4,y:y+0.35,w:9.2,h:0.9,fontFace:'Antonio',fontSize:frage.length>30?32:40,bold:true,color:FG,align:'center',valign:'middle'});
  s.addNotes(notes); return s;
}

// Agenda wie bei Magist: Hauptfrage, beide Teilfragen sichtbar, aktive hervorgehoben, Antworten eingeblendet
const TF=[['Do discounts drive revenue?','Yes, but not everywhere.'],['Do discounts cost us revenue and reputation?','Not our reputation, but money in the wrong place.']];
function agenda(aktiv,beantwortet,notes,leg){ const s=neu();
  if(leg){ // Farblegende oben rechts
    T(s,'Colors for:',{x:6.25,y:0.3,w:1.0,h:0.24,fontSize:11,color:MUTE,valign:'middle'});
    [['Revenue',GOLD,7.3],['Discount',ROT,8.4]].forEach(([t,c,x])=>{
      s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:0.34,w:0.16,h:0.16,fill:{color:c},line:{color:c,width:0},rectRadius:0.03});
      T(s,t,{x:x+0.24,y:0.3,w:0.8,h:0.24,fontSize:11,color:FG,valign:'middle'});}); }
  T(s,'Do Eniac\'s discounts pay off?',{x:0.5,y:0.75,w:9,h:0.8,fontFace:'Antonio',fontSize:34,bold:true,color:FG,align:'center',valign:'middle'});
  TF.forEach((q,i)=>{const y=2.15+i*1.1; const an=(i===aktiv)||beantwortet.includes(i);
    T(s,String(i+1),{x:1.6,y,w:0.4,h:0.4,fontFace:'Antonio',fontSize:22,bold:true,color:i===aktiv?CYAN:(an?FG:MUTE)});
    T(s,q[0],{x:2.1,y,w:6.5,h:0.4,fontSize:20,bold:i===aktiv,color:an?FG:MUTE,valign:'middle'});
    if(beantwortet.includes(i)) T(s,q[1],{x:2.1,y:y+0.42,w:6.5,h:0.35,fontSize:17,bold:true,color:GOLD});});
  s.addNotes(notes); return s; }

// 1 Titel
let s=pres.addSlide({masterName:'TITEL'});
T(s,'ENIAC · DISCOUNT ANALYSIS',{x:0.5,y:1.0,w:9,h:0.3,fontSize:12,bold:true,color:ROT,charSpacing:3,align:'center'});
T(s,'Eniac\'s Discount Strategy',{x:0.5,y:1.4,w:9,h:1.2,fontFace:'Antonio',fontSize:50,bold:true,color:FG,align:'center',valign:'middle'});
s.addImage({path:'img2/logo_team.png',x:4.34,y:2.8,w:1.32,h:1.0,altText:'Logo Team Discount Detectives: detective with magnifying glass and percent sign'});
T(s,'Team Discount Detectives',{x:0.5,y:4.0,w:9,h:0.35,fontSize:15,bold:true,color:FG,align:'center'});
T(s,'Walter · Miguel · Tim',{x:0.5,y:4.38,w:9,h:0.3,fontSize:13,color:MUTE,align:'center'});
s.addNotes('Tim. Ca. 10 Sekunden. Wir sind das Team Discount Detectives: Walter, Miguel und Tim.');

SP='Tim';
// 2 Hauptfrage (gleiche Position wie Agenda), Klammer zu Marketing und Board
s=neu();
T(s,'Do Eniac\'s discounts pay off?',{x:0.5,y:0.75,w:9,h:0.8,fontFace:'Antonio',fontSize:34,bold:true,color:FG,align:'center',valign:'middle'});
// seitliche Klammer: von den Enden der Frage nach außen und senkrecht auf die Boxen
[[0.8,1.15,0.75,0],[0.8,1.15,0,1.2],[8.45,1.15,0.75,0],[9.2,1.15,0,1.2]].forEach(([x,y,w,h])=>s.addShape(pres.shapes.LINE,{x,y,w,h,line:{color:MUTE,width:1.5}}));
[['Marketing','Do discounts drive revenue?'],['Board of Directors','Do discounts cost us revenue and reputation?']].forEach((a,i)=>{const x=0.6+i*4.5;
  card(s,x,2.35,4.2,1.6);
  T(s,a[0],{x:x+0.3,y:2.55,w:3.6,h:0.4,fontSize:18,bold:true,color:CYAN});
  T(s,a[1],{x:x+0.3,y:3.0,w:3.6,h:0.8,fontSize:19,color:FG,valign:'top'});});
s.addNotes('Tim. Ca. 25 Sekunden. Unsere Hauptfrage: Lohnen sich Eniacs Rabatte? [KLICK] Das Marketing fragt: Bringen Rabatte Umsatz? [KLICK] Das Board fragt: Kosten Rabatte uns Umsatz und Ruf?');

// 4 Agenda: Teilfrage 1 aktiv (Tim moderiert)
agenda(0,[],'Tim. Ca. 10 Sekunden. Kurz zur Orientierung: Orange steht bei uns immer für Umsatz, Rot immer für Rabatt. Wir beantworten die Hauptfrage in zwei Teilen. Zuerst die Sicht des Marketings: Bringen Rabatte Umsatz? Dazu übergebe ich an Walter, er stellt auch unsere Datengrundlage vor.',true);

SP='Walter';
// 3 Datengrundlage, große Zahlen ohne Kästen
s=neu(); kick(s,'SUB-QUESTION 1 · OUR DATA');
cap(s,'All completed orders from January 2017 to March 2018');
[['437','days',FG],['46,605','orders','4FA3E0'],['15.9','€ million revenue',GOLD]].forEach((a,i)=>{const x=0.5+i*3.05;
  T(s,a[0],{x,y:1.85,w:2.85,h:1.1,fontFace:'Antonio',fontSize:a[0].length>7?44:56,bold:true,color:a[2],align:'center',valign:'middle'});
  T(s,a[1],{x,y:3.0,w:2.85,h:0.5,fontSize:20,color:MUTE,align:'center',valign:'top'});});
s.addNotes('Walter. Ca. 15 Sekunden. Grundlage sind alle abgeschlossenen Bestellungen aus 437 Tagen: gut 46.600 Bestellungen und 15,9 Millionen Euro Umsatz.');

// 5 93 %
[0].forEach(()=>{s=neu(); kick(s,'SUB-QUESTION 1 · HOW MUCH DISCOUNT DO WE GIVE?'); cap(s,'Discounts are standard: 93% of all items are discounted');
  img(s,'img2_en/w21.png',{x:0.4,y:1.15,w:5.8,h:3.95},'Bar chart: share of items with and without discount');
  T(s,'56,203',{x:6.5,y:2.0,w:3.1,h:0.9,fontFace:'Antonio',fontSize:48,bold:true,color:ROT});
  T(s,'of 60,375 items\nwere sold at a discount',{x:6.5,y:2.95,w:3.1,h:0.8,fontSize:15,color:FG,valign:'top'});
  s.addNotes('Walter. Ca. 30 Sekunden. 93 Prozent aller Positionen sind rabattiert. [KLICK] Das sind über 56.000 von gut 60.000 Positionen. Rabatt ist bei Eniac der Normalfall.');});

// 6 Monat (Walter)
(PDF?['img2_en/g25_linien_ende.png']:['img2_en/g25_linien_start.png','img2_en/g25_linien.gif']).forEach((p,i)=>{s=neu(); kick(s,'SUB-QUESTION 1 · WHEN DO WE SELL?');
  s.addText([{text:'Monthly trend: ',options:{color:FG}},{text:'revenue',options:{color:GOLD}},{text:', ',options:{color:FG}},{text:'orders',options:{color:'4FA3E0'}},{text:' and ',options:{color:FG}},{text:'discount\u00A0%\u00A0AVG',options:{color:ROT}}],
    {x:0.5,y:0.6,w:7.1,h:0.4,fontFace:'Barlow',fontSize:15,bold:true,margin:0,isTextBox:true});
  img(s,p,{x:0.3,y:1.1,w:9.4,h:4.05},'Bar and line chart: revenue and average discount per month');
  if(!p.includes('_start')){ // November-Zahl oben rechts, auf Höhe von Kicker und Titel
    T(s,'NOVEMBER 2017',{x:6.3,y:0.24,w:3.2,h:0.25,fontSize:11,bold:true,color:CYAN,charSpacing:2,align:'right'});
    [['€2.89M revenue',GOLD],['7,189 orders','4FA3E0'],['21.5% avg. discount',ROT]].forEach((t,j)=>T(s,t[0],{x:6.7,y:0.5+j*0.2,w:2.8,h:0.21,fontSize:12,bold:true,color:t[1],align:'right'})); }
  s.addNotes(i?'Walter. Ca. 40 Sekunden. [Die Balken zeigen den Umsatz, danach erscheinen die Bestellungen in Blau und der Rabatt in Rot.] Im November 2017 waren es 2,89 Millionen Euro Umsatz und 7.189 Bestellungen, fast dreimal so viel wie in einem durchschnittlichen Monat. Umsatz und Bestellungen steigen gemeinsam. Der Rabatt lag mit 21,5 Prozent kaum höher als sonst. Den Peak treiben Black Friday und Weihnachten, nicht der Rabatt. Im Januar und Juli 2017 war der Rabatt am höchsten und der Umsatz auch etwas höher. Das wäre ein Ansatz für einen Test.':'Walter. [KLICK] startet die Animation.');});

// 7 Macs 41 %
chart(['img2_en/g33_start.png','img2_en/g33.gif'],'SUB-QUESTION 1 · WHERE DOES OUR REVENUE COME FROM?','Macs bring in 41% of revenue','Bar chart: revenue by category',
  ['Walter. [KLICK] startet die Animation.','Walter. Ca. 30 Sekunden. Macs bringen 41 Prozent des Umsatzes, zusammen mit Speicher und iPhones drei Viertel. Und das in jedem Monat.']);

SP='Tim';
// 8 Agenda: Teilfrage 1 beantwortet, Teilfrage 2 aktiv (Tim moderiert)
agenda(1,[0],'Tim. Ca. 15 Sekunden. Die erste Antwort: Ja, aber nicht überall. Den großen Umsatz bringen Saison und Macs, nicht der Rabatt. [KLICK] Jetzt die Sicht des Boards: Kosten Rabatte uns Umsatz und Ruf? Dazu Miguel.');
SP='Miguel';
// 10 Miguel: Umsatz gegen Stückzahl je Marke (Top 10 nach Umsatz, Miguels Reihenfolge)
chart(['img2_en/g_vergleich_start.png','img2_en/g_vergleich.gif'],'SUB-QUESTION 2 · WHICH BRANDS MATTER?','Apple is expensive, accessories are cheap','Grouped bar chart: share of revenue and units sold for the ten highest-revenue brands',
  ['Miguel. [KLICK] startet die Animation.','Miguel. Ca. 40 Sekunden. 8 Marken bringen 80 Prozent des Umsatzes, allein Apple 61 Prozent. Bei den verkauften Stück hat Apple aber nur 24 Prozent. Für 80 Prozent der Stück braucht es 34 Marken. Viel Stückzahl kommt also von vielen Marken mit günstigem Zubehör, das wenig Umsatz bringt. Deshalb kostet Rabatt auf Apple viel Geld und Rabatt auf Zubehör wenig.'],[['Share of revenue',GOLD],['Share of units sold','4FA3E0']]);
// 9 Preisklasse
chart(['img2_en/g43_start.png','img2_en/g43.gif','img2_en/g44.gif'],'SUB-QUESTION 2 · WHERE ARE DISCOUNTS HIGHEST?','The highest discounts go where the least revenue is made','Two bar charts: revenue and discount by price range',
  ['Miguel. [KLICK] Umsatz je Preisklasse.','Produkte über 1.000 Euro bringen 47 Prozent des Umsatzes, Produkte unter 50 Euro nur gut 3 Prozent. [KLICK]','Miguel. Ca. 40 Sekunden. Beim Rabatt ist es umgekehrt: unter 50 Euro im Schnitt 26,5 Prozent, über 1.000 Euro nur 11 Prozent.'],[['Revenue',GOLD],['Avg. discount',ROT]]);

// 11 Miguel: Apple gegen andere Marken als Paare (Klick 1 Apple, Klick 2 andere Marken)
(PDF?['img2_en/g_paare2_ende.png']:['img2_en/g_paare1_start.png','img2_en/g_paare1.gif','img2_en/g_paare2.gif']).forEach((p,i)=>{s=neu(); kick(s,'SUB-QUESTION 2 · WHAT DOES THIS MEAN FOR REVENUE AND REPUTATION?');
  cap(s,'Apple: lower discount rate, but almost half of all discount money');
  img(s,p,{x:0.4,y:1.15,w:9.2,h:4.0},'Paired columns Apple vs. other brands: units sold 24 vs. 76%, revenue 61 vs. 39%, avg. discount 11 vs. 18%, discount money 48 vs. 52%');
  const N=['Miguel. [KLICK] startet die Animation.',
    'Miguel. Apple macht nur 24 Prozent der verkauften Stück aus, bringt aber 61 Prozent des Umsatzes. Apple wird mit durchschnittlich 11 Prozent moderat rabattiert, trotzdem gehen 48 Prozent des Rabattgelds an Apple. [KLICK]',
    'Miguel. Ca. 40 Sekunden insgesamt. Die anderen Marken verkaufen dreimal so viele Stück, werden mit 18 Prozent stärker rabattiert und bekommen trotzdem nur etwa gleich viel Rabattgeld. Pro verkauftem Apple-Gerät fließen im Schnitt rund 72 Euro Rabatt, bei den anderen Marken rund 25 Euro. Zum Ruf: Apple wird nicht verramscht, das Markenbild ist nicht das Problem. Zum Umsatz: Fast die Hälfte des Rabattgelds geht an Geräte, die sich vermutlich auch so verkaufen.'];
  s.addNotes(PDF?N[2]:N[i]);});

SP='Tim';
// 12 Agenda: beide Teilfragen beantwortet
agenda(-1,[0,1],'Tim. Ca. 20 Sekunden. Zusammengefasst: Bringen Rabatte Umsatz? Ja, aber nicht überall, den großen Umsatz bringen Saison und Macs. [KLICK] Kosten sie uns Umsatz und Ruf? Den Ruf nicht, Apple wird moderat rabattiert. Aber fast die Hälfte des Rabattgelds geht an Apple-Geräte, die sich vermutlich auch so verkaufen.',true);

const ANTW1=process.env.ANTW1||'4FA3E0';
// 13 Antwort auf die Hauptfrage mit Kernsatz (Frage wie auf der Agenda, Antwort orange)
s=neu();
T(s,'Do Eniac\'s discounts pay off?',{x:0.5,y:0.75,w:9,h:0.8,fontFace:'Antonio',fontSize:34,bold:true,color:FG,align:'center',valign:'middle'});
T(s,'We\'re not losing money.',{x:0.3,y:1.85,w:9.4,h:0.8,fontFace:'Antonio',fontSize:38,bold:true,color:ANTW1,align:'center',valign:'middle'});
T(s,'But we\'re missing out on money\nwe could be earning.',{x:0.2,y:2.75,w:9.6,h:1.45,fontFace:'Antonio',fontSize:38,bold:true,color:GOLD,align:'center',valign:'middle',lineSpacingMultiple:1.0});
s.addNotes('Tim. Ca. 15 Sekunden. Damit zur Hauptfrage: Lohnen sich Eniacs Rabatte? [KLICK] Nach allem, was unsere Daten zeigen: Wir verlieren kein Geld. [KLICK] Aber wir verpassen Geld, das wir noch nicht verdienen. Und so holen wir es uns.');

// 14 Empfehlung: eine große Empfehlung, drei Bausteine
s=neu(); kick(s,'OUR RECOMMENDATION');
[['1','Lower the Apple discount'],['2','Target discounts at other brands'],['3','Manage discounts by season']].forEach((c,i)=>{const x=0.5+i*3.05;
  card(s,x,1.5,2.85,2.3);
  T(s,c[0],{x:x+0.3,y:1.75,w:1,h:0.7,fontFace:'Antonio',fontSize:38,bold:true,color:CYAN});
  T(s,c[1],{x:x+0.3,y:2.6,w:2.35,h:1.0,fontSize:21,bold:true,color:FG,valign:'top'});});
s.addNotes('Tim. Ca. 40 Sekunden. Unsere Empfehlung hat drei Bausteine. [KLICK] Erstens: weniger Rabatt auf Apple, von heute 11 Prozent auf 6 bis 7 Prozent. [KLICK] Zweitens: Rabatt dorthin, wo er als Kaufanreiz wirkt, bei anderen Marken und beim Zubehör, zum Beispiel zum Gerätekauf oder beim zweiten Stück, Walters Idee mit dem Ladegerät. [KLICK] Drittens: saisonal steuern. In der Saison verkauft sich viel von allein, außerhalb der Saison können wir gezielt Ladenhüter abverkaufen. [KLICK] Wir testen das zuerst vier Wochen und vergleichen vorher die Marktpreise.');

// 15 Rabatt umschichten: was weniger Apple-Rabatt bringt
(PDF?['img2_en/g_regler_balken_ende.png']:['img2_en/g_regler_linie_start.png','img2_en/g_regler_linie.gif','img2_en/g_regler_balken.gif']).forEach((p,i)=>{s=neu(); kick(s,'OUR RECOMMENDATION · SHIFT THE DISCOUNT');
  legende(s,[['Discount on other brands',ROT],['Revenue',GOLD]],0.68);
  T(s,'EXAMPLE CALCULATION',{x:6.3,y:0.24,w:3.2,h:0.25,fontSize:11,bold:true,color:CYAN,charSpacing:2,align:'right'});
  T(s,'January 2017 to March 2018',{x:6.3,y:0.5,w:3.2,h:0.22,fontSize:12,bold:true,color:MUTE,align:'right'});
  img(s,p,{x:0.4,y:1.05,w:9.2,h:4.1},'Bars: additional revenue at an Apple discount of 10 to 6 percent; line: possible discount on other brands with the same budget');
  const NR=['Tim. Ca. 40 Sekunden. Ein Beispielszenario: So könnte es aussehen, wenn wir den Rabatt bei Apple senken und bei anderen Marken erhöhen. [KLICK]',
    'Tim. Unten steht der Apple-Rabatt von 10 bis 6 Prozent. Die rote Linie zeigt, auf wie viel Prozent wir den Rabatt auf alle anderen Marken im Durchschnitt erhöhen könnten, mit demselben Budget: von heute 18 auf bis zu 25 Prozent. [KLICK]',
    'Tim. Und wenn wir das Geld nicht umschichten, sondern einbehalten: Jeder Prozentpunkt Apple-Rabatt entspricht rund 105.000 Euro. Bei 7 Prozent sind das bis zu 0,44 Millionen Euro mehr Umsatz, bei 6 Prozent 0,54 Millionen, jeweils im Datenzeitraum von gut 14 Monaten und bei gleicher Stückzahl. Bei gleicher Stückzahl ist das zugleich mehr Gewinn. Auf ein Jahr gerechnet sind es rund 0,36 beziehungsweise 0,45 Millionen Euro.'];
  s.addNotes(PDF?NR.join(' '):NR[i]);});

// 16 Danke
s=pres.addSlide({masterName:'TITEL'});
T(s,'Thank you for your attention',{x:0.3,y:1.2,w:9.4,h:1.0,fontFace:'Antonio',fontSize:34,bold:true,color:FG,align:'center',valign:'middle'});
s.addImage({path:'img2/logo_team.png',x:4.34,y:2.65,w:1.32,h:1.0,altText:'Logo Team Discount Detectives'});
T(s,'Team Discount Detectives',{x:0.5,y:3.8,w:9,h:0.35,fontSize:15,bold:true,color:FG,align:'center'});
T(s,'Walter · Miguel · Tim',{x:0.5,y:4.18,w:9,h:0.3,fontSize:13,color:MUTE,align:'center'});
s.addNotes('Tim. Vielen Dank für Ihre Aufmerksamkeit. Für Rückfragen haben wir einiges vorbereitet.');

// Anhang-Übersicht
s=neu(); kick(s,'APPENDIX');
cap(s,'Prepared for your questions');
[['A1','What research says','Three studies on discounts, brands and trust'],['A2','Apple discount calculation','€105,000 per percentage point and a 4.5% buffer'],['A3','Limits of our data','Cleaning, purchase prices, customer ID'],['A4','Margin scenarios','Loss-making sales at 10, 20 or 30% margin'],['A5','Discount by category','In percent and in euros'],['A6','Revenue over the year','Monthly revenue by category'],['A7','Discount money by brand','Discount in euros for the top 10 brands by revenue']].forEach((a,i)=>{const y=1.2+i*0.55;
  T(s,a[0],{x:0.6,y,w:0.7,h:0.5,fontFace:'Antonio',fontSize:20,bold:true,color:MUTE,valign:'middle'});
  T(s,a[1],{x:1.35,y,w:3.2,h:0.5,fontSize:17,bold:true,color:FG,valign:'middle'});
  T(s,a[2],{x:4.6,y,w:4.9,h:0.5,fontSize:14,color:MUTE,valign:'middle'});
  if(i<6) s.addShape(pres.shapes.LINE,{x:0.6,y:y+0.46,w:8.9,h:0,line:{color:LINE,width:0.75}});});
s.addNotes('Tim. Danke. Für Rückfragen haben wir im Anhang noch diese Folien vorbereitet.');
SP='';
// A1 Was die Forschung sagt, mit Literatur auf derselben Folie
s=neu(); kick(s,'APPENDIX A1 · WHAT RESEARCH SAYS');
[['Infrequent discounts protect the brand','Yoo, Donthu and Lee (2000)'],['Trust matters more than the lowest price','Smith and Brynjolfsson (2001)'],['Repeat customers pay more','Berends and Gerpott (2025)']].forEach((c,i)=>{const x=0.5+i*3.05;
  card(s,x,0.75,2.85,1.55);
  T(s,c[0],{x:x+0.25,y:0.88,w:2.4,h:0.95,fontSize:16,bold:true,color:FG,valign:'top'});
  T(s,c[1],{x:x+0.25,y:1.85,w:2.4,h:0.3,fontSize:11,color:CYAN,valign:'middle'});});
T(s,'REFERENCES',{x:0.5,y:2.5,w:9,h:0.25,fontSize:10,bold:true,color:MUTE,charSpacing:2});
s.addText([
 {text:'Berends, J., & Gerpott, T. J. (2025). Exploring price tolerance in online retail: A comparative analysis of price comparison website use and repeat purchases. ',options:{color:FG}},
 {text:'Electronic Commerce Research, 25',options:{color:FG,italic:true}},{text:'(4), 3165–3185. https://doi.org/10.1007/s10660-023-09791-5 (published online 2023)',options:{color:FG,breakLine:true}},
 {text:' ',options:{breakLine:true,fontSize:8}},
 {text:'Smith, M. D., & Brynjolfsson, E. (2001). Consumer decision-making at an Internet shopbot: Brand still matters. ',options:{color:FG}},
 {text:'The Journal of Industrial Economics, 49',options:{color:FG,italic:true}},{text:'(4), 541–558. https://doi.org/10.1111/1467-6451.00162',options:{color:FG,breakLine:true}},
 {text:' ',options:{breakLine:true,fontSize:8}},
 {text:'Yoo, B., Donthu, N., & Lee, S. (2000). An examination of selected marketing mix elements and brand equity. ',options:{color:FG}},
 {text:'Journal of the Academy of Marketing Science, 28',options:{color:FG,italic:true}},{text:'(2), 195–211. https://doi.org/10.1177/0092070300282002',options:{color:FG}}
],{x:0.5,y:2.8,w:9,h:2.25,fontFace:'Barlow',fontSize:11,margin:0,isTextBox:true,valign:'top',paraSpaceAfter:2});
s.addNotes('Für Rückfragen. Die Forschung stützt unsere Empfehlung: Häufige Rabatte senken den wahrgenommenen Wert einer Marke. Kunden kaufen auch zu höheren Preisen bei Händlern, denen sie vertrauen. Und Stammkunden akzeptieren höhere Preise als Preisvergleicher. Wir sind überzeugt: Weniger Rabatt auf Apple schützt die Marke, günstiges Zubehör bringt Kunden zurück. Ob sie wirklich wiederkommen, können wir ohne Kunden-ID nicht messen, das kann der Test prüfen.');

// A2 Rechenweg zur Empfehlung
s=neu(); kick(s,'APPENDIX A2 · APPLE DISCOUNT CALCULATION');
cap(s,'Even with 4.5% fewer Apple sales, we don\'t lose revenue');
[['105,000','€ per percentage point\nof Apple discount',ROT],['0.44','€ million more revenue at\n7% instead of 11% discount',GOLD],['4.5%','buffer in\nApple sales','4FA3E0']].forEach((a,i)=>{const x=0.5+i*3.05;
  T(s,a[0],{x,y:1.3,w:2.85,h:1.0,fontFace:'Antonio',fontSize:a[0].length>6?46:56,bold:true,color:a[2],align:'center',valign:'middle'});
  T(s,a[1],{x,y:2.35,w:2.85,h:0.75,fontSize:17,color:MUTE,align:'center',valign:'top'});});
T(s,'Basis: €10.5M Apple revenue at list prices, 11.1% avg. discount today, same unit sales assumed',{x:0.5,y:3.45,w:9,h:0.3,fontSize:11,color:MUTE,align:'center'});
T(s,'TEST PLAN',{x:0.5,y:4.0,w:9,h:0.25,fontSize:10,bold:true,color:MUTE,charSpacing:2});
[['What','iPads at 7% instead of 11% discount'],['When','6 weeks, not in November'],['Comparison','Same weeks of the previous year'],['Success','Less than 4.5% decline: roll out']].forEach((c,i)=>{const x=0.5+i*2.29;
  T(s,c[0],{x,y:4.3,w:2.1,h:0.28,fontSize:12,bold:true,color:CYAN});
  T(s,c[1],{x,y:4.58,w:2.1,h:0.5,fontSize:12,color:FG,valign:'top'});});
s.addNotes('Für Rückfragen. Ein Prozentpunkt Apple-Rabatt entspricht rund 105.000 Euro, weil Apple 10,5 Millionen Euro Umsatz zu Listenpreisen macht. Von 11 auf 7 Prozent sind das rund 0,44 Millionen Euro mehr Umsatz bei gleicher Stückzahl. Der Kunde zahlt dann pro Gerät rund 4,7 Prozent mehr, deshalb bleibt der Umsatz gleich, solange wir nicht mehr als 4,5 Prozent weniger Apple-Geräte verkaufen, also etwa 730 Geräte. Beispiel: MacBook für 1.000 Euro Listenpreis, heute 890 Euro, künftig 930 Euro.');

// A3 Grenzen der Daten
s=neu(); kick(s,'APPENDIX A3 · LIMITS OF OUR DATA');
cap(s,'What we had to clean and what is missing');
[['226,909 → 46,605','orders after cleaning'],['19,326 → 9,992','products in the catalog'],['No purchase prices','Margins can only be estimated']].forEach((a,i)=>{const x=0.5+i*3.05;
  card(s,x,1.3,2.85,1.5);
  T(s,a[0],{x:x+0.2,y:1.5,w:2.45,h:0.6,fontFace:'Antonio',fontSize:18,bold:true,color:i==2?CYAN:FG,align:'center',valign:'middle'});
  T(s,a[1],{x:x+0.2,y:2.15,w:2.45,h:0.5,fontSize:13,color:MUTE,align:'center',valign:'top'});});
T(s,[{text:'Completed orders only',options:{bullet:true}},{text:'Prices stored as text with several dots, e.g. 1.137.99',options:{bullet:true}},{text:'Order totals don\'t match the line items',options:{bullet:true}},{text:'Products missing from the catalog, and duplicates',options:{bullet:true}},{text:'No customer ID: new customers and loyalty cannot be measured',options:{bullet:true,color:CYAN}}],
  {x:0.6,y:3.1,w:8.8,h:1.6,fontSize:15,color:FG,paraSpaceAfter:4,valign:'top'});
s.addNotes('Für Rückfragen zu den Grenzen unserer Daten: Nach der Bereinigung bleibt rund ein Fünftel der Bestellungen. Vor allem fehlen Einkaufspreise, und es gibt keine Kunden-ID, deshalb können wir nichts über Neukunden oder Kundenbindung sagen. Deshalb sagen wir nicht, dass Rabatte Verlust machen, sondern schlagen Tests vor.');

// Anhang
s=neu(); kick(s,'APPENDIX A4 · WHETHER A DISCOUNT PAYS OFF DEPENDS ON THE MARGIN');
cap(s,'Share of sales with a discount above the margin, i.e. loss-making sales');
const hh=(t)=>({text:t,options:{bold:true,color:MUTE,fontSize:13,align:'center'}});
const rr=(k,u,a,b,c)=>[{text:k,options:{bold:true,color:FG}},{text:u,options:{color:GOLD,align:'center'}},{text:a,options:{color:FG,align:'center'}},{text:b,options:{color:FG,align:'center'}},{text:c,options:{color:FG,align:'center'}}];
s.addTable([[{text:'Category',options:{bold:true,color:MUTE,fontSize:13}},hh('Revenue share'),hh('at 10% margin'),hh('at 20% margin'),hh('at 30% margin')],
 rr('Mac','40.9%','35%','11%','3%'),rr('Storage','20.7%','70%','34%','10%'),rr('iPhone and iPad','14.4%','46%','10%','3%'),rr('Monitors and input','9.3%','65%','38%','17%'),rr('Cases and bags','2.1%','89%','68%','45%')],
 {x:0.5,y:1.15,w:9,colW:[2.6,1.6,1.6,1.6,1.6],fontFace:'Barlow',fontSize:15,rowH:0.5,valign:'middle',border:{type:'solid',pt:0.75,color:LINE},fill:{color:BG}});
T(s,'Purchase prices and margins are not in the dataset. The columns are scenarios, not an assumption about Eniac\'s actual margin.',{x:0.5,y:4.5,w:9,h:0.5,fontSize:12,color:MUTE});
s.addNotes('Für Rückfragen zur Marge.');
chart(['img2_en/a4_kombi.png'],'APPENDIX A5 · DISCOUNT BY CATEGORY','Macs: a low discount rate, but the largest amount in euros','Two bar charts: average discount in percent and discount in euros by category',['Für Rückfragen. Macs: 10,3 Prozent Rabatt, aber 0,77 Millionen Euro, 31 Prozent des gesamten Rabattgelds. Hüllen und Taschen: 32,7 Prozent, aber nur 0,15 Millionen Euro.']);
chart(['img2_en/a5_mac_oben.png'],'APPENDIX A6 · REVENUE OVER THE YEAR','Macs lead in every month','Stacked area: monthly revenue by category, Mac on top',['Für Rückfragen. Mac ist in allen 15 Monaten die umsatzstärkste Kategorie, mit 35 bis 72 Prozent des Monatsumsatzes.']);
chart(['img2_en/g_rabattmarke_ende.png'],'APPENDIX A7 · DISCOUNT MONEY BY BRAND','Almost half of all discount money goes to Apple','Bar chart: discount in euros and discount rate of the ten highest-revenue brands',['Für Rückfragen. Apple 1,17 Millionen Euro bei 11,1 Prozent Rabatt.'],[['Discount in euros',ROT]]);
// Fortschrittsbalken im Flammenverlauf: vom Hauptfrage-Slide bis "Rabatt umschichten", Startbild und GIF einer Folie zählen als eine Folie
{ const SL=pres.slides, txt=x=>JSON.stringify(x._slideObjects);
  const kicker=x=>{const m=JSON.stringify(x._slideObjects).match(/"text":"((?:SUB-QUESTION|OUR RECOMMENDATION)[^"]*)"/); return m?m[1]:null;};
  const ende=SL.findIndex(x=>txt(x).includes('Thank you for your attention'));
  let nr=1, vorher=null;
  for(let i=1;i<ende;i++){ const k=kicker(SL[i]); if(!(k&&k===vorher)) nr++; vorher=k;
    const f=Math.min(nr,15);
    SL[i].addImage({path:'img2_en/fortschritt_'+String(f).padStart(2,'0')+'.png',x:4.3,y:5.318,w:4.6,h:0.025});
  }
  if(nr!==15) console.log('WARNUNG Fortschritt: letzte Folie ist Nr. '+nr);
}
// Fragen-Hub: Zeilen der Übersicht verlinken auf ihre Folie, jede Anhangfolie verlinkt zurück
{ const SL=pres.slides, find=t=>SL.findIndex(x=>JSON.stringify(x._slideObjects).includes(t))+1;
  const hub=find('Prepared for your questions'), H=SL[hub-1];
  ['A1','A2','A3','A4','A5','A6','A7'].forEach((k,i)=>{ const z=find('APPENDIX '+k+' ·');
    H.addShape(pres.shapes.RECTANGLE,{x:0.55,y:1.2+i*0.55,w:9,h:0.5,fill:{color:BG,transparency:100},line:{type:'none'},hyperlink:{slide:z,tooltip:'Zu '+k}}); });
  for(let i=hub;i<SL.length;i++) SL[i].addText('← Overview',{x:7.9,y:0.24,w:1.7,h:0.32,fontSize:11,color:MUTE,align:'right',valign:'middle',margin:0,hyperlink:{slide:hub,tooltip:'Back to overview'}});
}
if(process.env.STATES){ // Aufbau-Zustände für das Portfolio-Video: jede Stufe als eigene Folie am Ende
  const SL=pres.slides, N0=SL.length, map={};
  const G={1:[[0],[1],[2,3,4]],2:[[1],[2,3,4,5],[6,7,8],[9,10,11]],3:[[6],[7,8],[9,10],[1,2,3,4,5]],4:[[1,2],[3,4],[5,6],[7,8]],
    5:[[1,2],[3],[4,5]],10:[[1,2,3,5,6],[4]],19:[[1,2,3,4,5,6,7,8,9,10,11],[12]],20:[[1],[2],[3]],21:[[1],[2,3,4],[5,6,7],[8,9,10]],25:[[0],[1,2,3]]};
  Object.entries(G).forEach(([n,gr])=>{ const o=SL[n-1], obs=o._slideObjects, master=(n==1||n==25)?'TITEL':'BILD';
    const inhalt=new Set(gr.flat()); const basis=obs.map((x,k)=>k).filter(k=>!inhalt.has(k)&&obs[k]._type!=='notes');
    map[n]=[]; let shown=[...basis];
    for(let g=0;g<=gr.length;g++){ if(g>0) shown=shown.concat(gr[g-1]);
      const s2=pres.addSlide({masterName:master}); const keep=new Set(shown);
      s2._slideObjects=obs.filter((x,k)=>keep.has(k)); s2._relsMedia=o._relsMedia; s2._rels=o._rels;
      map[n].push(pres.slides.length); } });
  require('fs').writeFileSync('video_en/states.json',JSON.stringify(map));
  pres.writeFile({fileName:'video_en/states.pptx'}).then(()=>console.log('states ok')); }
else
pres.writeFile({fileName:PDF?'pdfversion_en.pptx':'Eniac_CEO_Presentation_EN.pptx'}).then(()=>console.log('ok'));
