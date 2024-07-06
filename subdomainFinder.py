import itertools
import socket
import threading

def generate_domain_names(domain, max_len):
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789-'
    domain_names = set()

    # Generate domain names with max length of max_len symbols
    for length in range(1, max_len + 1):
        for combination in itertools.product(characters, repeat=length):
            domain_name = ''.join(combination)
            if '-' not in domain_name[0] and '-' not in domain_name[-1]: # Ensure domain name doesn't start or end with '-'
                domain_names.add(f"{domain_name}.{domain}")

    return domain_names

def check_domain_existence(domain_names):
    existing_domains = set()
    lock = threading.Lock()

    def check_domain(domain):
        try:
            socket.gethostbyname(domain)
            with lock:
                existing_domains.add(domain)
        except socket.error:
            pass

    threads = []
    for domain in domain_names:
        thread = threading.Thread(target=check_domain, args=(domain,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return existing_domains

def print_existing_domains(existing_domains):
    print("Existing subdomains:")
    for domain in existing_domains:
        print(domain)

if __name__ == "__main__":
    while True:
        domain = input("Enter the domain name (e.g. example.com): ").strip()
        if not domain:
            print("Domain name cannot be empty. Please try again.")
            continue
        break

    while True:
        try:
            max_len = int(input("Enter the maximum length of subdomain: "))
            if max_len < 1:
                print("Maximum length should be at least 1. Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for the maximum length.")

    print("Be patient!")
    
    generated_domains = generate_domain_names(domain, max_len)
    
    # Print existing domain names to console
    existing_domains = check_domain_existence(generated_domains)
    print_existing_domains(existing_domains)
    print("Subdomain search completed.")
