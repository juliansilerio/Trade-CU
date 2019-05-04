from bs4 import BeautifulSoup
import sys

def parse_html(sourceFile):
    with open(sourceFile) as source:
        soup = BeautifulSoup(source, 'html.parser')
        rows = soup.pre
        courses = str(rows).split("\n")[4:-1]
        courses = [list(filter(None, course.split("  "))) for course in courses if ("LECTURE" not in course and "Note" not in course)]
        return courses

def write_courses(courses, destFile):
    #with open(destFile) as dest:
    pass

def main():
    sourceFile = sys.argv[1]
    destFile = sys.argv[2]

    courses = parse_html(sourceFile)
    write_courses(courses, destFile)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Too few input arguments!")
        print("USAGE: parse_html.py [sourceFile] [destFile]")
        quit
    elif len(sys.argv) > 3:
        print("Too many arguments!")
        print("USAGE: parse_html.py [sourceFile] [destFile]")
        print("Proceeding with first two arguments")
    main()
