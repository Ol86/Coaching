# Coaching

Kleines Python-CLI zum Abrufen von Trainings- und Gesundheitsdaten aus
Garmin Connect. Bei jedem Lauf werden die Daten der aktuellen Kalenderwoche
abgerufen und als JSON-Datei in [`garmin_output/`](./garmin_output/) abgelegt.

## Funktionsumfang

Das Programm ruft für Montag bis Sonntag der aktuellen Kalenderwoche ab:

- tägliche Schlafdaten,
- HRV-Zusammenfassungen (Heart Rate Variability),
- aufgezeichnete Aktivitäten.

Die Daten werden nicht verändert oder bewertet. Eine Trainingsplan- oder
Coaching-Logik ist derzeit noch nicht enthalten.

## Voraussetzungen

- Python 3.14 oder neuer
- [uv](https://docs.astral.sh/uv/) für Installation und Ausführung
- ein Garmin-Connect-Konto mit Zugriff auf die gewünschten Daten

Die erwartete Python-Version ist zusätzlich in [`.python-version`](./.python-version)
festgelegt.

## Installation

Im Projektverzeichnis:

```powershell
uv sync
```

Damit werden die Projektabhängigkeiten und die virtuelle Umgebung
`.venv/` eingerichtet.

## Ausführung

Das CLI aus dem Projektverzeichnis starten:

```powershell
uv run coaching
```

Alternativ kann das Modul in der aktivierten virtuellen Umgebung über den
installierten Befehl `coaching` ausgeführt werden.

Beim ersten Start werden Benutzername und Passwort interaktiv abgefragt. Das
Passwort wird nicht als Klartext eingegeben, sondern über eine geschützte
Eingabe gelesen.

## Garmin-Authentifizierung

Die Garmin-Sitzung wird im Verzeichnis [`.garminconnect/`](./.garminconnect/)
gespeichert:

1. Existiert das Verzeichnis noch nicht, fragt das Programm nach den
   Zugangsdaten und legt anschließend einen Token-Store an.
2. Bei späteren Läufen wird der gespeicherte Token verwendet.
3. Ist der Token ungültig oder kann keine Verbindung hergestellt werden,
   fordert das Programm erneut Zugangsdaten an.

Der Token-Store enthält sensible Authentifizierungsdaten. Er darf nicht
committet, geteilt oder in Logs veröffentlicht werden. Bei Problemen mit der
Anmeldung kann der Token-Store gelöscht und die Anmeldung anschließend erneut
durchgeführt werden.

## Ausgabe

Für die aktuelle Kalenderwoche wird eine Datei nach folgendem Muster erzeugt:

```text
garmin_output/Summary_KW<kalenderwoche>.json
```

Beispiel:

```text
garmin_output/Summary_KW42.json
```

Die Datei enthält unter anderem:

```json
{
    "current_week": 42,
    "monday_of_current_week": "2026-10-12",
    "sunday_of_current_week": "2026-10-18",
    "garmin_data": {
        "sleep_data": [],
        "hrv_data": [],
        "activities": []
    }
}
```

Die Listen enthalten die von Garmin Connect gelieferten Originalobjekte.
Wenn für einen Datentyp keine Daten vorhanden sind, wird eine leere Liste
geschrieben und eine Warnung protokolliert. Bereits vorhandene Dateien für
dieselbe Kalenderwoche werden überschrieben.

Details zum Ausgabeordner und zum JSON-Format stehen in
[`garmin_output/README.md`](./garmin_output/README.md).

## Projektstruktur

```text
.
├── src/coaching/
│   ├── __init__.py             # CLI-Einstiegspunkt
│   ├── garmin.py               # Wochenabfrage und JSON-Ausgabe
│   └── garmin_connection.py    # Garmin-Authentifizierung und Verbindung
├── garmin_output/              # erzeugte Wochenzusammenfassungen
├── pyproject.toml              # Projekt- und Abhängigkeitsdefinition
├── uv.lock                     # reproduzierbar aufgelöste Versionen
└── .python-version             # erwartete Python-Version
```

## Hinweise zur Fehlerbehebung

- **Anmeldung schlägt fehl:** Internetverbindung prüfen und den Token-Store
  entfernen, damit beim nächsten Lauf eine neue Anmeldung erfolgt.
- **Zu viele Anfragen:** Einige Zeit warten und das Programm nicht wiederholt
  in kurzer Folge starten.
- **Keine Daten:** Garmin Connect kann für die aktuelle Woche noch keine
  Einträge liefern; die Ausgabe bleibt trotzdem gültiges JSON.
- **Keine Ausgabedatei:** Das Kommando aus dem Projektverzeichnis starten,
  da Ausgabe- und Token-Pfade relativ zum aktuellen Arbeitsverzeichnis sind.

## Entwicklungsstatus

Das Projekt befindet sich in einer frühen Entwicklungsphase. Tests,
automatisierte Datenvalidierung und die eigentliche Trainingsplanerstellung
folgen noch.