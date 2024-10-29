import os
from techka.website.collect import collect
from techka.website.processing import clean_data, get_emails, get_keywords, get_pdfs, get_subdomains

DATA_DIR = "data/output"
ALL_URLS = "data/output/all_urls.txt"

class WebsiteHandler:
    def init_commands(self, subparsers):
        website_parser = subparsers.add_parser("website", help="Website related commands")
        website_subparsers = website_parser.add_subparsers(dest="action", required=True)

        collect_parser = website_subparsers.add_parser("collect", help="Collect data from a website")
        collect_parser.add_argument("url", type=str, help="The target URL")
        collect_parser.add_argument("--auth-header", type=str, help="Authentication header in the format 'Key=Value'", required=False)
        collect_parser.add_argument("--target-only", action="store_true", help="Target only, no subdomains", required=False)

        website_subparsers.add_parser("clean", help="Remove all scraped data")

        process_parser = website_subparsers.add_parser("process", help="Process collected data")
        process_parser.add_argument("--subdomains", action="store_true", help="Extract subdomains")
        process_parser.add_argument("--emails", action="store_true", help="Extract emails from the collected data (includes PDFs)")
        process_parser.add_argument("--pdfs", action="store_true", help="Extract and print text from PDFs and documents")
        process_parser.add_argument("--keywords", nargs="+", help="List of keywords to search for (includes PDFs)")

    def handle(self, args):
        action_map = {
            "collect": self._website_collect,
            "clean": self._website_clean,
            "process": self._website_process,
        }
        action = args.action
        if action in action_map:
            action_map[action](args)

    def _website_collect(self, args):
        collect(args.url, args.auth_header, args.target_only)
        print("Website data collection completed.")

    def _website_clean(self, args):
        clean_data()
        print("Website data cleaned.")

    def _website_process(self, args):
        if args.subdomains:
            for subdomain in get_subdomains(ALL_URLS):
                print(subdomain)

        if args.emails:
            for email in get_emails(DATA_DIR):
                print(email) 

        if args.pdfs:
            for pdf_text in get_pdfs(DATA_DIR):
                print(pdf_text)

        if args.keywords:
            print(get_keywords(DATA_DIR, args.keywords))

