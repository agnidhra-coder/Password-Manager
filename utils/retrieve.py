from utils.dbconfig import dbconfig
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from rich import print as printc
from rich.table import Table
from rich.console import Console
import utils.aesutil as aesutil
import pyperclip

def computeMasterKey(mp, ds):
    pw = mp.encode()
    salt = ds.encode()
    key = PBKDF2(pw, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key

def createTable(title_):
    table = Table(title=title_)
    table.add_column("Website Name")
    table.add_column("URL")
    table.add_column("Email")
    table.add_column("Username")
    table.add_column("Password")

    return table

def retrieveEntries(mp, ds, search, decryptPassword=False):
    db = dbconfig()
    cursor = db.cursor()

    query = ""

    if len(search) == 0:
        query = "SELECT * FROM pm.entries"
    else:
        query = "SELECT * FROM pm.entries WHERE "
        for i in search:
            query+=f'{i} = "{search[i]}" AND '
        query = query[:-5]

    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        printc("[yellow][-][/yellow] No results for the entry")
        return
    
    if (decryptPassword and len(results)>1) or (not decryptPassword):
        table = createTable("Results")

        for i in results:
            table.add_row(i[0], i[1], i[2], i[3], "{hidden}") # type:ignore

        console = Console()
        console.print(table)

        return
    
    if len(results) == 1 and decryptPassword:
        mk = computeMasterKey(mp, ds)
        decrypted = aesutil.decrypt(key=mk, source=results[0][4], keyType='bytes') # type: ignore

        table = createTable("Results")

        for i in results:
            table.add_row(i[0], i[1], i[2], i[3], "{hidden}") # type:ignore

        console = Console()
        console.print(table)

        pyperclip.copy(decrypted.decode())
        printc("[green][+][/green] Password copied to clipboard")

    db.close()

def retrieveAll():
    db = dbconfig()
    cursor = db.cursor()

    query = "SELECT * FROM pm.entries"
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        printc("[yellow][-][/yellow] No results")
        return
    else:
        table = Table(title="Results")
        table.add_column("Website Name")
        table.add_column("URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")

        for i in results:
            table.add_row(i[0], i[1], i[2], i[3], "{hidden}") # type:ignore

        console = Console()
        console.print(table)

        return