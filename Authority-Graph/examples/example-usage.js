/**
 * Example Usage: Authority Graph Builder
 * 
 * Demonstrates real-world usage patterns for the PointZero Member C component
 */

const { buildAuthorityGraph, buildSingleWalletGraph } = require('../src/authority-graph-builder');

console.log("=".repeat(60));
console.log("EXAMPLE 1: Single Wallet with Multiple Authority Events");
console.log("=".repeat(60));

const example1 = [
  {
    wallet: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    contract: "0xdAC17F958D2ee523a2206206994597C13D831ec7", // USDT
    authority_type: "token_approval",
    target_entity: "0x1111111254EEB25477B68fb85Ed929f73A960582", // 1inch
    amount: "115792089237316195423570985008687907853269984665640564039457584007913129639935",
    block: 18392012,
    timestamp: 1712345678,
    tx_hash: "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
    log_index: 0
  },
  {
    wallet: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    contract: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
    authority_type: "token_approval",
    target_entity: "0x1111111254EEB25477B68fb85Ed929f73A960582", // 1inch
    amount: "MAX_UINT",
    block: 18392015,
    timestamp: 1712345690,
    tx_hash: "0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3",
    log_index: 1
  },
  {
    wallet: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    contract: "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", // BAYC NFT
    authority_type: "nft_approval_all",
    target_entity: "0x00000000000000ADc04C56Bf30aC9d3c0aAF14dC", // Seaport
    amount: null,
    block: 18392020,
    timestamp: 1712345700,
    tx_hash: "0x3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4",
    log_index: 0
  }
];

const graph1 = buildSingleWalletGraph(example1);
console.log(JSON.stringify(graph1, null, 2));

console.log("\n" + "=".repeat(60));
console.log("EXAMPLE 2: Multiple Wallets with Mixed Authority Types");
console.log("=".repeat(60));

const example2 = [
  {
    wallet: "0xAlice",
    contract: "0xTokenA",
    authority_type: "token_approval",
    target_entity: "0xDEX_Uniswap",
    amount: "1000000000000000000", // 1 token (18 decimals)
    block: 18392000,
    timestamp: 1712345600
  },
  {
    wallet: "0xBob",
    contract: "0xTokenB",
    authority_type: "token_approval",
    target_entity: "0xDEX_Sushiswap",
    amount: "MAX_UINT",
    block: 18392005,
    timestamp: 1712345650
  },
  {
    wallet: "0xAlice",
    contract: "0xNFT_Collection",
    authority_type: "nft_approval_all",
    target_entity: "0xMarketplace_OpenSea",
    amount: null,
    block: 18392010,
    timestamp: 1712345670
  },
  {
    wallet: "0xCharlie",
    contract: "0xTokenA",
    authority_type: "token_approval",
    target_entity: "0xDEX_Uniswap",
    amount: "0", // Revocation
    block: 18392012,
    timestamp: 1712345680
  },
  {
    wallet: "0xAlice",
    contract: "0xTokenA",
    authority_type: "token_approval",
    target_entity: "0xDEX_Pancakeswap",
    amount: "500000000000000000", // 0.5 token
    block: 18392008,
    timestamp: 1712345660
  }
];

const graphs2 = buildAuthorityGraph(example2);
console.log(JSON.stringify(graphs2, null, 2));

console.log("\n" + "=".repeat(60));
console.log("EXAMPLE 3: Deterministic Sorting (Same Block, Different Tx)");
console.log("=".repeat(60));

const example3 = [
  {
    wallet: "0xWallet1",
    contract: "0xContract3",
    authority_type: "token_approval",
    target_entity: "0xSpender",
    amount: "300",
    block: 1000,
    timestamp: 1712345678,
    tx_hash: "0xTxC",
    log_index: 2
  },
  {
    wallet: "0xWallet1",
    contract: "0xContract1",
    authority_type: "token_approval",
    target_entity: "0xSpender",
    amount: "100",
    block: 1000,
    timestamp: 1712345678,
    tx_hash: "0xTxA",
    log_index: 0
  },
  {
    wallet: "0xWallet1",
    contract: "0xContract2",
    authority_type: "token_approval",
    target_entity: "0xSpender",
    amount: "200",
    block: 1000,
    timestamp: 1712345678,
    tx_hash: "0xTxB",
    log_index: 1
  }
];

const graph3 = buildSingleWalletGraph(example3);
console.log(JSON.stringify(graph3, null, 2));
console.log("\nNote: Edges are sorted by tx_hash (0xTxA, 0xTxB, 0xTxC) even though");
console.log("they were provided in reverse order (C, A, B). This is deterministic.");

console.log("\n" + "=".repeat(60));
console.log("EXAMPLE 4: Amount Normalization Edge Cases");
console.log("=".repeat(60));

const example4 = [
  {
    wallet: "0xTest",
    contract: "0xToken1",
    authority_type: "token_approval",
    target_entity: "0xSpender",
    amount: "MAX_UINT",
    block: 1000,
    timestamp: 1712345678
  },
  {
    wallet: "0xTest",
    contract: "0xToken2",
    authority_type: "token_approval",
    target_entity: "0xSpender",
    amount: null,
    block: 1001,
    timestamp: 1712345679
  },
  {
    wallet: "0xTest",
    contract: "0xToken3",
    authority_type: "token_approval",
    target_entity: "0xSpender",
    amount: 0,
    block: 1002,
    timestamp: 1712345680
  },
  {
    wallet: "0xTest",
    contract: "0xToken4",
    authority_type: "token_approval",
    target_entity: "0xSpender",
    amount: "1000000000000000000",
    block: 1003,
    timestamp: 1712345681
  }
];

const graph4 = buildSingleWalletGraph(example4);
console.log(JSON.stringify(graph4, null, 2));
console.log("\nNote: MAX_UINT and null → 'unlimited', 0 → '0', regular amounts preserved");

console.log("\n" + "=".repeat(60));
console.log("All examples demonstrate:");
console.log("✓ Deterministic output (same input = same output)");
console.log("✓ Lossless transformation (all data preserved)");
console.log("✓ Proper sorting (block, tx_hash, log_index)");
console.log("✓ Amount normalization (unlimited, 0, regular)");
console.log("✓ No inference or scoring (pure transformation)");
console.log("=".repeat(60));