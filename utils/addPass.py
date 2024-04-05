from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import utils.aesutil as aesutil
from utils.dbconfig import dbconfig
from rich import print as printc


def computeMasterKey(mp, ds):
    pw = mp.encode()
    salt = ds.encode()
    key = PBKDF2(pw, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def addEntry(mp, ds, websiteName, websiteUrl, email, username):

    #get password
    ps = getpass("Enter password: ")
    mk = computeMasterKey(mp, ds)

    encrypted = aesutil.encrypt(mk, ps, keyType="bytes")

    # Add to db
    db = dbconfig()
    cursor = db.cursor()
    query = "INSERT INTO pm.entries (Website_name, website_url, email, username, password) VALUES (%s, %s, %s, %s, %s)"
    val = (websiteName, websiteUrl, email, username, encrypted)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added entry")
