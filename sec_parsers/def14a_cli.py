from argparse import ArgumentParser
from sec_parsers import Filing, download_sec_filing, set_headers

def print_subsection_content(parsed_doc, section, stop_at="Report"):
    """
    Find and print all the subsections of the given section
    In certain cases, to avoid printing sections around the given section
    use stop_at to mark the end section
    """
    if section is None:
        return True
    
    section_title = section.get('title')

    if stop_at.lower() in section_title.lower():
        return False
    
    print(f"#### {section_title}")
    print(section.text)
    print('\n')

    subsections = parsed_doc.get_subsections_from_section(section)
    for section in subsections:
        if not print_subsection_content(parsed_doc, section, stop_at):
            return False
    
    return True

def cli():
    cli_parser = ArgumentParser()
    cli_parser.add_argument("url", help="Link to SEC DEF14A html document")
    args = cli_parser.parse_args()

    set_headers("harish", "testaccriv@gmail.com")
    html = download_sec_filing(args.url)
    if not html:
        print("unable to download the html document")
        return
    
    filing = Filing(html)
    filing.set_filing_type("DEF-14A")
    filing.parse()
    compensation_section = filing.find_section_from_title("Compensation Discussion and Analysis")
    if not compensation_section:
        print("Compensation Discussion and Analysis section not found")
        return
    print_subsection_content(filing, compensation_section)



if __name__ == "__main__":
    cli()



    
