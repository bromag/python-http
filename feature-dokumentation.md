# Selenium HTTP Projekt – Feature-Dokumentation

Diese Dokumentation listet alle umgesetzten Features (Tests) in einer Tabelle auf.  
Die exakten Zeilennummern in `myproject.py` können je nach Version variieren.

**Zeilennummern ermitteln**
```bash
nl -ba myproject.py | grep -n "def cmd_"
```

## Feature-Übersicht (Tabelle)

| Command | Feature | Kurzbeschreibung | Testseite(n) | Output/Prüfung |
|---|---|---|---|---|
| `title` | Title Scraping | Öffnet `index.html` und gibt den `<title>` aus (`driver.title`). | `web/index.html` | Terminal: Titeltext |
| `get` | GET mit Variablen | Ruft `get.html?name=...&room=...` auf und liest `#result`. | `web/get.html` | Terminal: Inhalt von `#result` |
| `post` | Form Submission | Navigiert via Index nach `post.html`, füllt Inputs und klickt Submit, liest `#out`. | `web/post.html` | Terminal: Inhalt von `#out` |
| `list-cookies` | Cookies ausgeben | Navigiert via Index nach `cookies.html`, klickt `#set`, listet `driver.get_cookies()`. | `web/cookies.html` | Terminal: Cookies (name=value, domain, path) |
| `download` | Datei-Download | Klickt `#dl` auf `index.html`, wartet bis Datei im Download-Ordner stabil ist. | `web/index.html`, `web/files/*` | Terminal: `OK: downloaded ...` |
| `checkbox` | Checkbox auswählen | Navigiert via Index nach `checkbox.html`, wählt `cb1` oder `cb2`, liest `#status`. | `web/checkbox.html` | Terminal: Inhalt von `#status` |
| `dropdown` | Dropdown auswählen | Navigiert via Index nach `dropdown.html`, wählt Option im `<select id="drop">`, liest `#selected`. | `web/dropdown.html` | Terminal: Inhalt von `#selected` |
| `input` | Input-Test | Navigiert via Index nach `input.html`, schreibt Text in `#txt`, klickt `#send`, liest `#echo`. | `web/input.html` | Terminal: Inhalt von `#echo` |
| `slider` | Slider-Test | Navigiert via Index nach `slider.html`, setzt Range-Input `#slider`, liest `#value`. | `web/slider.html` | Terminal: Inhalt von `#value` |
| `hover` | Hover-Test | Navigiert via Index nach `hover.html`, hovert über `#box`, prüft `#tooltip`. | `web/hover.html` | Terminal: `tooltip_displayed=... text=...` |
| `dragdrop` | Drag & Drop | Navigiert via Index nach `dragdrop.html`, zieht `#source` auf `#target`, liest `#result`. | `web/dragdrop.html` | Terminal: Inhalt von `#result` |
| `newwindow` | New Window/Tab | Öffnet `newwindow.html`, klickt Link mit `target=_blank`, wechselt Fenster, prüft Inhalt, schliesst und geht zurück. | `web/newwindow.html`, `web/popup.html` | Terminal: Popup-Titel/H1 + Back-to-Titel |
| `login` | Login-Test | Navigiert zu `login.html`, füllt Username/Password, klickt Login, liest `#result`. | `web/login.html` | Terminal: `result=OK/FAIL` |
| `upload` | Upload-Test | Navigiert zu `upload.html`, setzt Datei in `<input type=file>`, klickt `#show`, liest `#result`. | `web/upload.html` | Terminal: `result=FILE:...` |
| `keys` | Key Presses | Navigiert zu `keys.html`, sendet Tasten an Input, liest `#last`. | `web/keys.html` | Terminal: z. B. `last=Enter` |

## Benötigte IDs in `index.html` (Navigation)
Empfohlen, damit alle Tests vom Index aus starten können:

- `nav-get`, `nav-post`, `nav-cookies`, `nav-checkbox`, `nav-dropdown`, `nav-input`, `nav-slider`, `nav-hover`, `nav-dragdrop`, `nav-newwindow`, `nav-login`, `nav-upload`, `nav-keys`
- Download-Link: `dl`

## Hinweise für die Bewertung
- Für die Abgabe ist es hilfreich, pro Command einen Terminal-Output (Screenshot oder Copy/Paste) beizulegen.
- Für Zeilennummern: `nl -ba myproject.py | grep -n "def cmd_"` verwenden.
