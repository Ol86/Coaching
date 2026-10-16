# Garmin-Output

Dieser Ordner enthält die wöchentlichen JSON-Zusammenfassungen, die durch
[`coaching`](../src/coaching/) aus Garmin Connect erzeugt werden.

## Dateinamen

Pro Ausführung wird eine Datei für die aktuelle ISO-Kalenderwoche geschrieben:

```text
Summary_KW<kalenderwoche>.json
```

Beispiel: `Summary_KW42.json`.

Die Datei wird relativ zum Projektverzeichnis geschrieben. Ein erneuter Lauf
innerhalb derselben Kalenderwoche überschreibt die vorhandene Datei.

## Inhalt

Eine Zusammenfassung hat diese Struktur:

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

### Felder

- `current_week`: ISO-Kalenderwochennummer.
- `monday_of_current_week`: Wochenbeginn im Format `YYYY-MM-DD`.
- `sunday_of_current_week`: Wochenende im Format `YYYY-MM-DD`.
- `garmin_data.sleep_data`: von Garmin Connect gelieferte tägliche
  Schlafdaten.
- `garmin_data.hrv_data`: HRV-Zusammenfassungen der Woche.
- `garmin_data.activities`: Aktivitäten der Woche.

Die Einträge in den drei Datenfeldern werden unverändert aus der
Garmin-Connect-API übernommen. Die genaue Struktur kann deshalb je nach
Garmin-Datentyp und API-Version variieren.

## Erzeugung

Die Dateien werden automatisch mit folgendem Kommando erstellt:

```powershell
uv run coaching
```

Das Programm fragt die Daten von Montag bis Sonntag der aktuellen Woche ab.
Wenn Garmin Connect für einen Datentyp keine Daten liefert, wird dafür eine
leere Liste gespeichert und eine Warnung ausgegeben.

Weitere Informationen zu Einrichtung, Anmeldung und Fehlerbehebung stehen in
der [Projekt-README](../README.md).

## Umgang mit den Dateien

Die JSON-Dateien können für Analysen, Visualisierungen oder eine spätere
Trainingsplan-Logik weiterverwendet werden. Sie können sensible Gesundheits-
und Aktivitätsdaten enthalten und sollten daher nicht ungeschützt geteilt
oder in ein öffentliches Repository hochgeladen werden.
