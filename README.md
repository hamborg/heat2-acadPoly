# heat2-acadPoly
Script for importing AutoCAD polylines into HEAT2 

Script af Lasse Hamborg (LHAM),
November 2022.

## h2poly
_Danish:_

Dette script bruges til at få geometri fra AutoCAD **polylines ind i HEAT2**.
For at køre scriptet, dobbeltklik på scriptet (.PY-filen). Det er ikke vigtigt, hvilken mappe scriptet ligger i.

### Geometri i AutoCAD - Forberedelse
Du kan med fordel optegne din ønskede geometri i AutoCAD med `polylines`.  
*Bemærk:* HEAT2 arbejder ikke med buer. Simplificér derfor disse om nødvendigt.

Sørg i øvrigt for at sætte dit nul-punkt/origo i AutoCAD til det dit ønskede nulpunkt/samme punkt som i HEAT2.
Dette gøres med kommandoen `UCS`.

Vælg alle de polylines du vil have ind i HEAT2.  
Du kan med fordel vælge de objekter, der skal 'bagerst' i simuleringen, først og de 'øverste' sidst.
(Du behøver ikke tage ALT på én gang, hvis du vil have et bedre overblik.)

kør kommandoen `list`. Tryk Enter, hvis den skriver det, indtil alle punkter er skrevet ud.

Marker og kopier nu al den tekst, der kom ud af `list`-kommandoen.
Det er ikke så vigtigt hvor du starter og slutter; Det vigtigeste at få med er linjerne med `at point (...)`.

### Åbn 'h2poly'-scriptet
#### Vælg skalering
Typisk er AutoCAD-geometri tegnet i mm, mens HEAT2-geometri er i m. Derfor er default-skalering sat til 1000.
Tryk Enter for at bruge denne default-skalering.

Hvis du ønskes denne ændret f.eks. pga. et andet tegningsforhold, så skriv dette ind.
(Der kan muligvis være behov for at lege lidt med denne, hvis det ikke er en oplagt skalering.)

#### Paste polylines
Indsæt nu al den kopierede tekst fra 'list'-kommandoen.
Det gøres med `Ctrl + V` eller højreklik (alt efter terminal).

Tryk enter 2-3 gange indtil der skrives `DONE!`.

#### Script færdig
Scriptet har nu oversat list-data'en til HEAT2-element(er).¹

Gå derfor ind i HEAT2; I pre-processoren, tryk på menu-knappen 'script'.
Indsæt de nye elementer ved at paste `Ctrl + V` dem ind på en tom linje.

Tryk `Ctrl + R`.

Voila!  
Geometrien skulle nu gerne være at se i pre-processoren.

> **¹ Note:**
> Hvis du har valgt flere elementer, er scriptet nødt til at bruge et sekund på at åbne Notepad.  
> Heri indsættes elementerne, markeres og kopieres på ny, inden Notepad lukker.  
> Det sker fordi, HEAT2 åbenbart ikke genkender linjeskiftene fra scriptet. (Der vil f.eks. stå `m (...) INSET_MATR_HEREm (...) INSET_MATR_HERE` i stedet for at have linjeskift inden `m`)  
> Hvis Notepad IKKE lukker, og den forklarende tekst stadigt står, så følg vejledningen heri.  
> Kort fortalt: Marker og slet alt - paste `Ctrl + V` - marker og kopier alt tekst igen. Luk da Notepad uden at gemme.

#### Tilføj materialer i HEAT2
I koden for elementerne findes `INSET_MATR_HERE` i slutningen af linjerne. Her skrives navnet på det materiale, der skal bruges for elementet.  
Hvis der ikke står noget gyldigt materiale, bruges overstående materiale.
Vælg et materiale i materialelisten. I koden for elementet, slet `INSET_MATR_HERE` og tryk `Ctrl + N`.

Hvis man har flere elementer med samme materiale, kan dette udnyttes ved at lave et 'tomt' element ovenover med det rigtige materiale.  
Det gøres simpelt ved at skrive i en ny linje over elementerne:

	s 0 0 0 0 (matriale navn)

På den måde kan disse også bruges til at skabe overblik i elementerne i koden. - Ret smart! :)

Find yderligere hjælp til HEAT2-script ved at trykke på 'help'-menuknappen.

### Kør igen
Scriptet kan køres så mange gange du vil. Så gentag hele mollevitten, hvis du har behov for det.  
Vær blot opmærksom på, at hver gang kopieres de nye elementer, og evt. gamle elementer glemmes.
Så sørg for at sætte elementerne ind i HEAT2 efter hver gang, du har kørt elementer igennem.

### Lidt info om scripting i HEAT2
I HEAT2 (og i HEAT3) er det ofte nemmere at opbygge sine modeller gennem scripting-modulet, som fremkommer gennem 'script'-menuknappen i pre-processoren.
Heri kan man skrive sine elementer ind i programmet vha. deres koordinater (typisk i meter [m]).
Det er ret lige til, men tryk på 'Help'-menuknappen for at læse om syntaxen.

Hvert element skrives på sin egen linje. Scriptet læses selvfølgelig oppefra og ned, og de nederste elementer trumfer derfor de øverste.  
F.eks.: Elementerne i en let træ-væg med isolering og med træ-rammer pr. x m kan opbygges:

	(Facadeplade)
	(Hele isoleringsområdet, ende til anden)
	(Gipsplade)
	(træ-ramme 1)
	(træ-ramme 2)
	(træ-ramme 3)
	(...)

Elementerne opbygges gennem koordinaterne (`x y`) og div. betegnelser. Kort fortalt er der 3 vigtige typer: `s`, `r` og `m`. (I HEAT3 er der andre væsentlige.)
De to første bygger rektangler op gennem koordinaterne for diagonalen. `r` bruger karakteristiske koordinater og `s` bruger relative koordinater.
`m` bruges derimod for polygoner (min. tre punkter). Heri skrives karakteristiske koordinater (x y) for alle punkterne.

Der **SKAL mellemrum mellem koordinaterne** - også selvom der bruges tabulering!  
F.eks.: En firkant, der starter 0.1 m til højre for Origo og 0.3 m oppe, som er 2 m bred og 4 m høj kan skrives:

	r 	0.1 	0.3 	2.1 	4.3
	s 	0.1 	0.3 	2.0 	4.0
	m 	0.1 0.3 	2.1 0.3 	2.1 4.3 	0.1 4.3

> NB: Tab mellem tal er ikke nødvendige, men øger overskueligheden. Mellemrum er dog et must - også med tab!

#### Materialer
Efter koordinaterne skrives navnet på elementets materiale som det står i materialelisten.
Det nemmeste er at finde materialet i listen, stille sig dét sted i scriptet, det skal stå og trykke `Ctrl + N`. (Bemærk det lille mellemrum, der kommer med automatisk.)  
F.eks.:

	s 	0.1 	0.3 	2.0 	4.0 	Steel, IEA
	m 	0.1 0.3 	2.1 0.3 	2.1 4.3 	0.1 4.3 	Steel, IEA

Hvis der ikke står skrevet et materiale (eller det er stavet forkert), benyttes forrige materiale. (Bemærk at `INSET_MATR_HERE` er et ukendt materiale. Derfor benyttes forrige materiale.)  
Det kan være uoverskueligt, at materialet står laaangt ude til højre. Derudover er det nemt at skifte materiale, hvis det kun skal gøres ét sted.

Udnyt derfor dette princip til at lave orden i 'h2poly's polygoner ved at lave tomme elementer ovenover.  
F.eks.:

	s 0 0 0 0 Steel, IEA
	s 	0.2 	0.3 	0.10 	0.012
	m 	0.110 	-0.316 	0.070 	-0.316 	0.070 	-0.046 	-0.138 	-0.046 	-0.220 	-0.316 	-0.300 	-0.316 	-0.300 	-0.331 	0.110 	-0.331 
	s 0 0 0 0 concrete, IEA
	m 	-0.137 	-0.061 	0.064 	-0.061 	0.064 	-0.316 	-0.214 	-0.316 

#### Kommentering og overskrifter
Kommentering skrives med `!`.
Dette kan med fordel bruges til at fjerne objekter midlertidigt eller lave overskrifter!  
F.eks.:

	! ETAGEADSKILDELSE
	!	x	y	x	y
	r 	-2 	2 	-2.25 	2.25 	concrete, IEA ! Rå betondæk
	!r 	-4 	4 	-4.25 	4.25 	concrete, IEA ! Stort betondæk - tester

### FEJLMELDING
**A:** Dette script er kun designet til HEAT2. Men det virker ret straight forward at bygge et script til HEAT3.
Indtil videre findes en beta-version af et script, der vha. Grasshopper hiver Rhino-geometri over i et script til HEAT3.
