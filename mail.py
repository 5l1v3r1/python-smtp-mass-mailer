import smtplib
import time
import copy
import sys
import re 
import random
from datetime import datetime

  
def validate_mail(email):  
	if(re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',email)):  
		return True
	else:  
		return False
def send_mails(verbose,html,timeout,test_mail,test_mail_every,fromaddr,to_adresses,message_content,from_name,smtp_server,smtp_port,username,password,subject,substitute):
	to_adresses=[mail for mail in to_adresses if validate_mail(mail[0])]
	message_content=message_content.replace("\n", "\r\n")
	toaddrs=copy.deepcopy(to_adresses)
	header_type=""	


	new_message_content=copy.deepcopy(message_content)
	new_subject=copy.deepcopy(subject)
	new_fromaddr=copy.deepcopy(fromaddr)
	new_from_name=copy.deepcopy(from_name)


	if substitute:
		substitute_max=max([len(mail_csv) for mail_csv in to_adresses])


	if html:
		header_type="Content-Type: text/html; charset=\"UTF-8\""
	
	#toaddrs_original_len=len(toaddrs)
	msg = "\r\n".join([
	  "From: %s<%s>",
	  "To: %s",
	  "Subject: %s",
	  header_type,
	  "%s"
	  ])
	
	server = smtplib.SMTP('%s:%s'%(smtp_server,smtp_port))
	
	try:
		if verbose:
			print("Login") 
		#server.ehlo()
		#server.starttls()
		#server.login(username,password)
	except:
		if verbose:
			print("Verify smtp credentials")
		exit(1)
	
	try:
		i=0
		#if toaddrs_original_len==0 and test_mail!="":
		#	if verbose:
		#		print("Sending test mail to %s ##################"%test_mail)
		#	server.sendmail("%s<%s>"%(from_name,fromaddr), test_mail, msg%(from_name,fromaddr,test_mail,subject,message_content))
		# 
		for email in to_adresses:


			if substitute:
				new_message_content=message_content.replace("[[[random-hash]]]","%032x"%random.getrandbits(128))
				new_subject=subject.replace("[[[random-hash]]]","%032x"%random.getrandbits(128))
				new_fromaddr=fromaddr.replace("[[[random-hash]]]","%032x"%random.getrandbits(128))
				new_from_name=from_name.replace("[[[random-hash]]]","%032x"%random.getrandbits(128))



				new_message_content=new_message_content.replace("[[[random-number]]]",random.choice("0123456789"))
				new_subject=new_subject.replace("[[[random-number]]]","%s"%random.choice("0123456789"))
				new_fromaddr=new_fromaddr.replace("[[[random-number]]]","%s"%random.choice("0123456789"))
				new_from_name=new_from_name.replace("[[[random-number]]]","%s"%random.choice("0123456789"))
				
				new_message_content=new_message_content.replace("[[[random-letter]]]",random.choice("azertyuiopqsdfghjklmwxcvbn"))
				new_subject=new_subject.replace("[[[random-letter]]]","%s"%random.choice("azertyuiopqsdfghjklmwxcvbn"))
				new_fromaddr=new_fromaddr.replace("[[[random-letter]]]","%s"%random.choice("azertyuiopqsdfghjklmwxcvbn"))
				new_from_name=new_from_name.replace("[[[random-letter]]]","%s"%random.choice("azertyuiopqsdfghjklmwxcvbn"))
		
				new_message_content=new_message_content.replace("[[[date-time]]]",datetime.now().strftime("%d/%m/%Y %H:%M"))
				new_subject=new_subject.replace("[[[date-time]]]",datetime.now().strftime("%d/%m/%Y %H:%M"))
				new_fromaddr=new_fromaddr.replace("[[[date-time]]]",datetime.now().strftime("%d/%m/%Y %H:%M"))
				new_from_name=new_from_name.replace("[[[date-time]]]",datetime.now().strftime("%d/%m/%Y %H:%M"))



				for sub_num in range(substitute_max):
					if sub_num < len(email):
						new_message_content=new_message_content.replace("[[[%d]]]"%sub_num,email[sub_num])
						new_subject=new_subject.replace("[[[%d]]]"%sub_num,email[sub_num])
						new_fromaddr=new_fromaddr.replace("[[[%d]]]"%sub_num,email[sub_num])
						new_from_name=new_from_name.replace("[[[%d]]]"%sub_num,email[sub_num])				



			


			if verbose:
				print("Sending mail to %s"%email[0])
			server.sendmail("%s<%s>"%(new_from_name,new_fromaddr), email[0], msg%(new_from_name,new_fromaddr,email[0],new_subject,new_message_content))
			toaddrs.remove(email)
			i+=1
			if test_mail_every!=0 and i%test_mail_every==0:
				time.sleep(timeout)
				if verbose:
					print("Sending test mail to %s ##################"%(test_mail[0]))
				server.sendmail("%s<%s>"%(new_from_name,new_fromaddr), test_mail[0], msg%(new_from_name,new_fromaddr,test_mail[0],new_subject,new_message_content))	
			time.sleep(timeout)
	
		if test_mail!="":
			if verbose:
				print("Sending test mail to %s ##################"%(test_mail[0]))
			server.sendmail("%s<%s>"%(new_from_name,new_fromaddr), test_mail[0], msg%(new_from_name,new_fromaddr,test_mail[0],new_subject,new_message_content))

	except Exception as e:
		if verbose:
			print("Error sending mail , not sent adresses are available in not_sent.txt")
			print(e)
			server.quit()
			with open("not_sent.txt","a+") as not_sent:
				not_sent_content=[ ";".join(one) for one in toaddrs ]
				not_sent.write("\n".join(not_sent_content)+"\n")
				not_sent.close()
			exit(2)
	
	server.quit()

def main():

	if "--help" in sys.argv:
		help()
		exit(0)

	validate_args=True

	substitute="--substitute" in sys.argv
	verbose="--verbose" in sys.argv
	html="--html" in sys.argv
	timeout=0
	if "--timeout" in sys.argv:
		try:
			timeout=int(sys.argv[sys.argv.index("--timeout")+1])
		except:
			print("--timeout must have int value")
			validate_args=False
			pass

	test_mail=""	
	if "--test-mail" in sys.argv:
		try:
			test_mail=sys.argv[sys.argv.index("--test-mail")+1]
		except:
			print("--test-mail must have string value")
			validate_args=False
			pass
	test_mail=test_mail.split(";")
	test_mail_every=0
	if "--test-mail-every" in sys.argv:
		if test_mail=="":
			print("You need to specify --test-mail if you want to activate --test-mail-every")
			validate_args=False
			pass
		try:
			test_mail_every=int(sys.argv[sys.argv.index("--test-mail-every")+1])	
		except:
			print("--test-mail must have int value")
			validate_args=False
			pass

	if "--fromaddr" in sys.argv:
		fromaddr=""
		try:
			fromaddr=sys.argv[sys.argv.index("--fromaddr")+1]
			if fromaddr[0:2]=="--":
				print("--fromaddr must have string value")
				validate_args=False
		except:
			print("--fromaddr must have string value")
			validate_args=False
			pass


	else:
		print("--fromaddr not specified")
		validate_args=False

	to_adresses=[]
	if "--to-adresses" in sys.argv:
		try:
			with open(sys.argv[sys.argv.index("--to-adresses")+1]) as adresses:
				to_adresses=adresses.read().splitlines()
				to_adresses=[ adr.split(";") for adr in to_adresses]
				#print(to_adresses)
				adresses.close()
			if sys.argv[sys.argv.index("--to-adresses")+1][0:2]=="--":
				print("--to-adresses must have string value and be file path")
				validate_args=False
		except:
			print("--to-adresses must have string value and be file path")
			validate_args=False
			pass

		



	if "--content" in sys.argv:
		try:
			with open(sys.argv[sys.argv.index("--content")+1]) as content:
				message_content=content.read()
				content.close()
			if sys.argv[sys.argv.index("--content")+1][0:2]=="--":
				print("--content must have string value and be file path")
				validate_args=False
		except:
			print("--content must have string value and be file path")
			validate_args=False
			pass


	else:
		print("--content not specified")
		validate_args=False
	
	from_name=""

	if "--from-name" in sys.argv:
		try:
			from_name=sys.argv[sys.argv.index("--from-name")+1]
			if sys.argv[sys.argv.index("--from-name")+1][0:2]=="--":
				print("--from-name must have string value")
				validate_args=False
		except:
			print("--from-name must have string value")
			validate_args=False
			pass



	if "--smtp-server" in sys.argv:
		try:
			smtp_server=sys.argv[sys.argv.index("--smtp-server")+1]
			if sys.argv[sys.argv.index("--smtp-server")+1][0:2]=="--":
				print("--smtp-server must have string value")
				validate_args=False
		except:
			print("--smtp-server must have string value")
			validate_args=False
			pass

	else:
		print("--smtp-server not specified")
		validate_args=False



	if "--smtp-port" in sys.argv:
		try:
			smtp_port=sys.argv[sys.argv.index("--smtp-port")+1]
			if sys.argv[sys.argv.index("--smtp-port")+1][0:2]=="--":
				print("--smtp-port must have string value")
				validate_args=False
		except:
			print("--smtp-port must have string value")
			validate_args=False
			pass

	else:
		print("--smtp-port not specified")
		validate_args=False

	

	if "--username" in sys.argv:
		try:
			username=sys.argv[sys.argv.index("--username")+1]
			if sys.argv[sys.argv.index("--username")+1][0:2]=="--":
				print("--username must have string value")
				validate_args=False
		except:
			print("--username must have string value")
			validate_args=False
			pass

	else:
		print("--username not specified")
		validate_args=False


	if "--password" in sys.argv:
		try:
			password=sys.argv[sys.argv.index("--password")+1]
			if sys.argv[sys.argv.index("--password")+1][0:2]=="--":
				print("--password must have string value")
				validate_args=False
		except:
			print("--password must have string value")
			validate_args=False
			pass

	else:
		print("--password not specified")
		validate_args=False


	if "--subject" in sys.argv:
		try:
			subject=sys.argv[sys.argv.index("--subject")+1]
			if sys.argv[sys.argv.index("--subject")+1][0:2]=="--":
				print("--subject must have string value")
				validate_args=False
		except:
			print("--subject must have string value")
			validate_args=False
			pass

	else:
		print("--subject not specified")
		validate_args=False

	

	if not validate_args:
		help()
		exit(4)
	else:
		send_mails(verbose, html, timeout, test_mail, test_mail_every, fromaddr, to_adresses, message_content, from_name, smtp_server, smtp_port, username, password, subject,substitute)

def help():
	print("############################## Arguments : #######################################")
	print("#                                                                                #")
	print("# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ OPTIONAL @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #")
	print("# @                                                                            @ #")
	print("# @ --help		: cancel others and show help                          @ #")
	print("# @ --verbose		: output logs in the console                           @ #")
	print("# @ --substitute		: substitute [[[N]]] by values in the maillist @ #")
	print("# @ --html		: mails will be sent as html                           @ #")
	print("# @ --timeout N		: wait N sec between 2 mails                           @ #")
	print("# @ --test-mail MAIL	: send a copy of the mail to MAIL at the end (csv line)@ #")
	print("# @ --test-mail-every N	: send a copy of the mail to test_mail every N mail    @ #")
	print("# @ --to-adresses FILE	: mails will be sent to adresses in the FILE file      @ #")
	print("# @ --from-name NAME	: Sender name                                          @ #")
	print("# @                                                                            @ #")
	print("# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #")
	print("#                                                                                #")
	print("# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ REQUIRED @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #")
	print("# @                                                                            @ #")
	print("# @ --fromaddr MAIL	: Sender mail                                          @ #")
	print("# @ --smtp-server SERVER: Smtp server                                          @ #")
	print("# @ --smtp-port PORT	: Smtp port                                            @ #")
	print("# @ --username USERNAME	: Smtp username                                        @ #")
	print("# @ --password PASSWORD	: Smtp password                                        @ #")
	print("# @ --subject SUBJECT	: Mail subject                                         @ #")
	print("# @ --content FILE: Mail content will be readen from FILE                      @ #")
	print("# @                                                                            @ #")
	print("# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #")
	print("#                                                                                #")
	print("##################################################################################")


if __name__ == '__main__':
	main()
#send_mails(verbose, html, timeout, test_mail, test_mail_every, fromaddr, to_adresses, message_content, from_name, smtp_server, smtp_port, username, password, subject)