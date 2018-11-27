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

    transfer_rta = {
        "jsonrpc":"2.0",
        "id":"0",
        "method":"transfer_rta",
        "params": {
            "destinations":[{"amount":100000,
              "address":"7BnERTpvL5MbCLtj5n9No7J5oE5hHiB3tVCK5cjSvCsYWD2WRJLFuWeKTLiXo5QJqt2ZwUaLy2Vh1Ad51K7FNgqcHgjW85o"}],
            "do_not_relay":True,
            "get_tx_key":True,
            "get_tx_hex":True,
            "get_tx_metadata":True
        }
    }

    pay = {
        "jsonrpc":"2.0", "id":"0",
        "method":"pay",
        "params": {
            "Address": "<PoS public address string>",
            "PaymentID": "<guid>",
            "BlockNumber": 0,
            "Amount": "<payment amount in atomic units serialized into string>",
            "Transactions": ["<signed transaction binary data>"]
        }
    }

    pay_status = {
        "jsonrpc":"2.0",
        "id":"0",
        "method":"pay_status",
        "params": {
            "PaymentID": [optional] "<guid>",
            "BlockNumber": <block number>
        }
    }

    sale_status = {
        "jsonrpc":"2.0",
        "id":"0",
        "method":"sale_status",
        "params": {
            "PaymentID":  "<guid>",
            "BlockNumber": "<block number>"
        }
    }


#var transferParams = new TransferParams
#{
#    Destinations = destinations.ToArray(),
#    GetTxHex = true,
#    GetTxMetadata = true,
#    GetTxKey = true
#};
#
#
#{"jsonrpc":"2.0","id":"0","method":"transfer","params":{
#  "destinations":[{"amount":100000000000,
#    "address":"7BnERTpvL5MbCLtj5n9No7J5oE5hHiB3tVCK5cjSvCsYWD2WRJLFuWeKTLiXo5QJqt2ZwUaLy2Vh1Ad51K7FNgqcHgjW85o"},
#    {"amount":200000000000,
#      "address":"75sNpRwUtekcJGejMuLSGA71QFuK1qcCVLZnYRTfQLgFU5nJ7xiAHtR5ihioS53KMe8pBhH61moraZHyLoG4G7fMER8xkNv"}]
#,"account_index":0,"subaddr_indices":[0],"priority":0,"ring_size":7,"get_tx_key": true}}'
#
#    public class TransferParams
#    {
#        [JsonProperty(PropertyName = "destinations")]
#        public Destination[] Destinations { get; set; }
#
#        [JsonProperty(PropertyName = "account_index")]
#        public uint? AccountIndex { get; set; }
#
#        [JsonProperty(PropertyName = "subaddr_indices")]
#        public uint[] SubaddrIndices { get; set; }
#
#        [JsonProperty(PropertyName = "mixin")]
#        public uint? Mixin { get; set; }
#
#        [JsonProperty(PropertyName = "unlock_time")]
#        public uint? UnlockTime { get; set; }
#
#        [JsonProperty(PropertyName = "payment_id")]
#        public string PaymentId { get; set; }
#
#        [JsonProperty(PropertyName = "get_tx_key")]
#        public bool? GetTxKey { get; set; }
#
#        [JsonProperty(PropertyName = "priority")]
#        public uint? Priority { get; set; }
#
#        [JsonProperty(PropertyName = "do_not_relay")]
#        public bool? DoNotRelay { get; set; }
#
#        [JsonProperty(PropertyName = "get_tx_hex")]
#        public bool? GetTxHex { get; set; }
#
#        [JsonProperty(PropertyName = "get_tx_metadata")]
#        public bool? GetTxMetadata { get; set; }
#    }
#}
#
