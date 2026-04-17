# Anweisungen für Gemini

- Alle Informationen, die du erhältst, speicherst du bitte nur im Kurzzeitgedächtnis und als .md-Dateien in diesem Ordner ab.
- Die Informationen zu meinem Startup gnossiZH sind in den folgenden Dateien aufgeteilt, um sie bei Bedarf erweitern zu können:
  - [[Produkt.md]]
  - [[Marketingstrategie.md]]
  - [[Datenquellen.md]]

## Master CSV to Markdown Converter

Im Ordner `gnossizh-ai` befindet sich ein Master-Skript namens `master_csv_to_md.py`.
Dieses Skript dient dazu, beliebige CSV-Dateien in einzelne Markdown-Dateien umzuwandeln.

### Anpassung des Skripts

Das Skript ist so konzipiert, dass es leicht anpassbar ist. Öffne die Datei `master_csv_to_md.py` und ändere die Werte im Abschnitt `--- CONFIGURATION ---`:

1.  **`CSV_FILE_PATH`**: Gib den Pfad zur CSV-Quelldatei an.
2.  **`OUTPUT_DIR_CONFIG`**: Definiere, in welchen Ordner die `.md`-Dateien gespeichert werden sollen. Du kannst einen Wert aus einer Spalte (`mapping_column`) verwenden, um die Dateien auf verschiedene Ordner (`directories`) zu verteilen.
3.  **`FILENAME_COLUMN`**: Lege fest, welche Spalte der CSV-Datei als Basis für den Dateinamen verwendet werden soll.
4.  **`CONTENT_STRUCTURE`**: Bestimme die Struktur und den Inhalt der Markdown-Dateien. Du kannst Titel, Eigenschaften, Trennlinien und den Hauptinhalt (`raw`) aus verschiedenen Spalten zusammensetzen.

Führe das Skript nach der Konfiguration aus, um die Markdown-Dateien zu erstellen.
