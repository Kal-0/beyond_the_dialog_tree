__version__ = "2.0.0"

import requests
import json

# Global Configuration for LLM Connectivity
llm_config = {
    "provider": "lmstudio", 
    "base_url": "http://127.0.0.1:1234/v1/chat/completions",
    "model": "google/gemma-3-4b",
    "api_key": "lm-studio"
}

def completion(messages, api_key="", proxy=''):
    url = llm_config["base_url"]
    
    # Original proxy fallback if explicitly maintained
    if proxy and "prima.wiki" in proxy and llm_config["provider"] == "openai":
        url = proxy
        
    used_api_key = api_key if api_key else llm_config["api_key"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {used_api_key}"
    }

    data = {
        "model": llm_config["model"],
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            completion_msg = response.json()["choices"][0]["message"]
            messages.append(completion_msg)
            return messages
        else:
            raise Exception(f"HTTP Return Error: {response.status_code}, {response.text}")
    except Exception as e:
        raise Exception(f"LLM Connection Error: {str(e)}")
