#!/usr/bin/env python3

import pytest
from ptlibx import driver as drv
#from ptlibx import graft_crypto as gc
from ptlibx import libpy as gc

ss = drv.session

def generate_one_time_key_pair():
    pub_key = 'pub-key'
    sec_key = 'sec-key'

    print('One-time-key-pair - generated:\npub-key [{}]\nsec-key [{}]'.format(pub_key, sec_key))
    return pub_key, sec_key

def get_rta_payment_id(key):
    print('rta-payment-id: [{}]'.format(gc.get_rta_payment_id(key)))
    return gc.get_rta_payment_id(key)

def mk_rpc_presale(rta_payment_id):
    bl_num = 0
    bl_hash = 'block-hash'
    auth_sample = []
    pos_proxy_id = 'pos-proxy-id'
    pos_proxy_wallet_address = 'pos-proxy-wallet-address'

    print('rpc: presale (supposed to be processed by ProxySupernode)')
    return bl_num, bl_hash, auth_sample, pos_proxy_id, pos_proxy_wallet_address

def mk_rpc_sale(payment_data, msg_key_set):
    print('rpc: sale (to ProxySupernode)')
    return 0

def mk_rpc_get_payment_data(rpid, bl_num, bl_hash):
    print('rpc: get-payment-data (to Wallet ProxySupernode)')
    return 0

def mk_rpc_pay(tx_blob, tx_key, msg_key):
    print('rpc: pay (to Wallet-ProxySupernode)')
    return 0

def generate_pos_data_encryption_key():
    return gc.get_pos_data_encryption_key()

def serialize_and_encrypt_payment_data(pde_key):
    return ''

def get_amount():
    return 0

def collect_payment_data(amount, payment_data):
    return {}

def generate_message_key():
    msg_key = 'random-message-key'
    print('msg-key [{}]'.format(msg_key))
    return msg_key

def encrypt_with_MRME(data, key):
    return 'payment-data-encrypted-with-MRME'

def encrypt_msg_key_for_auth_sample(auth_sample, msg_key):
    return []

def generate_qr_msg(rta_payment_id, pos_public_address, bl_num, bl_hash, pub_key, pde_key):
    print('QR msg - generated')
    return {}

def build_and_sign_tx():
    tx_blob_raw = {}
    tx_pvt_key = ''
    print('Wallet: build-and-sign-tx')
    return tx_blob_raw, tx_pvt_key








#@pytest.mark.skip(reason = 'skip')
def test():
    tn = 'rta-tx: validation-flow-2'
    print('\n  ##  {} test is beginning ...'.format(tn))

    pos_public_address = 'pos-public-address'

    ####################################################################################
    # PoS-party
    ####################################################################################

    # 1
    # generation of one-time identification keypair
    pub_key, sec_key = generate_one_time_key_pair()

    # generate rta-payment-id
    rpid = get_rta_payment_id(pub_key)

    # RPC presale
    bl_num, bl_hash, auth_sample, pos_proxy_id, pos_proxy_wallet_address = mk_rpc_presale(rpid)

    # 2
    # PoS data encryption key
    pde_key = generate_pos_data_encryption_key()

    # encrypted serialized payment data
    espd = serialize_and_encrypt_payment_data(pde_key)

    # payment data collection
    pdc = collect_payment_data(get_amount(), espd)

    # generate random message key
    msg_key = generate_message_key()

    # encrypted payment data with Multiple Recipients Message Encryption
    epd = encrypt_with_MRME(pdc, msg_key)

    # encrypt message key for each supernode in auth-sample
    msg_keys_encrypted = encrypt_msg_key_for_auth_sample(auth_sample, msg_key)

    # RPC sale
    # send encrypted payment data and encrypted message key in the sale request to the
    # Proxy Supernode to be multicasted by Proxy Supernode to auth-sample supernodes
    mk_rpc_sale(epd, msg_keys_encrypted)

    # 3 - auth-sample supernodes receive sale request, decode and store data using
    # rta-payment-id

    # 4
    # PoS generates QR code for Wallet
    qr_msg = generate_qr_msg(rpid, pos_public_address, bl_num, bl_hash, pub_key, pde_key)

    ####################################################################################
    # wallet-party
    ####################################################################################

    # 5
    # RPC get_payment_data (by rpid, bl_num, bl_hash from qr-msg)
    mk_rpc_get_payment_data(rpid, bl_num, bl_hash)

    # 6, 7
    # Wallet ProxySupernode (WPS) receives requst and returns requested data
    # If WPS does not have requested data - it does request to the one of
    # auth-sample supernode. The requst is sent as uicast-async-message

    # 8
    # build graft tx, store data (... - see Spec) to transaction_header.extra
    # and sign tx
    tx_blob_raw, tx_pvt_key = build_and_sign_tx()

    some_key = 'so-far-its-unclear-where-to-get-the-real-key'

    # encrypt tx-blob
    tx_blob_encrypted = encrypt_with_MRME(tx_blob_raw, some_key)

    # encrypt tx-pvt-key
    tx_pvt_key_encrypted = encrypt_with_MRME(tx_pvt_key, some_key)
    # probably the tx-blob and this tx-pvt-key can be joined before ecryption

    # RPC pay - send pt WPS
    mk_rpc_pay(tx_blob_encrypted, tx_pvt_key_encrypted, msg_keys_encrypted)

    # 9
    # WPS multicast received data (encrypted tx, tx-pvt-key and msg-key)
    # to auth-sample supernodes and proxy supernodes

    # 10
    # every auth-sample supernode
    # - broadcasts signed pay status with status = payment_pending over the P2P network
    # - checks correctness of the selected auth sample
    # - validates transaction
    # - multicasts the signed transaction to other supernodes in the auth sample
    # It's not completely clear - should be some of these actions emulated/done in here?

    # 11
    # PoS/Wallet ProxySupernode actions on receiving data (encrypted tx, tx-pvt-key and msg-key)
    # - service fee validation
    # - if ok - sign tx with pvt-id-key
    # - store it in tx-extra field
    # - multicast signed tx to the other supernode in auth-sample

    # 12
    # - wait some time for receiving by PoS of 'status = payment_pending'
    # Once received - create the tx request and send it to Prox Supernode
    # UNKNOWN THING - here PoS does use some RPC request that is not designed yet
    # This RPC request should be implemented inside of Supernode

    # 13
    # PPS (PoS Proxy Supernode) unicasts received tx-request to random supernode
    # from auth-sample

    # 14
    # Supernode from auth-sample on receiving tx-request
    # - checks the signature
    # - if ok - encrypts tx-blob and tx-pvt-key with PoS public one-time id-key
    # and sends it to the PoS Proxy Supernode

    # 15
    # PoS Proxy Supernode receives the answer from an auth sample supernode, sends
    # encrypted transaction blob and transaction private key to the PoS.

    # 16
    # Once PoS received encrypted tx-blob and pvt-key it
    # - decrypts tx-blob and pvt-key
    # - validates tx and amount
    # - if ok
    #   - sign tx with PoS private one-time id-key
    #   - add the signature to the transaction.rta_signatures,
    #   - encrypts transaction using Multiple Recipients Message Encryption for auth sample supernodes
    # - if fail
    #   - creates "status fail" message, including status and signature generated using the PoS private one-time identification key
    #   - encrypts signed "status fail" message using Multiple Recipients Message Encryption for auth sample supernodes
    # - send to its Proxy Supernode

    # 17
    # Proxy Supernode multicasts data to supernodes from auth-sample

    # 18
    # Every supernode in auth-sample does the foloowing:
    # - if got fail then ...
    # - if got tx signed by PoS then


    # 19
    # each supernode in auth-sample check signatures and decides about Consensus

    # 20
    # graftnode validates:
    # - correctness of selected auth-sample
    # - PoS signature
    # - signature from each of auth-sample members
    # - Wallet and PoS Proxy Supernode signatures
    # - the tx itself

    # 21
    # broadcasting status 'successful pay' by supernode in case of success

    # 22
    # supernode updates status
    # checks signature

    # 23
    # update PoS and Wallet status
    # Since this code emulates PoS and Wallet - there is no need to check itself




