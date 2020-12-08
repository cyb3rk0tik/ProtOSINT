#!/usr/bin/env python3

#Python libraries
import requests
from datetime import datetime
import re
import ipaddress

#Color setup
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def printAscii():
	"""
	ASCII Art
	"""
	print("""
	   ___           _            _       _   
	  / _ \_ __ ___ | |_ ___  ___(_)_ __ | |_ 
	 / /_)/ '__/ _ \| __/ _ \/ __| | '_ \| __|
	/ ___/| | | (_) | || (_) \__ \ | | | | |_ 
	\/    |_|  \___/ \__\___/|___/_|_| |_|\__|
	                                          
	""")


def checkProtonAPIStatut():
	"""
	This function check proton API statut : ONLINE / OFFLINE

	"""
	requestProton_mail_statut = requests.get('https://api.protonmail.ch/pks/lookup?op=index&search=test@protonmail.com')
	if requestProton_mail_statut.status_code == 200:
		print("Protonmail API is " + f"{bcolors.BOLD}ONLINE{bcolors.ENDC}")
	else:
		print("Protonmail API is " + f"{bcolors.BOLD}OFFLINE{bcolors.ENDC}")

	requestProton_vpn_statut = requests.get('https://api.protonmail.ch/vpn/logicals')
	if requestProton_vpn_statut.status_code == 200:
		print("Protonmail VPN is " + f"{bcolors.BOLD}ONLINE{bcolors.ENDC}")
	else:
		print("Protonmail VPN is " + f"{bcolors.BOLD}OFFLINE{bcolors.ENDC}")


def printWelcome():
	welcome = """
Let's take a look at your target:
1 - Test the validity of one protonmail account
2 - Try to find if your target have a protonmail account by generating multiple adresses by combining information fields inputted
3 - Find if your IP is currently affiliate to ProtonVPN
"""
	print(welcome)


def checkValidityOneAccount():
	"""
	PROGRAM 1 : Test the validity of one protonmail account
	
	"""
	invalidEmail = True
	regexEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]protonmail[.]\w{2,3}$'
	
	print("You want to know if a protonmail email is real ?")
	while invalidEmail:
		#Input
		mail = input("Give me your email: ")
		#Text if the input is valid
		if(re.search(regexEmail,mail)):
			invalidEmail = False
		else:
			print("Invalid Proton Email")
			invalidEmail = True

	#Check if the protonmail exist : valid / not valid
	requestProton = requests.get('https://api.protonmail.ch/pks/lookup?op=index&search='+str(mail))
	bodyResponse = requestProton.text
	
	protonNoExist = "info:1:0" #not valid
	protonExist = "info:1:1" #valid

	if protonNoExist in bodyResponse:
		print("Protonmail email is " + f"{bcolors.FAIL}not valid{bcolors.ENDC}")

	if protonExist in bodyResponse:
		print("Protonmail email is " + f"{bcolors.OKGREEN}valid{bcolors.ENDC}")
		regexPattern1 = "2048:(.*)::"
		regexPattern2 = "4096:(.*)::"
		try:
			timestamp = int(re.search(regexPattern1, bodyResponse).group(1))
		except:
			timestamp = int(re.search(regexPattern2, bodyResponse).group(1))
		dtObject = datetime.fromtimestamp(timestamp)
		print("Date and time of the creation:", dtObject)


def checkGeneratedProtonAccounts():
	"""
	PROGRAM 2 : Try to find if your target have a protonmail account by generating multiple adresses by combining information fields inputted
	
	"""

	#Input
	print("Let's go, try to find your protonmail target:")
	firstName = input("First name: ").lower()
	lastName = input("Last name: ").lower()
	yearOfBirth = input("Year of birth: ")
	pseudo1 = input("Pseudo 1: ").lower()
	pseudo2 = input("Pseudo 2: ").lower()
	zipCode = input("zipCode: ")

	#Protonmail domain
	domainList = ["@protonmail.com","@protonmail.ch"]

	#List of combinaison
	pseudoList=[]
	
	for domain in domainList:
		#For domain
		pseudoList.append(firstName+lastName+domain)
		pseudoList.append(lastName+firstName+domain)
		pseudoList.append(firstName[0]+lastName+domain)
		pseudoList.append(pseudo1+domain)
		pseudoList.append(pseudo2+domain)
		pseudoList.append(lastName+domain)
		pseudoList.append(firstName+lastName+yearOfBirth+domain)
		pseudoList.append(firstName[0]+lastName+yearOfBirth+domain)
		pseudoList.append(lastName+firstName+yearOfBirth+domain)
		pseudoList.append(pseudo1+yearOfBirth+domain)
		pseudoList.append(pseudo2+yearOfBirth+domain)
		pseudoList.append(firstName+lastName+yearOfBirth[-2:]+domain)
		pseudoList.append(firstName+lastName+yearOfBirth[-2:]+domain)
		pseudoList.append(firstName[0]+lastName+yearOfBirth[-2:]+domain)
		pseudoList.append(lastName+firstName+yearOfBirth[-2:]+domain)
		pseudoList.append(pseudo1+yearOfBirth[-2:]+domain)
		pseudoList.append(pseudo2+yearOfBirth[-2:]+domain)
		pseudoList.append(firstName+lastName+zipCode+domain)
		pseudoList.append(firstName[0]+lastName+zipCode+domain)
		pseudoList.append(lastName+firstName+zipCode+domain)
		pseudoList.append(pseudo1+zipCode+domain)
		pseudoList.append(pseudo2+zipCode+domain)
		pseudoList.append(firstName+lastName+zipCode[:2]+domain)
		pseudoList.append(firstName[0]+lastName+zipCode[:2]+domain)
		pseudoList.append(lastName+firstName+zipCode[:2]+domain)
		pseudoList.append(pseudo1+zipCode[:2]+domain)
		pseudoList.append(pseudo2+zipCode[:2]+domain)


	#Remove duplicates from list
	pseudoListUniq = [] 
	for i in pseudoList: 
	    if i not in pseudoListUniq: 
	        pseudoListUniq.append(i) 

	#Remove all irrelevant combinations
	for domain in domainList:
		if domain in pseudoListUniq: pseudoListUniq.remove(domain)
		if zipCode+domain in pseudoListUniq: pseudoListUniq.remove(zipCode+domain)
		if zipCode[:2]+domain in pseudoListUniq: pseudoListUniq.remove(zipCode[:2]+domain)
		if yearOfBirth+domain in pseudoListUniq: pseudoListUniq.remove(yearOfBirth+domain)
		if yearOfBirth[-2:]+domain in pseudoListUniq: pseudoListUniq.remove(yearOfBirth[-2:]+domain)
		if firstName+domain in pseudoListUniq: pseudoListUniq.remove(firstName+domain)

	print("===============================")
	print("I'm trying some combinaison: " + str(len(pseudoListUniq)))
	print("===============================")

	for pseudo in pseudoListUniq:
		requestProton = requests.get('https://api.protonmail.ch/pks/lookup?op=index&search='+str(pseudo))
		bodyResponse = requestProton.text

		protonNoExist = "info:1:0" #not valid
		protonExist = "info:1:1" #valid

		if protonNoExist in bodyResponse:
			print(pseudo + " is " + f"{bcolors.FAIL}not valid{bcolors.ENDC}")

		if protonExist in bodyResponse:
			regexPattern1 = "2048:(.*)::" #AES encryption with 2048-bits
			regexPattern2 = "4096:(.*)::" #AES encryption with 4096-bits
			try:
				timestamp = int(re.search(regexPattern1, bodyResponse).group(1))
			except:
				timestamp = int(re.search(regexPattern2, bodyResponse).group(1))
			dtObject = datetime.fromtimestamp(timestamp)
			print(pseudo + " is " + f"{bcolors.OKGREEN}valid{bcolors.ENDC}" + " - Creation date:", dtObject)


def checkIPProtonVPN():
	"""
	PROGRAM 3 : Find if your IP is currently affiliate to ProtonVPN
	
	"""
	while True:
	    try:
	        ip = ipaddress.ip_address(input('Enter IP address: '))
	        break
	    except ValueError:
	        continue

	requestProton_vpn = requests.get('https://api.protonmail.ch/vpn/logicals')
	bodyResponse = requestProton_vpn.text
	if str(ip) in bodyResponse:
		print("This IP is currently affiliate to ProtonVPN")
	else:
		print("This IP is currently not affiliate to ProtonVPN")
	#print(bodyResponse)


# Entry point of the script
def main():
	printAscii()
	checkProtonAPIStatut()
	printWelcome()
	choice = input("Choose a program: ")
	if choice == "1":
		checkValidityOneAccount() 
	if choice == "2":
		checkGeneratedProtonAccounts()
	if choice == "3":
		checkIPProtonVPN()

if __name__ == '__main__':
	main()
