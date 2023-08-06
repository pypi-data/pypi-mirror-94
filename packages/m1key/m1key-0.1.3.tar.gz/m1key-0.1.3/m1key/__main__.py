import argparse
from m1key import home
from m1key import project
from m1key import resume


def main():
    parser = argparse.ArgumentParser(
        description="A python package of my Tech Journey.")

    parser.add_argument("-i", "--introduce",
                        help="Gives introduction", action="store_true")

    subparsers = parser.add_subparsers(help="Subcommands")
    
    parser_project = subparsers.add_parser(
        "project", help="Project information")
    parser_project.add_argument(
        "-s", "--image-segment", help="Input an image ")
    parser_project.set_defaults(name="project")

    parser_resume = subparsers.add_parser(
        "resume", help="Helps to download Resume in different format")
    parser_resume.add_argument(
        "-d", "--download", help="Helps to download resume in pdf format", action="store_true")
    parser_resume.set_defaults(name="resume")

    args = parser.parse_args()
    
    if args.introduce:
        print(home.introduction())
    if hasattr(args, "name"):
        if args.name == "project":
            project.execute(args.image_segment)
        if args.name == "resume":
            if args.download:
                resume.download_resume()
                
