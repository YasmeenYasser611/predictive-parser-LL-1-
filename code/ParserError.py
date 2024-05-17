class ParserError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.token}: {self.message}'
    
'''
error_code = 123
token = 'some_token'
message = 'An error occurred during parsing'


try:
    # Some code that may raise a ParserError

    
    ...
except ParserError as e:
    print(f"ParserError occurred: {e}")
    # Handle the error appropriately 

def parse_data(data):
    tokens = data.split(',')  # Splitting data by comma
    parsed_data = []
    for token in tokens:
        if not token.isdigit():
            # If the token is not a digit, raise a ParserError
            raise ParserError(token=token, message="Invalid token encountered")
        parsed_data.append(int(token))
    return parsed_data

# Example usage:
data = "1,2,three,4,5"
try:
    parsed_data = parse_data(data)
    print("Parsed data:", parsed_data)
except ParserError as e:
    print(f"ParserError occurred: {e}")'''