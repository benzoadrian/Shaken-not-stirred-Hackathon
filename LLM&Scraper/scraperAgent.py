from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import boto3
import json
import re
import tempfile
import os
from flask import Flask, request, jsonify
import requests
import random

# Initialize the Bedrock client for LLM interaction.
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")

# Initialize the global variables
full_conversation = []
SYSTEM_PROMPT = """You are an assistant helping persons to book medical reservations. You should answer in the same language as the person who 
needs help. First, the person will tell you what he needs. Then, you will be given options for the reservation. 
The options will be presented as a list: [0. Option 0, 1. Option 1, ...]. Notice that the options are in French because the customers are in France.
You will have to rank the best 3 options from all the listed options, with respect to the needs of the person, or all of them if there are less than 3.
If not explicitly asked, you must not explain your answer.
The format for the answer, that you must imperatively follow, including the '[' and ']', is: [index of best option, index of next best option, index of next best option].
The index begins at 0.\n"""
user_message = "I have some headache, I want to visit a doctor."  # retrieved from WhatsApp
CUSTOMER_PROMPT = f"""Here is the message of the user:\n\n{user_message}\n"""
full_conversation.append({"role": "user", "content": SYSTEM_PROMPT + CUSTOMER_PROMPT})

url_start = ("https://www.doctolib.fr/cabinet-medical/paris/maison-abeille-chirurgie-dermatologique-medecine-dermo-esthetique/booking/specialities?bookingFunnelSource=profile")


def llm_decision(options, current_conversation):
    """
    options: list of the available options
    current_conversation: context to allow the LLM to answer

    Returns the top 3 most likely answers and the updated conversation.
    """
    # Formatting: create a string listing the options.
    options_str = str([f"{i}. {option}" for i, option in enumerate(options)])
    options_str = re.sub(r"'", "", options_str)
    options_str = re.sub(r",", ",\n", options_str)

    # Prompt for the LLM
    message = f"""Which option is the best?
Here is the list of options:
{options_str}
Do not explain your answer.
Do not forget to answer in the following format, without any addition: [index of best option, index of 2nd best option, index of 3rd best option]\n"""
    current_conversation.append({"role": "user", "content": message})
    body = json.dumps({
        "max_tokens": 256,
        "messages": current_conversation,
        "anthropic_version": "bedrock-2023-05-31"
    })

    # Generate answer via the Bedrock model.
    response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-5-haiku-20241022-v1:0")
    response_body = json.loads(response.get("body").read())
    response_text = response_body['content'][0]['text']
    full_conversation.append({"role": "assistant", "content": response_text + '\n'})

    return string_to_list(response_text), full_conversation


def string_to_list(input_string):
    # Extract the content between brackets.
    pattern = r'\[(.*)\]'
    match = re.search(pattern, input_string)
    if match:
        content = match.group(1)
        elements = [int(elem.strip()) for elem in content.split(',')]
        return elements
    else:
        return []


def list_to_string(input_list):
    # Convert the list to a string representation.
    return "[" + ", ".join(map(str, input_list)) + "]"


def summarize_conversation(full_conversation, infos):
    message = f"""Here is the medical consultation that you chose for the person:\n\n{infos}\n\nExplain in a concise way to the customer
if the reservation you found matches his situation."""
    full_conversation.append({"role": "user", "content": message})
    body = json.dumps({
        "max_tokens": 256,
        "messages": full_conversation,
        "anthropic_version": "bedrock-2023-05-31"
    })

    # Generate answer.
    response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-5-haiku-20241022-v1:0")
    response_body = json.loads(response.get("body").read())
    return response_body['content'][0]['text']

def run(llm_decision=llm_decision, url_start=url_start):
    """
    Navigates through the Doctolib website to find the time slot page.
    Returns the URL of the time slot page (if found), the conversation, and a summary.
    """
    global full_conversation
    path_taken = []  # Keep track of the path taken.

    # Create a unique temp directory for user data
    temp_dir = tempfile.mkdtemp()
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode since Cloud9 has no GUI
    options.add_argument('--no-sandbox')  # Required for running Chrome as root/in containers
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource issues
    options.add_argument(f'--user-data-dir={temp_dir}')  # Set unique user data directory
    options.add_argument('--disable-gpu')  # Disable GPU acceleration in headless mode
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # If you need to specify path to chrome and chromedriver
    chrome_path = os.path.expanduser('~/chrome-bin/chrome-linux64/chrome')
    chromedriver_path = os.path.expanduser('~/chromedriver-bin/chromedriver-linux64/chromedriver')
    
    # Set the service to use your specific chromedriver
    from selenium.webdriver.chrome.service import Service
    service = Service(executable_path=chromedriver_path)
    
    # Initialize the driver with the service and options
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("return navigator.webdriver")

    # Navigate to the starting URL.
    driver.get(url_start)
    time.sleep(random.random()*3+1)  # Allow page to load.
    driver.save_screenshot("time_slot_page.png")
    # Click the "Refuser" button to decline cookies.
    decline_buttons = driver.find_elements(By.XPATH,
                                           "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'refuser')]")
    if decline_buttons:
        print("Cookie pop-up found. Clicking the decline button.")
        for button in decline_buttons:
            button.click()
    else:
        print("No cookie pop-up found. Continuing without clicking.")
    time.sleep(random.random()*1+1)

    max_steps = 5
    for step in range(max_steps):
        time.sleep(random.random()*3+1)
        # Use a locator to detect the time slot page by checking for unique text.
        # Step 1: Try to find time slot elements
        time_slot_elements = driver.find_elements(By.XPATH, "//button[contains(@class, 'availabilities-slot')]")

        if time_slot_elements:
            print("Time slot page reached!")
            final_url = driver.current_url
            print("Final URL:", final_url)
            # driver.save_screenshot("time_slot_page.png")
            driver.quit()
            return final_url, full_conversation, summarize_conversation(full_conversation, path_taken)

        # Locate the specialty options.
        # We broadly search for any element with a role attribute set to "button".
        option_elements = driver.find_elements(By.CSS_SELECTOR, '[role="button"]')
        time.sleep(random.random()*3+1)
        options = [elem.text.strip() for elem in option_elements if elem.text.strip() != ""]
        if not options:
            print("Time slot page reached!")
            final_url = driver.current_url
            print("Final URL:", final_url)
            # Optionally save a screenshot: driver.save_screenshot("time_slot_page.png")
            driver.quit()
            return final_url, full_conversation, summarize_conversation(full_conversation, path_taken)
            print("No options found on this page. Exiting navigation.")
            print(path_taken)
            print(full_conversation)
            driver.quit()
            break

        print(f"Step {step}: Found options: {options}")
        print(options)
        # options = options.split('\n')
        # Decide which option to click.
        selected_option, full_conversation = llm_decision(options, full_conversation)
        time.sleep(random.random()*3+1)
        # Assume selected_option is a list and we use the first one.
        try:
            selected_index = selected_option[0]

        except ValueError:
            print("Selected option not found in options list.")
            driver.quit()
            return None, full_conversation, summarize_conversation(full_conversation, path_taken)
        path_taken.append(options[selected_option[0]])
        print(selected_index)
        print(path_taken)

        # Click the chosen option.
        time.sleep(random.random()*2+1)
        print(option_elements[selected_index])
        driver.save_screenshot('example.png')
        option_elements[selected_index].click()

        # Wait for the new content to load.
        time.sleep(random.random()*2+1)
    else:
        print("Did not reach the time slot page within the allowed steps.")
        driver.quit()

    return None, full_conversation, summarize_conversation(full_conversation, path_taken)


def main(llm_decision=llm_decision, url_start=url_start):
    return run(llm_decision=llm_decision, url_start=url_start)
print(main())

# GET
# constantly listen to requests
# if request received, set user_text to the text received
# go to POST




# POST
#  a, _, c = main()
# send "Link to Doctolib: " + a + "\" + c
 
# ======= Integration: Listening for GET requests and posting to an API =======
# Here we use Flask to listen for incoming GET requests that supply a 'message' parameter.
# When a GET request is received, we update the user message, run our main logic,
# then POST the resulting information to a designated API.


app = Flask(__name__)

# Replace with your actual target API URL for POSTing the result.
API_POST_URL = "https://ukcwhtroh3.execute-api.us-west-2.amazonaws.com/default/send-whatsapp"
processed_messages = set()

@app.route('/receive', methods=['POST'])
def receive():
    print("received")
    global user_message, full_conversation, CUSTOMER_PROMPT
    print(request.args)
    # Get the user message from query parameters.
    user_message = request.args.get('message')
    sender = request.args.get('sender')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
        
    if (user_message, sender) in processed_messages:
                return jsonify({"status": "skipped", "reason": "Message already processed"}), 200
                
    processed_messages.add((user_message, sender))
    
    print(user_message + " received")
    # Initialize conversation with the system prompt and customer message.
    CUSTOMER_PROMPT = f"Here is the message of the user:\n\n{user_message}\n"
    full_conversation = [{"role": "user", "content": SYSTEM_PROMPT + CUSTOMER_PROMPT}]

    # Run the booking logic.
    final_url, conversation, summary = main()
    if not final_url:
        final_url = "No final URL found."

    # Prepare payload for the POST request.
    payload = {
        "message": f"Link to Doctolib: {final_url}\n{summary}\nP.S. FUCK AWS!!!",
        "sender": sender
    }
    print("Posting payload:", payload)

    # Send the result to the specified API endpoint.
    try:
        post_response = requests.post(API_POST_URL, json=payload)
        post_response.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Failed to post data: {e}"}), 500

    return jsonify({
        "status": "success",
        "data": payload
    }), 200

if __name__ == '__main__':
    # Run the Flask app on port 5000 (or any port you choose)
    app.run(host="0.0.0.0", port=5000)
