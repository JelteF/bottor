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
features die wij nodig hebben.

### Week 3
- Vermenigvuldigen van rijen en kolommen in de in de vorm van de API
Omdat de client en de server naast elkaar worden ontwikkeld werd de client eerst
geimplementeerd met een vaste datastructuur gebaseerd op de afgesproken API.
Bij het maken van die datastructuur bleek er wat onnodige informatie expcliciet
meegegeven te worden. Dit is uit de API gehaald en de datastructuur is toen
gebaseerd op de vernieuwde API.

- Basis protocol naar server implementeren voor matrices
Het implementeren van het protocol was niet al te ingewikkeld. De requests
library voor Python is vrij simpel.

- Client cpu load bepalen
- Client cpu load sturen naar de server

- Verminderen van de request overhead op de server

### Week 4
- Verslag schrijven
