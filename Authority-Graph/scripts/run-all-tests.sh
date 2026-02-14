#!/bin/bash

# Run All Tests Script for Member C Authority Graph Builder
# Tests both JavaScript and Python implementations

echo "=========================================="
echo "Member C Authority Graph Builder"
echo "Running All Tests"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track failures
FAILED=0

# Test JavaScript
echo -e "${YELLOW}Testing JavaScript Implementation...${NC}"
echo ""
node tests/javascript/test-authority-graph-builder.js
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ JavaScript tests passed${NC}"
else
    echo -e "${RED}✗ JavaScript tests failed${NC}"
    FAILED=1
fi
echo ""

# Test Python
echo -e "${YELLOW}Testing Python Implementation...${NC}"
echo ""
python tests/python/test_authority_graph_builder.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python tests passed${NC}"
else
    echo -e "${RED}✗ Python tests failed${NC}"
    FAILED=1
fi
echo ""

# Run examples
echo -e "${YELLOW}Running JavaScript Example...${NC}"
echo ""
node examples/javascript/example-usage.js > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ JavaScript example ran successfully${NC}"
else
    echo -e "${RED}✗ JavaScript example failed${NC}"
    FAILED=1
fi
echo ""

echo -e "${YELLOW}Running Python Example...${NC}"
echo ""
python examples/python/example_usage.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python example ran successfully${NC}"
else
    echo -e "${RED}✗ Python example failed${NC}"
    FAILED=1
fi
echo ""

# Summary
echo "=========================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo "=========================================="
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    echo "=========================================="
    exit 1
fi