import dotenv from 'dotenv'
import { ethers } from 'ethers'
var fs = require('fs');

import { analyzeTransaction } from './analyze'
import { decodeSequencerBatch } from './decode'
import { FourBytesApi } from './FourBytesApi'

function getEnv(key: string) {
  const value = process.env[key]
  if (!value) {
    throw new Error(`Env variable ${key} is not present!`)
  }
  return value
}

function getArgs() {
  if (process.argv.length !== 4) {
    printHelpAndExit()
  }
  const readFile = process.argv[2]
  const writeFile = process.argv[3]
  // if (!/^0x[a-f\d]{64}$/i.test(txHash)) {
  //   printHelpAndExit()
  // }
  return { readFile, writeFile }
}

function printHelpAndExit(): never {
  console.log('USAGE: yarn start [txhash]')
  process.exit(1)
}

export async function run() {
  dotenv.config()

  const alchemyApiKey = getEnv('ALCHEMY_API_KEY')
  const { readFile, writeFile } = getArgs()

  const rpcUrl = `https://eth-mainnet.alchemyapi.io/v2/${alchemyApiKey}`
  const provider = new ethers.providers.JsonRpcProvider(rpcUrl)
  const fourBytesApi = new FourBytesApi()

  // const { data, project } = await analyzeTransaction(provider, txHash)
  // const data = txHash;

  try {
    const jsonString = fs.readFileSync(readFile)
    const tx = JSON.parse(jsonString)
    const project = "Optimism OVM 2.0";
    await decodeSequencerBatch(project, tx.input, null, writeFile)
  } catch(err) {
    console.log(err)
    return
  }
}
