#Test script for checking Sidecar health for Moonbeam network deployments
#Usage:
# - from command line, type "python3 sidecarhealthcheck" to run endpoint tests on all known Sidecar deployments.
# - from command line, type "python3 sidecarhealthcheck [network name1] [network name2]..." to run endpoint tests on specified network(s).
# To add more networks or endpoints, modify the respective dictionary directly in code.
# Please check the Substrate-sidecar-API for what the endpoints do: https://paritytech.github.io/substrate-api-sidecar/dist/

# importing the requests library
import requests
import random
import sys

# networks
networks = {}
networks["moonriver"]="https://moonriver-rest-api.moonriver.moonbeam.network"  
networks["moonbaserelay"]="https://alphanet-rest-api.testnet.moonbeam.network"
#networks["testfail"]="https://moonriver-rest-api.moonriver.moonbeammer.network" 

# api-endpoints
endpoints = {}
endpoints["nodeversion"]="/node/version"
endpoints["runtimespec"]="/runtime/spec"
endpoints["headblock"]="/blocks/head"
endpoints["headblockheader"]="/blocks/head/header"
endpoints["block"]="/blocks/"

# the server seems to be blocking Python default request header, so have to mock one. 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# number of samples to take for the retrieve block endpoint test
blocksamplenumber = 5

#network's head block number
networkheadblocknum = {}

#helper method to form the URL for the HTTP request, parameter is optional
def form_request(base_url, end_point, parameter = None):
      if parameter is None:
            return base_url+end_point
      else:
            return base_url+end_point+str(parameter)

#helper method to execute the HTTP request
def perform_test(network, endpoint):
      if endpoint == "block":
            if network not in networkheadblocknum.keys():
                  r = perform_test(network, "runtimespec")
                  if r.status_code == requests.codes.ok:
                        data = r.json()
                        headblockheight = data["at"]["height"]
                        networkheadblocknum[network] = int(headblockheight)
            request_url = form_request(networks[network], endpoints[endpoint], random.randint(1, networkheadblocknum[network]))
      else:
            request_url = form_request(networks[network], endpoints[endpoint])
      return requests.get(url = request_url, headers=headers)

#Accepts the network name, endpoint name, and a boolean for whether to display the full JSON resonse object
def perform_and_display(network, endpoint, verbose):
      r = perform_test(network, endpoint)
      if r.status_code == requests.codes.ok:
            print("Network: {"+network+ "} Endpoint: {"+ endpoint+ "} test completed successfully in " + str(r.elapsed.total_seconds()) + " seconds.")
            if verbose:
                  print("Detailed Response:")
                  print(r.json())
      else:
            print("Network: {"+network+ "} Endpoint: {"+ endpoint+ "} test failed to complete in " + str(r.elapsed.total_seconds()) + " seconds.")
            print("HTTP response status code is: " + str(r.status_code))
      print()

#Perform the standard endpoint tests for a given network
def perform_standard_tests(network):
      perform_and_display(network, "nodeversion", True)
      perform_and_display(network, "runtimespec", True)
      perform_and_display(network, "headblock", False)
      perform_and_display(network, "headblockheader", True)
      for i in range (blocksamplenumber):
            print ("Block Test #"+str(i+1)+":")
            perform_and_display(network, "block", False)


def main():

      if len(sys.argv)>1 :
            for i in range (1, len(sys.argv)):
                  if sys.argv[i] in networks.keys():
                        perform_standard_tests(sys.argv[i])
                  else:
                        print("Do not recognize the network name: " +sys.argv[i])
      else:
            for network in networks.keys():
                  perform_standard_tests(network)


if __name__ == "__main__":
    main()