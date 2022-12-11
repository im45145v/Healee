const {
  FileCreateTransaction,
  FileContentsQuery,
  PrivateKey,
  Hbar,
} = require("@hashgraph/sdk");
const hedera = require("@hashgraph/sdk");
const express = require("express");

const app = express();
app.use(express.json());
const port = 3000;

require("dotenv").config();

const accountId = process.env.ACCOUNT_ID;
const privateKey = process.env.PRIVATE_KEY;

// If we weren't able to grab it, we should throw an error
if (accountId == null || privateKey == null) {
  throw new Error(
    "Environment variables myAccountId and myPrivateKey must be present"
  );
}

const client = hedera.Client.forTestnet();

client.setOperator(accountId, privateKey);

app.get("/", (req, res) => {
  res.send(
    `That is not a valid endpoint hehe :)\n\n\n\nClient info: ${client.operatorAccountId}`
  );
});

app.get("/fetch", async (req, res) => {
  const fileId = req.body.fileId;
  if (!fileId) {
    throw new Error("fileId not provided! :(");
  }
  const query = new FileContentsQuery().setFileId(fileId);

  const contents = await query.execute(client);

  console.log(`File with id ${fileId} fetched!`);
  console.log(contents);
  res.json(JSON.parse(contents));
});

app.get("/add", async (req, res) => {
  console.log(req.body);
  const contents = JSON.stringify(req.body);
  const fileKey = PrivateKey.generateED25519();
  const filePubKey = fileKey.publicKey;
  console.log(`File length is ${contents.length}`);
  const transaction = await new FileCreateTransaction()
    .setKeys([filePubKey])
    .setContents(contents)
    .setMaxTransactionFee(new Hbar(2))
    .freezeWith(client);
  const signTx = await transaction.sign(fileKey);
  const submitTx = await signTx.execute(client);
  const receipt = await submitTx.getReceipt(client);

  const newFileId = receipt.fileId;
  console.log(`New File created with ID: ${newFileId}`);
  res.send(newFileId.toString());
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
