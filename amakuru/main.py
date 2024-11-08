import re
import argparse
from database import career_paths, roadmaps

def handle_user_choice(matches: list[str]) -> None:
    try:
        choice = int(input("Select an option (by number): "))

        if choice == len(matches) + 1:
            print("Exiting the program. Thank you for using Amakuru!")
        elif 1 <= choice <= len(matches):
            career = matches[choice - 1]
            
            if career:
                print(f"You selected: {career}")
                
                print(f"Creating Amakuru roadmap for {career}...")
                
                if roadmaps.get(career):
                    # Printing roadmap link for now
                    print(f"roadmap link = {roadmaps.get(career).get('link')}")
                
                # create pdf from amakuru design, 
                # pull data from roadmaps.sh content as html design & paste, 
                # add at the top of the pdf file, a link to the roadmap video to watch, a link to roadmaps.sh and a link to the Mosh Hamedani guide 
        else:
            print("Invalid choice. Please run the program again.")
    
    except ValueError:
        print("Invalid input. Please enter a number.")

def search_career(user_input: str) -> None:
    pattern = re.compile(re.escape(user_input), re.IGNORECASE)

    matches = [career for career in career_paths if pattern.search(career)]
    
    if len(matches) > 0:
        print(f">>>> You searched for \"{user_input}\", do you mean any of the following career paths?")
        
        for i, match in enumerate(matches, start=1):
            print(f">>>> {i}. {match}")
        
        print(f">>>> {len(matches) + 1}. None of the above (Quit the program)")
    else:
        return print(">>>> We could not find this career path so we are quitting the program, please try again.")

    handle_user_choice(matches)

def welcome():
    print("Welcome to Amakuru - Empowering Women in Tech!")
     
    user_input = input("Please enter the career path you are interested in: ")
 
    search_career(user_input)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Run the Amakuru CLI tool.")
    
    parser.add_argument("command", help="The command to run the Amakuru program")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "start":
        welcome()
    else:
        print("Invalid command. Please use 'start' to begin the program.")

if __name__ == "__main__":
    main()