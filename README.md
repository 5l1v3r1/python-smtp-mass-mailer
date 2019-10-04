#PYTHON SMTP MASS MAILER BY S-MAN
## CLI Arguments 
                                                                        
### OPTIONAL 

    --help				: cancel all others and show the help
    --substitute		: substitute [[[N]]] by values in the maillist   
    					 Available tags :
    					 	+ [[[random-hash]]] 	: prints random hash
    					 	+ [[[random-number]]]   : prints random number
    					 	+ [[[random-letter]]]   : prints random letter
    					 	+ [[[date-time]]] 		: prints date and time in DD/MM/YYYY HH:MM format
    					 	+ [[[N]]]               : N must be an int , will be replaced by the column number N in the mails file [[[0]]] is for reciver mail                                     
	--verbose			: output logs in the console                           		
	--html 				: mails will be sent as html                                      
	--timeout N 		: wait N sec between 2 mails                                 
	--test-mail MAIL 	: send a copy of the mail to MAIL at the end            
	--test-mail-every N : send a copy of the mail to test_mail every N mail  
	--to-adresses FILE 	: mails will be sent to adresses in the FILE file     
	--from-name NAME 	: Sender name                                           

### REQUIRED
                                                                        
	--fromaddr MAIL 	: Sender mail                                            
	--smtp-server SERVER: Smtp server                                       
	--smtp-port PORT 	: Smtp port                                             
	--username USERNAME : Smtp username                                      
	--password PASSWORD : Smtp password                                      
	--subject SUBJECT 	: Mail subject                                         
	--content FILE 		: Mail content will be readen from FILE                   
                                                                        

## IMPORT

### CALL
You can integrate the function that send mails by calling the cli or by importing send_mails functinon and calling it with the right arguments

### send_mails function

#### signature 

	send_mails(verbose,html,timeout,test_mail,test_mail_every,fromaddr,to_adresses,message_content,from_name,smtp_server,smtp_port,username,password,subject,substitute)

#### args

	verbose | type : Boolean 
	html | type : Boolean 
	timeout | type : int  
	test_mail | type : List |  comment : the test_mail arg must contain empty list or a list with one mail at position 0 , other values are optional 
	test_mail_every | type : int | comment : if you want to disable this just put 0
	fromaddr | type : string
	to_adresses | type : List(l) of Lists(lX) | comment : lX will contain mail at position 0 and other values are used if you want to substitue them in mails
	message_content | type : string 
	from_name | type : string
	smtp_server | type : string
	smtp_port | type : string
	username | type : string
	password | type : string
	subject | type : string
	substitute | type : Boolean