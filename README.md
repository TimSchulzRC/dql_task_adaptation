Die Simulation, mit der die Daten für das KT-Modell-Training generiert wurden befindet sich in der Datei "simulation/simulation.ipynb". Im selbigen Verzeichnis befindet sich der Code mit dem die Modelle trainiert wurden jeweils in einem eigenen Unterverzeichnis. Zudem ist in diesem Ordner der generierte Datensatz als CSV-Date zu finden.

Mit dem Code im Verzeichnis "assistments" wurden die Modelle mit dem Skill-builder-Datensatz trainiert.

Die Modell-Trainings können geführt werden, indem zuerst das Notebook "prepare_dataset.ipynb" im jeweiligen Ordner vollständig von oben nach unten ausgeführt wird. Danach kann jeweils das Notebook "{modellname}.ipynb" vollständig von oben nach unten ausgeführt werden, um die Modelle zu trainieren.

Der Code für die Anwendung des DKT-Modells befindet sich im Notebook "test_trained_model.ipynb".

Alle Notebooks können mit der Python Umgebung im Verzeichnis ".venv" ausgeführt werden.
