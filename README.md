# CLI Arguments 
                                                                        
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
                                                                        
