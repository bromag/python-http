#!/usr/bin/env python3
# ^ Shebang: erlaubt das Script direkt auszuführen (z.B. ./selenium-http.py),
#   falls die Datei ausführbar ist und Python3 vorhanden ist.

import argparse
# ^ Für Command-Line-Argumente wie: "title", "get", "--name", "--headless"

import os
# ^ Für Dateisystem-Operationen (Download-Ordner erstellen, absolute Pfade)

import sys
# ^ Für Fehlerausgaben (stderr) und Exit-Codes (sys.exit)

import time
# ^ Für kurze Wartezeiten (sleep), damit JS auf der Seite Zeit hat, Output zu schreiben

from pathlib import Path
# ^ Für einfache Pfadmanipulationen (z.B. Path("downloads") / "test.txt")

from urllib.parse import urlencode
# ^ Baut aus einem Dictionary einen URL-Querystring:
#   {"name":"X","room":"Y"} -> "name=X&room=Y"

from selenium import webdriver
# ^ Selenium WebDriver: steuert den Browser (Firefox) automatisiert.

from selenium.webdriver.common.by import By
# ^ "By" definiert, wie Elemente gefunden werden (By.ID, By.NAME, By.CSS_SELECTOR, ...)

from selenium.webdriver.firefox.options import Options
# ^ Firefox-spezifische Browser-Optionen (headless, Fenstergrösse, etc.)


def make_driver(headless: bool, download_dir: str) -> webdriver.Firefox:
    os.makedirs(download_dir, exist_ok=True)

    opts = Options()
    if headless:
        opts.add_argument("--headless")
    opts.add_argument("--width=1200")
    opts.add_argument("--height=900")

    # Download-Verhalten (ohne FirefoxProfile)
    opts.set_preference("browser.download.folderList", 2)
    opts.set_preference("browser.download.dir", os.path.abspath(download_dir))
    opts.set_preference("browser.download.useDownloadDir", True)
    opts.set_preference("browser.helperApps.alwaysAsk.force", False)

    # PDF ohne Nachfrage speichern
    opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

    # Optional: PDF Viewer deaktivieren (damit es wirklich downloaded statt angezeigt wird)
    opts.set_preference("pdfjs.disabled", True)

    # Optional: Download-UI nicht anzeigen
    opts.set_preference("browser.download.manager.showWhenStarting", False)

    return webdriver.Firefox(options=opts)


def base_url(port: int) -> str:
    """
    Baut die Basis-URL zu deinem lokalen Webserver.
    Beispiel: port=8000 -> http://127.0.0.1:8000
    """
    return f"http://127.0.0.1:{port}"


def cmd_title(driver: webdriver.Firefox, url: str) -> None:
    """
    Feature: Scraping eines HTML-Tags.
    Wir öffnen die Seite und lesen den <title>-Text via driver.title aus.
    """
    driver.get(url)         # Öffnet URL im Browser
    print(driver.title)     # Gibt den <title> der Seite aus


def cmd_get(driver: webdriver.Firefox, url: str, name: str, room: str) -> None:
    """
    Feature: GET Request mit Variablen.
    Wir hängen Query-Parameter an die URL an und lesen den Text aus dem <div id="result">.
    """
    # Querystring generieren: name=...&room=...
    qs = urlencode({"name": name, "room": room})

    # Seite mit Query-Parametern öffnen (GET)
    driver.get(f"{url}?{qs}")

    # Element finden, in das die Seite das Ergebnis schreibt (via JavaScript)
    el = driver.find_element(By.ID, "result")

    # Text ausgeben, z.B.: "name=Giuliano, room=A101"
    print(el.text)


def cmd_post(driver: webdriver.Firefox, url: str, user: str, msg: str) -> None:
    """
    Feature: POST / Form Submission mit Variablen.
    Unsere Testseite hat ein Formular. Selenium füllt die Inputs und klickt auf Submit.
    Danach lesen wir den Output aus <pre id="out">.
    """
    driver.get(url)  # POST-Demo-Seite öffnen

    # Formularfelder anhand ihres "name"-Attributs finden und Werte eintragen
    driver.find_element(By.NAME, "user").send_keys(user)
    driver.find_element(By.NAME, "msg").send_keys(msg)

    # Submit-Button finden (CSS Selector) und klicken
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Kurze Wartezeit, damit das JavaScript Zeit hat, den Output zu rendern
    time.sleep(0.1)

    # Output-Element finden und den Text ausgeben
    out = driver.find_element(By.ID, "out")
    print(out.text)


def cmd_list_cookies(driver: webdriver.Firefox, url: str) -> None:
    """
    Feature: Cookies ausgeben.
    Unsere Cookies-Demo-Seite setzt Cookies per Button-Klick.
    Selenium liest danach alle Cookies aus und gibt sie aus.
    """
    driver.get(url)  # Cookies-Demo-Seite öffnen

    # Button klickt JS an, das Cookies setzt (z.B. session_id, theme)
    driver.find_element(By.ID, "set").click()

    # Kurzes Delay, damit Cookie-Setzen sicher abgeschlossen ist
    time.sleep(0.1)

    # Cookies aus dem Browser auslesen (Liste von Dictionaries)
    cookies = driver.get_cookies()

    if not cookies:
        print("(no cookies)")
        return

    # Schöne Ausgabe: name=value + domain/path
    for c in cookies:
        print(
            f"{c.get('name')}={c.get('value')}  "
            f"domain={c.get('domain')} path={c.get('path')}"
        )


# ---------------------------
# Download-Test (Erweiterung)
# ---------------------------

def wait_for_download(path: Path, timeout_s: int = 10) -> None:
    """
    Wartet, bis die Datei existiert und die Dateigrösse stabil ist.
    So stellen wir sicher, dass der Download wirklich fertig ist.
    """
    start = time.time()
    last_size = -1

    while time.time() - start < timeout_s:
        if path.exists():
            size = path.stat().st_size
            # Fertig, wenn Datei >0 Bytes und zwei Mal hintereinander gleich gross ist
            if size > 0 and size == last_size:
                return
            last_size = size
        time.sleep(0.2)

    raise RuntimeError(f"Download did not finish in time: {path}")


def cmd_download(driver: webdriver.Firefox, url: str, download_dir: str, filename: str) -> None:
    """
    Feature: Datei herunterladen.
    Erwartet auf der Seite ein <a id="dl" href="...">Download</a>.
    Klickt den Link und prüft, ob die Datei im Download-Ordner angekommen ist.
    """
    target = Path(download_dir) / filename

    # Damit der Test eindeutig ist: vorhandene Datei löschen
    if target.exists():
        target.unlink()

    # Download-Seite öffnen
    driver.get(url)

    # Link mit id="dl" klicken (muss in download.html so existieren)
    driver.find_element(By.ID, "dl").click()

    # Warten bis Download fertig
    wait_for_download(target)

    print(f"OK: downloaded {target.resolve()}")


def parse_args():
    """
    CLI-Argumente definieren und einlesen.
    Dadurch sind Aufrufe möglich wie:
      python selenium-http.py get --name Giuliano --room A101 --headless
      python selenium-http.py download --file test.txt --headless
    """
    p = argparse.ArgumentParser(
        description="Python Selenium Projekt (GET/POST/Scrape/Cookies)"
    )

    # Pflichtargument: welches Kommando ausgeführt werden soll
    p.add_argument("command", help="title|get|post|list-cookies|download")

    # Optionale Argumente mit Default-Werten
    p.add_argument("--port", type=int, default=8000, help="Port deines lokalen Webservers")
    p.add_argument("--headless", action="store_true", help="Browser ohne Fenster ausführen")

    # GET-Parameter Defaults
    p.add_argument("--name", default="Giuliano", help="GET Parameter: name")
    p.add_argument("--room", default="A101", help="GET Parameter: room")

    # POST-Feld Defaults
    p.add_argument("--user", default="giu", help="POST Feld: user")
    p.add_argument("--msg", default="Hallo", help="POST Feld: msg")

    # Download Defaults
    p.add_argument("--download-dir", default="./downloads", help="Ordner für Downloads")
    p.add_argument("--file", default="test.pdf", help="Dateiname, der heruntergeladen wird")
    return p.parse_args()


def main():
    """
    Einstiegspunkt:
    - Argumente lesen
    - URLs zusammenbauen
    - Browser starten
    - passendes Kommando ausführen
    - Browser sauber beenden
    """
    args = parse_args()

    # Kommando normalisieren (Leerzeichen entfernen, klein schreiben)
    cmd = args.command.strip().lower()

    # URLs zur lokalen Testsite zusammenbauen
    url_index = f"{base_url(args.port)}/index.html"
    url_get = f"{base_url(args.port)}/get.html"
    url_post = f"{base_url(args.port)}/post.html"
    url_cookies = f"{base_url(args.port)}/cookies.html"

    # Download-Seite: du brauchst im web-root eine "download.html" mit <a id="dl" ...>
    url_download = f"{base_url(args.port)}/index.html"

    driver = None
    try:
        # Firefox starten (headless optional) + Download-Ordner übergeben
        driver = make_driver(args.headless, args.download_dir)

        # Dispatch: je nach "command" das passende Feature ausführen
        if cmd == "title":
            cmd_title(driver, url_index)
        elif cmd == "get":
            cmd_get(driver, url_get, args.name, args.room)
        elif cmd == "post":
            cmd_post(driver, url_post, args.user, args.msg)
        elif cmd == "list-cookies":
            cmd_list_cookies(driver, url_cookies)
        elif cmd == "download":
            cmd_download(driver, url_download, args.download_dir, args.file)
        else:
            # Unbekanntes Kommando -> Fehlerausgabe + Exit Code 2
            print(f"Unknown command: {cmd}", file=sys.stderr)
            sys.exit(2)

    finally:
        # Wichtig: Browser immer schliessen, auch bei Fehlern
        if driver:
            driver.quit()


# Standard-Python-Pattern:
# Wenn die Datei direkt ausgeführt wird, rufe main() auf.
# Wenn die Datei importiert wird, passiert nichts automatisch.
if __name__ == "__main__":
    main()