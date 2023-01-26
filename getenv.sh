#!/bin/bash
#########################################################
#       RETRIEVE VALUES OF ENVIRONMENT VARIABLES        #
#########################################################
# Author: Stian Øverby
#
# This script is used to retrive environment variables from the pods of a wanted 
# context in a kubernetes cluster. 
#
# Prelimenaries:
#   Save the file with a prefered filename. You of course will need a shell like bash.
#   
#   Run 'chmod u+x filename' in your shell to give the user you are on execution priviliges.
#
# Usage:
#
#   ./filename
#

# Show all available contexts
contexts=$(kubectl config get-contexts | awk 'NR > 1 {print $2}')

printf "\n== START CONTEXT NAMES ==\n\n"
echo "$contexts" 
printf "\n== END CONTEXT NAMES ==\n\n"

# Prompt the user for the context
read -p "Enter the wanted context => " context

# Check if the context exists
if ! echo "$contexts" | grep -q "^$context$"
then
    echo "Error: The context '$context' does not exist" >&2
    exit 1
fi

# Change to the specified context
kubectl config use-context $context

# Check if context is gcp, and that the user is not already logged in. If 
# gcp-contex and not legged in, redirect to authentication.
active_account=$(gcloud config list --format 'value(core.account)')
if [[ $context == *"gcp"* ]] && [[ ! -n $active_account ]]; then
    echo "Redirecting to log-in since environment requires authentication..."
    gcloud auth login
fi

# Print application names to stdout
applications=$(kubectl get application | awk 'NR > 1 {print $1}')

printf "\n== START APPLICATION NAMES ==\n\n"
echo "$applications"
printf "\n== END APPLICATION NAMES ==\n\n"

# Prompt the user for the application
read -p "Enter the name of the application => " application

# Get the name of the first pod with the specified application
pod_name=$(kubectl get pods --field-selector=status.phase=Running -l app=$application -o jsonpath='{.items[0].metadata.name}')

# Get the value of the AZURE_APP_JWK environment variable
azure_app_jwk=$(kubectl exec $pod_name -- env | grep ^AZURE_APP_JWK= )

# Get the value of the AZURE_APP_CLIENT_SECRET environment variable
azure_app_client_secret=$(kubectl exec $pod_name -- env | grep AZURE_APP_CLIENT_SECRET)

# Print env vars to stdout
printf "\n=== START ENV VARS ===\n\n"
echo "$azure_app_jwk"
printf "\n"
echo "$azure_app_client_secret"
printf "\n=== END ENV VARS ===\n"
