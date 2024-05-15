import requests
import json

# NSX-T Manager details
nsx_manager_ip = "YOUR_NSX_MANAGER_IP"
nsx_manager_username = "YOUR_USERNAME"
nsx_manager_password = "YOUR_PASSWORD"

# Authenticate with NSX-T Manager
auth_url = f"https://{nsx_manager_ip}/api/v1/tokens"
auth_data = {
    "username": nsx_manager_username,
    "password": nsx_manager_password
}
auth_response = requests.post(auth_url, data=json.dumps(auth_data), verify=False)
auth_response.raise_for_status()
access_token = auth_response.json()["token"]

# List Tier 0 Gateways
t0_gateways_url = f"https://{nsx_manager_ip}/api/v1/tier-0s"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}
t0_gateways_response = requests.get(t0_gateways_url, headers=headers, verify=False)
t0_gateways_response.raise_for_status()
t0_gateways = t0_gateways_response.json()["results"]

# List Tier 1 Gateways
t1_gateways_url = f"https://{nsx_manager_ip}/api/v1/tier-1s"
t1_gateways_response = requests.get(t1_gateways_url, headers=headers, verify=False)
t1_gateways_response.raise_for_status()
t1_gateways = t1_gateways_response.json()["results"]

# Generate gfw.json for each gateway
for t0_gateway in t0_gateways:
    gateway_id = t0_gateway["id"]
    gateway_name = t0_gateway["display_name"]
    # Customize gfw.json content for Tier 0 gateway
    gfw_content = {
        "gateway_id": gateway_id,
        "gateway_name": gateway_name,
        "gateway_type": "tier_0"
        # Add more fields as needed
    }
    with open(f"gfw_{gateway_id}.json", "w") as f:
        json.dump(gfw_content, f, indent=4)

for t1_gateway in t1_gateways:
    gateway_id = t1_gateway["id"]
    gateway_name = t1_gateway["display_name"]
    # Customize gfw.json content for Tier 1 gateway
    gfw_content = {
        "gateway_id": gateway_id,
        "gateway_name": gateway_name,
        "gateway_type": "tier_1"
        # Add more fields as needed
    }
    with open(f"gfw_{gateway_id}.json", "w") as f:
        json.dump(gfw_content, f, indent=4)

print("gfw.json files generated successfully.")
