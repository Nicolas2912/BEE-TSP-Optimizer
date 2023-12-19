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

* Die Klasse `BeeTSP` erbt von der Klasse `Bee`.
* Berechnung der Gesamtdistanz mit eval.
* Erzeugung einer zufälligen Route mit random.
* Initialisierung der Lösung mit initialRandSolution.
* Erzeugung zufälliger Städtekoordinaten mit randCoords.
* Berechnung der Distanzen zwischen Städten mit evalDistances.
* Durchführung einer Mutation mit mutate.
* Durchführung einer Elite-Suche mit eliteSearch.
* Durchführung einer besten Suche mit bestSearch.
* Füllung der Bienenpopulation mit globalFill.
* Sortierung der Bienenpopulation mit calculateBests.
* Visualisierung der besten Route mit visualize.
* Ausführung des gesamten Algorithmus mit solve.

### Efiziente Implementation in Matlab

* ...

## Resultate

* Code live ausführen
* Wahl der Parameter
* Auf eventuelle Besonderheiten eingehen (lokale Minima, Zeit etc.)

## Verbesserungsmöglichkeiten

* Parameter optimieren
