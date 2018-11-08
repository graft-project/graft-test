#!/usr/bin/env python3

class RequestTemplate():
    announce = {
                  "jsonrpc":"2.0",
                  "method":"send_supernode_announce",
                  "id":0,
                  "params":{
                      "signed_key_images":[
                        {
                          "key_image":"f219e6151c84",
                          "signature":"f88d136f02683407b0bff9a1473761"
                        }
                      ],
                      "timestamp":1530799007,
                      "address":"F4KrqowwEoY6K9J8dV75toToyYYmHdMbkWgFCm4A9uMhND3uGtnMFU4gAGLBVYFEbz2zC9jrVvCS96x3HUcy6nAd4q4Robb",
                      "stake_amount":53370100000000000,
                      "height":114374,
                      "secret_viewkey":"5ee2b4d62214d4ae3385c80e4485cb7547690144c3bbddf31fd75351900a8b0e",
                      "network_address":"54.226.23.229:28690/dapi/v2.0"
                  }
                }

    broadcast = {
                  "json_rpc" : "2.0",
                  "method" : "broadcast",
                  "id" : "0",
                  "params": {
                    "sender_address" : "",
                    "callback_uri" : "",
                    "data" : ""
                  }
                }

    multicast = {
                  "json_rpc" : "2.0",
                  "method" : "multicast",
                  "id" : "0",
                  "params": {
                    "receiver_addresses" : [ "address1", "address2" ],
                    "sender_address" : "",
                    "callback_uri" : "",
                    "data" : ""
                  }
                }

    unicast = {
      "jsonrpc":"2.0",
      "id":"0",
      "method":"unicast",
      "params": {
        "sender_address":"F8C3ZSW9XFHJuz78vqJiFo3S5bnMug8nA8QziJ5YgJtHcFXZZ9QYmXQVut6CkMhoLwXeuhcFdeDUm8dxBKgLRbG7RcA7Fvq",
        "receiver_address":"FAemK2QsWwsDAxgCKsTJUbhk1XwAu1eg4eVkYNbYSkQzLP8wobvgG7ia1tXcpSY6k4f7rFmypq6wHKT4fYJJ3XFL1KRgNrj",
        "callback_uri":"",
        "data":"eyJQYXltZW50SUQiOiI2MGU2YTYyMC04NWE2LTQ3OGQtODAyZC02ZGIwNzEzNzQwMWYiLCJCbG9ja051bWJlciI6MTc2MX0=",
        "wait_answer": False
      }
    }

    sale = {
      "jsonrpc":"2.0",
      "id":"0",
      "method":"sale",
      "params": {
        "Address":"F8C3ZSW9XFHJuz78vqJiFo3S5bnMug8nA8QziJ5YgJtHcFXZZ9QYmXQVut6CkMhoLwXeuhcFdeDUm8dxBKgLRbG7RcA7Fvq",
        "SaleDetails":"",
        "PaymentID":"",
        "Amount": 250
      }
    }

    sale_details = {
      "jsonrpc":"2.0",
      "id":"0",
      "method":"sale_details",
      "params": {
        "PaymentID":"",
        "BlockNumber": 250
      }
    }





