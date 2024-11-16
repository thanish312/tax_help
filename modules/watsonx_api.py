import os
from ibm_watsonx_ai import GenerativeModel
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Use environment variables for sensitive information
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_SERVICE_URL = os.getenv("WATSONX_SERVICE_URL")

# Check if the API key and service URL are set
if not WATSONX_API_KEY or not WATSONX_SERVICE_URL:
    raise ValueError("API key and service URL must be set in environment variables.")

# Initialize Watsonx.ai client
authenticator = IAMAuthenticator(WATSONX_API_KEY)
watsonx_model = GenerativeModel(authenticator=authenticator)
watsonx_model.set_service_url(WATSONX_SERVICE_URL)

def generate_instructions(country, tax_form, transcripts):
    """
    Generate a detailed guide for filling out tax forms using IBM Watsonx.ai.
    
    Args:
        country (str): The selected country.
        tax_form (str): The selected tax form.
        transcripts (list): List of video transcriptions for additional context.
    
    Returns:
        str: Generated instructions or an error message.
    """
    # Validate inputs
    if not isinstance(country, str) or not isinstance(tax_form, str):
        return "Country and tax form must be strings."
    
    if not isinstance(transcripts, list) or not all(isinstance(t, str) for t in transcripts):
        return "Transcripts must be a list of strings."

    # Construct the prompt
    prompt = (
        f"Provide a detailed step-by-step guide for filling {tax_form} in {country}. "
        "Reference the following video transcriptions for guidance:\n"
    )
    prompt += "\n\n".join(transcripts)

    try:
        # Generate response using Watsonx.ai
        response = watsonx_model.generate_text(
            model="gpt-3.5-turbo",  # Make sure this model is available
            input=prompt,
            temperature=0.7,
            max_new_tokens=2000
        )
        return response["generated_text"]
    except Exception as e:
        return f"Failed to generate instructions: {str(e)}"

# Example usage
if __name__ == "__main__":
    country = "United States"
    tax_form = "1040"
    transcripts = [
        "In this video, we discuss the importance of gathering all necessary documents.",
        "Make sure to check your income sources before filling out the form."
    ]

    instructions = generate_instructions(country, tax_form, transcripts)
    print(instructions)
