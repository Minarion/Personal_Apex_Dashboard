# Inbuilt
import requests
from typing import Optional

# Third Party

# Local
import keys
import request_info

def get_api_data(
    request_type: str,
    api_key: str,
    platform: str,
    user_name: Optional[None | str] = None,
    user_id: Optional[None | str] = None,
    api_url: str = "https://api.apexlegendsstatus.com",
    optionals: list = [],
) -> dict:

    allowed_request_types = [
        "bridge",           # Player statistics
        "games",            # [Whitelist Only] Game history
        "leaderboard",      # [Whitelist Only] Leaderboard
        "maprotation",      # Next map(s) in rotation
        "predator",         # RP needed to hit Pred rank (+ amount of Masters per platform)
        "servers",          # Server status
        "origin",           # User ID from User Name (PC specific)
        "nametouid",        # User ID from User Name + Platform
    ]

    error_codes = {
        400: "Try again in a few minutes",
        403: "Unauthorized / Unknown API key",
        404: "The player could not be found",
        405: "External API error",
        410: "Unknown platform provided",
        429: "Rate limit reached",
        500: "Internal error",
    }

    request_type = request_type.lower()

    if request_type not in allowed_request_types:
        return {"request_type": f"{request_type} is not a valid option"}

    base_request = f"{api_url}/{request_type}?auth={api_key}"

    match request_type:
        case "bridge":
            if user_name: base_request += f"&player={user_name}"
            elif user_id: base_request += f"&uid={user_name}"
            else: return {"user_name & user_id": "At least one must not be empty"}

            base_request += f"&platform={platform}"

    api_response = requests.get(base_request)

    if api_response.status_code in error_codes:
        return {api_response.status_code: error_codes[api_response.status_code]}

    api_data = {
        "status_code": api_response.status_code,
        "headers": api_response.headers,
        "encoding": api_response.encoding,
        "text": api_response.text,
        "json": api_response.json,
    }

    if optionals and any([api_section in api_data for api_section in optionals]):
        return {
            key: api_data[key] 
            for key in optionals
            if key in api_data
        }

    else:
        return api_data

output = get_api_data(
    request_type=request_info.request_type,
    api_key=keys.api_key,
    platform=request_info.platform,
    user_name=request_info.user_name,
    optionals=request_info.optionals,
)

print(output)