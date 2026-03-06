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

from selenium.webdriver.common.action_chains import ActionChains
# ^ Für komplexe Interaktionen wie Hover, Drag&Drop, etc.

from selenium.webdriver.common.keys import Keys
# ^ Für Tastatureingaben (Keys.ENTER, Keys.ARROW_DOWN, etc.)


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

# ---------------------------
# Hilfsfunktion: Basis-URL zum lokalen Webserver
# ---------------------------

def base_url(port: int) -> str:
    """
    Baut die Basis-URL zu deinem lokalen Webserver.
    Beispiel: port=8000 -> http://127.0.0.1:8000
    """
    return f"http://127.0.0.1:{port}"

# ---------------------------
# Einfaches Auslesen von <title>
# ---------------------------

def cmd_title(driver: webdriver.Firefox, url: str) -> None:
    """
    Feature: Scraping eines HTML-Tags.
    Wir öffnen die Seite und lesen den <title>-Text via driver.title aus.
    """
    driver.get(url)         # Öffnet URL im Browser
    print(driver.title)     # Gibt den <title> der Seite aus
    

# ---------------------------
# Navigation und Interaktion
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
# dropdown.html Test
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

# ---------------------------
# POST/Form-Test
# ---------------------------

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

# ---------------------------
# Cookies-Test
# ---------------------------

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
# Checkbox-Test
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
# Input-Test
# ---------------------------

def cmd_input(driver: webdriver.Firefox, index_url: str, text: str) -> None:
    """
    Input-Test: vom Index auf input.html navigieren und Text eingeben.
    """
    go_from_index(driver, index_url, "nav-input")

    txt = driver.find_element(By.ID, "txt")
    txt.clear()
    txt.send_keys(text)

    driver.find_element(By.ID, "send").click()

    time.sleep(0.1)
    print(driver.find_element(By.ID, "echo").text)

# ---------------------------
# slider Test
# ---------------------------

def cmd_slider(driver: webdriver.Firefox, index_url: str, value: int) -> None:
    """
    Slider-Test:
    - startet auf index.html
    - navigiert zu slider.html
    - setzt den Slider auf einen gewünschten Wert
    - gibt den Text aus #value aus
    """
    go_from_index(driver, index_url, "nav-slider")

    slider = driver.find_element(By.ID, "slider")

    # Slider-Wert via JS setzen (stabiler als Dragging)
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
        slider,
        str(value),
    )

    time.sleep(0.1)
    print(driver.find_element(By.ID, "value").text)

# ---------------------------
# hover Test
# ---------------------------
def cmd_hover(driver: webdriver.Firefox, index_url: str) -> None:
    """
    Hover-Test:
    - startet auf index.html
    - navigiert zu hover.html
    - führt einen Hover über das Element #hover-area aus
    - gibt den Text aus #hover-result aus
    """
    go_from_index(driver, index_url, "nav-hover")

    hover_area = driver.find_element(By.ID, "box")
    
    ActionChains(driver).move_to_element(hover_area).perform()
    time.sleep(0.1)

    tooltip = driver.find_element(By.ID, "tooltip")
    print(f"tooltip_displayed={tooltip.is_displayed()} text={tooltip.text}")

# ---------------------------
# drag and drop
# ---------------------------
def cmd_dragdrop(driver: webdriver.Firefox, index_url: str) -> None:
    """
    Drag&Drop-Test:
    - startet auf index.html
    - navigiert zu dragdrop.html
    - draged von #source nach #target
    - gibt den Text aus #result aus
    """
    go_from_index(driver, index_url, "nav-dragdrop")

    source = driver.find_element(By.ID, "source")
    target = driver.find_element(By.ID, "target")


    js = """
    const src = arguments[0];
    const dst = arguments[1];

    const dataTransfer = new DataTransfer();

    function fire(el, type) {
      const evt = new DragEvent(type, {
        bubbles: true,
        cancelable: true,
        dataTransfer: dataTransfer
      });
      el.dispatchEvent(evt);
    }

    fire(src, "dragstart");
    fire(dst, "dragenter");
    fire(dst, "dragover");
    fire(dst, "drop");
    fire(src, "dragend");
    """

    driver.execute_script(js, source, target)
    time.sleep(0.2)

    print(driver.find_element(By.ID, "result").text)

# ---------------------------
# new window
# ---------------------------
def cmd_newwindow(driver: webdriver.Firefox, index_url: str) -> None:
    """
    New Window-Test:
    - startet auf index.html
    - navigiert zu newwindow.html
    - klickt den Button, der ein neues Fenster öffnet
    - wechselt zum neuen Fenster und gibt den <title> aus
    """
    go_from_index(driver, index_url, "nav-newwindow")

    driver.find_element(By.ID, "open").click()
    time.sleep(0.2)

    windows = driver.window_handles
    if len(windows) < 2:
        print("Error: new window did not open", file=sys.stderr)
        return

    driver.switch_to.window(windows[1])
    print(driver.title)

# ---------------------------
# Login
# ---------------------------
def cmd_login(driver: webdriver.Firefox, index_url: str, user: str, password: str) -> None:
    """
    Login-Test:
    - startet auf index.html
    - navigiert zu login.html
    - füllt Benutzername und Passwort aus und klickt Login
    - gibt den Text aus #status aus
    """
    go_from_index(driver, index_url, "nav-login")

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(user)

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "login").click()
    time.sleep(0.1)

    print(driver.find_element(By.ID, "result").text)

# ---------------------------
# keys Test
# ---------------------------
def cmd_keys(driver: webdriver.Firefox, index_url: str) -> None:
    """
    Keys-Test:
    - startet auf index.html
    - navigiert zu keys.html
    - fokussiert das Eingabefeld und sendet einige Tasten (z.B. "Hello" + ENTER)
    - gibt den Text aus #output aus
    """
    go_from_index(driver, index_url, "nav-keys")

    input_box = driver.find_element(By.ID, "box")
    input_box.click()  # Fokus setzen

    input_box.send_keys("Hello World")
    input_box.send_keys(Keys.ARROW_DOWN)

    time.sleep(0.1)
    print(driver.find_element(By.ID, "output").text)

# ---------------------------
# Upload-Test
# ---------------------------
def cmd_upload(driver: webdriver.Firefox, index_url: str, filepath: str) -> None:
    """
    Upload test:
    - starts on index.html
    - navigates to upload.html
    - sets file path in <input type="file">
    - clicks show
    - prints #result
    """
    go_from_index(driver, index_url, "nav-upload")

    file_input = driver.find_element(By.ID, "file")
    file_input.send_keys(os.path.abspath(filepath))

    driver.find_element(By.ID, "show").click()
    time.sleep(0.1)

    print(driver.find_element(By.ID, "result").text)

# ---------------------------
# Download-Test
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

    p.add_argument("command", help="title|get|post|list-cookies|download|checkbox|dropdown|input|slider|hover|dragdrop|newwindow|login|upload|keys")
    p.add_argument("--port", type=int, default=8000, help="Port deines lokalen Webservers")
    p.add_argument("--headless", action="store_true", help="Browser ohne Fenster ausführen")

    p.add_argument("--name", default="Giuliano", help="GET Parameter: name")
    p.add_argument("--room", default="A101", help="GET Parameter: room")

    p.add_argument("--user", default="test", help="POST Feld: user")
    p.add_argument("--msg", default="Hallo", help="POST Feld: msg")

    p.add_argument("--download-dir", default="./downloads", help="Ordner für Downloads")
    p.add_argument("--file", default="test.pdf", help="Dateiname, der heruntergeladen wird")

    p.add_argument("--check", default="1", choices=["1", "2"], help="Welche Checkbox auswählen (1 oder 2)")

    p.add_argument("--input-text", default="Hello World", help="Text, der im Input-Feld eingegeben wird")

    p.add_argument("--slider", type=int, default=50, help="Wert für den Slider (0-100)")

    p.add_argument("--login_user", default="admin", help="Benutzername für Login")
    p.add_argument("--login_pass", default="secret", help="Passwort für Login")

    p.add_argument("--upload-file", default="./web/files/test.pdf", help="Path of file to upload")

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
        elif cmd == "input":
            cmd_input(driver, url_index, args.input_text)
        elif cmd == "slider":
            cmd_slider(driver, url_index, args.slider)
        elif cmd == "dropdown":
            cmd_dropdown(driver, url_index, args.dropdown_value)
        elif cmd == "hover":
            cmd_hover(driver, url_index)
        elif cmd == "dragdrop":
            cmd_dragdrop(driver, url_index)
        elif cmd == "newwindow":
            cmd_newwindow(driver, url_index)
        elif cmd == "login":
            cmd_login(driver, url_index, args.login_user, args.login_pass)
        elif cmd == "upload":
            cmd_upload(driver, url_index, args.upload_file)
        elif cmd == "keys":
            cmd_keys(driver, url_index)
        else:
            print(f"Unknown command: {cmd}", file=sys.stderr)
            sys.exit(2)

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()