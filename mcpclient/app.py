import asyncio
import json
import logging
import google.generativeai as genai
from langchain_mcp_adapters.client import MultiServerMCPClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache MCP clients by server key
mcp_clients = {}

# Define available MCP servers
# Load server configs once
def load_server_configs(path='mcpServers.json'):
    with open(path, 'r') as f:
        return json.load(f)

# Lazy-load the config only once
SERVER_CONFIGS = load_server_configs()

def get_mcp_client(server_key):
    if server_key not in SERVER_CONFIGS:
        raise ValueError(f"Unknown server key: {server_key}")
    if server_key not in mcp_clients:
        mcp_clients[server_key] = MultiServerMCPClient({server_key: SERVER_CONFIGS[server_key]})
    return mcp_clients[server_key]

def lambda_handler(event, context):
    logger.info("Lambda invoked")

    # Default values
    prompt = "Create a form with 4 questions on history for Greece"
    server_key = "weavely"

    # Parse POST body if present
    try:
        if "body" in event and event["body"]:
            body = json.loads(event["body"])
            prompt = body.get("prompt", prompt)
            server_key = body.get("server", server_key)

            if server_key not in SERVER_CONFIGS:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Unknown server key: {server_key}"})
                }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in request body."})
        }

    try:
        # Run async logic synchronously for Lambda
        response = asyncio.run(handle_request(prompt, server_key))
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": response
        }
    except Exception as e:
        logger.exception("Failed to process request")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

async def handle_request(prompt, server_key):
    client = get_mcp_client(server_key)

    logger.info(f"Fetching tools from MCP server [{server_key}]...")
    tools = await client.get_tools()

    if not tools:
        return json.dumps({"error": "No tools found on MCP server."})

    # Log all tools and their args schema for debugging
    for i, tool in enumerate(tools):
        logger.info(f"Tool #{i}: {tool.name}")
        logger.info(f"Description: {tool.description}")
        logger.info(f"Args schema: {json.dumps(tool.args_schema, indent=2)}")

    tool = tools[0]

    # Determine argument key to use based on tool's args schema
    args = {}
    props = tool.args_schema.get("properties", {})

    if "prompt" in props:
        args["prompt"] = prompt
    elif "query" in props:
        args["query"] = prompt
    elif "text" in props:
        args["text"] = prompt
    else:
        # If no known key found, put prompt under first key if exists
        keys = list(props.keys())
        if keys:
            args[keys[0]] = prompt
        else:
            return json.dumps({"error": "Tool does not accept any arguments."})

    logger.info(f"Invoking tool {tool.name} with args: {args}")
    result = await tool.ainvoke(args)

    return json.dumps({"result": result})

async def load_mcp_servers(path='mcp_servers.json'):
    with open(path, 'r') as f:
        return json.load(f)
    
if __name__ == "__main__":
    # Set your desired test prompt and server
    prompt = "Mitel"
    server_key = "gdrive"

    # Run the async handler manually
    response = asyncio.run(handle_request(prompt, server_key))
    print("Response from MCP server:")
    print(response)

    genai.configure(api_key="AIzaSyCWVFRKpjFnuFICr4QdqSmJOSeSQPHP_wE")
    #for m in genai.list_models():
    #    print(m.name, m.supported_generation_methods)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content("Which are the contents of google drive folder and details?" + response)
    print(response.text)