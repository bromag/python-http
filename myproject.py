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

from selenium.webdriver.support.ui import Select
# ^ Für die Interaktion mit <select> Dropdowns (Select(driver.find_element(...)))


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
    

# ---------------------------
# Navigation & Interaktion
# ---------------------------
def go_from_index(driver: webdriver.Firefox, index_url: str, link_id: str) -> None:
    """
    Öffnet index.html und klickt den Link mit der ID link_id.
    Voraussetzung: index.html enthält Links mit IDs (z.B. nav-get, nav-post, ...).
    """
    driver.get(index_url)
    driver.find_element(By.ID, link_id).click()
    time.sleep(0.1)

# ---------------------------
# dropdown.html Test (Erweiterung)
# ---------------------------
def cmd_dropdown(driver: webdriver.Firefox, index_url: str, value: str) -> None:
    """Dropdown-Test:
    - startet auf index.html
    - navigiert zur dropdown.html
    - wählt einen Wert im <select id="drop">
    - gibt den Text aus #selected aus
    """
    go_from_index(driver, index_url, "nav-dropdown")

    select = Select(driver.find_element(By.ID, "drop"))
    select.select_by_value(value)

    time.sleep(0.1)
    print(driver.find_element(By.ID, "selected").text)

def cmd_get(driver: webdriver.Firefox, index_url: str, get_url: str, name: str, room: str) -> None:
    """
    GET: vom Index auf get.html navigieren, dann get.html mit Query-Parametern laden.
    """
    go_from_index(driver, index_url, "nav-get")

    qs = urlencode({"name": name, "room": room})
    driver.get(f"{get_url}?{qs}")

    print(driver.find_element(By.ID, "result").text)


def cmd_post(driver: webdriver.Firefox, index_url: str, user: str, msg: str) -> None:
    """
    POST/Form: vom Index auf post.html navigieren, Felder ausfüllen und Submit klicken.
    """
    go_from_index(driver, index_url, "nav-post")

    driver.find_element(By.NAME, "user").send_keys(user)
    driver.find_element(By.NAME, "msg").send_keys(msg)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(0.1)
    print(driver.find_element(By.ID, "out").text)


def cmd_list_cookies(driver: webdriver.Firefox, index_url: str) -> None:
    """
    Cookies: vom Index auf cookies.html navigieren, Cookies setzen und ausgeben.
    """
    go_from_index(driver, index_url, "nav-cookies")

    driver.find_element(By.ID, "set").click()
    time.sleep(0.1)

    cookies = driver.get_cookies()
    if not cookies:
        print("(no cookies)")
        return

    for c in cookies:
        print(
            f"{c.get('name')}={c.get('value')}  "
            f"domain={c.get('domain')} path={c.get('path')}"
        )

# ---------------------------
# Checkbox-Test (Erweiterung)
# ---------------------------

def cmd_checkbox(driver: webdriver.Firefox, index_url: str, which: str) -> None:
    """
    Checkbox: vom Index auf checkbox.html navigieren und cb1 oder cb2 auswählen.
    """
    go_from_index(driver, index_url, "nav-checkbox")

    cb_id = "cb1" if which == "1" else "cb2"
    cb = driver.find_element(By.ID, cb_id)

    if not cb.is_selected():
        cb.click()

    time.sleep(0.1)
    print(driver.find_element(By.ID, "status").text)


# ---------------------------
# Download-Test (Erweiterung)
# ---------------------------
def wait_for_download(path: Path, timeout_s: int = 10) -> None:
    """
    Wartet, bis die Datei existiert und die Dateigrösse stabil ist.
    """
    start = time.time()
    last_size = -1

    while time.time() - start < timeout_s:
        if path.exists():
            size = path.stat().st_size
            if size > 0 and size == last_size:
                return
            last_size = size
        time.sleep(0.2)

    raise RuntimeError(f"Download did not finish in time: {path}")


def cmd_download(driver: webdriver.Firefox, index_url: str, download_dir: str, filename: str) -> None:
    """
    Download: startet vom Index und klickt den Download-Link (id="dl").
    Erwartet, dass index.html einen Link mit id="dl" hat, der auf die Datei zeigt.
    """
    target = Path(download_dir) / filename
    if target.exists():
        target.unlink()

    driver.get(index_url)
    driver.find_element(By.ID, "dl").click()

    wait_for_download(target)
    print(f"OK: downloaded {target.resolve()}")


def parse_args():
    p = argparse.ArgumentParser(description="Python Selenium Projekt (Firefox)")

    p.add_argument("command", help="title|get|post|list-cookies|download|checkbox|dropdown")
    p.add_argument("--port", type=int, default=8000, help="Port deines lokalen Webservers")
    p.add_argument("--headless", action="store_true", help="Browser ohne Fenster ausführen")

    p.add_argument("--name", default="Giuliano", help="GET Parameter: name")
    p.add_argument("--room", default="A101", help="GET Parameter: room")

    p.add_argument("--user", default="test", help="POST Feld: user")
    p.add_argument("--msg", default="Hallo", help="POST Feld: msg")

    p.add_argument("--download-dir", default="./downloads", help="Ordner für Downloads")
    p.add_argument("--file", default="test.pdf", help="Dateiname, der heruntergeladen wird")

    p.add_argument("--check", default="1", choices=["1", "2"], help="Welche Checkbox auswählen (1 oder 2)")

    p.add_argument("--dropdown-value", default="drop2", help="Dropwown-Wert auswählen (z.B. drop1, drop2, drop3)")
    return p.parse_args()


def main():
    args = parse_args()
    cmd = args.command.strip().lower()

    url_index = f"{base_url(args.port)}/index.html"
    url_get = f"{base_url(args.port)}/get.html"

    driver = None
    try:
        driver = make_driver(args.headless, args.download_dir)

        if cmd == "title":
            cmd_title(driver, url_index)
        elif cmd == "get":
            cmd_get(driver, url_index, url_get, args.name, args.room)
        elif cmd == "post":
            cmd_post(driver, url_index, args.user, args.msg)
        elif cmd == "list-cookies":
            cmd_list_cookies(driver, url_index)
        elif cmd == "download":
            cmd_download(driver, url_index, args.download_dir, args.file)
        elif cmd == "checkbox":
            cmd_checkbox(driver, url_index, args.check)
        elif cmd == "dropdown":
            cmd_dropdown(driver, url_index, args.dropdown_value)
        else:
            print(f"Unknown command: {cmd}", file=sys.stderr)
            sys.exit(2)

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()