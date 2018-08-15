﻿"""

Author: Sam Celani

File:   StartConsumer.py

Description:

    This
    
    It is part of the ARPA-E Project: NEXTCAR.


Imported Files:

    configInit.py

        Helps to determine where the script should be listening.

    RabbitMQ_Rx.py

        Receives, parses, and ships data to the MABX.
        
"""

###########################################################

#
#   IMPORTS
#       All imports are nested in a try-except block
#       to avoid fatal errors, or at least to simply
#       put them off for a little bit.
#

try:

    import configInit
    import pika
    import RabbitMQ_Rx
    import time

except Exception as ex:
    print(ex)

###########################################################

    
# for data inbound to vehicle
if __name__ == "__main__":
    
    #######################################################

    #
    #   DEFAULTING VARIABLES
    #

    SERVERIP = '35.54.5.207'        ##  I don't know what this is
    SERVERIP = '141.219.181.216'    ##  Kuilin's server ip
    SERVERIP = '141.219.205.25'     ##  Sam's server IP
    SERVERIP = '166.152.103.250'    ##  Mobile Lab?
    CREDENTIALS = pika.PlainCredentials('aps-lab', 'aps-lab')       ##  Username/Password, must be setup on server
    IP = '192.168.150.10'           ##  IP of the UDP connection to the uAutoBox (don't change)
    REMOTEIP = '192.168.150.1'      ##  IP of the uAutoBox (DON'T CHANGE)
    PORT = 5002                     ##  UDP port for the uAutoBox (don't change)
    LOGNAME = 'cacc_test_exchange'  ##  Name of the exchange
    ROUTING_KEY = 'controller_1'    ##  Routing key

    #######################################################


###########################################################

#
#   USE OF CONFIGINIT
#

try:
    # kuilin, beta, sam, mobile_lab, tony_url
    datum = configInit.init('mobile_lab')
    SERVERIP = datum[0]
    if len(datum) is 3:
        ROUTING_KEY = datum[1]
        LOGNAME = datum[2]
        print( SERVERIP, LOGNAME, ROUTING_KEY ,sep='\n',end='\n\n')
    elif len(datum) is 4:
        credA = datum[1][0]
        credB = datum[1][1]
        if not datum[1][0] is None:
            CREDENTIALS = pika.PlainCredentials(credA,credB)
        else:
            CREDENTIALS = None
        ROUTING_KEY = datum[2]
        LOGNAME = datum[3]
                                           
        print( SERVERIP, "("+credA+', '+credB+")", LOGNAME, ROUTING_KEY ,sep='\n',end='\n\n')
    else:
        # shouldn't even be possible
        print('What?')
except:
    print('Proceeding with default connection information:\n')
    
    print( SERVERIP, "("+credA+', '+credB+")", LOGNAME, ROUTING_KEY ,sep='\n',end='\n\n')

###########################################################

    
    con = RabbitMQ_Rx.Consumer(SERVERIP, CREDENTIALS, IP, PORT, REMOTEIP, LOGNAME, ROUTING_KEY, FANOUT_ROUTING_KEY)
    con.start()

    print('Script ''StartConsumer'' Started.  Press ^C or close window to stop...')
    while True:
        time.sleep(1.0)
        #main loop
        pass
