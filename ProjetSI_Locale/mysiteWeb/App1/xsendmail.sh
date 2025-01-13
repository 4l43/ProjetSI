#!/bin/bash 
.sh
SERVER="smtp.gmail.com"
PORT="587"
USER="41014348"
SENDER_ADDRESS="41014348@parisnanterre.fr"
SENDER_NAME="41014348"
RECIPIENT_NAME="Sylvain"
RECIPIENT_ADDRESS="alex.brindusoiu30@gmail.com"
SUBJECT="Tets"
MESSAGE="Tets"


read -r -s -p "Entrer your password : " PASS


curl -v \
    --ssl-reqd --url "smtps://$SERVER:$PORT" \
    --tlsv1.2 \
    --user "$USER:$PASS"\
    --mail-from  "$SENDER_ADDRESS"\
    --mail-rcpt "$RECIPIENT_ADDRESS"\
    --header "Subject: $SUBJECT"\
    --header "From: $SENDER_NAME <$SENDER_ADDRESS>"\
    --header "To: $RECIPIENT_NAME <$RECIPIENT_ADDRESS>"\
    --data "$MESSAGE"
