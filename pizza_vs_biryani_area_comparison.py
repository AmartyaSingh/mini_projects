import colorama
from colorama import Fore, Style


class PVB():
    def __init__(self) -> None:
        self.states = []
        self.state_areas = []
        self.uts = []
        self.ut_areas = []
        self.state_area_dict = {}
        self.ut_area_dict = {}
        self.state_codes = {}
        self.ut_codes = {}
        self.red_total_area = 0
        self.blue_total_area = 0
        self.states_file_path = 'states_areas.txt'

    def get_state_with_sizes(self):
        with open(self.states_file_path, "r") as file:
            content = file.readlines()

        states_flag = False
        ut_flag = False
        for line in content:
            if line.startswith("States of India:"):
                states_flag = True
                continue
            if line.startswith("Union Territories of India:"):
                ut_flag = True
                continue
            if line.strip() != "" and states_flag and not ut_flag:
                state_name_area = line.split(":")
                state_area = state_name_area[1].strip()
                state_area = state_area.replace(',', '')
                self.state_areas.append(int(state_area[:-4]))
                state_name = state_name_area[0].split(". ")[1].strip()
                self.states.append(state_name)
            if line.strip() != "" and ut_flag:
                ut_name_area = line.split(":")
                ut_area = ut_name_area[1].strip().strip(',')
                ut_area = ut_area.replace(',', '')
                self.ut_areas.append(int(ut_area[:-4]))
                ut_name = ut_name_area[0].split(". ")[1].strip()
                self.uts.append(ut_name)

    def create_dict_state_area(self):
        for state, area in zip(self.states, self.state_areas):
            self.state_area_dict[state] = area
        for ut, area in zip(self.uts, self.ut_areas):
            self.ut_area_dict[ut] = area

    def create_dict_state_code(self):
        for index, state in enumerate(self.states):
            self.state_codes[index+1] = state

    def display_state_ut_dict(self):
        print("States: Area\n" + str(self.state_area_dict))
        print("Union Territories: Area\n" + str(self.ut_area_dict))

    def display_state_ut_code_dict(self):
        # Initialize Colorama
        colorama.init()
        print("States: Code\n")
        # Find the length of the longest state name
        max_length_states = max(len(state) for state in self.state_codes.values())
        # Find the length of the longest ut name
        max_length_uts = max(len(state) for state in self.ut_codes.values())
        max_length = max(max_length_states, max_length_uts)
        # Print the aligned states
        for value, state in self.state_codes.items():
            print("{:<{}}: {:>2}".format(Fore.BLUE + state + Style.RESET_ALL, max_length, Fore.GREEN + str(value) + Style.RESET_ALL))
        
        # Print the aligned uts
        for value, ut in self.ut_codes.items():
            print("{:<{}}: {:>2}".format(Fore.YELLOW + ut + Style.RESET_ALL, max_length, Fore.GREEN + str(value) + Style.RESET_ALL))
        
        print("\n")
        # Deinitialize Colorama
        colorama.deinit()

    def create_dict_ut_code(self):
        for index, ut in enumerate(self.uts):
            self.ut_codes[index+29] = ut

    def team_segregation(self):
        try:
            # Initialize Colorama
            colorama.init()

            red_user_input = input(Fore.RED + "Enter #RED states code (separate code with space): " + Style.RESET_ALL)
            parse_red_input = red_user_input.split(" ")
            blue_user_input = input(Fore.BLUE + "Enter #BLUE states code (separate code with space): " + Style.RESET_ALL)
            parse_blue_input = blue_user_input.split(" ")
            
            for red_code in parse_red_input:
                if int(red_code) in self.state_codes.keys():
                    self.red_total_area += self.state_area_dict[self.state_codes[int(red_code)]]
                elif int(red_code) in self.ut_codes.keys():
                    self.red_total_area += self.ut_area_dict[self.ut_codes[int(red_code)]]
                else:
                    print(Fore.RED + f"Invalid code: {red_code}" + Style.RESET_ALL)
            
            for blue_code in parse_blue_input:
                if int(blue_code) in self.state_codes.keys():
                    self.blue_total_area += self.state_area_dict[self.state_codes[int(blue_code)]]
                elif int(blue_code) in self.ut_codes.keys():
                    self.blue_total_area += self.ut_area_dict[self.ut_codes[int(blue_code)]]
                else:
                    print(Fore.RED + f"Invalid code: {blue_code}" + Style.RESET_ALL)

            if self.red_total_area > 0 or self.blue_total_area > 0:
                print("\nRed Team Total Area:", Fore.LIGHTRED_EX + str(self.red_total_area) + Style.RESET_ALL)
                print("Blue Team Total Area:", Fore.LIGHTBLUE_EX + str(self.blue_total_area) + Style.RESET_ALL)
                print("\n")
            # Deinitialize Colorama
            else:
                raise ValueError
            colorama.deinit()
            
        except ValueError:
            print(Fore.RED + "Invalid input, retry removing spaces before and after code insertions." + Style.RESET_ALL)
            self.team_segregation()

if __name__ == "__main__":   
    pvb = PVB()
    pvb.get_state_with_sizes()
    pvb.create_dict_state_area()
    pvb.create_dict_state_code()
    pvb.create_dict_ut_code()
    pvb.display_state_ut_code_dict()
    pvb.team_segregation()

