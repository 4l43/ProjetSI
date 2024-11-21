#!/bin/bash 

SERVER = "smtp-relay.gmail.com"
PORT = "587"
USER = "41014348"
SENDER_ADDRESS = "u41005688@gmail.com"
SENDER_NAME = "41014348"
RECIPIENT_NAME = "Sylvain"
RECIPIENT_ADDRESS = "41005688@parisnanterre.fr"
SUBJECT = "Tets"
MESSAGE = "Tets"


read -r -s -p "Entrer your password : " PASS
echo ""

curl -v\
    --ssl-reqd --url "smtps://$SERVER:$PORT" \
    --user "$USER:$PASS"\
    --mail-from  "$SENDER_ADDRESS"\
    --mail-rcpt "$RECIPIENT_ADDRESS"\
    --header "Subject: $SUBJECT"\
    --header "From: $SENDER_NAME <$SENDER_ADDRESS>"\
    --header "To: $RECIPIENT_NAME <$RECIPIENT_ADDRESS>"\
    --data "$MESSAGE"