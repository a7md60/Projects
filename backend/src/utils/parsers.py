import json

def parse_json_with_quotes(json_str):
    try:
        # Parse the JSON string into a Python dictionary
        parsed_data = json.loads(json_str, strict=False)
        
        return parsed_data
    
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing error: {str(e)}")

