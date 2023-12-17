# BEE-TSP-Optimizer

(Da mehrere das TSP-Problem haben ist es höchst wahrscheinlich sinnlos das TSP im Allgemeinen nochmal zu erklären)

1. Grundlagen des Bienenalgorithmus (auch nur kurz erklärt, da andere das ja auch bestimmt haben)
2. Anpassung des Bienenalgorithmus an das TSP-Problem
3. Implementation (grober Aufbau)
4. Resultate (Demo)
5. Herausforderungen
6. Verbesserungsmöglichkeiten (?)

---

## Grundlagen des Bienalgorithmus

* Scout-Bienen (ns; durchsuchen zufällig den gesamten Raum/Umgebung)
* Von ns werden nb und ne Bienen rekrutiert
* Rekrutierte Bienen schauen nach Futterquellen (In der Nachbarschaft von bisherigen Lösungen; lokale Suche)
* Restliche Bienen suchen unabhängig von den bisherigen Lösungen nach besseren Lösungen (globale Suche)
* [Bild von dem Algorithmus einfügen]

## Anpassung des Bienenalgorithmus an das TSP-Problem

* Gegeben: TSP-Problem -> diskretes Problem
* Fragestellung: Was ist die Nachbarschaft einer Route?
* Idee: Zwei-Kanten-Tausch als Nachbarschaft einer Route
* Futterstelle -> gefundenen Routen
* ns -> Anzahl der Routen, die zufällig generiert werden

## Implementation

* Die Klasse `BeeTSP` erbt von der Klasse Bee.
* Sie hat eine __init__ Methode, die die Initialisierung der Klasse handhabt. Sie nimmt verschiedene Parameter wie ns, nb, ne, nrb, nre, iterations und inp entgegen. inp kann entweder die Länge der Route oder die Koordinaten sein.
* Die Methode eval berechnet die Gesamtdistanz einer gegebenen Route.
* Die Methode random erzeugt eine zufällige Route.
* Die Methode initialRandSolution initialisiert die Lösung mit zufälligen Routen.
* Die Methode randCoords erzeugt zufällige Koordinaten für die Städte.
* Die Methode evalDistances berechnet die Distanzen zwischen allen Städten.
* Die Methode mutate führt eine Mutation auf einer gegebenen Route durch, indem sie zwei zufällige Städte in der Route vertauscht.
* Die Methode eliteSearch führt eine Elite-Suche durch, bei der die besten Routen ausgewählt und mutiert werden, um möglicherweise bessere Routen zu finden.
* Die Methode bestSearch führt eine ähnliche Suche wie die Elite-Suche durch, aber auf den restlichen Routen (nicht den besten).
* Die Methode globalFill füllt den Rest der Bienenpopulation mit zufälligen Routen auf.
* Die Methode calculateBests sortiert die Bienenpopulation nach ihrer Fitness (Gesamtdistanz der Route).
* Die Methode visualize visualisiert die beste gefundene Route.
* Die Methode solve führt den gesamten Algorithmus aus, indem sie die oben genannten Methoden in einer bestimmten Reihenfolge aufruft.
