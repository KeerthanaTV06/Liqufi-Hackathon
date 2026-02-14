/**
 * ASCII Art Visualization of Authority Graph
 * 
 * Creates a text-based visualization that can be viewed in terminal
 */

const { buildAuthorityGraph } = require('../src/authority-graph-builder');

/**
 * Generate ASCII visualization of authority graph
 */
function visualizeGraphASCII(authorityData) {
    console.log('\n' + '═'.repeat(80));
    console.log('                    🔐 AUTHORITY GRAPH VISUALIZATION');
    console.log('═'.repeat(80) + '\n');

    Object.entries(authorityData).forEach(([walletAddr, walletData], walletIndex) => {
        // Wallet header
        console.log(`\n┌${'─'.repeat(76)}┐`);
        console.log(`│ 👤 WALLET: ${walletAddr.padEnd(62)} │`);
        console.log(`└${'─'.repeat(76)}┘`);

        walletData.authority_edges.forEach((edge, edgeIndex) => {
            const isLast = edgeIndex === walletData.authority_edges.length - 1;
            const connector = isLast ? '└' : '├';
            const line = isLast ? ' ' : '│';

            // Contract info
            const contractIcon = edge.type.includes('nft') ? '🎨' : '💰';
            console.log(`  ${connector}──${contractIcon} CONTRACT: ${edge.contract}`);
            console.log(`  ${line}     │`);
            console.log(`  ${line}     ├─ Type: ${edge.type}`);
            console.log(`  ${line}     ├─ Amount: ${edge.amount}`);
            console.log(`  ${line}     ├─ Block: ${edge.block}`);
            console.log(`  ${line}     │`);

            // Target entity
            const targetIcon = edge.target_entity.includes('Swap') ? '🔄' : '🏪';
            console.log(`  ${line}     └──▶ ${targetIcon} TARGET: ${edge.target_entity}`);
            
            if (!isLast) {
                console.log(`  ${line}`);
            }
        });
    });

    console.log('\n' + '═'.repeat(80));
    console.log('Legend: 👤 Wallet | 💰 Token | 🎨 NFT | 🔄 DEX | 🏪 Marketplace');
    console.log('═'.repeat(80) + '\n');
}

/**
 * Generate a more detailed tree visualization
 */
function visualizeGraphTree(authorityData) {
    console.log('\n' + '╔'.repeat(80));
    console.log('                    AUTHORITY GRAPH - TREE VIEW');
    console.log('╚'.repeat(80) + '\n');

    const stats = {
        totalWallets: 0,
        totalEdges: 0,
        totalContracts: new Set(),
        totalTargets: new Set()
    };

    Object.entries(authorityData).forEach(([walletAddr, walletData]) => {
        stats.totalWallets++;
        stats.totalEdges += walletData.authority_edges.length;

        walletData.authority_edges.forEach(edge => {
            stats.totalContracts.add(edge.contract);
            stats.totalTargets.add(edge.target_entity);
        });
    });

    // Print statistics
    console.log('📊 GRAPH STATISTICS:');
    console.log('─'.repeat(50));
    console.log(`   Wallets:          ${stats.totalWallets}`);
    console.log(`   Authority Edges:  ${stats.totalEdges}`);
    console.log(`   Unique Contracts: ${stats.totalContracts.size}`);
    console.log(`   Unique Targets:   ${stats.totalTargets.size}`);
    console.log('─'.repeat(50) + '\n');

    // Print detailed tree
    Object.entries(authorityData).forEach(([walletAddr, walletData], walletIndex) => {
        const isLastWallet = walletIndex === Object.keys(authorityData).length - 1;
        const walletConnector = isLastWallet ? '└──' : '├──';
        const walletLine = isLastWallet ? '   ' : '│  ';

        console.log(`${walletConnector} 👤 ${walletAddr}`);

        walletData.authority_edges.forEach((edge, edgeIndex) => {
            const isLastEdge = edgeIndex === walletData.authority_edges.length - 1;
            const edgeConnector = isLastEdge ? '└──' : '├──';
            const edgeLine = isLastEdge ? '   ' : '│  ';

            const contractIcon = edge.type.includes('nft') ? '🎨' : '💰';
            const targetIcon = edge.target_entity.toLowerCase().includes('swap') ? '🔄' : '🏪';

            console.log(`${walletLine}${edgeConnector} ${contractIcon} ${edge.contract}`);
            console.log(`${walletLine}${edgeLine}   ├─ [${edge.type}]`);
            console.log(`${walletLine}${edgeLine}   ├─ Amount: ${edge.amount}`);
            console.log(`${walletLine}${edgeLine}   ├─ Block: ${edge.block}`);
            console.log(`${walletLine}${edgeLine}   └─▶ ${targetIcon} ${edge.target_entity}`);
            
            if (!isLastEdge) {
                console.log(`${walletLine}│`);
            }
        });

        if (!isLastWallet) {
            console.log('│');
        }
    });

    console.log('\n' + '═'.repeat(80) + '\n');
}

/**
 * Generate a matrix-style visualization
 */
function visualizeGraphMatrix(authorityData) {
    console.log('\n' + '▓'.repeat(80));
    console.log('                    AUTHORITY MATRIX VIEW');
    console.log('▓'.repeat(80) + '\n');

    // Collect all unique contracts and targets
    const contracts = new Set();
    const targets = new Set();

    Object.values(authorityData).forEach(walletData => {
        walletData.authority_edges.forEach(edge => {
            contracts.add(edge.contract);
            targets.add(edge.target_entity);
        });
    });

    const contractList = Array.from(contracts);
    const targetList = Array.from(targets);

    console.log('WALLET → CONTRACT → TARGET RELATIONSHIPS:\n');

    Object.entries(authorityData).forEach(([walletAddr, walletData]) => {
        console.log(`\n🔹 ${walletAddr}`);
        console.log('   ' + '─'.repeat(70));

        // Create matrix
        const matrix = {};
        walletData.authority_edges.forEach(edge => {
            const key = `${edge.contract}→${edge.target_entity}`;
            matrix[key] = edge;
        });

        contractList.forEach(contract => {
            const hasContract = walletData.authority_edges.some(e => e.contract === contract);
            if (hasContract) {
                const contractIcon = walletData.authority_edges.find(e => e.contract === contract).type.includes('nft') ? '🎨' : '💰';
                console.log(`   ${contractIcon} ${contract}`);

                targetList.forEach(target => {
                    const key = `${contract}→${target}`;
                    if (matrix[key]) {
                        const edge = matrix[key];
                        console.log(`      └─▶ ${target} [${edge.amount}]`);
                    }
                });
            }
        });
    });

    console.log('\n' + '▓'.repeat(80) + '\n');
}

// Example usage
if (require.main === module) {
    const sampleEvents = [
        {
            wallet: "0xAlice",
            contract: "0xUSDT",
            authority_type: "token_approval",
            target_entity: "0xUniswap",
            amount: "unlimited",
            block: 18392000,
            timestamp: 1712345600
        },
        {
            wallet: "0xAlice",
            contract: "0xUSDC",
            authority_type: "token_approval",
            target_entity: "0xUniswap",
            amount: "1000000000000000000",
            block: 18392005,
            timestamp: 1712345650
        },
        {
            wallet: "0xAlice",
            contract: "0xBAYC_NFT",
            authority_type: "nft_approval_all",
            target_entity: "0xOpenSea",
            amount: "unlimited",
            block: 18392010,
            timestamp: 1712345670
        },
        {
            wallet: "0xBob",
            contract: "0xUSDT",
            authority_type: "token_approval",
            target_entity: "0xSushiSwap",
            amount: "unlimited",
            block: 18392008,
            timestamp: 1712345660
        },
        {
            wallet: "0xBob",
            contract: "0xDAI",
            authority_type: "token_approval",
            target_entity: "0xUniswap",
            amount: "500000000000000000",
            block: 18392012,
            timestamp: 1712345680
        },
        {
            wallet: "0xCharlie",
            contract: "0xCryptoPunks",
            authority_type: "nft_approval_all",
            target_entity: "0xOpenSea",
            amount: "unlimited",
            block: 18392015,
            timestamp: 1712345690
        }
    ];

    console.log('🔨 Building authority graph...\n');
    const authorityGraph = buildAuthorityGraph(sampleEvents);

    // Show all visualization styles
    visualizeGraphASCII(authorityGraph);
    visualizeGraphTree(authorityGraph);
    visualizeGraphMatrix(authorityGraph);

    console.log('✅ Visualization complete!\n');
}

module.exports = {
    visualizeGraphASCII,
    visualizeGraphTree,
    visualizeGraphMatrix
};
