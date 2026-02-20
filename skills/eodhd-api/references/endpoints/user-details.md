# User Details API

Status: complete
Source: financial-apis (User API)
Docs: https://eodhd.com/financial-apis/user-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /internal-user
Method: GET
Auth: api_token (query)

## Purpose

Returns account details for the subscriber associated with the given API token. Use this endpoint to verify authentication, check remaining API quota, monitor daily usage, retrieve subscription information, and check Marketplace subscription status including reset times. No symbol or additional parameters are required.

> **Note**: The actual endpoint path is `/api/internal-user`. The legacy `/api/user` path may also work but `/api/internal-user` returns the complete response including `availableDataFeeds` and `availableMarketplaceDataFeeds`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API access token |

## Response (shape)

```json
{
  "name": "Helmut Schiller",
  "email": "helmut.shiller@gmx.de",
  "subscriptionType": "monthly",
  "paymentMethod": "PayPal",
  "apiRequests": 5301,
  "apiRequestsDate": "2026-01-25",
  "dailyRateLimit": 100000,
  "extraLimit": 500,
  "inviteToken": null,
  "inviteTokenClicked": 0,
  "subscriptionMode": "paid",
  "canManageOrganizations": false,
  "availableDataFeeds": [
    "Bulk Splits and Dividends API",
    "News API",
    "EOD Historical Data",
    "Search API",
    "dividends",
    "Dividends Data Feed",
    "Split Data Feed",
    "Live (delayed) Data API",
    "CBOE Data API",
    "Sentiment Data API",
    "Exchanges List API",
    "Daily Treasury Bill Rates",
    "Daily Treasury Real Long-Term Rates, Daily Treasury Long-Term Rates",
    "Daily Treasury Par Yield Curve Rates",
    "Daily Treasury Par Real Yield Curve Rates"
  ],
  "availableMarketplaceDataFeeds": {
    "dailyRateLimit": 100000,
    "requestsSpent": 80,
    "timeToReset": "19:01 GMT+0000",
    "subscriptions": ["US Stock Options Data API"]
  }
}
```

> **Note**: When no Marketplace subscriptions are active, `availableMarketplaceDataFeeds` is an empty array `[]` instead of an object.

### Output Format

| Field | Type | Description |
|-------|------|-------------|
| name | string | Name of the subscriber associated with the API token |
| email | string | Email of the subscriber associated with the API token |
| subscriptionType | string | Subscription type (e.g., monthly, yearly, commercial) |
| paymentMethod | string | Payment method (e.g., PayPal, Stripe, Wire, Not Available) |
| apiRequests | integer | Number of API calls on the latest day of API usage. Resets at midnight GMT, but shows the previous day's count until a new request is made after reset |
| apiRequestsDate | string (YYYY-MM-DD) | Date of the latest API request |
| dailyRateLimit | integer | Maximum number of API calls allowed per day for the main subscription |
| extraLimit | integer | Remaining amount of additionally purchased API calls |
| inviteToken | string\|null | Invitation token for the affiliate program |
| inviteTokenClicked | integer | Number of invite token clicks |
| subscriptionMode | string | Subscription mode: `demo`, `free`, or `paid` |
| canManageOrganizations | boolean | Whether the user can manage organizations |
| availableDataFeeds | array | List of available data feed names for the main subscription |
| availableMarketplaceDataFeeds | object\|array | Marketplace subscription info (object when active, empty array `[]` when none) |

### Marketplace Data Feeds Object

When Marketplace subscriptions are active, `availableMarketplaceDataFeeds` is an object:

| Field | Type | Description |
|-------|------|-------------|
| dailyRateLimit | integer | Maximum daily API calls per Marketplace subscription (100,000) |
| requestsSpent | integer | Number of Marketplace API calls used in the current 24-hour period |
| timeToReset | string | Time when all Marketplace subscription limits reset (e.g., `19:01 GMT+0000`). Shared across all Marketplace products — based on when the user first made any Marketplace API request. |
| subscriptions | array | List of active Marketplace subscription names |

## Example Requests

```bash
# Get user details (recommended endpoint)
curl "https://eodhd.com/api/internal-user?api_token=YOUR_TOKEN"

# Using the demo key
curl "https://eodhd.com/api/internal-user?api_token=demo"

# Using the helper client
python eodhd_client.py --endpoint user
```

## Notes

- No symbol or date parameters are required
- The `apiRequests` counter resets at midnight GMT each day (for the main subscription)
- The count shown reflects the latest day any request was made; it does not update until a new request occurs after the midnight reset
- API calls vs API requests: some endpoints consume more than 1 API call per request (see rate-limits.md for details)
- Useful for verifying that your API token is valid and checking remaining quota before making data requests
- API call consumption: 1 call per request
- **Marketplace limits**: The `availableMarketplaceDataFeeds.timeToReset` field shows when all Marketplace subscription limits reset. Each Marketplace subscription has its own separate 100,000-call limit, but they all share the same reset time.
- **Marketplace reset time**: The reset time is based on when the user first made any Marketplace API request. All Marketplace subscriptions reset at this same time every 24 hours.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

When an error occurs, the API returns a JSON response with error details:

```json
{
  "error": "Error message description",
  "code": 403
}
```

### Handling Errors

**Python Example**:
```python
import requests

def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            print("Error: API limit exceeded. Please upgrade your plan.")
        elif e.response.status_code == 403:
            print("Error: Invalid API key. Check your credentials.")
        elif e.response.status_code == 429:
            print("Error: Rate limit exceeded. Please slow down your requests.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check status codes before processing response data
- Implement exponential backoff for 429 errors
- Cache responses to reduce API calls
- Monitor your API usage in the user dashboard
