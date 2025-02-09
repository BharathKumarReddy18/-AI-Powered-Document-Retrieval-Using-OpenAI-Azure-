import logging
import os
import json
import azure.functions as func
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from azure.search.documents.models import VectorizedQuery, VectorFilterMode
from azure.search.documents import SearchItemPaged

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")


search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_API_KEY),
)


def initialize_openai_client():
    endpoint = os.getenv("OPENAI_ENDPOINT")
    api_key = os.getenv("OPENAI_API_KEY")
    api_version = os.getenv("API_VERSION")

    if not all([endpoint, api_key, api_version]):
        raise ValueError(
            "One or more environment variables for OpenAI are missing or invalid."
        )

    return AzureOpenAI(
        azure_endpoint=endpoint, api_key=api_key, api_version=api_version
    )


def generate_embeddings(embedding_client, text):
    emb = embedding_client.embeddings.create(model="text-embedding-3-small", input=text)
    res = json.loads(emb.model_dump_json())
    return res["data"][0]["embedding"]


def perform_vector_search_and_remove_duplicates(
    search_client, query_vector, Category=None
):
    filter_condition = f"Category eq '{Category}'" if Category else None
    results = search_client.search(
        vector_queries=[
            VectorizedQuery(
                vector=query_vector, k_nearest_neighbors=50, fields="vector"
            )
        ],
        vector_filter_mode=VectorFilterMode.PRE_FILTER,
        filter=filter_condition,
        top=10,
    )

    unique_results = {}
    for result in results:
        if result["URL"] not in unique_results:
            unique_results[result["URL"]] = result

    return list(unique_results.values())


def create_system_message(content_chunks):
    system_message = os.getenv("SYSTEM_MESSAGE")
    if not content_chunks:
        return f"{system_message}\n\nContext:\nNOTFOUND"
    content_message = "\n".join(content_chunks)
    return f"{system_message}\n\nContext:\n{content_message}"


def format_search_results(results: list[dict]):
    search_results = []
    search_meta = []

    for result in results:
        
        score = result.get('@search.score', 0)  
        score_percentage = round(score * 100, 2)  

        search_results.append(result.get("content"))
        search_meta.append(
            {
                "name": result.get("Name", "Unknown"),  
                "Category": result.get("Category", "Unknown"),  
                "url": result.get("URL", "#"),  
                "score": f"{score_percentage}%"  
            }
        )
    
    return search_results, search_meta


def handle_error(e):
    logging.error(f"An error occurred: {e}")
    return {"error": f"An unexpected error occurred: {str(e)}"}


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing HTTP request for SharePoint document search.")

    try:
        query = req.params.get("query")
        Category = req.params.get("Category")

        if not query:
            return func.HttpResponse(
                json.dumps({"error": "Query parameter is required."}),
                status_code=400,
                mimetype="application/json",
            )

        embedding_client = initialize_openai_client()
        embedding = generate_embeddings(embedding_client, query)

        results = perform_vector_search_and_remove_duplicates(
            search_client, embedding, Category
        )

        search_results, search_meta = format_search_results(results)

        system_message = (
            create_system_message(search_results)
            if search_results
            else os.getenv("SYSTEM_MESSAGE")
        )

        message_text = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ]

        generated_response = embedding_client.chat.completions.create(
            model="gpt-35-turbo-16k", messages=message_text, temperature=0.1
        )
        gpt_response = generated_response.choices[0].message.content.replace("\n", "")

        
        print(gpt_response)
        response = {
            "query": query,
            "Category": Category,
            "results": search_meta,
            "gpt_response": gpt_response,
        }

        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json",
            headers=headers,
        )

    except Exception as e:
        error_response = handle_error(e)
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return func.HttpResponse(
            json.dumps(error_response),
            status_code=500,
            mimetype="application/json",
            headers=headers,
        )
