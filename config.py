from getpass import getpass
import hashlib
import random
import string
from utils.dbconfig import dbconfig

from rich import print as printc
from rich.console import Console

console = Console()


def generateDeviceSecret(length=10):
    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits, k=length
        )
    )


def config():
    db = dbconfig()
    cursor = db.cursor()

    printc("[green][+] Creating new config [/green]")

    try:
        cursor.execute("CREATE DATABASE pm")

    except Exception as e:
        printc("[red][!] An error occured while creating database")
        console.print_exception(show_locals=True)
    printc("[green][+][/green] Database 'pm' created")

    # Create tables
    query = "CREATE TABLE pm.secrets (Masterkey_hash TEXT NOT NULL, Device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created")

    query = "CREATE TABLE pm.entries (Website_name TEXT NOT NULL, website_url TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")

    mp = ""
    while True:
        mp = getpass("Choose a MASTER PASSWORD: ")
        if mp == getpass("Re-type MASTER PASSWORD: ") and mp != "":
            break
        printc("[yellow][-] Please Enter again[/yellow]")

    # Hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+] Saved MASTER PASSWORD[/green]")

    # Generate DEVICE SECRET
    ds = generateDeviceSecret()
    printc("[green][+] DEVICE SECRET generated[/green]")

    # add mp and ds to 'secrets' database
    query = "INSERT INTO pm.secrets (Masterkey_hash, Device_secret) VALUES (%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()
    printc("[green][+][/green] Added to Database")
    printc("[green]Configuration Done![/green]")

    db.close()


config()
