import argparse
from m1key import home
from m1key import segment
from m1key import resume
from m1key import education
from m1key import thug


def main():
    parser = argparse.ArgumentParser(
        description="A python package of my Tech Journey.")

    parser.add_argument("-i", "--introduce",
                        help="Gives introduction", action="store_true")

    subparsers = parser.add_subparsers(help="Subcommands")

    parser_project = subparsers.add_parser(
        "project", help="Project information")
    parser_project.add_argument(
        "-s", "--image-segment", dest="image",
        help="""Input an image i.e give location of an image, 
                it will extract top 2 dominant colors from the given 
                image and will redraw the entire image with those 2 colors""")
    parser_project.add_argument(
        "-t", "--thug-life", action="store_true", help="Thug Life")
    parser_project.set_defaults(name="project")

    parser_resume = subparsers.add_parser(
        "resume", help="Helps to download Resume in different format")
    parser_resume.add_argument(
        "-d", "--download", help="Helps to download resume in pdf format", action="store_true")
    parser_resume.set_defaults(name="resume")

    parser_education = subparsers.add_parser(
        "education", help="Information about my education (Matrix,Secondary,Undegrad)")
    parser_education.add_argument(
        "-m", "--matrix", action="store_true", help="Gives information about my 10th class results")
    parser_education.add_argument(
        "-x", "--secondary", action="store_true", help="Gives information about my 12th class results")
    parser_education.add_argument(
        "-u", "--undergrad", action="store_true", help="Gives information about my Undergraduation")
    parser_education.set_defaults(name="education")

    args = parser.parse_args()

    if args.introduce:
        print(home.introduction())
    if hasattr(args, "name"):
        if args.name == "project":
            if args.image:
                segment.execute(args.image)
            if args.thug_life:
                print("Loading ..... Please wait ...")
                thug.execute()
        if args.name == "resume":
            if args.download:
                resume.download_resume()
        if args.name == "education":
            if args.matrix:
                education.matrix()
            if args.secondary:
                education.secondary()
            if args.undergrad:
                education.undergraduation()
