API_KEY=$AQUA_API_KEY
API_SECRET=$AQUA_API_SECRET
TIMESTAMP=$(date -u +%s)
ENDPOINT="https://eu-1.api.cloudsploit.com/v2/tokens"
METHOD="POST"

# Define the body of the POST request

POST_BODY='{"validity":240,"allowed_endpoints":["GET"]}'

# Create the string to sign
STRING_TO_SIGN="$TIMESTAMP$METHOD/v2/tokens$POST_BODY"
echo "String to sign: '$STRING_TO_SIGN'"

# Create HMAC signature
SIGNATURE=$(echo -n "$STRING_TO_SIGN" | openssl dgst -sha256 -hmac "$API_SECRET" -hex | sed 's/.*= //g')
echo "API_KEY: $API_KEY"
echo "API_SECRET: $API_SECRET"
echo "Signature: $SIGNATURE"

# Issue the signed request to get authentication token
RESPONSE=$(curl -vv -s -X $METHOD $ENDPOINT \
 -H "Content-Type: application/json" \
 -H "X-API-Key: $API_KEY" \
 -H "X-Timestamp: $TIMESTAMP" \
 -H "X-Signature: $SIGNATURE" \
 -d $POST_BODY)

# Extract status and token from the response
STATUS=$(echo $RESPONSE | jq -r '.status')

# Check the status
if [ $STATUS -eq 200 ]; then
 echo "Login successful."
 TOKEN=$(echo $RESPONSE | jq -r '.data')
 echo -n $TOKEN > ./.aqua_token
else
 echo "Request failed. Status: $RESPONSE"
 exit 1
fi