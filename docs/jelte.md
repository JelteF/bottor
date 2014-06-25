# Hoofdtaak: Client

### Week 2
- Literatuuronderzoek naar structuur en protocol van bestaande botnets
Veel botnets maken gebruik van het HTTP protocol omdat bijna elke firewall dit
verkeer door laat. Daar bovenop wordt dan hun eigen protocol geïmplementeerd.
Dit bestaat vaak uit het opvragen van een nieuwe opdracht door de cliënt zodat
de command server niet overbelast raakt.

- Samenwerken met Jaap om een protocol samen te stellen tussen client en server
De basis API is bestaat uit het versturen van het versturen van de rijen van de
eerste matrix en kolommen van de tweede matrix. Dan vermenigvuldigt de client
elke rij met elke kolom en stuurte de resultaten daarvan terug.

- Libraries uitzoeken voor gebruik in de client
Om vanuit Python HTTP requests te sturen naar een server is de requests library
het simpelst om te gebruiken. Het is ook ruimschoots uitgebreid genoeg voor de
features die wij nodig hebben. Voor het meten van het CPU gebruik is psutil de
meest gebruikelijk optie. Angezien we ook geen ingewikkelde metingen hoeven te
doen voor de CPU load heeft deze library genoeg functionaliteit.

### Week 3
- Vermenigvuldigen van rijen en kolommen in de in de vorm van de API
Omdat de client en de server naast elkaar worden ontwikkeld werd de client eerst
geimplementeerd met een vaste datastructuur gebaseerd op de afgesproken API.
Bij het maken van die datastructuur bleek er wat onnodige informatie expcliciet
meegegeven te worden. Dit is uit de API gehaald en de datastructuur is toen
gebaseerd op de vernieuwde API.

- Basis protocol naar server implementeren voor matrices
Het implementeren van het protocol was niet al te ingewikkeld. De requests
library voor Python is vrij simpel te gebruiken. In combinatie met de standaard
json module was het geen enkel probleem om json data te versturen naar de
server.

- Client cpu load bepalen en sturen naar de server
De CPU load moet gemeten worden in een apparte thread van het main programma,
aangezien er anders niet gemeten kan worden met vastgesteld interval. Een
interval is nodig zodat de server op de hoogte gesteld kan worden van de staat
van de client.

- Verminderen van de request overhead op de server
Nadat de communicatie tussen de client en server werkte bleek dat de elke
request toch een behoorlijke overhead had. Dit hebben we op een aantal verschillende
manieren verminderd. Een van de eerste dingen om de relatieve overhead te
verminderen was meer rijen en kolommen sturen per request. De overhead per
request gaat in principe lineair omhoog (r + k) en het werk dat de client kan
uitvoeren gaat kwadratisch omhoog (r * k)


### Week 4
- Verslag schrijven
