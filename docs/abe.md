Abe
===

## Hoofdtaak = Web gedeelte van de server

## week 2
* opzetten framework voor webserver

## week 3
* maken van webpagina's voor administratie en overzicht
* interfacing met andere onderdeel van webserver (jaap)

### Week 4
- Verslag schrijven

### Verricht werk

#### Week 2
In de eerste week een grote hoeveelheid code gereed gemaakt voor gebruik binnen
dit nieuwe project, het is ondertussen de 5e keer dat ik gebruik maak van de
weblibrary flask voor python dus stond de server-basis voor ons project als een
huis. We kozen opnieuw voor flask binnen python omdat in python vrijwel alles
mogelijk is en de learning-curve niet heel hoog is. Ook kwamen we tot deze
keuze uit de literatuurstudie over botnets die net zoals wij nu vaak het
internetprotocol gebruiken om firewalls te ontwijken. Voor ons is dat
natuurlijk minder van toepassing omdat wij een vriendelijke variant van een
botnet maken.

#### Week 3
Omdat maandag het framework al helemaal klaarstond om gevuld te worden kon ik
voorspoedig aan de gang met de webpagina's voor netbot, de naam die over het
weekend ontstond. Ik begon met de layout van het systeem dat duurde wel een
half dagje en nadat dat klaar was begon ik met de status pagina. De status
haalt de peers op uit de database waarin staat welke job op de peer draait,
hoeveel de peer aan cpupower gebruikt, of de peer active is en de ip-locatie
van de peer.
Om ervoor te zorgen dat die data beschikbaar is heb ik met jelte daarvoor het
protocol doorgenomen. Eerst begonnen we met een handshake, vervolgens doet de
client een request om een task te ontvangen van de server, als die task is
ontvangen begint de client met het pingen van de server met zijn status.

Vervolgens begon ik aan het matrix gedeelte van de website, op deze pagina
moeten nieuwe matrices aangeleverd kunnen worden aan de server die vervolgens
gebruikt kunnen worden in een job. Dit betekende interfacing met jaap, die op
de server verantwoordelijk was voor de verdeling van matrices. Ik maakte een
API aan en een Controller voor het Matrix model dat reeds door hem geschapen
was. API haalde simpelweg alle entries op uit de database, maar dit betekende
dat je ook de taskmatrix kon zien, een matrix die alleen gedurende de job
gebruikt wordt om bij te houden welke tasks voltooid waren. Die moesten we er
natuurlijk niet tussen hebben dus maakte ik in het database model, na overleg
met jaap, een type aan. Ik onderscheidde 3 types: data, task, result. Op deze
manier kon ik gemakkelijk alleen de data matrices laden op de webpagina.

Na dit gedaan te hebben kwam ik tot een conclusie, dat de opdeling van matrices
niet adequaat was. Ik besloot de manier waarop matrices in het geheugen werden
geladen aan te pakken. Na het weekend van week 3 had ik dit voltooid en kon ik
verder gaan met de matrices pagina.

#### Week 4
Aan de matrices pagina moest nog de fileupload van nieuwe data matrices
toegevoegd worden, en aan het begin van week vier was dit voltooid.
Omdat ik heb webprogrammeren veel werk vond vroeg ik aan Jelte of hij een
pagina aan kon maken die nieuwe jobs kan maken. Jelte die geenszins in
tijdsgebrek zat ging hier mee akkoord en leverde diezelfde dag nog resultaat.
Een pagina waarop je nieuwe jobs kon maken.

Omdat er nog geen pagina was om de aangemaakte jobs te zien ging ik vervolgens
daarmee aan de slag. Jelte wees me er enigszins terecht op dat ik de pagina
niet volledig dynamisch hoefde te implementeren dus maakte ik geen gebruik van
de database interactie library backbone. Die ik voor de matrix pagina wel
gebruikte, als ik verder ga met dit project ga ik dit alsnog wel doen. Dit
omdat ik de manier van implementatie erg aestetisch.
