class Character:
    def __init__(self, name):
        self.name = name
        self.neurotransmitters = {
            "NT1": "serotonin",
            "NT2": "dopamine",
            "NT3": "norepinephrine",
            "NT4": "epinephrine",
            "NT5": "acetylcholine",
            "NT6": "GABA",
            "NT7": "glutamate",
            "NT8": "endorphins",
            "NT9": "histamine",
            "NT10": "glycine"
        }
        self.receptors = {
            "R1": "serotonin",
            "R2": "dopamine",
            "R3": "norepinephrine",
            "R4": "epinephrine",
            "R5": "acetylcholine",
            "R6": "GABA",
            "R7": "glutamate",
            "R8": "endorphins",
            "R9": "histamine",
            "R10": "glycine",
        }
        self.levels = {key: 100 for key in self.neurotransmitters.keys()}
        self.efficiencies = {key: 100 for key in self.receptors.keys()}
        self.conditions = []

        self.update_conditions()

    def update_conditions(self):
        self.conditions.clear()
        neurotransmitter_relations = {nk: rk for nk, rk in zip(self.neurotransmitters.keys(), self.receptors.keys())}

        neurotransmitter_effects = {
            "NT1": {"too_much": "Serotonin syndrome (agitation, restlessness, rapid heart rate)", "too_little": "Depression, anxiety"},
            "NT2": {"too_much": "Schizophrenia, mania", "too_little": "Parkinson's disease, depression, certain addictions"},
            "NT3": {"too_much": "Hypertension, anxiety, panic", "too_little": "Depression, mental cloudiness, low energy"},
            "NT4": {"too_much": "Hypertension, anxiety, panic", "too_little": "Depression, mental cloudiness, low energy"},
            "NT5": {"too_much": "Muscle weakness, blurred vision, breathing difficulties", "too_little": "Cognitive deficits (e.g., Alzheimer's disease)"},
            "NT6": {"too_much": "Sedation, respiratory distress", "too_little": "Anxiety, seizures, epilepsy"},
            "NT7": {"too_much": "Excitotoxicity, potential neurodegenerative diseases like Alzheimer's and Parkinson's", "too_little": "Psychosis, coma, death"},
            "NT8": {"too_much": "Decreased pain response, dependence", "too_little": "Increased sensitivity to pain"},
            "NT9": {"too_much": "Allergies, inflammation, gastric acid release", "too_little": "Sedation, low gastric acid release"},
            "NT10": {"too_much": "Excessive inhibition of neuronal activity, respiratory distress", "too_little": "Hyperexcitability, seizures"}
        }

        for nt_key, nt_level in self.levels.items():
            receptor_key = neurotransmitter_relations[nt_key]
            receptor_efficiency = self.efficiencies[receptor_key] / 100
            adjusted_nt_level = nt_level * receptor_efficiency

            if adjusted_nt_level < 100:
                self.conditions.append(f"{self.neurotransmitters[nt_key]} deficiency risk - {neurotransmitter_effects[nt_key]['too_little']}")
            if adjusted_nt_level > 150:
                self.conditions.append(f"{self.neurotransmitters[nt_key]} excess risk - {neurotransmitter_effects[nt_key]['too_much']}")

        for receptor_key, efficiency in self.efficiencies.items():
            if efficiency < 100:
                self.conditions.append(f"{self.receptors[receptor_key]} receptor deficiency risk")
            if efficiency > 150:
                self.conditions.append(f"{self.receptors[receptor_key]} receptor excess risk")

        if not self.conditions:
            self.conditions.append("Healthy")

class Brain:
    def __init__(self, character):
        self.character = character

    def modify_neurotransmitter(self, neurotransmitter, amount):
        if neurotransmitter in self.character.levels:
            self.character.levels[neurotransmitter] += amount
            self.character.update_conditions()

    def modify_receptor_efficiency(self, receptor, amount):
        if receptor in self.character.efficiencies:
            self.character.efficiencies[receptor] += amount
            self.character.update_conditions()


class Food:
    def __init__(self, name, effects, explanation):
        self.name = name
        self.effects = effects
        self.explanation = explanation


class Activity:
    def __init__(self, name, effects, explanation):
        self.name = name
        self.effects = effects
        self.explanation = explanation

class Game:
    def __init__(self, character_name):
        self.character = Character(character_name)
        self.brain = Brain(self.character)
        self.last_action_effect = ""
        self.info_text = ""
        self.neurotransmitter_info = {
            "GABA": {
                "receptors": "GABA(A), GABA(B) receptors",
                "too_much": "Sedation, respiratory distress",
                "too_little": "Anxiety, seizures, epilepsy",
                "precursors": "Glutamate",
                "cofactors": "Vitamin B6"
            },
            "Glutamate": {
                "receptors": "AMPA, NMDA, Kainate, Metabotropic Glutamate receptors",
                "too_much": "Excitotoxicity, potential neurodegenerative diseases like Alzheimer's and Parkinson's",
                "too_little": "Psychosis, coma, death",
                "precursors": "Glutamine",
                "cofactors": "N/A"
            },
            "Dopamine": {
                "receptors": "D1, D2, D3, D4, D5 receptors",
                "too_much": "Schizophrenia, mania",
                "too_little": "Parkinson's disease, depression, certain addictions",
                "precursors": "Tyrosine",
                "cofactors": "Vitamin B6, Folate, Iron"
            },
            "Serotonin": {
                "receptors": "7 families of serotonin receptors (5-HT1, 5-HT2, etc.) with multiple subtypes",
                "too_much": "Serotonin syndrome (agitation, restlessness, rapid heart rate)",
                "too_little": "Depression, anxiety",
                "precursors": "Tryptophan",
                "cofactors": "Vitamin B6, Folate"
            },
            "Norepinephrine": {
                "receptors": "Alpha-1, Alpha-2, Beta receptors",
                "too_much": "Hypertension, anxiety, panic",
                "too_little": "Depression, mental cloudiness, low energy",
                "precursors": "Dopamine",
                "cofactors": "Vitamin C, Copper"
            },
            "Acetylcholine": {
                "receptors": "Muscarinic and Nicotinic receptors",
                "too_much": "Muscle weakness, blurred vision, breathing difficulties",
                "too_little": "Cognitive deficits (e.g., Alzheimer's disease)",
                "precursors": "Choline",
                "cofactors": "Vitamin B5"
            },
            "Endorphins": {
                "receptors": "Mu, delta, and kappa opioid receptors",
                "too_much": "Decreased pain response, dependence",
                "too_little": "Increased sensitivity to pain",
                "precursors": "N/A",
                "cofactors": "N/A"
            },
            "Epinephrine": {
                "receptors": "Alpha-1, Alpha-2, Beta receptors",
                "too_much": "Hypertension, anxiety, panic",
                "too_little": "Depression, mental cloudiness, low energy",
                "precursors": "Norepinephrine",
                "cofactors": "Vitamin C, Copper"
            },
            "Histamine": {
                "receptors": "H1, H2, H3, H4 receptors",
                "too_much": "Allergies, inflammation,gastric acid release",
                "too_little": "Sedation, low gastric acid release",
                "precursors": "Histidine",
                "cofactors": "Vitamin B6, Copper"
            },
            "Glycine": {
                "receptors": "Glycine receptors, and as a co-agonist of NMDA receptors",
                "too_much": "Excessive inhibition of neuronal activity, respiratory distress",
                "too_little": "Hyperexcitability, seizures",
                "precursors": "Serine",
                "cofactors": "Vitamin B6"
            }
        }
        self.foods = [
            Food(
                "Banana",
                {"neurotransmitters": {"NT1": 5}},
                "Bananas contain tryptophan, which is a precursor to serotonin. Consuming bananas can increase serotonin levels."
            ),
            Food(
                "Chocolate",
                {"neurotransmitters": {"NT2": 10, "NT6": -5}},
                "Chocolate contains phenylethylamine, which can cause the brain to release dopamine. However, it also contains substances that can inhibit GABA."
            ),
            Food(
                "Almonds",
                {"neurotransmitters": {"NT6": 5}},
                "Almonds are rich in magnesium, which is known to reduce anxiety. This is possibly linked to increased GABA activity."
            ),
            Food(
                "Salmon",
                {"neurotransmitters": {"NT1": 7}},
                "Salmon is rich in omega-3 fatty acids, which are known to improve brain function and mood, possibly by increasing serotonin levels."
            ),
            Food(
                "Coffee",
                {"neurotransmitters": {"NT3": 10, "NT4": 10}},
                "Coffee increases the release of catecholamines such as norepinephrine and epinephrine, which can increase alertness and energy levels."
            ),
            Food(
                "Spinach",
                {"neurotransmitters": {"NT6": 5, "NT1": 5, "NT2": 5, "NT7": 5, "NT9": 5}},
                "Spinach is high in various nutrients and can have a positive effect on GABA, serotonin, dopamine, glutamate, and histamine levels."
            ),
            Food(
                "Eggs",
                {"neurotransmitters": {"NT1": 5, "NT2": 5}},
                "Eggs are rich in choline and can increase the production of acetylcholine, a neurotransmitter important for memory and communication among brain cells."
            ),
            Food(
                "Turkey",
                {"neurotransmitters": {"NT1": 5}},
                "Turkey is rich in tryptophan, which is a precursor to serotonin. Consuming turkey can help increase serotonin levels."
            ),
            Food(
                "Avocado",
                {"neurotransmitters": {"NT2": 5}},
                "Avocado contains tyrosine, which is a precursor to dopamine. Eating avocado can help increase dopamine levels."
            ),
            Food(
                "Blueberries",
                {"neurotransmitters": {"NT3": 5}},
                "Blueberries are rich in antioxidants that can enhance the production of norepinephrine, improving mood and memory."
            ),
            Food(
                "Cheddar Cheese",
                {"neurotransmitters": {"NT5": 5}},
                "Cheddar cheese contains choline, which is used by the body to produce acetylcholine, a neurotransmitter important for memory and muscle control."
            ),
            Food(
                "Broccoli",
                {"neurotransmitters": {"NT7": 5}},
                "Broccoli is rich in glutamate, an amino acid that acts as a neurotransmitter involved in cognitive functions."
            ),
            Food(
                "Yogurt",
                {"neurotransmitters": {"NT6": 5}},
                "Yogurt contains probiotics which can have a positive effect on the production of GABA, a neurotransmitter that reduces anxiety and stress."
            ),
            Food(
                "Chili Peppers",
                {"neurotransmitters": {"NT8": 5}},
                "Chili peppers can trigger the release of endorphins, the body's natural painkillers, and can improve mood."
            ),
            Food(
                "Tomatoes",
                {"neurotransmitters": {"NT9": 5}},
                "Tomatoes contain histidine, which can be converted into histamine. Histamine is involved in the immune response, digestion, and central nervous system."
            ),
            Food(
                "Beans",
                {"neurotransmitters": {"NT10": 5}},
                "Beans are rich in glycine, an inhibitory neurotransmitter that can improve sleep and decrease anxiety."
            ),
            Food(
                "Green Tea", 
                {"neurotransmitters": {"NT6": 5, "NT2": 5, "NT1": 5}}, 
                "Green tea contains L-theanine which can increase levels of GABA, dopamine, and serotonin."
            ),
            Food(
                "Nuts and Seeds", 
                {"neurotransmitters": {"NT1": 5}}, 
                "Nuts and seeds are rich in omega-3 fatty acids, which are known to improve brain function and mood."
            ),
            Food(
                "Whole Grains", 
                {"neurotransmitters": {"NT1": 5}}, 
                "Whole grains contain tryptophan which is a precursor to serotonin."
            ),
            Food(
                "Curcumin (Turmeric)", 
                {"receptors": {"R2": 5}}, 
                "Curcumin, found in turmeric, has been shown to modulate the activity of dopamine receptors."
            ),
            Food(
                "Magnesium-rich foods", 
                {"receptors": {"R7": 5}}, 
                "Foods rich in magnesium, such as spinach, nuts, and seeds, are known to modulate NMDA glutamate receptors."
            ),
            Food(
                "Excessive Caffeine", 
                {"receptors": {"R3": -5, "R4": -5}}, 
                "Excessive consumption of caffeine can lead to desensitization of adenosine receptors, affecting sleep quality and increasing anxiety."
            ),
            Food(
                "Alcohol", 
                {"receptors": {"R6": -5, "R7": -5}}, 
                "Chronic alcohol consumption can negatively affect GABA and glutamate receptors, leading to changes in mood and cognitive function."
            ),
            Food(
                "High Sugar Intake", 
                {"receptors": {"R2": -5}}, 
                "Consuming high amounts of sugar can lead to reduced sensitivity of dopamine receptors, affecting mood and reward processing."
            ),
        ]
        self.activities = [
           Activity(
                "Exercise",
                {"neurotransmitters": {"NT2": 10, "NT8": 5}},
                "Exercise has been shown to increase dopamine and endorphin levels, which can improve mood and reduce pain."
            ),
            Activity(
                "Meditation",
                {"neurotransmitters": {"NT6": 10}},
                "Meditation can increase GABA levels, which helps to reduce anxiety and improve mood."
            ),
            Activity(
                "Listening to Music",
                {"neurotransmitters": {"NT2": 5, "NT1": 5}},
                "Listening to music you enjoy can increase dopamine and serotonin levels, improving mood and relaxation."
            ),
            Activity(
                "Reading a Book",
                {"neurotransmitters": {"NT6": 5}},
                "Reading a book can be relaxing and help in reducing stress, possibly through increasing GABA levels."
            ),
            Activity(
                "Socializing",
                {"neurotransmitters": {"NT2": 7, "NT8": 5}},
                "Socializing and spending time with friends can increase dopamine and endorphin levels, contributing to a better mood and reduced stress."
            ),
            Activity(
                "Playing a Musical Instrument",
                {"neurotransmitters": {"NT2": 5, "NT1": 4}},
                "Playing a musical instrument can be a form of creative expression and has been shown to increase dopamine and serotonin levels."
            ),
            Activity(
                "Gardening",
                {"neurotransmitters": {"NT6": 5, "NT8": 4}},
                "Gardening can be a relaxing activity that reduces stress and increases endorphin levels."
            ),
            Activity(
                "Taking a Walk in Nature",
                {"neurotransmitters": {"NT1": 5, "NT6": 5}},
                "Taking a walk in a natural environment can be calming and has been shown to increase serotonin and GABA levels, improving mood and reducing anxiety."
            ),
            Activity(
                "Deep Breathing", 
                {"receptors": {"R6": 5}}, 
                "Deep breathing exercises can increase the efficiency of GABA receptors, helping to reduce anxiety and stress."
            ),
            Activity(
                "Learning a New Skill", 
                {"receptors": {"R5": 5}}, 
                "Engaging in learning improves brain plasticity and can increase the efficiency of acetylcholine receptors, which are important for learning and memory."
            ),
            Activity(
                "Playing Video Games", 
                {"receptors": {"R2": 5}}, 
                "Playing video games can increase the efficiency of dopamine receptors, improving mood and concentration."
            ),
            Activity(
                "Yoga", 
                {"receptors": {"R1": 5, "R6": 5}}, 
                "Yoga can increase the efficiency of serotonin and GABA receptors, helping to improve mood and reduce anxiety."
            ),
            Activity(
                "Cold Exposure", 
                {"receptors": {"R3": 5, "R4": 5}}, 
                "Exposure to cold can increase the efficiency of norepinephrine and epinephrine receptors, improving alertness and mood."
            ),
            Activity(
                "Solving Puzzles", 
                {"receptors": {"R7": 5}}, 
                "Solving puzzles and engaging in problem-solving activities can increase the efficiency of glutamate receptors, which are involved in learning and memory."
            ),
            Activity(
                "Allergy Management", 
                {"receptors": {"R9": 5}}, 
                "Proper allergy management can optimize the function of histamine receptors, which are involved in immune responses and brain function."
            ),
            Activity(
                "Adequate Sleep", 
                {"receptors": {"R10": 5}}, 
                "Getting adequate sleep can increase the efficiency of glycine receptors, which are involved in the regulation of sleep and relaxation."
            ),
            Activity(
                "Cognitive Behavioral Therapy", 
                {"receptors": {"R1": 5}}, 
                "Cognitive Behavioral Therapy has been shown to modulate serotonin receptor sensitivity, which can be beneficial in the treatment of depression."
            ),
            Activity(
                "Regular Physical Exercise", 
                {"receptors": {"R8": 5}}, 
                "Regular physical exercise has been shown to increase the sensitivity of endorphin receptors, which can improve mood and reduce pain."
            ),
            Activity(
                "Chronic Stress", 
                {"receptors": {"R1": -5, "R2": -5}}, 
                "Chronic stress can lead to changes in the sensitivity of cortisol receptors and can negatively affect serotonin and dopamine levels."
            ),
            Activity(
                "Lack of Physical Activity", 
                {"receptors": {"R8": -5}}, 
                "A sedentary lifestyle can lead to reduced sensitivity of endorphin receptors and can negatively affect mood."
            ),
            Activity(
                "Social Isolation", 
                {"receptors": {"R1": -5, "R2": -5}}, 
                "Social isolation can lead to changes in dopamine and serotonin receptors, negatively affecting mood and social behavior."
            )
        ]

    def modify(self, modify_func, resource_type):
        resource_map = self.character.neurotransmitters if resource_type == "neurotransmitter" else self.character.receptors
        resource_name = f"{resource_type.capitalize()} to modify"
        resource_num = input(f"Which {resource_name.lower()}? ({', '.join(resource_map.keys())}): ")
        if resource_num in resource_map:
            effect_map = {"increase": 1, "decrease": -1}
            effect = input("Increase or decrease? ").lower()
            if effect in effect_map:
                modify_func(resource_num, 25 * effect_map[effect])
            else:
                print("Invalid selection!")
        else:
            print("Invalid selection!")

    def consume_food(self, food):
        nt_effects = food.effects.get('neurotransmitters', {})
        receptor_effects = food.effects.get('receptors', {})
    
        nt_effects_str = ', '.join([f"{self.character.neurotransmitters[nt_key]} levels by {effect}%" for nt_key, effect in nt_effects.items()])
        receptor_effects_str = ', '.join([f"{self.character.receptors[receptor_key]} receptor efficiency by {effect}%" for receptor_key, effect in receptor_effects.items()])
    
        self.last_action_effect = f"{self.character.name} consumed {food.name}. {food.explanation} This changed {nt_effects_str} and {receptor_effects_str}."
    
        for nt_key, effect in nt_effects.items():
            receptor_key = "R" + nt_key[2:]
            receptor_multiplier = self.character.efficiencies[receptor_key] / 100
            self.brain.modify_neurotransmitter(nt_key, effect * receptor_multiplier)
    
        for receptor_key, effect in receptor_effects.items():
            self.brain.modify_receptor_efficiency(receptor_key, effect)
    
        self.character.update_conditions()

    def perform_activity(self, activity):
        nt_effects_str = ', '.join([f"{self.character.neurotransmitters[nt_key]} levels by {effect}%" for nt_key, effect in activity.effects.get("neurotransmitters", {}).items()])
        receptor_effects_str = ', '.join([f"{self.character.receptors[receptor_key]} receptor efficiency by {effect}%" for receptor_key, effect in activity.effects.get("receptors", {}).items()])
        self.last_action_effect = f"{self.character.name} performed {activity.name}. {activity.explanation} This changed {nt_effects_str} and {receptor_effects_str}."
        for nt_key, effect in activity.effects.get("neurotransmitters", {}).items():
            receptor_key = "R" + nt_key[2:]
            receptor_multiplier = self.character.efficiencies[receptor_key] / 100
            self.brain.modify_neurotransmitter(nt_key, effect * receptor_multiplier)
        for receptor_key, effect in activity.effects.get("receptors", {}).items():
            self.brain.modify_receptor_efficiency(receptor_key, effect)
        self.character.update_conditions()

    def display_info(self):
        neurotransmitter_info = {
            "GABA": {
                "receptors": "GABA(A), GABA(B) receptors",
                "too_much": "Sedation, respiratory distress",
                "too_little": "Anxiety, seizures, epilepsy",
                "precursors": "Glutamate",
                "cofactors": "Vitamin B6"
            },
            "Glutamate": {
                "receptors": "AMPA, NMDA, Kainate, Metabotropic Glutamate receptors",
                "too_much": "Excitotoxicity, potential neurodegenerative diseases like Alzheimer's and Parkinson's",
                "too_little": "Psychosis, coma, death",
                "precursors": "Glutamine",
                "cofactors": "N/A"
            },
            "Dopamine": {
                "receptors": "D1, D2, D3, D4, D5 receptors",
                "too_much": "Schizophrenia, mania",
                "too_little": "Parkinson's disease, depression, certain addictions",
                "precursors": "Tyrosine",
                "cofactors": "Vitamin B6, Folate, Iron"
            },
            "Serotonin": {
                "receptors": "7 families of serotonin receptors (5-HT1, 5-HT2, etc.) with multiple subtypes",
                "too_much": "Serotonin syndrome (agitation, restlessness, rapid heart rate)",
                "too_little": "Depression, anxiety",
                "precursors": "Tryptophan",
                "cofactors": "Vitamin B6, Folate"
            },
            "Norepinephrine": {
                "receptors": "Alpha-1, Alpha-2, Beta receptors",
                "too_much": "Hypertension, anxiety, panic",
                "too_little": "Depression, mental cloudiness, low energy",
                "precursors": "Dopamine",
                "cofactors": "Vitamin C, Copper"
            },
            "Acetylcholine": {
                "receptors": "Muscarinic and Nicotinic receptors",
                "too_much": "Muscle weakness, blurred vision, breathing difficulties",
                "too_little": "Cognitive deficits (e.g., Alzheimer's disease)",
                "precursors": "Choline",
                "cofactors": "Vitamin B5"
            },
            "Endorphins": {
                "receptors": "Mu, delta, and kappa opioid receptors",
                "too_much": "Decreased pain response, dependence",
                "too_little": "Increased sensitivity to pain",
                "precursors": "N/A",
                "cofactors": "N/A"
            },
            "Epinephrine": {
                "receptors": "Alpha-1, Alpha-2, Beta receptors",
                "too_much": "Hypertension, anxiety, panic",
                "too_little": "Depression, mental cloudiness, low energy",
                "precursors": "Norepinephrine",
                "cofactors": "Vitamin C, Copper"
            },
            "Histamine": {
                "receptors": "H1, H2, H3, H4 receptors",
                "too_much": "Allergies, inflammation,gastric acid release",
                "too_little": "Sedation, low gastric acid release",
                "precursors": "Histidine",
                "cofactors": "Vitamin B6, Copper"
            },
            "Glycine": {
                "receptors": "Glycine receptors, and as a co-agonist of NMDA receptors",
                "too_much": "Excessive inhibition of neuronal activity, respiratory distress",
                "too_little": "Hyperexcitability, seizures",
                "precursors": "Serine",
                "cofactors": "Vitamin B6"
            }
        }

        return neurotransmitter_info