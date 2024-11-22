#!/usr/bin/python3

import os
import sys
import time
import pdfkit
import shutil

# import argparse
import subprocess
from pathlib import Path
from jinja2 import Template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from database import Database
from models.career import Career
from models.roadmap import Roadmap

db = Database()

vowels = ["a", "e", "i", "o", "u"]

directory = os.getcwd()


def open_file(path: str):
    if sys.platform == "darwin":
        return subprocess.run(["open", path])

    if sys.platform == "linux" or sys.platform == "linux2":
        return subprocess.run(["xdg-open", path])

    return os.startfile(path)


def get_roadmap_content(roadmap_link: str) -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    print("\nPulling data from roadmaps.sh...")

    driver.get(roadmap_link)

    time.sleep(3)

    page_height = driver.execute_script("return document.body.scrollHeight")
    page_width = driver.execute_script("return document.body.scrollWidth")

    driver.set_window_size(page_width, page_height)

    result = driver.get_screenshot_as_base64()

    driver.quit()

    print("\nSuccessfully pulled data from roadmaps.sh...")

    return result


def get_roadmap(career: Career):
    roadmap: Roadmap = career.roadmap

    if not roadmap:
        return print("No Roadmap!")

    roadmap_content = get_roadmap_content(roadmap.link)

    if not roadmap_content:
        return print("Could not get screenshot!")

    print(f"\nGenerating your {career.name} career path for you!")

    template = Template(open(f"{directory}/src/template.html", "r").read())

    updated_template = template.render(
        career_title=career.name,
        video_link=roadmap.video,
        roadmap_link=roadmap.link,
        roadmap_content=roadmap_content,
        career_title_article="an" if vowels.count(career.name[0].lower()) > 0 else "a",
        guide=(
            f"<li><a href={roadmap.guide}>Explore Mosh Hamedani Guide</a></li>"
            if roadmap.guide
            else ""
        ),
    )

    output_path = os.path.join(
        str(Path.home() / "Downloads"), f"Amakuru Career Path - {career.name}.pdf"
    )

    pdfkit.from_string(
        input=updated_template,
        output_path=output_path,
        configuration=pdfkit.configuration(wkhtmltopdf=shutil.which("wkhtmltopdf")),
    )

    return output_path


def handle_user_choice(matches: list[Career]) -> None:
    try:
        choice = int(input("\nSelect an option (by number): "))

        if not choice:
            return print("Invalid choice. Please run the program again.")

        if choice == len(matches) + 1:
            return print("Exiting the program. Thank you for using Amakuru!")

        if 1 > choice or choice > len(matches):
            return print("Invalid choice. Please run the program again.")

        career = matches[choice - 1]

        if not career:
            return print(
                "Could not find the career, exiting the program. Thank you for using Amakuru!"
            )

        print(f"\nCreating Amakuru roadmap for {career.name}...")

        roadmap_path = get_roadmap(career)

        if not roadmap_path:
            return print("Could not generate roadmap")

        print("\nSuccessfully generated your Amakuru roadmap")

        should_open_file = input(
            "\nDo you want to open your roadmap file now? (yes/no): "
        ).lower()

        if should_open_file != "yes":
            return print(f"\nFile path - {roadmap_path}")

        print("\nOpening roadmap file now...")

        time.sleep(2)

        open_file(roadmap_path)

    except ValueError:
        print("\nInvalid input. Please enter a number.")


def search_career(user_input: str) -> None:
    matches = db.get_careers(user_input)

    if len(matches) > 0:
        print(
            f'\n>>>> You searched for "{user_input}", do you mean any of the following career paths?'
        )

        for i, match in enumerate(matches, start=1):
            print(f">>>> {i}. {match.name}")

        print(f">>>> {len(matches) + 1}. None of the above (Quit the program)")
    else:
        return print(
            "\n>>>> We could not find this career path so we are quitting the program, please try again."
        )

    handle_user_choice(matches)


def welcome():
    print("\nWelcome to Amakuru - Empowering Women in Tech!")

    db.populate_database()

    user_input = input("\nPlease enter the career path you are interested in: ")

    search_career(user_input)


# def main():
#     # Create argument parser
#     parser = argparse.ArgumentParser(description="Run the Amakuru CLI tool.")

#     parser.add_argument("command", help="The command to run the Amakuru program")

#     # Parse arguments
#     args = parser.parse_args()

#     if args.command == "start":
#         welcome()
#     else:
#         print("Invalid command. Please use 'start' to begin the program.")


if __name__ == "__main__":
    welcome()
