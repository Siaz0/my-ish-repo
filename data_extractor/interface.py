import json
import os
from extractor import run_extraction

def display_header():
    print("=" * 60)
    print("      AUTOMATED DATA EXTRACTOR - CONFIGURATION TOOL      ")
    print("=" * 60)

def get_urls():
    urls = []
    print("\nEnter URLs to extract data from (type 'done' when finished):")
    while True:
        url = input("URL: ").strip()
        if url.lower() == "done":
            break
        if url:
            urls.append(url)
    return urls

def get_fields():
    available_fields = ["title", "email", "name"]
    selected = []
    print("\nAvailable fields: title, email, name")
    print("Enter field names one by one (type 'done' when finished):")
    while True:
        field = input("Field: ").strip().lower()
        if field == "done":
            break
        if field in available_fields:
            selected.append(field)
        else:
            print("Invalid field. Choose from: title, email, name")
    return selected

def get_mode():
    print("\nSelect extraction mode:")
    print("1. Auto detect")
    print("2. Force HTML scraping")
    print("3. Force API fetch")
    choice = input("Enter choice (1/2/3): ").strip()
    return {"1": "auto", "2": "html", "3": "api"}.get(choice, "auto")

def get_output_settings():
    output_file = input("\nOutput file name (default: data_output.txt): ").strip() or "data_output.txt"
    log_file = input("Log file name (default: run_log.txt): ").strip() or "run_log.txt"
    return output_file, log_file

def save_config(urls, fields, mode, output_file, log_file):
    config = {
        "urls": urls,
        "fields": fields,
        "mode": mode,
        "output_file": output_file,
        "log_file": log_file
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("\nConfiguration saved successfully as config.json!")

def start_extraction():
    print("\nStarting extraction process...\n")
    with open("config.json", "r") as f:
        config = json.load(f)
    run_extraction(config)
    print("\nProcess completed! Check your output and log files.\n")

def main():
    os.system("clear" if os.name != "nt" else "cls")
    display_header()

    print("\nWhat would you like to do?")
    print("1. Create new extraction config")
    print("2. Run existing config")
    print("3. Exit")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        urls = get_urls()
        fields = get_fields()
        mode = get_mode()
        output_file, log_file = get_output_settings()
        save_config(urls, fields, mode, output_file, log_file)
        start_now = input("\nWould you like to start extraction now? (y/n): ").strip().lower()
        if start_now == "y":
            start_extraction()
    elif choice == "2":
        start_extraction()
    else:
        print("\nExiting...")

if __name__ == "__main__":
    main()
