
#!/bin/bash

# Define the endpoint URL
URL="https://eu-central-1.edge.cloud.aquasec.com/codesec/v1/api/repositories"

# Read the token from the file
TOKEN=$(<.aqua_token)

# Make the HTTP request with the Authorization header
curl -vv -H "Authorization: Bearer $TOKEN" "$URL"
