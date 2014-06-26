Jaap
====

### Hoofdtaak = Scheduling/TaskManager serverside

#### Week 2
* Uitzoeken hoe de workload te verdelen
* Opzetten basis/structuur TaskManager/Distributor
* Protocol/API structuur bedenken en vastleggen met Jelte

#### Week 3
* API werkend (icm client-side van Jelte)
* Interface met Abe rond krijgen
* TaskManager/Workload distributor uitbreiden met functionaliteit
* Performance improvement

#### Week 4
* Puntjes op de i zetten
* Verslag

### Verricht werk/LabReport

#### Week 2
Bedacht hoe de structuur er aan de serverside uit moet komen te zien. Gekozen is
voor een splitsing van jobs en tasks. Een job is een matrix multiplicatie. Bij
een request van een client wordt een task (een deeltaak) uit de job gegenereerd
en aan de client gegeven. De TASK_SIZE is te setten in de Constants file, dit
staat voor het aantal rijen en kolommen dat opgestuurd wordt naar een client.
(Een TASK_SIZE van 3 betekent dat er 3 rijen en 3 kolommen opgestuurd worden
naar de client, resulterende in 9 entries van de resultmatrix. Deze
week ben ik begonnen met een niet zo efficiente opzet. Dit met het oog op het
feit dat er
snel wat werkends moet staan waar Jelte en Abe mee kunnen communiceren. Niet zo
efficient is: elke matrix wordt bij een update naar file geschreven, en altijd
uit file gelezen. Dit is natuurlijk geen snelle implementatie, dit moet later
veranderd worden.
Ook ben ik deze week bezig geweest met me weer verdiepen in het Flask framework
dat we gebruiken. Deze heb ik in het verleden een keer eerder gebruikt (Project
Software Engineering), dus het is weer even wennen. Gaandeweg raak ik weer bij
in het Flask framework, en aan het eind van de week zit ik er weer helemaal in.
Bij het bouwen van de verschillende onderdelen besteed ik direct aandacht aan
het schrijven van enkele unittests voor de afzonderlijke onderdelen, zodat
eventuele malfunctie direct op te sporen is, en dit niet bij het samenvoegen van
onderdelen met Jelte en Abe aan het licht komt. Tot nu toe blijkt dit een goede
keuze te zijn, want door de complexiteit sluipen er kleine, moeilijk op te
sporen foutjes op. De unittest helpt hier goed bij. Het kost een halfuurtje
extra om de tests te schrijven, maar aan het eind scheelt het je uren debuggen.

#### Week 3
Maandagavond was, zoals beloofd aan mijn groepsgenoten, de basisstructuur van de
taskmanager af. Van het weekend wat extra werk verricht, omdat het een tamelijk
grote taak betrof die toch even af moest zodat Abe en Jelte ermee konden werken.
Inlezen van matrices, een task uitlezen uit de eerste job met
nog niet aan andere clients toegewezen berekeningen, resultaten ontvangen en
terugschrijven. Zoals gezegd was het Flask framework weer even wennen, maar de
structuur en bijbehorende API werkt. We komen er begin deze week direct achter
dat het lezen en schrijven naar files bij elke request veel overhead geeft
(zoals verwacht), dus het plaatsen van de matrices in het geheugen is nu van
hoogste prioriteit. Jelte, met meer Flask ervaring, vertelt dat objecten in
Flask gewoon in geheugen blijven staan tijdens de Flask sessie, dus ik gooi de
boel om en zet de matrices in een dictionary in het Matrix object op hun id.
Inmiddels is het al woensdag eind van de dag. De rest van de week ben ik met
Jelte bezig geweest allerhande verbeteringen aan te brengen in de serverside
structuur en kleine bugs op te lossen. De aangebrachte verbeteringen zijn
voornamelijk op het gebied van geheugen: Hoeveel I/O requests zijn er nodig om
een matrix te laden of resultaten op te slaan? Zoals boven al vermeld worden de
matrices waarmee gewerkt wordt standaard in het geheugen geladen, totdat de job
voltooid is. Een andere bron van onnodige overhead vonden we in het opsturen van
de matrices. Een matrix wordt uitgelezen uit een tekstbestand, waardoor de
entries van de matrix ingelezen worden als strings. Hierna werden ze in
2-dimensionale arrays gezet als floats, maar bij het verzenden in JSON-formaat
worden ze weer omgezet in strings. Aan de client-side worden ze vervolgens weer
uitgepakt en geconverteerd naar floats. Het is dus vrij nutteloos aan de
server-side floats te gebruiken, en de conversie van string naar float en van
float naar string bracht een merkbare vertraging teweeg bij elke request.
Ook heb ik de support voor meerdere jobs
in een queue toegevoegd, plus de detectie van inactieve clients. Zo worden de
eerste jobs als eerst afgehandeld. Wanneer een job voltooid is wordt de
resultmatrix naar file geschreven en de matrices uit geheugen gehaald.

#### Week 4
Maandag ben ik deels bezig geweest met de poster. De verdere maandag en de
dinsdag ben ik bezig geweest met het doorlopen van de code en het testen van de
resultaten. Er zijn de laatste dagen flink wat aanpassingen gemaakt aan de code
waardoor sommige dingen niet meer werkten zoals het hoorde. Zo was de uitkomst
van een A x B vermenigvuldiging de uitkomst van de A x B^Transpose
vermenigvuldiging. Verder werd de job nooit op voltooid gezet, en werd de
resultmatrix zodoende nooit weggeschreven. De dinsdag en de woensdag ben ik
bezig geweest met deze codingfoutjes op te sporen en te repareren.
