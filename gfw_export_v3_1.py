import requests
import json

# Replace with your NSX IP, username, and password
nsx_ip = "nsxip"
username = "your_username"
password = "your_password"

# Disable warnings for unverified HTTPS requests (Not recommended for production)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_gateways(gateway_type):
    url = f"https://{nsx_ip}/policy/api/v1/infra/{gateway_type}"
    response = requests.get(url, auth=(username, password), verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    gateways = response.json()
    return [gateway['id'] for gateway in gateways['results']]

def get_gfw_rules(gateway_type, gateway_id):
    url = f"https://{nsx_ip}/policy/api/v1/infra/{gateway_type}/{gateway_id}/gateway-firewall"
    response = requests.get(url, auth=(username, password), verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def main():
    all_gfw_rules = {
        "tier0": {},
        "tier1": {}
    }
    
    tier0_ids = get_gateways('tier-0s')
    for tier0_id in tier0_ids:
        gfw_rules = get_gfw_rules('tier-0s', tier0_id)
        all_gfw_rules["tier0"][tier0_id] = gfw_rules
    
    tier1_ids = get_gateways('tier-1s')
    for tier1_id in tier1_ids:
        gfw_rules = get_gfw_rules('tier-1s', tier1_id)
        all_gfw_rules["tier1"][tier1_id] = gfw_rules
    
    # Save the collected GFW rules to a file
    with open('gfw_rules.json', 'w') as file:
        json.dump(all_gfw_rules, file, indent=2)

if __name__ == "__main__":
    main()
