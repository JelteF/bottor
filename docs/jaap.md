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

### Verricht werk

#### Week 2
Bedacht hoe de structuur er aan de serverside uit moet komen te zien. Gekozen is
voor een splitsing van jobs en tasks. Een job is een matrix multiplicatie. Bij
een request van een client wordt een task (een deeltaak) uit de job gegenereerd
en aan de client gegeven. De TASK_SIZE is te setten in de Constants file. Deze
week ben ik begonnen met een niet zo efficiente opzet. Dit met het oog omdat er
snel wat werkends moet staan waar Jelte en Abe mee kunnen communiceren. Niet zo
efficient is: elke matrix wordt bij een update naar file geschreven, en altijd
uit file gelezen. Dit is natuurlijk geen snelle implementatie, dit moet later
veranderd worden.
Ook ben ik deze week bezig geweest met me weer verdiepen in het Flask framework
dat we gebruiken. Deze heb ik in het verleden een keer eerder gebruikt (Project
Software Engineering), dus het is weer even wennen.

#### Week 3
Maandagavond was, zoals beloofd aan mijn groepsgenoten, de basisstructuur van de
taskmanager af. Inlezen van matrices, een task uitlezen uit de eerste job met
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
structuur en kleine bugs op te lossen. Ook heb ik de support voor meerdere jobs
in een queue toegevoegd, plus de detectie van inactieve clients. Zo worden de
eerste jobs als eerst afgehandeld. Wanneer een job voltooid is wordt de
resultmatrix naar file geschreven en de matrices uit geheugen gehaald.

#### Week 4

