import algosdk from 'algosdk';
import * as fs from 'fs/promises';

const ALGONODE_TOKEN = 'no token required';
const ALGONODE_SERVER = 'https://testnet-api.algonode.cloud';
const ALGONODE_PORT = '443';

const client = new algosdk.Algodv2(
  ALGONODE_TOKEN,
  ALGONODE_SERVER,
  ALGONODE_PORT
);

let account = algosdk.generateAccount();


let compileProgram = async(client: algosdk.Algodv2, target: string): Promise < Uint8Array > => {
    let data = await fs.readFile(target)
    let compileResponse = await client.compile(data).do()
    return new Uint8Array(Buffer.from(compileResponse.result, "base64"));
}

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

let setup = async function() {
    console.log("Waiting for funds from faucet for address " + account.addr + " ...")
    console.log("Visit: https://bank.testnet.algorand.network/?account=" + account.addr)
    while (true) {
        let accountInfo = await client.accountInformation(account.addr).do();
        if (accountInfo.amount > 0) {
            break;
        }
        await new Promise(r => setTimeout(r, 100));
    }

    let manager = await compileProgram(client, "auction.teal")
    let clear = await compileProgram(client, "clear.teal")
    let localInts = 4
    let localBytes = 4
    let globalInts = 0
    let globalBytes = 1
    console.log("Deploying contract:")
    let params = await client.getTransactionParams().do();
    const contract_txn = algosdk.makeApplicationCreateTxn(account.addr, params, algosdk.OnApplicationComplete.NoOpOC, manager,
        clear, localInts, localBytes, globalInts, globalBytes, []);
    let tx_result1 = await postTransaction([contract_txn], client)
    console.log("Contract created with id:", tx_result1.id)
    fs.writeFile("public_info.json",
        JSON.stringify(
        {
            "CTF_Address": account.addr,
            "AppID": tx_result1.id.toString()
        })
    )
    fs.writeFile("private_info.json",
        JSON.stringify(
        {
            "CTF_PrivateKey": account.sk.toString()
        })
    )
}

setup()
