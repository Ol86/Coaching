# Garmin-Connect-Token-Store

Dieser Ordner enthält die lokal gespeicherten Sitzungsdaten für die
Anmeldung bei Garmin Connect. Das Programm verwendet diese Daten, damit bei
jedem Lauf nicht erneut Benutzername und Passwort eingegeben werden müssen.

## Inhalt

Die Datei `garmin_tokens.json` wird automatisch von der Garmin-Connect-
Bibliothek angelegt oder aktualisiert. Sie enthält sensible
Authentifizierungsdaten und darf nicht gelesen, geteilt oder in ein
öffentliches Repository hochgeladen werden.

Die Datei ist im Projekt bereits durch die `.gitignore` ausgeschlossen.
Diese README-Datei bleibt dagegen absichtlich versionierbar, damit der Zweck
des Ordners dokumentiert ist.

## Verwendung

Normalerweise ist keine manuelle Aktion erforderlich. Starte das Programm aus
dem Projektverzeichnis:

```powershell
uv run coaching
```

Wenn noch kein Token-Store vorhanden ist, fragt das Programm interaktiv nach
den Garmin-Connect-Zugangsdaten. Bei späteren Läufen wird der gespeicherte
Token wiederverwendet.

## Erneute Anmeldung erzwingen

Wenn die Anmeldung dauerhaft fehlschlägt oder der gespeicherte Token
ungültig geworden ist, kann `garmin_tokens.json` gelöscht werden. Beim
nächsten Lauf wird eine neue Anmeldung angefordert.

```powershell
Remove-Item .garminconnect\garmin_tokens.json
uv run coaching
```

Die Datei nur löschen, wenn das Programm nicht gleichzeitig läuft.

## Sicherheit

- Den Inhalt von `garmin_tokens.json` niemals in Issues, Logs, Screenshots
  oder Chat-Nachrichten einfügen.
- Den Token-Store nicht in Backups oder öffentliche Artefakte übernehmen.
- Falls Token versehentlich veröffentlicht wurden, die Garmin-Connect-
  Sitzung widerrufen beziehungsweise das Passwort ändern und anschließend
  einen neuen Token-Store erzeugen.

Weitere Informationen zur Einrichtung und zum Abruf der Daten stehen in der
[Projekt-README](../README.md).
