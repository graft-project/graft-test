GRAFT 2/2 Multisig Light Wallet - TESTS
Design
[RFC-006-GMLW] GRAFT Multisig Light Wallet.md

Components
Wallet Backend (WB)
Light Client Wallet (LCW)
Third Independent Wallets - 2  (WTI1 and WTI2)

Prerequisites
LCW should be installed on Mobile phone. Wallet mustn`t contain any transactions. Balance should be equal 0.
WB should be installed on any device (?). Wallet mustn`t contain any transactions. Balance should be equal 0.
Third wallets should be installed on any device and must have amount>0 (GRFT1000 is possible).

Acceptance tests

Create backend wallet
Сheck balance WB and LCW 
Check transfer regular Tx and Tx time
3.1 Check transfer regular Tx with 1 output and Tx time
3.2 Check transfer regular Tx with 2 outputs and Tx time
Check Sync between WB and LCW
4.1 Check Sync on the Tx level
4.2 Check Blockchain synchronization
Check Tx size

Steps 

Step
Description
##
Test Result
1
Create backend wallet
1.1
Open LCW


You can see the main screen LCW
1.2
Push button/run function  “Create WB”


You can see dialog request for entering the WB address
1.3
Enter in data field WB address


You can receive information about  your backend wallet:
Address
Balance
BC height 

1.4
Check WB and LCW balances 


WB balance should be equal LCW balance
1.5
Check WB and LCW Key Images


WB key image should be equal LCW key image
2
Сheck balance WB and LCW
2.1
Check balance in LCW and WB


Both balances should be equal
2.2
Close LCW




2.3
Go to WTI and make regular Tx from WTI to WB


Transfer <WB address> 100
2.4
Send Tx


Balance WTI should be decrease on sum=100 +Fee for mining
2.5
Check balance 


WB balance should be equal 100
2.6
Open LCW and check balance


LCW  balance must be equal 100
3
Check transfer regular Tx and Tx time
3.1
Check transfer regular Tx with 1 output and Tx time
3.1.1
Go to LCW and make regular Tx from LCW  to WTI1


Transfer <WTI1 address> 10
3.1.2
Send Tx


System should require sign
3.1.3
Check time request from system


Request must received in N = 2 sec
3.1.4
Sign Tx


System should response OK
3.1.5
Check time request from system


Request must received in M <= 30 sec
3.1.6
Check balance


Balance must be equal GRFT100, amount = 10+Fee for mining should be locked
3.1.7
Wait 15-20 min




3.1.8
Check balance


Balance must be equal GRFT90-Fee for mining, locked amount  should be equal 0
3.2
Check transfer regular Tx with 2 outputs and Tx time
3.2.1
Go to LCW and make regular Tx from LCW  to WTI1


Transfer <WTI1 address> 10 <WTI2 address> 20
3.2.2
Send Tx


System should require sign
3.2.3
Check time request from system


Request must received in N = 2 sec
3.2.4
Sign Tx


System should response OK
3.2.5
Check time request from system


Request must received in M <= 30 sec
3.2.6
Check balance


Balance must be equal GRFT100, amount = 30+Fee for mining should be locked
3.2.7
Wait 15-20 min




3.2.8
Check balance


Balance must be equal GRFT70 - Fee for mining, locked amount  should be equal 0
4
Check Sync between WB and LCW
4.1
Check Sync on the Tx level
4.1.1
Close WB




4.1.2
Go to LCW  check balance


Save balance Amount1= balance amount
4.1.3
Make regular Tx


Transfer <WTI1 address> 10
4.1.4
Send Tx


You can receive ERROR ???
4.1.5
Open WB




4.1.6
Go to LCW and make regular Tx


Transfer <WTI1 address> 10
4.1.7
Send Tx


System should require sign
4.1.8
Close WB




4.1.9
Go to LCW and sign Tx


You can receive ERROR ???
4.1.10
Open WB




4.1.11
Go to LCW and make regular Tx


Transfer <WTI1 address> 10
4.1.12
Send Tx


System should require sign
4.1.13
Sign Tx


System should response OK
4.1.14
Wait 15-20 min




4.1.15
Check balance


Balance must be equal Amount1-10 - Fee for mining, locked amount  should be equal 0
4.1.16
Go to WB and check balance


WB balance should be equal LCW balance
4.2
Check Blockchain synchronization
4.2.1
Open LCW and check Blockchain height


bc_heihgt
4.2.2
Open WB and check Blockchain height


bc_heihgt
4.2.3
Close WB




4.2.4
Wait 10-15 min




4.2.5
Check Blockchain height in LCW


Bc_heihgt should be equal last  value
4.2.6
Open WB and resync


refresh
4.2.7
Check Blockchain height


bc_heihgt
4.2.8
Go to LCW and check Blockchain height


LCW bc_heihgt should be equal WB bc_heihgt
5
Check Tx size
5.1
Go to WB and search payment_id for regular Tx to 1 output WTI1




5.2
Go to Blockchain Explorer and search Tx by payment_ID


Blockchain Explorer should show Yx detail on the screen 
5.3
Check Tx size


Tx sice should be <=3 Kb

