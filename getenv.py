#!/usr/bin/env python3

"""
Author: Stian Øverby

This script is used to retrieve environment variables from the pods of a desired
context in a Kubernetes cluster.

Preliminaries:
    1. Save the file with a preferred filename.
    2. Make sure you have a shell like bash.
    3. Run 'chmod u+x filename' in your shell to give the user execution privileges.
    4. Installing python3 is a prerequisite

Usage:
    1. Open a terminal and navigate to the directory where the script is located.
    2. Run './filename' to execute the script.
"""

import subprocess
import os

devnull = open(os.devnull, 'w')

# Show all available contexts
contexts = subprocess.check_output(["kubectl", "config", "get-contexts"], universal_newlines=True)
contexts = contexts.strip().split("\n")[1:]
contexts = [context.split()[1] for context in contexts]

ctx_choices = {idx : ctx for idx, ctx in enumerate(contexts)}
print("\n== START CONTEXT NAMES ==\n")
for c in ctx_choices:
    print("[", c , "]", ctx_choices[c])
print("\n== END CONTEXT NAMES ==\n")

# Prompt the user for the context
choice = int(input("Enter the number of the wanted context => "))

# Check if the choice exsists
if choice in ctx_choices:
    print(f"You chose the context: {ctx_choices[choice]}")
else: 
    print(f"There is no choice with the '{choice}' key. Try inputing another index!")
    exit(1)

chosen_ctx = ctx_choices[choice]

# Change to the specified context
subprocess.run(["kubectl", "config", "use-context", chosen_ctx], stderr=devnull)

# Check if context is gcp, and that the user is not already logged in. If gcp-context and not logged in, redirect to authentication.
active_account = subprocess.check_output(["gcloud", "config", "list", "--format", "value(core.account)"], universal_newlines=True).strip()
if "gcp" in chosen_ctx and not active_account:
    print("Redirecting to log-in since environment requires authentication...")
    subprocess.run(["gcloud", "auth", "login"])
else:
    print(f"Already logged in as: {active_account}")

# Print application names to stdout
applications = subprocess.check_output(["kubectl", "get", "application"], universal_newlines=True, stderr=devnull)
applications = applications.strip().split("\n")[1:]
applications = [application.split()[0] for application in applications]

app_choices = { idx : app for idx, app in enumerate(applications)}
print("\n== START APPLICATION NAMES ==\n")
for c in app_choices:
    print("[", c , "]", app_choices[c])
print("\n== END APPLICATION NAMES ==\n")

# Prompt the user for the application
choice = int(input("Enter the number of the wanted application => "))

# Check if the choice exsists
if choice in app_choices:
    print(f"You chose the application: {app_choices[choice]}")
else: 
    print(f"There is no choice with the '{choice}' key. Try inputing another index!")
    exit(1)

application = app_choices[choice]

# Get the name of the first pod with the specified application
pod_name = subprocess.check_output(
    [  "kubectl"
    ,  "get"
    ,  "pods"
    ,  "--field-selector=status.phase=Running"
    ,  "-l"
    ,  f"app={application}"
    ,  "-o"
    ,  "jsonpath='{.items[0].metadata.name}'"
    ]
    , universal_newlines=True
    , stderr=devnull
)
pod_name = pod_name.strip("'")

env_variables =     [   "AZURE_APP_CLIENT"
                    ,   "AZURE_APP_CLIENT_ID"
                    ,   "AZURE_APP_JWK"
                    ,   "AZURE_APP_CLIENT_SECRET"
                    ,   "AZURE_APP_JWKS"
                    ]

# Fetch the values of the env variables
values = []
for env_variable in env_variables:
    print("Fetching...")
    value = subprocess.check_output(["kubectl", "exec", pod_name, "--", "env"], universal_newlines=True, stderr=devnull)
    value = value.strip().split("\n")
    value = [line for line in value if env_variable in line]
    if value:
        values.append(value[0])

# Echo the values, replace the spaces with newlines, and sort the env variables
sorted_values = sorted(values)

# Output the env variables
print("\n=== START ENV VARS ===\n")
print("\n".join(sorted_values))
print("\n=== END ENV VARS ===\n")
