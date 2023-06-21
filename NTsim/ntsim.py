import tkinter as tk
from tkinter import messagebox, StringVar, Label, Button, Toplevel, Listbox
from neurosim.nt import Game, Food, Activity

class NeuroSimulatorApp(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Neuro Simulator")
        self.geometry("600x400")
        
        self.status_text = StringVar()
        self.status_label = Label(self, textvariable=self.status_text, wraplength=500)
        self.status_label.pack()
        
        self.food_var = StringVar(self)
        self.food_options = [food.name for food in self.game.foods]
        self.food_dropdown = tk.OptionMenu(self, self.food_var, *self.food_options)
        self.food_dropdown.pack()
        self.consume_food_button = Button(self, text="Consume Selected Food", command=self.consume_food)
        self.consume_food_button.pack()
        
        self.activity_var = StringVar(self)
        self.activity_options = [activity.name for activity in self.game.activities]
        self.activity_dropdown = tk.OptionMenu(self, self.activity_var, *self.activity_options)
        self.activity_dropdown.pack()
        self.perform_activity_button = Button(self, text="Perform Selected Activity", command=self.perform_activity)
        self.perform_activity_button.pack()
        
        self.info_button = Button(self, text="Info on Neurotransmitters", command=self.display_info)
        self.info_button.pack()
        
        self.quit_button = Button(self, text="Quit", command=self.quit)
        self.quit_button.pack()
        
        self.update_status_text()

    def update_status_text(self):
        status = []
        for key, neurotransmitter in self.game.character.neurotransmitters.items():
            level = self.game.character.levels[key]
            status.append(f"{key} ({neurotransmitter}): {level}%")
        for key, receptor in self.game.character.receptors.items():
            efficiency = self.game.character.efficiencies[key]
            status.append(f"{key} ({receptor}): {efficiency}%")
        for condition in self.game.character.conditions:
            status.append(condition)
        self.status_text.set("\n".join(status))

    def consume_food(self):
        selected_food = self.food_var.get()
        for food in self.game.foods:
            if food.name == selected_food:
                self.game.consume_food(food)
                messagebox.showinfo("Food Effect", self.game.last_action_effect)  # Add this line
                break
        self.update_status_text()

    def perform_activity(self):
        selected_activity = self.activity_var.get()
        for activity in self.game.activities:
            if activity.name == selected_activity:
                self.game.perform_activity(activity)
                messagebox.showinfo("Activity Effect", self.game.last_action_effect)  # Add this line
                break
        self.update_status_text()

    def display_info(self):
        info_window = Toplevel(self)
        info_window.title("Neurotransmitter Info")
        info_listbox = Listbox(info_window, width=80, height=20)
        info_listbox.pack()
    
        neurotransmitter_info = self.game.display_info()
    
        for neurotransmitter, info in neurotransmitter_info.items():
            info_listbox.insert(tk.END, f"{neurotransmitter}:")
            for key, value in info.items():
                info_listbox.insert(tk.END, f"  {key}: {value}")
        info_listbox.insert(tk.END, "")


if __name__ == "__main__":
    # Initialize the game with a character named "Bob Testsubject"
    game = Game("Bob Testsubject")
    
    # Initialize and run the GUI
    app = NeuroSimulatorApp(game)
    app.mainloop()