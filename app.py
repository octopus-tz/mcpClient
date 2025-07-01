import asyncio
import json
import logging
from langchain_mcp_adapters.client import MultiServerMCPClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache MCP clients by server key
mcp_clients = {}

# Define available MCP servers
SERVER_CONFIGS = {
    'weavely': {
        'transport': 'sse',
        'url': 'https://mcp.weavely.ai/sse',
    },
    'cloudflare': {
        'transport': 'sse',
        'url': 'https://demo-day.mcp.cloudflare.com/sse',
    },
    # Add more if needed
}

# Retrieve or initialize the appropriate MCP client
def get_mcp_client(server_key):
    if server_key not in SERVER_CONFIGS:
        raise ValueError(f"Unknown server key: {server_key}")
    if server_key not in mcp_clients:
        mcp_clients[server_key] = MultiServerMCPClient({server_key: SERVER_CONFIGS[server_key]})
    return mcp_clients[server_key]

# Lambda entry point
def lambda_handler(event, context):
    logger.info("Lambda invoked")

    # Default values
    query = "What events are listed for demo day?"
    server_key = "cloudflare"

    # Parse POST body if present
    try:
        if "body" in event and event["body"]:
            body = json.loads(event["body"])
            query = body.get("query", query)
            server_key = body.get("server", server_key)
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": '{"error": "Invalid JSON in request body."}'
        }

    try:
        # Run async logic
        response = asyncio.run(handle_request(query, server_key))
        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": response
        }
    except Exception as e:
        logger.exception("Failed to process request")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Async MCP interaction
async def handle_request(query, server_key):
    client = get_mcp_client(server_key)

    logger.info(f"Fetching tools from MCP server [{server_key}]...")
    tools = await client.get_tools()

    if not tools:
        return json.dumps({"error": "No tools found on MCP server."})

    tool = tools[0]
    args = {"query": query}

    logger.info(f"Invoking tool {tool.name} with args: {args}")
    result = await tool.ainvoke(args)

    return json.dumps({"result": result})

