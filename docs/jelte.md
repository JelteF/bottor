# Hoofdtaak: Client

### Week 2
##### Literatuuronderzoek naar structuur en protocol van bestaande botnets
Veel botnets maken gebruik van het HTTP protocol omdat bijna elke firewall dit
verkeer door laat. Daar bovenop wordt dan hun eigen protocol geïmplementeerd.
Dit bestaat vaak uit het opvragen van een nieuwe opdracht door de cliënt zodat
de command server niet overbelast raakt.

##### Samenwerken met Jaap om een protocol samen te stellen tussen client en server
De basis API is bestaat uit het versturen van het versturen van de rijen van de
eerste matrix en kolommen van de tweede matrix. Dan vermenigvuldigt de client
elke rij met elke kolom en stuurte de resultaten daarvan terug.

##### Libraries uitzoeken voor gebruik in de client
Om vanuit Python HTTP requests te sturen naar een server is de requests library
het simpelst om te gebruiken. Het is ook ruimschoots uitgebreid genoeg voor de
features die wij nodig hebben. Voor het meten van het CPU gebruik is psutil de
meest gebruikelijk optie. Angezien we ook geen ingewikkelde metingen hoeven te
doen voor de CPU load heeft deze library genoeg functionaliteit.

### Week 3
##### Vermenigvuldigen van rijen en kolommen in de in de vorm van de API
Omdat de client en de server naast elkaar worden ontwikkeld werd de client eerst
geimplementeerd met een vaste datastructuur gebaseerd op de afgesproken API.
Bij het maken van die datastructuur bleek er wat onnodige informatie expcliciet
meegegeven te worden. Dit is uit de API gehaald en de datastructuur is toen
gebaseerd op de vernieuwde API.

##### Basis protocol naar server implementeren voor matrices
Het implementeren van het protocol was niet al te ingewikkeld. De requests
library voor Python is vrij simpel te gebruiken. In combinatie met de standaard
json module was het geen enkel probleem om json data te versturen naar de
server.

##### Client cpu load bepalen en sturen naar de server
De CPU load moet gemeten worden in een apparte thread van het main programma,
aangezien er anders niet gemeten kan worden met vastgesteld interval. Een
interval is nodig zodat de server op de hoogte gesteld kan worden van de staat
van de client.

##### Verminderen van de request overhead op de server
Nadat de communicatie tussen de client en server werkte bleek dat de elke
request toch een behoorlijke overhead had. Voor enige optimalisatie duurde het
versturen van het request ongeveer 5 keer zoveel tijd als de daadwerkelijke
die nodig was voor de client om zijn stuk matrix uit te rekenen. Dit hebben we
op een aantal verschillende manieren verminderd.

Een van de eerste dingen om de relatieve overhead te verminderen was veel meer
rijen en kolommen sturen per request.  De overhead per request gaat in theorie
lineair omhoog (r + k) en het werk dat de client kan uitvoeren gaat kwadratisch
omhoog (r * k). Dit hielp erg goed in de verhouding in tijd tussen de request en
en het werk van de client te verbeteren. Het rekenen duurde nu ongeveer
anderhalf keer zo lang als de tijd die nodig was om de request te versturen. Dit
was natuurlijk nog steeds niet goed genoeg, maar ondertussen liepen we tegen een
ander probleem aan. Hoewel de overhead relatief steeds beter werd naarmate er
meer data per keer werd verstuurd, werd uiteraard de absolute tijd voor die per
request nodig was steeds hoger. Dit liep al tegen de 5 seconden per request aan.
Dit was onacceptabel aangezien de server dan geen andere requests meer af kon
handelen in die tijd.

Er waren 2 grote posten waardoor die tijd zo op liep. Als eerste werd er zonder
goede reden een matrix weggeschreven naar de hardeschijf. De code voor het
wegschrijven van matrices was niet erg efficient, dus deze is verbetert en
verder wordt deze specifieke matrix ook niet meer weggeschreven.

De tweede post lag in de JSON serialisatie. Deze post is op twee verschillende
manieren vermindert. Allereerst is de structuur van de API aangepast. In plaats
van het sturen van rijen en kolommen als losse arrays, stuurt de server nu twee
2D arrays, A en B, respectievelijk bestaande uit de rijen van de eerste matrix
en de kolommen van de tweede matrix die de client met elkaar moet
vermenigvuldigen. Daarna was het een al een stukje sneler, maar het was nog niet
eigenlijk nog niet snel genoeg. We hebben getest waar het grootste probleem zat
bij de serialisatie en dat bleek het serialiseren van alle floats te zijn. Dit
bleek toen eigenlijk vrij onzinnig om uberhaupt te doen. Die floats die
geserialised werden stonden als strings in het matrix bestand. Bij het inladen
van een matrix werden ze omgezet naar floats en dan werden ze bij het
serialiseren weer omgezet naar strings. Daarna werden ze bij de client bij het
deserialiseren weer omgezet naar floats. We hebben het dus gewoon strings gelaten
en zijn ze pas bij de client expliciet gaan omzetten naar floats. Uiteindelijk
heeft dit alles ervoor gezorgd dat de requests minder dan een seconde server
tijd in beslag nemen.


### Week 4
- Verslag schrijven
