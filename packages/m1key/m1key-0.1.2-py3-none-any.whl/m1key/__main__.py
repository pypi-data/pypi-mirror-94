import argparse
from m1key import home
from m1key import project


def main():
    parser = argparse.ArgumentParser(
        description="A python package of my Tech Journey.")
    parser.add_argument("-i", "--introduce",
                        help="Gives introduction", action="store_true")
    parser.add_argument("-p", "--project",
                        help="A journey of my projects", choices=["img_seg", "sub"])
    
    subparsers = parser.add_subparsers(help="Subcommands")
    parser_project = subparsers.add_parser("project", 
                                           help="Project information")
    parser_project.add_argument("-s", "--image-segment", 
                                help="Input an image ")
    parser_project.set_defaults(name="project")
    args = parser.parse_args()
    if args.introduce:
        print(home.introduction())
    if hasattr(args, "name"):
        if args.name=="project":
            project.execute(args.image_segment)

    