# Deployment & Setup: Cooperative Project Tracking System

Diese Anleitung erklärt, wie du das Tracking-System für die Genossenschaftsprojekte in Betrieb nimmst.

## 1. Airtable Einrichtung

Erstelle zwei Tabellen in deiner Airtable-Base:

### Tabelle A: `Sources`
Diese Tabelle enthält die Übersichtsplattformen der Genossenschaften.
- **`Genossenschaft`**: Name (Single line text)
- **`URL`**: Link zur Projektübersicht (URL). 
  *   **Tipp**: Wenn Airtable AI dir ganzen Text statt nur die URL ausgibt, nutze diese Formel in einem Formel-Feld: 
    `REGEX_EXTRACT({DeinQuellFeld}, "https?://[^\\s]+[^.,;\\s]")`

### Tabelle B: `Projects`
Hier speichert der Crawler die einzelnen Bauvorhaben.
- **`Project Name`**: Name des Projekts (Single line text)
- **`Cooperative`**: Name der Genossenschaft (Single line text)
- **`Status`**: Status (Single select: `Planning`, `Construction`, `Rental`, `Completed`)
- **`Construction Start`**: Baustart (Single line text / Date)
- **`Move-in Date`**: Bezugstermin (Single line text / Date)
- **`Rental Start`**: Vermietungsstart (Single line text)
- **`Source URL`**: Link zum Projekt (URL)
- **`Last Update`**: Zeitpunkt der letzten Prüfung (Date/Time)

> [!IMPORTANT]
> **Airtable "Update" Hinweis**: Wenn du einen Datensatz aktualisieren willst, benötigt n8n die **Record ID** (beginnt mit `rec...`). Die URL des Projekts reicht hierfür nicht aus. Du musst den Datensatz erst suchen ("Search"), um die ID zu erhalten, oder sie mitspeichern.

---

## 2. Coolify Konfiguration

### Umgebungsvariablen (Variables)
Hinterlege folgende Werte in deinem Coolify-Service:
- `AIRTABLE_API_KEY`: Dein Personal Access Token von Airtable.
- `AIRTABLE_BASE_ID`: Die ID deiner Base (findest du in der Airtable API-Dokumentation).

### Docker-Setup
Das System nutzt das vorhandene `Dockerfile`. Nutze `/home/gravity-test/gnossiZH/Projekte` als Source-Pfad.

---

## 3. Automatisierung

Um den Crawler täglich laufen zu lassen:

### n8n (Optional)
Erstelle einen Workflow mit einer **Cron Node** (z.B. täglich 04:00 Uhr). Diese triggert entweder:
- Einen Webhook in Coolify, um den Service zu starten.
- Einen SSH-Befehl: `docker exec <container_id> python track_projects.py`

### Coolify Cron (Direkt)
Hinterlege in den Service-Einstellungen einen "Scheduled Job" oder Cron-Eintrag für:
`python track_projects.py`

### n8n Tipps für Regex & Prompts

Wenn du n8n nutzt, um die Daten vorzufiltern:

#### In einer n8n Expression (JavaScript):
Nutze diesen Ausdruck, um Fehler bei leeren Feldern zu vermeiden:
`{{ $json.text.match(/https?:\/\/\S+[^.,;\s]/) ? $json.text.match(/https?:\/\/\S+[^.,;\s]/)[0] : "" }}`

#### Im LLM-Prompt (n8n OpenAI/Anthropic Node):
Anstatt Regex zu nutzen, gib der KI eine klare Anweisung:
> "Extrahiere die URL der Projektübersicht aus dem folgenden Text. Gib **nur** die nackte URL zurück. Falls keine URL gefunden wird, gib einen leeren String zurück."

---

## 4. Lokaler Test
Du kannst das Skript jederzeit manuell testen:
```bash
python track_projects.py
```
*(Hinweis: Im aktuellen "Test-Modus" wird nur die erste Genossenschaft gescannt, um Ressourcen zu sparen. Entferne `test_mode=True` im Skript für den Live-Betrieb).*
