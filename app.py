import asyncio
import logging
from langchain_mcp_adapters.client import MultiServerMCPClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔁 Reuse across warm starts
mcp_client = None

def get_mcp_client():
    global mcp_client
    if mcp_client is None:
        mcp_client = MultiServerMCPClient({
            'cloudflare': {
                'transport': 'sse',
                'url': 'https://mcp.weavely.ai/sse',
                #'url': 'https://demo-day.mcp.cloudflare.com/sse',
            }
        })
    return mcp_client

# Lambda entrypoint
def lambda_handler(event, context):
    logger.info("Lambda invoked")

    # Extract user input from the API Gateway event
    query = event.get("queryStringParameters", {}).get("query", "What events are listed for demo day?")

    # Run async MCP logic
    response = asyncio.run(handle_request(query))

    # Return the response to API Gateway
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": response
    }

# Async logic to run MCP interaction
async def handle_request(query):
    client = get_mcp_client()

    logger.info("Fetching tools from MCP server...")
    tools = await client.get_tools()

    if not tools:
        return '{"error": "No tools found on MCP server."}'

    tool = tools[0]

    args = {"query": query}
    logger.info(f"Invoking tool {tool.name} with args: {args}")
    result = await tool.ainvoke(args)

    return f'"{result}"'
