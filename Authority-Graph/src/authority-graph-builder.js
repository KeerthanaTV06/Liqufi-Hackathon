/**
 * PointZero Member C: Authority Graph Builder
 * 
 * Pure transformation layer that converts authority events into normalized graph structure.
 * - Deterministic: Same input always produces same output
 * - Lossless: Preserves all input data
 * - No inference: No risk scoring, no heuristics
 */

/**
 * Normalize amount field to consistent string representation
 * @param {string|number} amount - Raw amount value
 * @returns {string} Normalized amount
 */
function normalizeAmount(amount) {
  if (amount === null || amount === undefined) {
    return "unlimited";
  }
  
  const amountStr = String(amount).toUpperCase();
  
  // Handle common unlimited approval patterns
  if (amountStr === "MAX_UINT" || 
      amountStr === "UNLIMITED" || 
      amountStr.includes("115792089237316195423570985008687907853269984665640564039457584007913129639935")) {
    return "unlimited";
  }
  
  // Handle zero as string
  if (amountStr === "0") {
    return "0";
  }
  
  // Return as string to preserve precision
  return String(amount);
}

/**
 * Build authority graph from array of authority events
 * @param {Array} events - Array of authority transition events
 * @returns {Object} Wallet-grouped authority graph with normalized edges
 */
function buildAuthorityGraph(events) {
  // Validate input
  if (!Array.isArray(events)) {
    throw new Error("Input must be an array of events");
  }
  
  if (events.length === 0) {
    return {};
  }
  
  // Group events by wallet
  const walletGroups = {};
  
  for (const event of events) {
    // Validate required fields
    if (!event.wallet) {
      throw new Error("Event missing required field: wallet");
    }
    if (!event.contract) {
      throw new Error("Event missing required field: contract");
    }
    if (!event.authority_type) {
      throw new Error("Event missing required field: authority_type");
    }
    if (!event.target_entity) {
      throw new Error("Event missing required field: target_entity");
    }
    if (event.block === null || event.block === undefined) {
      throw new Error("Event missing required field: block");
    }
    if (event.timestamp === null || event.timestamp === undefined) {
      throw new Error("Event missing required field: timestamp");
    }
    
    const wallet = event.wallet;
    
    if (!walletGroups[wallet]) {
      walletGroups[wallet] = [];
    }
    
    // Build normalized edge
    const edge = {
      type: event.authority_type,
      contract: event.contract,
      target_entity: event.target_entity,
      amount: normalizeAmount(event.amount),
      block: Number(event.block),
      timestamp: Number(event.timestamp),
      revocation_possible: "UNKNOWN"
    };
    
    // Add optional fields if present
    if (event.tx_hash) {
      edge.tx_hash = event.tx_hash;
    }
    if (event.log_index !== null && event.log_index !== undefined) {
      edge.log_index = Number(event.log_index);
    }
    
    walletGroups[wallet].push(edge);
  }
  
  // Sort edges within each wallet group by block ascending
  // Secondary sort by tx_hash and log_index for determinism
  for (const wallet in walletGroups) {
    walletGroups[wallet].sort((a, b) => {
      // Primary: block number
      if (a.block !== b.block) {
        return a.block - b.block;
      }
      
      // Secondary: tx_hash (if present)
      if (a.tx_hash && b.tx_hash && a.tx_hash !== b.tx_hash) {
        return a.tx_hash.localeCompare(b.tx_hash);
      }
      
      // Tertiary: log_index (if present)
      if (a.log_index !== undefined && b.log_index !== undefined) {
        return a.log_index - b.log_index;
      }
      
      // Fallback: timestamp
      return a.timestamp - b.timestamp;
    });
  }
  
  // Build output format
  const results = {};
  
  for (const wallet in walletGroups) {
    results[wallet] = {
      wallet: wallet,
      authority_edges: walletGroups[wallet]
    };
  }
  
  return results;
}

/**
 * Build authority graph for a single wallet (convenience method)
 * @param {Array} events - Array of authority events for one wallet
 * @returns {Object} Single wallet authority graph
 */
function buildSingleWalletGraph(events) {
  const graphs = buildAuthorityGraph(events);
  const wallets = Object.keys(graphs);
  
  if (wallets.length === 0) {
    throw new Error("No events provided");
  }
  
  if (wallets.length > 1) {
    throw new Error("Multiple wallets detected. Use buildAuthorityGraph() for batch processing.");
  }
  
  return graphs[wallets[0]];
}

// Export functions
module.exports = {
  buildAuthorityGraph,
  buildSingleWalletGraph,
  normalizeAmount
};

// Example usage (commented out for library use)
/*
const exampleEvents = [
  {
    wallet: "0xABC",
    contract: "0xTOKEN",
    authority_type: "token_approval",
    target_entity: "0xDEX",
    amount: "MAX_UINT",
    block: 18392012,
    timestamp: 1712345678,
    tx_hash: "0xTX1",
    log_index: 0
  },
  {
    wallet: "0xABC",
    contract: "0xNFT",
    authority_type: "nft_approval_all",
    target_entity: "0xMARKET",
    amount: null,
    block: 18392015,
    timestamp: 1712345690,
    tx_hash: "0xTX2",
    log_index: 1
  },
  {
    wallet: "0xDEF",
    contract: "0xTOKEN",
    authority_type: "token_approval",
    target_entity: "0xDEX",
    amount: "1000000000000000000",
    block: 18392010,
    timestamp: 1712345670,
    tx_hash: "0xTX3",
    log_index: 0
  }
];

const graphs = buildAuthorityGraph(exampleEvents);
console.log(JSON.stringify(graphs, null, 2));
*/