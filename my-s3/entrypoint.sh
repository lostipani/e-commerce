#!/bin/sh
BUCKET_NAME=$1
KEY_ID="GKf41436429ec06e878386451a"
SECRET="a3ec6af28a9e18a48e90e8214cd6e4c26686f8a8605d9484940f39ea97a5431b"

/garage server &
GARAGE_PID=$!
echo "setup:: Waiting for Garage to start..."
until /garage status > /dev/null 2>&1; do sleep 1; done

echo "setup:: Getting node ID..."
NODE_ID=$(/garage status | awk '/NO ROLE ASSIGNED/ {print $1}')
echo "setup:: Node ID: $NODE_ID"
echo "setup:: Assigning layout..."
/garage layout assign -z dc1 -c 1G "$NODE_ID"
echo "setup:: Applying layout..."
/garage layout apply --version 1

echo "setup:: Creating (if not existing) bucket $BUCKET_NAME..."
/garage bucket create $BUCKET_NAME || echo "Bucket may already exist"
/garage key import --yes -n my-s3-key "$KEY_ID" "$SECRET"
/garage bucket allow $BUCKET_NAME --key "$KEY_ID" --read --write --owner


wait $GARAGE_PID