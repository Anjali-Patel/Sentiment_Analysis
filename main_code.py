import preprocesing
import yaml

# Load config file
config_path = '/Users/anjali/Desktop/Practice/config.yml'
config = preprocesing.load_config(config_path)

# User input
user_message = input("Please enter your message: ")

# Step 1: Remove trailing punctuation
punctuations_to_del = config['punctuations_to_del']
user_message = preprocesing.remove_trailing_punctuation(user_message, punctuations_to_del)
print("Message after removing trailing punctuation:", user_message)

# Step 2: Check if message is too long
max_char_length = config['max_char_len']
if preprocesing.is_message_too_long(user_message, max_char_length):
    print("Error: The message is too long.")
else:
    print("Message length is valid.")

# Step 3: Check if message contains only digits
exclude_num_msg = config['exclude_num_msg']
if preprocesing.is_digits_only_message(user_message, exclude_num_msg):
    print("Error: The message contains only digits and is invalid.")
else:
    print("Message does not contain only digits.")

# Step 4: Send a response from config.yml
response_message = config['responses']
print("Response:", response_message)
