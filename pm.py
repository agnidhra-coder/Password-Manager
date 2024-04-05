import utils.addPass
import utils.retrieve
import utils.generate
import utils.clearAll
from utils.dbconfig import dbconfig

import argparse
from rich import print as printc
import pyperclip
from getpass import getpass
import hashlib

parser = argparse.ArgumentParser(description='Description')

parser.add_argument('option', help='(a)dd / (e)xtract / (g)enerate')
parser.add_argument("-s", "--site", help="Used to enter website name")
parser.add_argument("-u", "--url", help="Used to enter website URL")
parser.add_argument("-e", "--email", help="Used to enter email")
parser.add_argument("-i", "--user", help="Used to enter username")
parser.add_argument("--length", help="Used to enter length of the password to generate",type=int)
parser.add_argument("-c", "--copy", action='store_true', help='Copy password to clipboard')

args = parser.parse_args()

def inputAndValidateMasterPassword():
	mp = getpass("MASTER PASSWORD: ")
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT * FROM pm.secrets"
	cursor.execute(query)
	result = cursor.fetchall()[0]
	if hashed_mp != result[0]:  # type: ignore
		printc("[red][!] WRONG MASTER PASSWORD! [/red]")
		return None

	return [mp,result[1]] # type:ignore


def main():
	if args.option in ["add","a"]:
		if args.url == None:
			# if args.site == None:
			# 	printc("[red][!][/red] Site Name (-s) required ")
			if args.url == None:
				printc("[red][!][/red] Site URL (-u) required ")
			return
		
		if args.email == None:
			args.email = ""
		if args.site == None:
			args.site = f"{args.url}"
		if args.user == None:
			args.user = args.email
			

		res = inputAndValidateMasterPassword()
		if res is not None:
			utils.addPass.addEntry(res[0], res[1], args.site, args.url, args.email, args.user)

	if args.option in ["extract","e"]:
		if args.site == None and args.url == None and args.email == None and args.user == None:
			# retrieve all
			printc("[red][!][/red] Please enter at least one search field (sitename/url/email/username)")
			return
		res = inputAndValidateMasterPassword()

		search = {}
		if args.site is not None:
			search["Website_name"] = args.site
		if args.url is not None:
			search["website_url"] = args.url
		if args.email is not None:
			search["email"] = args.email
		if args.user is not None:
			search["username"] = args.user

		if res is not None:
			utils.retrieve.retrieveEntries(res[0], res[1], search, decryptPassword = args.copy)
			
	if args.option in ["generate","g"]:
		if args.length == None:
			args.length = 10
		password = utils.generate.generatePassword(args.length)
		pyperclip.copy(password)
		printc("[green][+][/green] Password generated and copied to clipboard")
		
	if args.option in ["clear", "x"]:
		printc("[red]WARNING! You are about to delete all entries, do you want to continue? (y/n):[/red]")
		check = input()
		if check == 'y':
			utils.clearAll.clearAllEntries()
			printc("[green][+][/green] Cleared all entries")
		else:
			printc("[green][-][/green] No entries deleted")
			return
	if args.option in ["all"]:
		utils.retrieve.retrieveAll()

main()