import sys
import argparse
import ipinfo
from ipwhois import IPWhois
from datetime import datetime


def _normalize_date(value):
    """Return YYYY-MM-DD when possible, accepting datetime or str."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    if isinstance(value, str):
        # Try common RDAP/ISO formats
        for fmt in (
            '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S%z'
        ):
            try:
                return datetime.strptime(value, fmt).strftime('%Y-%m-%d')
            except Exception:
                continue
        return value  # fall back to raw string
    return None

def format_section(title, char='='):
    return f"{char * 60}\n{title}\n{char *60}"

def ipinfo_lookup(ip_address, ipinfo_token=None):
    print(format_section(f"IPINFO GEOLOCATION DATA", '-'))
    try:
        handler = ipinfo.getHandler(ipinfo_token)
        details = handler.getDetails(ip_address)
        print(f"IP Address:       {details.ip}")
        print(f"City:             {details.city if details.city else 'N/A'}")
        print(f"Region:           {details.region if details.region else 'N/A'}")
        print(f"Country:          {details.country if details.country else 'N/A'}")
        print(f"Location:         {details.loc if details.loc else 'N/A'}")
        print(f"Potal ode:        {details.postal if details.postal else 'N/A'}")
        print(f"Timezone:         {details.timezone if details.timezone else 'N/A'}")
        print(f"Organization:     {details.org if details.org else 'N/A'}")
        if hasattr(details, 'asn') and details.asn:
            print(f"ASN Information:")
            print(f"  ASN:          {details.asn.get('asn'), 'N/A'}")
            print(f"  Name:         {details.asn.get('name'), 'N/A'}")
            print(f"  Domain:       {details.asn.get('domain'), 'N/A'}")
            print(f"  Route:        {details.asn.get('route'), 'N/A'}")
            print(f"  Type:         {details.asn.get('type'), 'N/A'}")
        if hasattr(details, 'company') and details.company:
            print(f"Company:")
            print(f"  Name:         {details.asn.get('name'), 'N/A'}")
            print(f"  Domain:       {details.asn.get('domain'), 'N/A'}")
            print(f"  Type:         {details.asn.get('type'), 'N/A'}")
        if hasattr(details, 'privacy') and details.privacy:
            print(f"Privacy/Proxy:")
            print(f"  VPN:          {details.asn.get('vpn'), False}")
            print(f"  Proxy:        {details.asn.get('proxy'), False}")
            print(f"  Tor:          {details.asn.get('tor'), False}")
            print(f"  Relay:        {details.asn.get('relay'), False}")
            print(f"  Hosting:      {details.asn.get('hosting'), False}")
    except Exception as e:
        print(f"Error fetching IPInfo data: {str(e)}")

def whois_lookup(ip):
    print(format_section(f"WHOIS REGISTRATION DATA", '-'))

    """
    Perform RDAP lookup for an IP and print details in domain-like WHOIS format:
      Registrar, Organization, Registrant, Address, City, State, Country,
      Created, Expires, Updated, Statuses.
    """
    try:
        obj = IPWhois(ip)
        rdap = obj.lookup_rdap(depth=1)

        network = rdap.get('network', {}) or {}
        objects = rdap.get('objects', {}) or {}
        events  = network.get('events', []) or rdap.get('events', []) or []

        ip_address   = ip
        registrar    = rdap.get('asn_registry') or network.get('parent_handle') or network.get('handle')
        start_address = network.get('start_address') or None
        end_address = network.get('end_address') or None
        cidr = network.get('cidr') or None
        country = network.get('country') or None
        type = network.get('type') or None
        organization = rdap.get('asn_description') or None

        # Try to infer registrant-like info even without vCard (best-effort)
        # Some RDAP servers may include minimal 'entities' or simple names
        preferred_obj = None
        for obj in objects.values():
            roles = obj.get('roles', []) or []
            if any(r.lower() in ('registrant', 'administrative', 'technical') for r in roles):
                preferred_obj = obj
                break
        if not preferred_obj and objects:
            preferred_obj = next(iter(objects.values()))

        if preferred_obj:
            contact = preferred_obj.get('contact', {}) or {}
            registrant = contact.get('name', str) or None
            addr_list = contact.get('address', []) or []
            if isinstance(addr_list, list) and addr_list:
                first_addr = addr_list[0]
                if isinstance(first_addr, dict):
                    address = first_addr.get('value') or None

        # Gather statuses (network.status can be list or str)
        statuses = []
        net_status = network.get('status', [])
        if isinstance(net_status, list):
            statuses.extend(net_status)
        elif net_status:
            statuses.append(net_status)

        # Dates from RDAP events
        created = None
        updated = None
        expires = None  # IP allocations typically lack explicit expiry in RDAP
        for ev in events:
            action = (ev.get('action') or '').lower()
            date   = _normalize_date(ev.get('timestamp'))
            if action in ('registration', 'created', 'announcement') and date:
                created = created or date
            elif action in ('last changed', 'last update', 'updated') and date:
                updated = updated or date
            elif action in ('expiration', 'expires') and date:
                # rare in IP RDAP, but capture if present
                expires = expires or date

        # --- Print in domain-like style ---
        print(f"IP Details:       {ip_address}")
        if start_address and end_address:
            print(f"  IP Range:       {start_address} - {end_address}")
        if cidr:
            print(f"  CIDR:           {cidr}")
        if type:
            print(f"  Type:           {type}")
        if registrar:
            print(f"Registrar:        {registrar}")
        if organization:
            print(f"Organization:     {organization}")
        if registrant:
            print(f"Registrant:       {registrant}")
        if address:
            address = address.replace('\n',' ')
            print(f"  Address:        {address}")
        if country:
            print(f"  Country:        {country}")
        if created:
            print(f"Created:          {created}")
        if expires:
            print(f"Expires:          {expires}")
        if updated:
            print(f"Updated:          {updated}")
        if statuses:
            print("Statuses:")
            for s in statuses:
                print(f"  - {s}")
    
    except Exception as e:
        print(f"Error fetching WHOIS data: {str(e)}")     

def main():
    parser = argparse.ArgumentParser(
        description='IP Enricmnent Tool - Gather GeoIP and WHOIS information',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python ip_enrich.py 8.8.8.8
  python ip_enrich.py 1.1.1.1 --token YOUR_IP_INFO_TOKEN

PowerShell Usage:
  python ip_enrich.py 8.8.8.8
  python C:\\path\\to\\ip_enrich.py 1.1.1.1
"""
    )

    parser.add_argument('ip', help='IP address to enrich')
    parser.add_argument('-t', '--token', help='IPInfo API token (optional, for higher rate limits)', default=None)
    args = parser.parse_args()
    print(format_section(f"IP ENRICHMENT REPORT", '='))
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        ipinfo_lookup(args.ip, '63c8018c78d15a')
        whois_lookup(args.ip)
    except KeyboardInterrupt:
        print('\n\nOperation cancelled by user')
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()