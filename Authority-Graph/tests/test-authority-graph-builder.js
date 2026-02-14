/**
 * Test Suite for Authority Graph Builder
 * 
 * Validates deterministic behavior, edge cases, and schema compliance
 */

const { buildAuthorityGraph, buildSingleWalletGraph, normalizeAmount } = require('../src/authority-graph-builder');

// Test helpers
function assertEqual(actual, expected, message) {
  const actualStr = JSON.stringify(actual);
  const expectedStr = JSON.stringify(expected);
  if (actualStr !== expectedStr) {
    throw new Error(`${message}\nExpected: ${expectedStr}\nActual: ${actualStr}`);
  }
  console.log(`✓ ${message}`);
}

function assertThrows(fn, message) {
  try {
    fn();
    throw new Error(`${message} - Expected error but none was thrown`);
  } catch (e) {
    if (e.message.includes('Expected error')) {
      throw e;
    }
    console.log(`✓ ${message}`);
  }
}

// Test 1: Basic single event transformation
function testBasicTransformation() {
  const events = [
    {
      wallet: "0xABC",
      contract: "0xTOKEN",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "1000000",
      block: 100,
      timestamp: 1712345678
    }
  ];
  
  const result = buildAuthorityGraph(events);
  
  const expected = {
    "0xABC": {
      wallet: "0xABC",
      authority_edges: [
        {
          type: "token_approval",
          contract: "0xTOKEN",
          target_entity: "0xDEX",
          amount: "1000000",
          block: 100,
          timestamp: 1712345678,
          revocation_possible: "UNKNOWN"
        }
      ]
    }
  };
  
  assertEqual(result, expected, "Basic single event transformation");
}

// Test 2: Amount normalization
function testAmountNormalization() {
  assertEqual(normalizeAmount("MAX_UINT"), "unlimited", "MAX_UINT → unlimited");
  assertEqual(normalizeAmount("UNLIMITED"), "unlimited", "UNLIMITED → unlimited");
  assertEqual(normalizeAmount(null), "unlimited", "null → unlimited");
  assertEqual(normalizeAmount(undefined), "unlimited", "undefined → unlimited");
  assertEqual(normalizeAmount("0"), "0", "Zero string");
  assertEqual(normalizeAmount(0), "0", "Zero number");
  assertEqual(normalizeAmount("1000000"), "1000000", "Regular amount string");
  assertEqual(normalizeAmount(1000000), "1000000", "Regular amount number");
}

// Test 3: Block ordering (determinism)
function testBlockOrdering() {
  const events = [
    {
      wallet: "0xABC",
      contract: "0xTOKEN1",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "100",
      block: 103,
      timestamp: 1712345690
    },
    {
      wallet: "0xABC",
      contract: "0xTOKEN2",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "200",
      block: 101,
      timestamp: 1712345670
    },
    {
      wallet: "0xABC",
      contract: "0xTOKEN3",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "300",
      block: 102,
      timestamp: 1712345680
    }
  ];
  
  const result = buildAuthorityGraph(events);
  const edges = result["0xABC"].authority_edges;
  
  assertEqual(edges[0].block, 101, "First edge is block 101");
  assertEqual(edges[1].block, 102, "Second edge is block 102");
  assertEqual(edges[2].block, 103, "Third edge is block 103");
  assertEqual(edges[0].amount, "200", "Correct amount for first edge");
  assertEqual(edges[1].amount, "300", "Correct amount for second edge");
  assertEqual(edges[2].amount, "100", "Correct amount for third edge");
}

// Test 4: Multiple wallets
function testMultipleWallets() {
  const events = [
    {
      wallet: "0xABC",
      contract: "0xTOKEN",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "100",
      block: 100,
      timestamp: 1712345678
    },
    {
      wallet: "0xDEF",
      contract: "0xTOKEN",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "200",
      block: 101,
      timestamp: 1712345680
    },
    {
      wallet: "0xABC",
      contract: "0xNFT",
      authority_type: "nft_approval",
      target_entity: "0xMARKET",
      amount: null,
      block: 102,
      timestamp: 1712345690
    }
  ];
  
  const result = buildAuthorityGraph(events);
  
  assertEqual(Object.keys(result).length, 2, "Two wallets in output");
  assertEqual(result["0xABC"].authority_edges.length, 2, "Wallet 0xABC has 2 edges");
  assertEqual(result["0xDEF"].authority_edges.length, 1, "Wallet 0xDEF has 1 edge");
}

// Test 5: Optional fields (tx_hash, log_index)
function testOptionalFields() {
  const events = [
    {
      wallet: "0xABC",
      contract: "0xTOKEN",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "100",
      block: 100,
      timestamp: 1712345678,
      tx_hash: "0xTX1",
      log_index: 5
    }
  ];
  
  const result = buildAuthorityGraph(events);
  const edge = result["0xABC"].authority_edges[0];
  
  assertEqual(edge.tx_hash, "0xTX1", "tx_hash preserved");
  assertEqual(edge.log_index, 5, "log_index preserved");
}

// Test 6: Deterministic sorting with tx_hash and log_index
function testDeterministicSorting() {
  const events = [
    {
      wallet: "0xABC",
      contract: "0xTOKEN1",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "100",
      block: 100,
      timestamp: 1712345678,
      tx_hash: "0xTX2",
      log_index: 1
    },
    {
      wallet: "0xABC",
      contract: "0xTOKEN2",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "200",
      block: 100,
      timestamp: 1712345678,
      tx_hash: "0xTX1",
      log_index: 0
    },
    {
      wallet: "0xABC",
      contract: "0xTOKEN3",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "300",
      block: 100,
      timestamp: 1712345678,
      tx_hash: "0xTX1",
      log_index: 2
    }
  ];
  
  const result = buildAuthorityGraph(events);
  const edges = result["0xABC"].authority_edges;
  
  // Same block, sorted by tx_hash then log_index
  assertEqual(edges[0].tx_hash, "0xTX1", "First by tx_hash");
  assertEqual(edges[0].log_index, 0, "First by log_index within tx");
  assertEqual(edges[1].log_index, 2, "Second by log_index within tx");
  assertEqual(edges[2].tx_hash, "0xTX2", "Last tx_hash");
}

// Test 7: Empty input
function testEmptyInput() {
  const result = buildAuthorityGraph([]);
  assertEqual(result, {}, "Empty array returns empty object");
}

// Test 8: Validation errors
function testValidationErrors() {
  assertThrows(
    () => buildAuthorityGraph("not an array"),
    "Rejects non-array input"
  );
  
  assertThrows(
    () => buildAuthorityGraph([{ contract: "0xTOKEN" }]),
    "Rejects event missing wallet"
  );
  
  assertThrows(
    () => buildAuthorityGraph([{ wallet: "0xABC" }]),
    "Rejects event missing contract"
  );
  
  assertThrows(
    () => buildAuthorityGraph([{
      wallet: "0xABC",
      contract: "0xTOKEN",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "100"
      // missing block and timestamp
    }]),
    "Rejects event missing block"
  );
}

// Test 9: Single wallet convenience method
function testSingleWalletGraph() {
  const events = [
    {
      wallet: "0xABC",
      contract: "0xTOKEN",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "100",
      block: 100,
      timestamp: 1712345678
    }
  ];
  
  const result = buildSingleWalletGraph(events);
  
  assertEqual(result.wallet, "0xABC", "Returns single wallet graph");
  assertEqual(result.authority_edges.length, 1, "Contains edges");
}

// Test 10: Determinism test (same input = same output)
function testDeterminism() {
  const events = [
    {
      wallet: "0xABC",
      contract: "0xTOKEN1",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "100",
      block: 103,
      timestamp: 1712345690
    },
    {
      wallet: "0xDEF",
      contract: "0xTOKEN2",
      authority_type: "token_approval",
      target_entity: "0xDEX",
      amount: "200",
      block: 101,
      timestamp: 1712345670
    }
  ];
  
  const result1 = buildAuthorityGraph(events);
  const result2 = buildAuthorityGraph(events);
  
  assertEqual(result1, result2, "Same input produces identical output");
}

// Run all tests
console.log("\n🧪 Running Authority Graph Builder Tests\n");

try {
  testBasicTransformation();
  testAmountNormalization();
  testBlockOrdering();
  testMultipleWallets();
  testOptionalFields();
  testDeterministicSorting();
  testEmptyInput();
  testValidationErrors();
  testSingleWalletGraph();
  testDeterminism();
  
  console.log("\n✅ All tests passed!\n");
} catch (error) {
  console.error("\n❌ Test failed:", error.message, "\n");
  process.exit(1);
}