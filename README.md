# GRAFT TESTS
This Repository is designed to accumulate information about tests run on the GRAFT Blockchain components code.
We use following tests in debug:
- GRAFT auto tests
- Graft manual tests (acceptance and functionality tests)

We welcome your participation in GRAFT network testing and developing new tests.

# GRAFT auto tests
All Graft auto tests are located in tests/  directory.
To run autotests please use guide: https://github.com/graft-project/GraftNetwork/tree/master/tests

# Graft manual tests
Graft manual tests are  located in https://github.com/graft-project/graft-test/tree/master/acceptance_tests   directory. 
We use following acceptance  and functionality tests for Graft network debug:

## Disqualification Flow acceptance tests
Disqualification Flow acceptance tests are located in https://github.com/graft-project/graft-test/blob/master/acceptance_tests/%5BRFC-005-DF%5D-Disqualification-Flow-acceptance%20tests.md directory.

Disqualification Flow acceptance tests validate work of the GRAFT Network  in accordance with the design described in https://github.com/graft-project/DesignDocuments/blob/master/RFCs/%5BRFC-005-DF%5D-Disqualification-Flow.md
> Note:  Before running these tests, carefully read the environmental requirements.

## RTA Transaction acceptance tests
RTA transaction acceptance tests are located in  https://github.com/graft-project/graft-test/blob/master/acceptance_tests/%5BRFC-003-RTVF%5D-RTA%20Transaction%20Validation%20Flow%20-%20acceptance%20tests.md#rta-transaction-validation-flow---acceptance-tests

RTA transaction acceptance tests validate work of the GRAFT Network  in accordance with the design described in https://github.com/graft-project/DesignDocuments/blob/master/RFCs/%5BRFC-003-RTVF%5D-RTA-Transaction-Validation-Flow.md

>Note:  Before running these tests, carefully read the environmental requirements.

## CLI wallet functionality tests

[ToDo]

## Exchange Broker Network and Collateralized DEX acceptance tests

[ToDo]

Exchange Broker Network and Collateral DEX acceptance tests validate work of the GRAFT Network  in accordance with the design described in https://github.com/graft-project/DesignDocuments/blob/master/RFCs/%5BRFC-008-DDR%5D%20-%20DEX%20Design%20RFC.md#exchange-broker-network-and-collateralized-dex

## GRAFT 2/2 Multisig Light Wallet acceptance tests

GRAFT 2/2 Multisig Light Wallet acceptance tests are located in https://github.com/graft-project/graft-test/blob/master/acceptance_tests/%5BRFC-006-GMLW%5DGRAFT%20Multisig%20Light%20Wallet%20-%20acceptance%20test.md directory.

[ToDo]:  GRAFT 2/2 Multisig Light Wallet acceptance tests validate work of the GRAFT Network  in accordance with the design described in https://github.com/graft-project/DesignDocuments/blob/master/RFCs/%5BRFC-006-GMLW%5D%20GRAFT%20Multisig%20Light%20Wallet.md
 
## Writing new Graft tests

When writing new autotests, please implement all functions in .cpp or .c files, and only put function headers in .h files. This will help keep the fairly complex test suites somewhat sane going forward.
