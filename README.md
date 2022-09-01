# sidecar-health-check
A Python script to check the health of Moonbeam Sidecar instances

# Usage
 - from command line, type "python3 sidecarhealthcheck" to run endpoint tests on all known Sidecar deployments.
 - from command line, type "python3 sidecarhealthcheck [network name1] [network name2]..." to run endpoint tests on specified network(s). To add more networks or endpoints, modify the respective dictionary directly in code.
 - To add in more specifc blocks to check, edit the "problematicblocks" dictionary object in the code. 