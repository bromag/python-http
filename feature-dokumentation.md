# Selenium HTTP Projekt – Feature-Dokumentation (mit Zeilennummern)

Basis: `myproject.py` (Zeilennummern gemäss `nl -ba myproject.py`)

## Feature-Übersicht (Tabelle)

| Command | Feature | Kurzbeschreibung | Datei | Zeilen (von–bis) |
|---|---|---|---|---|
| `title` | Title Scraping | Öffnet `index.html` und gibt den `<title>` aus (`driver.title`). | `myproject.py` | 84–90 |
| `get` | GET mit Variablen | Navigiert via Index zu GET und lädt `get.html?name=...&room=...`, liest `#result`. | `myproject.py` | 123–132 |
| `post` | Form Submission | Navigiert via Index nach `post.html`, füllt Inputs, klickt Submit, liest `#out`. | `myproject.py` | 138–149 |
| `list-cookies` | Cookies ausgeben | Navigiert via Index nach `cookies.html`, klickt `#set`, listet `driver.get_cookies()`. | `myproject.py` | 155–173 |
| `download` | Datei-Download | Klickt `#dl` auf `index.html`, wartet auf fertigen Download (stabile Dateigrösse). | `myproject.py` | 418–431 (+ Helper 400–415) |
| `checkbox` | Checkbox auswählen | Navigiert via Index nach `checkbox.html`, wählt `cb1` oder `cb2`, liest `#status`. | `myproject.py` | 179–192 |
| `dropdown` | Dropdown auswählen | Navigiert via Index nach `dropdown.html`, wählt Option in `<select id="drop">`, liest `#selected`. | `myproject.py` | 108–121 |
| `input` | Input-Test | Navigiert via Index nach `input.html`, setzt Text in `#txt`, klickt `#send`, liest `#echo`. | `myproject.py` | 199–212 |
| `slider` | Slider-Test | Navigiert via Index nach `slider.html`, setzt `#slider` per JS, liest `#value`. | `myproject.py` | 218–238 |
| `hover` | Hover-Test | Navigiert via Index nach `hover.html`, hovert über `#box`, prüft `#tooltip`. | `myproject.py` | 243–259 |
| `dragdrop` | Drag & Drop | Navigiert via Index nach `dragdrop.html`, simuliert HTML5 Drag&Drop (JS Events), liest `#result`. | `myproject.py` | 264–303 |
| `newwindow` | New Window/Tab | Navigiert via Index nach `newwindow.html`, öffnet neuen Tab/Fenster, wechselt und gibt `driver.title` aus. | `myproject.py` | 308–327 |
| `login` | Login-Test | Navigiert via Index nach `login.html`, füllt Credentials, klickt Login, liest `#result`. | `myproject.py` | 332–351 |
| `upload` | Upload-Test | Navigiert via Index nach `upload.html`, setzt Datei in `<input type=file>`, klickt `#show`, liest `#result`. | `myproject.py` | 378–395 |
| `keys` | Key Presses | Navigiert via Index nach `keys.html`, sendet Keys (Text + Pfeil runter), liest `#output`. | `myproject.py` | 356–373 |

## Technische Helper / Infrastruktur

| Komponente | Zweck | Datei | Zeilen (von–bis) |
|---|---|---|---|
| `make_driver(...)` | Startet Firefox + setzt Download-Preferences | `myproject.py` | 43–67 |
| `base_url(...)` | Basis-URL für lokalen Webserver | `myproject.py` | 73–78 |
| `go_from_index(...)` | Startpunkt Index + Navigation über Link-ID | `myproject.py` | 96–103 |
| `wait_for_download(...)` | Wartet auf fertigen Download (Dateigrösse stabil) | `myproject.py` | 400–415 |
| `parse_args()` | CLI-Argumente / Defaults | `myproject.py` | 434–462 |
| `main()` | Command-Dispatch / Ablaufsteuerung | `myproject.py` | 465–513 |

## Hinweise
- Die Tabelle referenziert nur `myproject.py`. Die zugehörigen HTML-Dateien liegen unter `web/`.
