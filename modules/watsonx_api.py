import requests

WATSON_ASSISTANT_API_KEY = "xyMJfE6RlMLIsq9cTQec4xMiakW78X4yn2xY2cPCQqgo"
WATSON_ASSISTANT_URL = "https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/d51040cc-d2e0-45bc-a079-42c76dfde5cb"
WATSON_ASSISTANT_ID = "765aad8c-d43c-42cc-bb76-d9c9679edf5d"  # The Assistant ID for your Watson Assistant

def generate_instructions(country, tax_form, transcripts):
    """
    Generate a detailed guide for filling out tax forms using IBM Watson Assistant v2.
    
    Args:
        country (str): The selected country.
        tax_form (str): The selected tax form.
        transcripts (list): List of video transcriptions for additional context.
    
    Returns:
        str: Generated instructions or an error message.
    """
    # Construct the prompt
    prompt = (
        f"Provide a detailed step-by-step guide for filling {tax_form} in {country}. "
        "Reference the following video transcriptions for guidance:\n"
    )
    prompt += "\n\n".join(transcripts)

    # API endpoint for Watson Assistant
    url = f"{WATSON_ASSISTANT_URL}/v2/assistants/{WATSON_ASSISTANT_ID}/message"

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {WATSON_ASSISTANT_API_KEY}",
        "Content-Type": "application/json",
    }

    # Payload for the request
    payload = {
        "input": {
            "message_type": "text",
            "text": prompt,
        },
        "context": {},  # Add context if needed for Watson Assistant
    }

    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response
        output = response.json()
        return output.get("output", {}).get("generic", [{}])[0].get("text", "No response.")
    except requests.exceptions.RequestException as e:
        return f"Failed to generate instructions: {e}"
