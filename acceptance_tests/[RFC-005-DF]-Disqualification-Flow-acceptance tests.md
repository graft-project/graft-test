# Disqualification Flow - acceptance tests

## Environment:

1. Hardware / Systems Requirement: Minimum hardware requirements include:
 
 **OS:** Ubuntu **18.04** LTS Bionic

Name|Build Requirments	|Run Requirements
----|-------------------|----------------
RAM, GB |	8	|2
CPU, Cores	|2	|2
Storage, GB	|100	|100

>_Note:_ In order to GraftNode (also called the cryptonode) work properly 28680 (P2P) port should be opened for incoming and outgoing traffic. If you are using other ports, please, make sure that you are open P2P port of the cryptonode.

2. RTA network
3. 8 AWS EC2 instances with Ununtu 18.04 running graftnoded and supernode
4. 8 stake wallets  for Supernode stakes. Each Wallet should have more than GRFT 50 000 amount. Each Wallet should send Stake Tx for amount >=GRFT 50000 
5. Before tests:

   5.1 Run `curl --request GET http://<SN1 IP address>:28690/dapi/v2.0/cryptonode/getwalletaddress` and save info about SN1:
      - Wallet_public_address1
      - Id_key1
      - Signature1

   5.2 Run `curl --request GET http://<SN2 IP address>:28690/dapi/v2.0/cryptonode/getwalletaddress` and save info about SN2:
      - Wallet_public_address2
      - Id_key2
      - Signature2

6. You should know current BC height


## TESTS:

 ##|Description|User Story|
------|-----------|----------|
Test#1| Disqualification of a SN by Type1 criteria (unresponsiveness of a random SN)| As a SN owner,I want to make sure that my SN is in the disqualification list (disqualification Type 1) and does not take part in the signing of an RTA Tx (is not  in the BBL and AuthSample lists but presents in the active SN list)|
Test#2| Unblocking SN disqualified by Type 1 criteria| As a SN owner, I want to ensure my SN is not blocked from signing RTA Tx and added to BBList after unblocking 
Test#3| Existence of disqualification Tx of Type 1 for disqualified SN| As an owner of the SN, I want to check availability of the DisqTx of Type 1 and ensure the number of signatures is equal to 8.
Test#4| Disqualification of a SN by Type2 criteria (lack of response from SN in Auth Sample)| As an owner of 2 SNs, I want to make sure that my SNs are in the disqualification list (disqualification Type 2) and does not take part in the signing of RTA Tx (are not  in the BBL and AuthSample but present in the active SN list). 
Test#5| Unblocking SN disqualified by Type 2 criteria| As  SNs owner, I want to be sure that my 2 SNs unblocked for participation in signing Tx and added to BBList after Type 2 disqualification
Test#6| Existence of disqualification Tx of Type 2  for disqualified SN| As an owner of the SNs, I want to check the availability of the DisqTx of Type 2 and  ensure the number of  signatories is equal to 6, and all 6 SN signed disqTx also signed the RTA Tx .
Test#7|Disqualification policy|Not used
Test#8|Unblocking  SN disqualified  by criteria of disqualification policy|Not used
Test#9|Participation of an active SN to Qualification Sample|Not used


## Details:

### Test #1  Disqualification of a SN by Type1 criteria (unresponsiveness of a random SN) 
   > As a SN owner,I want to make sure that my SN is in the disqualification list (disqualification Type 1) and does not take part in the signing of an RTA Tx (is not  in the BBL and AuthSample lists but presents in the active SN list)

##|Steps| Expected Result|
------|------|-----------------|
1.1 |To check the presence of the SN in BBL list run: `curl --header "Content-Type: application/json" --data '' --request GET http://<SN1 IP address>:28690/debug/blockchain_based_list/<block height> 2>/dev/null \| python -mjson.tool` | SN should be present in BBL: `…  { "Address": "<Wallet_public_address1>",  "PublicId": "<Id_key1>", "StakeAmount": <SN1 stake amount>  }, ... ` |
1.2| Shut down SN: `kill <# of the SN1  process in ubuntu>`  and wait 3-5 blocks. Run `ps -ela` | You shouldn't find the SN process in the ubuntu process list|
1.3| To check the absence of the  SN in BBL List run: `curl --header "Content-Type: application/json" --data '' --request GET http://<SN1 IP address>:28690/debug/blockchain_based_list/<block height> 2>/dev/null \| python -mjson.too`|SN should be absent in BBL|
1.4| Select Disq.List and check SN in Disq.List| SN should be present in Disq.List|
1.4.1|Save ID of your disq.Tx for Test#3 |
1.4.2| Save DisqExpiringBlock for Test#2|
1.5| To check the absence of the  SN in AuthSample List run: `curl --request GET http://<SN1 IP address>:28690/debug/auth_sample/aabbccddeeff 2>/dev/null \| python -mjson.tool`| SN should be  absent in Auth Sample List|
1.6|To check the presence of the  SN in SN List run: `curl --header "Content-Type: application/json" --data '' --request GET http:/<SN1 IP address>:28690/debug/supernode_list/1 2>/dev/null \| python -mjson.tool`| SN should be present in the SN List : `… {                 ""Address"": ""<Wallet_public_address1>"",                 ""AuthSampleBlockchainBasedListTier"": 0,                  ""BlockchainBasedListTier"": 0,                 ""IsAvailableForAuthSample"": false,                 ""IsStakeValid"":true,                ""LastUpdateAge"": 4,                 ""PublicId"":<Id_key1> ""42001a6ec3804d4305efb8538515395f4c6c521ff91c069e9e6fa2a404b33041"",                 ""StakeAmount"": <amount of SN1 stake Tx>,                ""StakeExpiringBlock"": 340123,                 ""StakeFirstValidBlock"": 340001             },… ` |
                
### Test #2 Unblocking SN disqualified by Type 1 criteria: 
  > As a SN owner, I want to ensure my SN is not blocked from signing RTA Tx and added to BBList after unblocking
  
##|Steps| Expected Result|
------|------|-----------------|
2.1| After  Test#1||
2.2| Run SN: `./graftnoded --testnet --log-file /home/ubuntu/graft/GraftLog/` and wait for blockchain synchronization| In case of successful synchronization, you  can see on the screen information: `Synchronized OK`|
2.3| Wait Block height= DisqExpiringBlock + 5||
2.4| To check the appearance  of the  SN in BBL list run: `curl --header "Content-Type: application/json" --data '' --request GET http://<SN1 IP address>:28690/debug/blockchain_based_list/<block height> 2>/dev/null \| python -mjson.tool`| SN should be present in  BBL:` …  {  "Address": "<Wallet_public_address1>",  "PublicId": "<Id_key1>", "StakeAmount": <SN1 stake amount>  }, ...`|
2.5| Select Disq.List and check SN in Disq.List| SN should be absent in Disq.List|
2.6| To check the presence of the  SN in AuthSample List run: `curl --request GET http://<SN1 IP address>:28690/debug/auth_sample/aabbccddeeff 2>/dev/null \| python -mjson.tool`| SN should be present in Auth Sample List: `{                ""Address"": """<Wallet_public_address1>"",                ""AuthSampleBlockchainBasedListTier"": 1,                ""BlockchainBasedListTier"": 1,                ""IsAvailableForAuthSample"": true,                ""IsStakeValid"": true,                ""LastUpdateAge"": 24,                ""PublicId"": ""<Id_key1>"",                ""StakeAmount"": <SN1 stake amount>,                ""StakeExpiringBlock"": 340123,                ""StakeFirstValidBlock"": 340001             },`|
2.7| To check presence of the SN in SN List run: ` curl --header "Content-Type: application/json" --data '' --request GET http:/<SN1 IP address>:28690/debug/supernode_list/1 2>/dev/null \| python -mjson.tool` | SN should be present in response - the SN List : ` … {                 ""Address"": ""<Wallet_public_address1>"",                 ""AuthSampleBlockchainBasedListTier"": 0,                 ""BlockchainBasedListTier"": 0,                 ""IsAvailableForAuthSample"": false,                 ""IsStakeValid"":true,                 ""LastUpdateAge"": 4,                 ""PublicId"":<Id_key1> ""42001a6ec3804d4305efb8538515395f4c6c521ff91c069e9e6fa2a404b33041"",                  ""StakeAmount"": <Amount of SN1 stake TX>,                 ""StakeExpiringBlock"": 340123,                 ""StakeFirstValidBlock"": 340001            }, ...` |

### Test #3 Existence of disqualification Tx of Type 1 for disqualified SN
  > As an owner of the SN, I want to check availability of the DisqTx of Type 1 and ensure the number of signatures is equal to 8.

##|Steps| Expected Result|
------|------|-----------------|
3.1|Open tx by Graft Blockchain Explorer and search your disq.Tx by Tx hash (see p.1.4.1)| Tx should be visible  in  Graft Blockchain Explorer|
3.2| Check key images|Tx cannot contain any key images|
3.3| Check mining fee| Tx  should have zero mining fee|
3.4| Check Disq SN| Disq SN should be only 1|
3.5| Check signatories| Signatories must be equal to 8 |

### Test #4 Disqualification of a SN by Type2 criteria (lack of response from SN in Auth Sample)
  > As an owner of 2 SNs, I want to make sure that my SNs are in the disqualification list (disqualification Type 2) and does not take part in the signing of RTA Tx (are not  in the BBL and AuthSample but present in the active SN list)

##|Steps| Expected Result|
------|------|-----------------|
4.1|To check the presence  SNs in BBL list run: `curl --header "Content-Type: application/json" --data '' --request GET http://<SN1 IP address>:28690/debug/blockchain_based_list/<block height> 2>/dev/null \| python -mjson.tool`| SNs should be present in  BBL:` … { "Address": "<Wallet_public_address1>",  "PublicId": "<Id_key1>","StakeAmount": <SN1 stake amount> }, { "Address": "<Wallet_public_address2>", "PublicId": "<Id_key2>","StakeAmount": <SN2 stake amount> },...`|
4.2|Shut down 2 SNs  `kill <# of the SN1  process in ubuntu>`, `kill <# of the SN2  process in ubuntu>` and wait 3-5 blocks| |
4.3| To check the absence  SNs in BBL list run: `curl --header "Content-Type: application/json" --data '' --request GET http://<SN1 IP address>:28690/debug/blockchain_based_list/<block height> 2>/dev/null \| python -mjson.tool` |SN1 and SN2 should be absent in BBL|
4.4| Select Disq.List and check SN in Disq.List| SN1 and SN2  should be present in Disq.List|
4.4.1| Save Tx hash for disqTX and Tx hash RTA tx for Test # 6||
4.4.2| Save DisqExpiringBlock Test # 5||
4.5| To check the presence of SNs in SN List run: `curl --header "Content-Type: application/json" --data '' --request GET http:/<SN1 IP address>:28690/debug/supernode_list/1 2>/dev/null \| python -mjson.tool` | SN and SN2  should be present in response - the SN List : `…{                ""Address"": ""<Wallet_public_address1>"",                ""AuthSampleBlockchainBasedListTier"": 0,                ""BlockchainBasedListTier"": 0,                ""IsAvailableForAuthSample"": false,                ""IsStakeValid"":true,                ""LastUpdateAge"": 4,                ""PublicId"":<Id_key1> ""42001a6ec3804d4305efb8538515395f4c6c521ff91c069e9e6fa2a404b33041"",                ""StakeAmount"": <Amount of SN1 stake TX>,                ""StakeExpiringBlock"": 340123,                ""StakeFirstValidBlock"": 340001            },…{                ""Address"": ""<Wallet_public_address2>"",                ""AuthSampleBlockchainBasedListTier"": 0,                ""BlockchainBasedListTier"": 0,                ""IsAvailableForAuthSample"": false,                ""IsStakeValid"":true,                ""LastUpdateAge"": 4,                ""PublicId"":<Id_key2> ""42001a6ec3804d4305efb8538515395f4c6c521ff91c069e9e6fa2a404b33041"",                ""StakeAmount"": <Amount of SN2 stake TX>,                ""StakeExpiringBlock"": 340123,                ""StakeFirstValidBlock"": 340001            },...`|

### Test #5 Unblocking SN disqualified by Type 2 criteria
  > As  SNs owner, I want to be sure that my 2 SNs unblocked for participation in signing Tx and added to BBList after Type 2 disqualification

##|Steps| Expected Result|
------|------|-----------------|
5.1|After  Test#4||
5.2|Run SN1:`./graftnoded --testnet --log-file /home/ubuntu/graft/GraftLog/` and wait for blockchain synchronization. Run SN2: `./graftnoded --testnet --log-file /home/ubuntu/graft/GraftLog/` and wait for blockchain synchronization.|In case of successful synchronization, you  can see on the screen information: `Synchronized OK`|
5.3| Wait Block height= DisqExpiringBlock + 5||
5.4| To check the appearance  of the  SNs in BBL list run: `curl --header "Content-Type: application/json" --data '' --request GET http://<SN1 IP address>:28690/debug/blockchain_based_list/<block height> 2>/dev/null \| python -mjson.tool`| SN should be present in  BBL: `… { "Address": "<Wallet_public_address1>", "PublicId": "<Id_key1>","StakeAmount": <SN1 stake amount> },… { "Address": "<Wallet_public_address2>", "PublicId": "<Id_key2>","StakeAmount": <SN2 stake amount> },...`|
5.5|Select Disq.List and check SN in Disq.List|SNs should be absent  in Disq.List|
5.6|To check the presence of the  SN in AuthSample List run: `curl --request GET http://<SN1 IP address>:28690/debug/auth_sample/aabbccddeeff 2>/dev/null \| python -mjson.tool` |SN1 and SN2  should be present in Auth Sample List: `...{                ""Address"": """<Wallet_public_address1>"",                ""AuthSampleBlockchainBasedListTier"": 1,                ""BlockchainBasedListTier"": 1,                ""IsAvailableForAuthSample"": true,                ""IsStakeValid"": true,                ""LastUpdateAge"": 24,                ""PublicId"": ""<Id_key1>"",                ""StakeAmount"": <SN1 stake amount>,                ""StakeExpiringBlock"": 340123,                ""StakeFirstValidBlock"": 340001            },…{                ""Address"": """<Wallet_public_address2>"",                ""AuthSampleBlockchainBasedListTier"": 1,                ""BlockchainBasedListTier"": 1,                ""IsAvailableForAuthSample"": true,                ""IsStakeValid"": true,                ""LastUpdateAge"": 24,                ""PublicId"": ""<Id_key2>"",                ""StakeAmount"": <SN1 stake amount>,                ""StakeExpiringBlock"": 340123,                ""StakeFirstValidBlock"": 340001            },...`|
5.7| To check the presence of SNs in SN List run: `curl --header "Content-Type: application/json" --data '' --request GET http:/<SN1 IP address>:28690/debug/supernode_list/1 2>/dev/null \| python -mjson.tool` | SN and SN2  should be present in response - the SN List : `…{                ""Address"": ""<Wallet_public_address1>"",                ""AuthSampleBlockchainBasedListTier"":<SN1 tier #>,                ""BlockchainBasedListTier"": <SN1 tier #>,                ""IsAvailableForAuthSample"": true,                ""IsStakeValid"":true,                ""LastUpdateAge"": 4,                ""PublicId"":<Id_key1> ""42001a6ec3804d4305efb8538515395f4c6c521ff91c069e9e6fa2a404b33041"",                ""StakeAmount"": <Amount of SN1 stake TX>,                ""StakeExpiringBlock"": 340123,                ""StakeFirstValidBlock"": 340001            },…{                ""Address"": ""<Wallet_public_address2>"",                ""AuthSampleBlockchainBasedListTier"": <SN2 tier #>,                ""BlockchainBasedListTier"": <SN2 tier #>,                ""IsAvailableForAuthSample"": true,                ""IsStakeValid"":true,                ""LastUpdateAge"": 4,                ""PublicId"":<Id_key2> ""42001a6ec3804d4305efb8538515395f4c6c521ff91c069e9e6fa2a404b33041"",                ""StakeAmount"": <Amount of SN2 stake TX>,                ""StakeExpiringBlock"": 340123,                ""StakeFirstValidBlock"": 340001            },...`|

### Test #6 Existence of disqualification Tx of Type 2 for disqualified SN
  > As an owner of the SNs, I want to check the availability of the DisqTx of Type 2 and  ensure the number of  signatories is equal to 6, and all 6 SN signed disqTx also signed the RTA Tx
  
##|Steps| Expected Result|
------|------|-----------------|
6.1| Open tx by Graft Blockchain Explorer and search your disqualification Tx by disq Tx hash (see p.4.4.1)| Tx should be visible  in the Graft Blockchain Explorer|
6.2| Check type of Tx| Tx must be disqualification|
6.3| Check key images| Tx cannot contain any key images|
6.4| Check mining fee| Tx should have zero mining fee|
6.5| Check Disq SNs| Disq SNs should be 2: SN1 and SN2|
6.6| Check signatures of disqTx| Disq Tx should be signed  by 6 SNs|
6.7| Open tx by Graft Blockchain Explorer and search Tx by RTA Tx hash (see p.4.4.1)|Tx should be visible  in  Graft Blockchain Explorer
6.8| Check type of Tx| Tx must be RTA|
6.9| Check signatures of RTA Tx| RTA Tx should be signed  by 6 SNs and there are 6 SNs that signed disq.Tx|

### Test #7 Disqualification policy
### Test #8 Unblocking  SN disqualified  by criteria of disqualification policy
### Test #9 Participation of an active SN to Qualification Sample
