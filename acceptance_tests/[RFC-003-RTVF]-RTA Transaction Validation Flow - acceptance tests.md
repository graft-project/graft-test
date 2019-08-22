# RTA Transaction Validation Flow - acceptance tests

## Prerequisites

### Environment:

1. **OS**: Ubuntu **18.04** LTS Bionic

||Build Requirements|Run Requirements|
|-----|-----|-----|
|RAM, GB|8|2|
|CPU, Cores|2|2|
|Storage, GB|100|100|

> Note: In order to GraftNode (also called the cryptonode) work properly 28680 (P2P) port should be opened for incoming and outgoing traffic. If you are using other ports, please, make sure that you are open P2P port of the cryptonode.

2. RTA network - 3 seeds with mining
3. 5 additional AWS EC2 instances with Ununtu 18.04:
   
   3.1. 4 instances with  installed and synchronized  SN + 1 instance without installed and synchronized  graftnode and SN
   
   3.2. 11 wallets:
   
     - 7 stake wallets  for 8 Supernode stakes. 1 stake wallet should work for 2 Supernodes. Each Wallet should have GRFT 350000.00 amount. 
     - 2 wallets for Proxy SN and Wallet Proxy SN
     - 1 wallet for Customer. The wallet should have amount >0 (for example, GRFT1000.00) for payment to merchant. 
     - 1 wallet for Merchant.

#### Test Result description:

|||
|--|---|
|**Ok**|Test passed successfully|
|**Critical**|Brokers errors that make it impossible to pass the general wallet flow (scenario)|
|**Major**|Important (but not brokers) errors that significantly affect the passage of the main scenario, but which can be circumvented or replaced by an alternative solution|
|**Minor**|Errors that inconvenience in the work and which can be solved in an alternative way|
|**Untested**|Сommand not tested|

## TESTS:

### a) Supernode Staking

|##|Description|User Story|
|------|------|-----|
|Test #1|Verify SN synchronization | As a SN owner I want to make sure that my SN is synchronized with Graft Network and ready to work|
|Test #2|Stake Transaction  with insufficient  T1 funds |As a SN owner I want to send stake Tx and want to make sure that network  controls stake amount|
|Test #3|Stake Transaction  with exact T1 funds | As a SN owner I want to participate in the signing of RTA tx. For that I should send Stake Tx and then I should be  included to BBL if my Tx amount >=amount for Tier 1|
|Test #4|Stake Transaction with extra  funds (enough for T2) |As a SN owner I want to raise the Stake Tier level. For that I send additional Stake Tx with amount >= amount for Tier 2 - my previous Stake amount.Note: stake period of  additional Stake Tx should be minimal (for Test 4)|
|Test #5|Continue Stake with T1 funds after expired Stake with T2|As a SN owner I want to continue my participation in the RTA Tx signing with T1 after expired Stake with T2|
|Test #6|SN receives locked amount after expired Stake with T2|As a SN owner I want to receive unlocked amount of additional Stake Tx  after expired Stake with T2|
|Test #7|Stake Transaction with between T3-T4 funds|As a SN owner I want to raise the Stake Tier level. For that I send additional Stake Tx with amount >= amount for Tier 3 - my previous Stake amounts+delta.|
|Test #8|Stake Transaction  with T4 funds|As a SN owner I want to raise the Stake Tier level. For that I send additional Stake Tx with amount >= amount for Tier 4 - my previous Stake amounts.|
|Test #9|Stake multiple transactions|As a SN owner I cannot make a multiple Stake Tx|
|Test#10|Stake  Transactions for  2 SNs from  1 stake  wallet|As an owner of 2 SN I  want to make Stakes for my 2  SNs  from 1 stake wallet|
|Test#11|AuthSample with number of SNs less than 8| As a Merchant (or a Customer) I want to make sure  that in AuthSample participate not less than 8 SNs for acceptance  of RTA Transaction|
|Test#12|Bring SN back up -> verify that qualified again| As a SN owner I want to make sure  that my SN should participate in the  acceptance  of RTA Transaction after restart |
|Test#13|RTA Transaction with number of signers less than 6| As a Merchant (or a Customer) I want to make sure that RTA Transaction accepted not less than 6 SN from AuthSample|
|Test#14|Stake Transaction  with stake period less than minimum allowed limit| As a SN owner I want to make sure that system controls minimum  allowed stake period in the Stake transaction - it cannot be less than 60|



### b) RTA Tx Flow

|##|Description|User Story|
|-----|-----|-----|
|Test#15|Generation of info for RTA transaction (QR-code or Json) |As a Merchant I want to sale my good in cryptocurrency and generate QR code in my PoS programm|
|Test#16|Customer pays for purchase |As a Customer I want to pay for my purchase by reading QR code and acceptance RTA transaction from ny cryptocurrency Graft wallet|
|Test#17|Merchant receives payment  for goods sold|As a Merchant I want to receive payment for sold good |
|Test#18|SN receives Fee for the participation in Auth Sample List|As a SN  owner I want to get a Fee for the participation in Auth Sample List|
|Test#19|Proxy SN receives Fee for the participation in a signing of RTA Transaction|As a Proxy SN  owner I want to get a Fee for the participation in a signing of RTA Transaction|
|Test#20|Wallet Proxy SN receives Fee for the participation in a signing of RTA Transaction|As a Wallet Proxy SN  owner I want to get a Fee for the participation in a signing of RTA Transaction|
|Test#21|Failed RTA Transaction transfer due to non-receipt of 6 signatures at the scheduled time|As a Merchant I want to receive  info about unsuccessful Transaction and about.As a Customer I want to receive  info about unsuccessful Transaction and about |
|Test#22|Failed RTA Transaction transfer due to non-receipt of response at the scheduled time|As a Customer I want to receive  info  about the end of the waiting time of successful RTA Tx|


## Details

### Supernode Staking

### Test#1: Verify SN synchronization

1.1. Install SN with : https://github.com/graft-project/graft-ng/wiki/Supernode-Install-&-Usage-Instruction

1.2. Synchronize SN with : https://github.com/graft-project/graft-ng/wiki/Supernode-Install-&-Usage-Instruction#graft-supernode-configuration

**_Expected Result_**: 

displayed info `Synchronization OK `

1.3. Run stake wallet:

```ruby
./graft-wallet-cli --wallet-file SN1 \--password "" --testnet --trusted-daemon --daemon-address localhost:28681
```
where :
- **SN1** - Wallet_name - name of your wallet, which you opened for this SN

- **SN1_testpsw -Wallet_Psw** - psw to your wallet, which you opened for this SN (in our case is empty)

**_Expected Result_** (for example):

```ruby
Balance: 299999.9856666400, unlocked balance: 299999.9856666400 
Refresh done, blocks received: 185634 
Currently selected account: [0] Primary account 
Tag: (No tag assigned) 
[wallet F6qk6a]:
```



### Test#2 Stake Transaction  with insufficient  T1 funds 


2.1 Being in the Ubuntu run command:
```ruby
curl --request GET http://localhost:28690/dapi/v2.0/cryptonode/getwalletaddress
```
**_Expected Result_**:
```ruby
{"testnet":true,
"wallet_public_address":"F6qk6a...",
"id_key":"4014fcfb….",
"signature":"45f78cd..."}
```
2.2 Save info:
- **wallet_public_address** - as a stake_wallet_address_1
- **Id_key** - as a Supernode_public_ID_key_1
- **Signature** - as a SuperNode_Signature_1

2.3 Run wallet :

```ruby
./graft-wallet-cli --wallet-file SN1 \--password "" --testnet --trusted-daemon --daemon-address localhost:28681
```
where :

- **SN1** - Wallet_name - name of your wallet, which you opened for this SN
- **SN1_testpsw -Wallet_Psw** - psw to your wallet, which you opened for this SN (in our case is empty)

2.4 Send Stake transaction with amount = GRFT40000 and stake period = 5000
```ruby
stake_transfer <stake_wallet_address_1> 40000 5000 <Supernode_public_ID_key_1> <SuperNode_Signature_1>
```
**_Expected Result_**:

```ruby
…
Stake amount 40000.000000 is less than the minimum supernode stake 50000.000000; are you sure you want to submit this partial stake? (Y/Yes/N/No): 
```

Enter  `Y`

```ruby
…
Transaction successfully submitted, transaction <1fb70...>
You can check its status by using the `show_transfers` command.
```
2.5 Exit from wallet.

2.6 Run API to get SN List info

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```
**_Expected Result_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 0,
               ""BlockchainBasedListTier"": 0,
               ""IsAvailableForAuthSample"": false,
               ""IsStakeValid"": false,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""4014fcfb…."",
               ""StakeAmount"": 40000,
                  "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
}
…
```


### Test#3 Stake Transaction  with exact T1 funds 


3.1. After Test#2

3.2. Send New Stake Transaction with amount GRFT10001 and stake period = 5000

```ruby
stake_transfer <stake_wallet_address_1> 10001 5000  <Supernode_public_ID_key_1> <SuperNode_Signature_1>
```

**_Expected Result_**:

```ruby
Transaction successfully submitted, transaction <3fd81...>
You can check its status by using the `show_transfers` command.
```
3.3 Exit from wallet.

3.4 Run API to get SN List info

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```
where:

- `18.210.158.2` - IP address is not your Supernode

**_Expected Result_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 0,
               ""BlockchainBasedListTier"": 0,
               ""IsAvailableForAuthSample"": false,
               ""IsStakeValid"": false,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""4014fcfb…."",
               ""StakeAmount"": 40000,
              "StakeExpiringBlock": 316210,
                "StakeFirstValidBlock": 311211
}
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 1,
                "BlockchainBasedListTier": 1,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 10001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
 ```

3.5 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address of your SN
- **bc height** - height of blockchain

**_Expected Result_**:

```ruby
…
{
                   "Address": ""F6qk6a..."",
                   "PublicId": ""4014fcfb…."",
                   "StakeAmount": 500010000000000
               },
…
```

3.6 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address of your SN

**_Expected Result_**:

```ruby
{
                "Address": ""F6qk6a..."",
                "ExpiringBlock": 316217,
                "LastUpdateAge": 130,
                "PublicId": ""4014fcfb…."",
                "StakeAmount": 500010000000000
            },
```

### Test#4 Stake Transaction with extra  funds (enough for T2) 


4.1 After Test#3

4.2. Send New Stake Transaction with amount GRFT40001 and stake period = 60

```ruby
stake_transfer <stake_wallet_address_1> 40001 60  <Supernode_public_ID_key_1> <SuperNode_Signature_1>
```

**_Expected Result_**:

```ruby
Transaction successfully submitted, transaction <4dcf1...>
You can check its status by using the `show_transfers` command.
```
4.3  Run `balance` command and save result

**_Expected Result_** (for example):

```ruby
Balance: 150007.2131303450, unlocked balance: 50005.2131303450
```
4.4. Exit from wallet.

4.5 Run API to get SN List info

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```
where:

- `18.210.158.2` - IP address is not your Supernode

**_Expected Result_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 0,
               ""BlockchainBasedListTier"": 0,
               ""IsAvailableForAuthSample"": false,
               ""IsStakeValid"": false,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""4014fcfb…."",
               ""StakeAmount"": 40000,
               ""StakeExpiringBlock"": 311270
               ""StakeFirstValidBlock"": 311210
}
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 1,
                "BlockchainBasedListTier": 1,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 10001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 2,
                "BlockchainBasedListTier": 2,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 40001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
```

4.6 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address of your SN
- **bc height** - height of blockchain

**_Expected Result_**:

```ruby
…
{
                   "Address": ""F6qk6a..."",
                   "PublicId": ""4014fcfb…."",
                   "StakeAmount": 900020000000000
               },
…
```

4.7 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address of your SN

**_Expected Result_**:

```ruby
{
                "Address": ""F6qk6a..."",
                "ExpiringBlock": 316217,
                "LastUpdateAge": 130,
                "PublicId": ""4014fcfb…."",
                "StakeAmount": 900020000000000
            },
```

### Test#5 Continue Stake with T1 funds after expired Stake with T2

5.1 After Test#3

5.2 Wait 60 blocks

5.3 Run API to get SN List info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```
where:
`18.210.158.2` - IP address is not your Supernode

**_Expected Result:_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 0,
               ""BlockchainBasedListTier"": 0,
               ""IsAvailableForAuthSample"": false,
               ""IsStakeValid"": false,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""4014fcfb…."",
               ""StakeAmount"": 40000,
               ""StakeExpiringBlock"": 311270
               ""StakeFirstValidBlock"": 311210
}
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 1,
                "BlockchainBasedListTier": 1,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 10001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
```
5.4 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address of your SN
- **bc height** - height of blockchain

**_Expected Result_**:

```ruby
…
{
                   "Address": ""F6qk6a..."",
                   "PublicId": ""4014fcfb…."",
                   "StakeAmount": 500010000000000
               },
…
```

5.5 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address your SN

**_Expected Result_**:

```ruby
{
                "Address": ""F6qk6a..."",
                "ExpiringBlock": 316217,
                "LastUpdateAge": 130,
                "PublicId": ""4014fcfb…."",
                "StakeAmount": 500010000000000
            },
 ```


### Test#6 SN receives locked amount after expired Stake with T2


6.1 After Test#5

6.2 Run stake wallet:

```ruby
./graft-wallet-cli --wallet-file SN1 \--password "" --testnet --trusted-daemon --daemon-address localhost:28681
```

where :

- **SN1** - Wallet_name - name of your wallet, which you opened for this SN
- **SN1_testpsw -Wallet_Psw** - psw to your wallet, which you opened for this SN (in our case is empty)

**_Expected Result:_** (for example):

```ruby
Balance: 150007.2131303450, unlocked balance: 50005.2131303450
Refresh done, blocks received: 185634
Currently selected account: [0] Primary account
Tag: (No tag assigned)
[wallet F6qk6a]:
```

6.3 Run `balance` command and check  wallet amount with saved result from Test#4

**_Expected Result:_**:

Stake amount (40001 - Mining Reward) should be returned to the stake wallet

_(for example):_

Test#4:

```ruby
Balance: 150007.2131303450, unlocked balance: 50005.2131303450
```
Now:

```ruby
Balance: 190997.2131303450, unlocked balance: 90995.2131303450
```


### Test#7 Stake Transaction with between T3-T4 funds


7.1 After Test#6

7.2 Send New Stake Transaction with amount GRFT100001 and stake period = 5000:

```ruby
stake_transfer <stake_wallet_address_1> 100001 5000 <Supernode_public_ID_key_1> <SuperNode_Signature_1>
```
**_Expected Result_**:

```ruby
Transaction successfully submitted, transaction <3fd81...>
You can check its status by using the `show_transfers` command.
```
7.3 Exit from wallet.

7.4 Run API to get SN List info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```

where:

- `18.210.158.2` - IP address is not your Supernode

**_Expected Result_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 0,
               ""BlockchainBasedListTier"": 0,
               ""IsAvailableForAuthSample"": false,
               ""IsStakeValid"": false,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""4014fcfb…."",
               ""StakeAmount"": 40000,
              "StakeExpiringBlock": 316210,
                "StakeFirstValidBlock": 311211
}
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 1,
                "BlockchainBasedListTier": 1,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 10001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 3,
                "BlockchainBasedListTier": 3,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 100001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
```

7.5 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address your SN
- **bc height** - height of blockchain

**_Expected Result_**:

```ruby
…
{
                   "Address": ""F6qk6a..."",
                   "PublicId": ""4014fcfb…."",
                   "StakeAmount": 1500020000000000
               },
…
```

7.6 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address of your SN

**_Expected Result_**:

```ruby
{
                "Address": ""F6qk6a..."",
                "ExpiringBlock": 316217,
                "LastUpdateAge": 130,
                "PublicId": ""4014fcfb…."",
                "StakeAmount": 1500020000000000
            },
```


### Test #8 Stake Transaction  with T4 funds


8.1 After Test#7

8.2 Send New Stake Transaction with amount GRFT100001 and stake period = 5000:

```ruby
stake_transfer <stake_wallet_address_1> 100001 5000 <Supernode_public_ID_key_1> <SuperNode_Signature_1>
```

**_Expected Result_**:

```ruby
Transaction successfully submitted, transaction <3fd81...>
You can check its status by using the `show_transfers` command.
```

8.3 Exit from wallet.

8.4 Run API to get SN List info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```

where:

- `18.210.158.2` - IP address is not your Supernode

**_Expected Result:_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 0,
               ""BlockchainBasedListTier"": 0,
               ""IsAvailableForAuthSample"": false,
               ""IsStakeValid"": false,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""4014fcfb…."",
               ""StakeAmount"": 40000,
              "StakeExpiringBlock": 316210,
                "StakeFirstValidBlock": 311211
}
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 1,
                "BlockchainBasedListTier": 1,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 10001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 3,
                "BlockchainBasedListTier": 3,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 100001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
{
                "Address":""F6qk6a..."",
                "AuthSampleBlockchainBasedListTier": 4,
                "BlockchainBasedListTier": 4,
                "IsAvailableForAuthSample": true,
                "IsStakeValid": true,
                "LastUpdateAge": 86,
                "PublicId":""4014fcfb…."",
                "StakeAmount": 100001,
                "StakeExpiringBlock": 316217,
                "StakeFirstValidBlock": 311218
            },
…
```

8.5 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```
where :

- `23.20.194.109` - IP address your SN
- **bc height** - height of blockchain

**_Expected Result_**:

```ruby
…
{
                   "Address": ""F6qk6a..."",
                   "PublicId": ""4014fcfb…."",
                   "StakeAmount": 2500030000000000
               },
…
```

8.6 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```
where :
- `23.20.194.109` - IP address your SN

**_Expected Result_**:
```ruby
{
                "Address": ""F6qk6a..."",
                "ExpiringBlock": 316217,
                "LastUpdateAge": 130,
                "PublicId": ""4014fcfb…."",
                "StakeAmount": 2500030000000000
            },
```


### Test #9 Stake multiple transactions


9.1 After Test#8 (or open stake wallet)

9.2 Send New Stake Transaction with 2 amounts GRFT10001 and stake period = 5000:

```ruby
stake_transfer <stake_wallet_address_1> 10001 5000 <Supernode_public_ID_key_1> <SuperNode_Signature_1> <stake_wallet_address_1> 10001 5000 <Supernode_public_ID_key_1> <SuperNode_Signature_1>
```

**_Expected Result_**:

You cannot send Stake multiple transaction :

```ruby
Error: stake transaction must be sent to a single destination
```


### Test#10 Stake  Transactions for  2 SNs from  1 stake  wallet


10.1 After Test#9

10.2 Save parameters of  SN1 stake wallet: 

10.2.1 Save stake wallet name1, address1 and password1

10.2.2 Run `seed` and save result:

**_Expected Result_**:

```ruby
NOTE: the following 25 words can be used to recover access to your wallet. Write them down and store them somewhere safe and secure. Please do not store them in your email or on file storage services outside of your immediate control.

lemon evenings invoke total vastness inkling yeti zeal
tufts oxidant elite boil skirting habitat jockey ongoing 
goblet broken unfit vein violin drowning biggest biplane invoke
```
10.3 In the new window open instance with SN2

10.4  Restore stake wallet 1 to run :

```ruby
./graft-wallet-cli --testnet --restore-deterministic-wallet --electrum-seed "<seed1>" --generate-new-wallet  <wallet_name1> --restore-height 1
```
where:

- **Seed1** - saved seed for stake wallet1 (p.10.2.2)
- **Wallet_name1** - name of stake wallet1

10.5 Kill supernode process

```ruby
kill  <supernode process number>
```
10.6 Go to config.ini and enter address1 (p.10.2.1) as stake-wallet

10.7 Run supernode process with https://github.com/graft-project/graft-ng/wiki/Supernode-Install-&-Usage-Instruction#graft-supernode-configuration 


**_Expected Result_**: displayed info `Synchronization OK `

10.8 Run command:

```ruby
curl --request GET http://localhost:28690/dapi/v2.0/cryptonode/getwalletaddress
```

**_Expected Result_**:

```ruby
{"testnet":true,
"wallet_public_address":"F6qk6a...",
"id_key":"5014fcfb….",
"signature":"55f78cd..."}
```
10.9 Save info:

- **wallet_public_address** - should be a stake_wallet_address_1
- **Id_key** - as a Supernode_public_ID_key_2
- **Signature** - as a SuperNode_Signature_2

10.10 Run wallet :

```ruby
./graft-wallet-cli --wallet-file SN1 \--password "" --testnet --trusted-daemon --daemon-address localhost:28681
```
where :

- **SN1** - Wallet_name - name of your wallet, which you opened for this SN
- **SN1_testpsw -Wallet_Psw** - psw to your wallet, which you opened for this SN (in our case is empty)

10.11 Send Stake transaction with amount = GRFT50001 and stake period = 5000:

```ruby
stake_transfer <stake_wallet_address_1> 50001 5000 <Supernode_public_ID_key_2> <SuperNode_Signature_2>
```

**_Expected Result_**:

```ruby
Transaction successfully submitted, transaction <1fb70...>
You can check its status by using the `show_transfers` command.
```
10.12 Run `balance` command and save balance

**_Expected Result_** (for example): 

```ruby
Balance: 150007.2131303450, unlocked balance: 50005.2131303450
```
10.13 Exit from wallet

10.14 Run API to get SN List info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```

where:
- `18.210.158.2 `- IP address is not your Supernode

**_Expected Result_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 1,
               ""BlockchainBasedListTier"": 1,
               ""IsAvailableForAuthSample"": true,
               ""IsStakeValid"": true,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""5014fcfb…."",
               ""StakeAmount"": 50001,
              "StakeExpiringBlock": 316210,
                "StakeFirstValidBlock": 311211
}
…
```

10.15 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```

where :

- `23.20.194.109` - IP address of your SN
- **bc height** - height of blockchain

**_Expected Result_**:

```ruby
…
{
                   "Address": ""F6qk6a..."",
                   "PublicId": ""5014fcfb…."",
                   "StakeAmount": 500010000000000
               },
…
```

10.16 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```

where :

- `23.20.194.109` - IP address your SN

**_Expected Result_**:

```ruby
{
                "Address": ""F6qk6a..."",
                "ExpiringBlock": 316217,
                "LastUpdateAge": 130,
                "PublicId": ""5014fcfb…."",
                "StakeAmount": 500010000000000
            },
```

10.17 Run stake wallet:

```ruby
./graft-wallet-cli --wallet-file SN1 \--password "" --testnet --trusted-daemon --daemon-address localhost:28681
```
where :

- **SN1** - Wallet_name - name of your wallet, which you opened for this SN
- **SN1_testpsw -Wallet_Psw** - psw to your wallet, which you opened for this SN (in our case is empty)


10.18   Run `balance` command and check  balance with result from p.10.12

**_Expected Result:_** (for example): 

P.10.12 

```ruby
Balance: 150007.2131303450, unlocked balance: 50005.2131303450
```
Now: 

```ruby
Balance: 100006.2131303450, unlocked balance: 4.2131303450
```


### Test#11 AuthSample with number of SNs less than 8


> Note: for this test we need only 8 supernodes with stake transactions.

11.1 After Test#10

11.2 Exit wallet

11.3 Kill supernode process:

```ruby
kill <number of supernode process>
```
11.4 Wait  2 blocks (about 5 min)

11.5 Run API to get SN List info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null \| python -mjson.tool
```

where:

- `18.210.158.2` - IP address is not your Supernode

**_Expected Result_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 0,
               ""BlockchainBasedListTier"" : 0,
               ""IsAvailableForAuthSample"":false,
               ""IsStakeValid"": true,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""5014fcfb…."",
               ""StakeAmount"": 50001,
              "StakeExpiringBlock": 316210,
                "StakeFirstValidBlock": 311211
}
…
```

11.6 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```

where :

- `23.20.194.109` - IP address your SN
- **bc height** - height of blockchain

**_Expected Result_**:

SN2 is absent in the Blockchain Base List


11.7 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```

where :

- `23.20.194.109` - IP address your SN2

**_Expected Result_**:

SN2 is absent in the Auth Sample List


### Test#12 Bring SN back up -> verify that qualified again


12.1 After Test#11

12.2 Run supernode with https://github.com/graft-project/graft-ng/wiki/Supernode-Install-&-Usage-Instruction#graft-supernode-configuration 

**_Expected Result_**: 

displayed info `Synchronization OK` 
 
12.3 Wait 2 blocks (about 5 min)

12.4 Run API to get SN List info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://18.210.158.2:28690/debug/supernode_list/1 2>/dev/null | python -mjson.tool
```

where:

- `18.210.158.2` - IP address is not your Supernode

**_Expected Result_**:

```ruby
…
{
               ""Address"": ""F6qk6a..."",
               ""AuthSampleBlockchainBasedListTier"": 1,
               ""BlockchainBasedListTier"": 1,
              ""IsAvailableForAuthSample"": true,
               ""IsStakeValid"": true,
               ""LastUpdateAge"": 4,
               ""PublicId"": ""5014fcfb…."",
               ""StakeAmount"": 50001,
              "StakeExpiringBlock": 316210,
                "StakeFirstValidBlock": 311211
}
…
```

12.5 Run API to get Blockchain Base List (BBL) info:

```ruby
curl --header "Content-Type: application/json" --data '' --request GET http://23.20.194.109:28690/debug/blockchain_based_list/<bc height> 2>/dev/null | python -mjson.tool
```

where :

- `23.20.194.109` - IP address your SN
- **bc height** - height of blockchain

**_Expected Result_**:

```ruby
…
{
                   "Address": ""F6qk6a..."",
                   "PublicId": ""5014fcfb…."",
                   "StakeAmount": 500010000000000
               },
…
```

12.6 Run API to get Auth Sample List info:

```ruby
curl --request GET http://23.20.194.109:28690/debug/auth_sample/aabbccddeeff" 2>/dev/null | python -mjson.tool
```

where :

- `23.20.194.109` - IP address your SN

**_Expected Result_**:

```ruby
{
                "Address": ""F6qk6a..."",
                "ExpiringBlock": 316217,
                "LastUpdateAge": 130,
                "PublicId": ""5014fcfb…."",
                "StakeAmount": 500010000000000
            },
```


### Test#13 RTA Transaction with number of signers less than 6

> Note: for this test we need only 8 supernodes with stake transactions.

13.1 After Test#12

13.2 Run cli-wallet:

```ruby
./graft-wallet-cli --wallet-file Cli_wallet \--password "<testpsw>" --testnet --trusted-daemon --daemon-address localhost:28681
```

where :

- **Cli_wallet** - Wallet_name - name of your cli wallet
- **testpsw -Wallet_Psw** - psw to your wallet, which you opened for this SN (in our case is empty)


13.3 Send RTA transaction with GRFT10 amount and wait:

```ruby
transfer_rta <wallet address> 10
```

Where:

- **wallet address** - recipient's  address

**_Expected Result_**:

```ruby
Wallet password:
Unencrypted payment IDs are bad for privacy: ask the recipient to use subaddresses instead
tx type: 0

Transaction 1/1:
Spending from address index 0
Sending 10.0000000000.  The transaction fee is 1.0000000000
Is this okay?  (Y/Yes/N/No):
```
and stop on this step

13.4  In another window of this instance kill supernode process:

```ruby
kill <number of supernode process>
```
13.5 Return to previous window and continue RTA transaction:

Enter  `Y` 

**_Expected Result_**:

```ruby
Error:
```

13.6 Go to second window with killed supernode process and run it again with https://github.com/graft-project/graft-ng/wiki/Supernode-Install-&-Usage-Instruction#graft-supernode-configuration :

```ruby
./supernode --log-file <path_to_log_file> >/dev/null 2>&1 &
```

13.7 Wait 2 blocks (about 5 min)

13.8 Send RTA transaction again and  response to all requirements with GRFT10 amount:

```ruby
transfer_rta <wallet address> 10
```
where:

- **wallet address** - recipient's  address

**_Expected Result_**:

```ruby
Transaction successfully submitted, transaction <1f34b...>
You can check its status by using the `show_transfers` command.
```


### Test#14 Stake Transaction  with stake period less than minimum allowed limit


14.1 After Test#13

14.2 Being in cli-wallet (or reopen stake wallet) send stake transaction with stake period equal 1:

```ruby
stake_transfer <stake_wallet_address_1> 50001 1 <Supernode_public_ID_key_2> <SuperNode_Signature_2>
```

**_Expected Result_**:

```ruby
You cannot send stake transaction with stake period less than minimum required 60

Error: locked blocks number 1 is less than minimum required 60
```



### RTA Tx Flow

Calculation example: https://docs.google.com/spreadsheets/d/1Trcrko854IvxZ2sE_MwLa6M8ut-xwByujAP-NLwDmgM/edit#gid=0

![2019-08-22_17-38-32](https://user-images.githubusercontent.com/45132833/63523940-c314ba00-c503-11e9-8c2d-cbb2d1fb058c.png)

 
>NOTE: Before test you should save balances of all wallets:
>- Stake wallets of 8 SNS , who participates in signing of RTA Transaction
>- Customer's  wallet
>- Merchant's wallet
>- Proxy SN's wallet
>- Wallet Proxy SN's wallet

### Test#15 Generation of information for a RTA Transaction

15.1 Order good with price GRFT10 (or enter  GRFT10 in the sale functionality)

15.2 Press “Sale” button (or enter)

**_Expected Result_**:

```ruby
Sending 1000.0000000000.  The transaction fee is 1.000000000
The RTA fee is 7.00000000000
Is this okay?  (Y/Yes/N/No): 
```
After enter `Y` you should get  QR-code or Json with following information about Transaction:

```ruby
Sending - 1000.0000000000
Transaction fee - 1.0000000000
RTA fee - 7.0000000000
SN1 fee - 0.625
SN2 fee - 0.625
SN3 fee - 0.625
SN4 fee - 0.625
SN5 fee - 0.625
SN6 fee - 0.625
SN7 fee - 0.625
SN8 fee - 0.625
Proxy SN fee  - 1.00000000
Wallet Proxy SN fee - 1.00000000
```

### Test#16 Customer pays for purchase

16.1 After Test#15

16.2 Customer should open his Graft Wallet and scan (or copy/paste) QR code/information from Test#15

**_Expected Result_**:

```ruby
Sending 1000.0000000000.  The transaction fee is 1.000000000
The RTA fee is 7.0000000000
Is this okay?  (Y/Yes/N/No): 
```

16.3 Customer should press `pay` button in his wallet

**_Expected Result_**:

After 5 sec Customer should get  information about successful transaction.
Amount = 1000 grft should be locked in the Customer's wallet balance.


### Test#17 Merchant receives payment  for goods sold


17.1 After Test#16

17.2 Merchant  should get information about successful payment for purchase sold.

17.3 Wait 16-17 blocks (about 30-40 min)

**_Expected Result_**:

Balance of Merchant's wallet should be risen on  GRFT992.0000000

### Test#18 SN receives Fee for the participation in Auth Sample List

18.1 After Test#17

18.2 **_Expected Result_**:

Balance of the stake wallet of each SN, who participated in Auth Sample,  should be risen on  GRFT0.625


### Test#19 Proxy SN receives Fee for the participation in a signing of RTA Transaction

19.1 After Test#17

19.2 **_Expected Result:_**

Balance of the wallet of Proxy SN participated in signing of RTA Transaction  should be risen on  GRFT 1.0000


### Test#20 Wallet Proxy SN receives Fee for the participation in a signing of RTA Transaction

20.1 After Test#17

20.2 **_Expected Result_**:

Balance of the wallet of Wallet Proxy SN participated in signing of RTA Transaction  should be risen on  GRFT 1.0000


### Test#21 Failed RTA Transaction transfer due to non-receipt of 6 signatures at the scheduled time

> Note: Before this test you should open 3 additional  window of instances with su[ernodes in stake 

21.1 Repeat Test#15

21.2 Repeat Test#16 before p.16.3

21.3 Go to  the  window of the other instance with SN that is in stake and participates in the Auth Sample List and kill supernode process:

```ruby
kill <number of supernode process>
```
21.4 Repeat p.21.3 for 2 another SNs 

21.5 Return to window with opened Customer's wallet and and continue RTA transaction

**_Expected Result_**:

```ruby
Error: 
```

### Test#22 Failed RTA Transaction transfer due to non-receipt of response at the scheduled time

> Note: Before this test you should have 8 SNs in a stake 

22.1 Repeat Test#15 

22.2 Wait 7 blocks (about 15 min)

**_Expected Result_**:

```ruby
Error: transaction time is out
```
