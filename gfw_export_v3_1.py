import requests
import json

# Replace with your NSX IP, username, and password
nsx_ip = "nsxip"
username = "your_username"
password = "your_password"

# Disable warnings for unverified HTTPS requests (Not recommended for production)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_tier0_gateways():
    url = f"https://{nsx_ip}/policy/api/v1/infra/tier-0s"
    response = requests.get(url, auth=(username, password), verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    tier0_gateways = response.json()
    return [gateway['id'] for gateway in tier0_gateways['results']]

def get_gfw_rules(tier0_id):
    url = f"https://{nsx_ip}/policy/api/v1/tier-0s/{tier0_id}/gateway-firewall"
    response = requests.get(url, auth=(username, password), verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def main():
    tier0_ids = get_tier0_gateways()
    all_gfw_rules = {}
    
    for tier0_id in tier0_ids:
        gfw_rules = get_gfw_rules(tier0_id)
        all_gfw_rules[tier0_id] = gfw_rules
    
    # Print or save the collected GFW rules
    print(json.dumps(all_gfw_rules, indent=2))

if __name__ == "__main__":
    main()
