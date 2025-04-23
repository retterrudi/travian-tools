from dataclasses import dataclass, astuple
from enum import Enum
from typing import KeysView, Tuple

import numpy as np
import math

class TroopsSpartans(Enum):
    Hoplite = "Hoplite"
    Sentinel = "Sentinel"
    Shieldsman =  "Shieldsman"
    Twinsteel_Therion = "Twinsteel Therion"
    ElpidaRider = "Elpida Rider"
    CorinthianCrusher = "Corinthian Crusher"
    Ram = "Ram"
    Ballista = "Ballista"
    Ephor = "Ephor"
    Settler = "Settler"

@dataclass
class Resources:
    lumber: int = 0
    clay: int = 0
    iron: int = 0
    crop: int = 0

    def __add__(self, other: 'Resources'): 
        if isinstance(other, Resources): 
            return Resources(
                self.lumber + other.lumber, 
                self.clay + other.clay, 
                self.iron + other.iron, 
                self.crop + other.crop
            )
        else: 
            raise TypeError("Can only add Resources objects to each other")

    def __sub__(self, other: 'Resources'):
        if isinstance(other, Resources):
            return Resources(
                self.lumber - other.lumber, 
                self.clay - other.clay, 
                self.iron - other.iron, 
                self.crop - other.crop
            )
        else: 
            raise TypeError("Can only subtract Resources objects from each other")

    def __mul__(self, other: int):
        if isinstance(other, int):
            return Resources(
                self.lumber * other,
                self.clay * other, 
                self.iron * other, 
                self.crop * other
            )
        else: 
            return NotImplemented

    def __rmul__(self, other: int):
        return self.__mul__(other)

    def __getitem__(self, key: str) -> int:
        if key in self.__dict__:
            return self.__dict__[key]
        else: 
            raise KeyError(f"Resource '{key}' not found")

    def keys(self) -> KeysView:
        """Return a view object that displays a list of all the keys."""
        return self.__dict__.keys()

    def sum(self) -> int:
        return self.lumber + self.clay + self.iron + self.crop

    def has_negative_resources(self) -> bool:
        return any([self.lumber < 0, self.clay < 0, self.iron < 0, self.crop < 0])


def find_max_number_of_builds(available_resources: Resources, costs: Resources) -> int:
    max_builds = math.inf
    for key in available_resources.keys():
        if costs[key] > 0:
            max_builds = min(max_builds, math.floor(available_resources[key] / costs[key]))
    return max_builds if max_builds != math.inf else 0


def optimize_troops_coarse_then_fine(
        initial_resources: Resources, 
        troop1_cost: Resources, 
        troop2_cost: Resources, 
        step_size=10, 
        refine_window=10
    ) -> Tuple[int, int, int, Resources, Resources]:
    """
    Finds an approximate solution using a coarse grid search followed by fine-tuning.

    Args:
        initial_resources (dict): Starting resources.
        troop1_cost (dict): Costs for troop 1.
        troop2_cost (dict): Costs for troop 2.
        step_size (int): The step size for the initial coarse search.
        refine_window (int): How many steps around the best coarse point to search finely.

    Returns:
        tuple: (best_n1, best_n2, min_remaining_sum, final_remaining_resources, final_cost)
               for the best combination found.
    """
    NUMBER_OF_RESOURCES = 4

    best_n1_coarse = 0
    best_n2_coarse = 0
    min_remaining_sum_coarse = initial_resources.sum()
    min_abs_diff_coarse = math.inf

    # --- 1. Coarse Search ---
    # Find the max number of troop type 1
    max_troop1 = find_max_number_of_builds(initial_resources ,troop1_cost)

    for n1 in range(0, max_troop1 + 1, step_size): # Iterate with step_size
        cost_for_n1 = n1 * troop1_cost
        remaining_after_n1 = initial_resources - cost_for_n1

        possible_to_build_t2 = not remaining_after_n1.has_negative_resources()
        if not possible_to_build_t2: continue

        max_t2_given_n1 = find_max_number_of_builds(remaining_after_n1, troop2_cost)

        # if max_t2_given_n1 == int('inf'):
        #     if np.all(cost2_vector <= 0): max_t2_given_n1 = 0
        #     else: max_t2_given_n1 = 0 # Or handle large number if cost truly zero

        for n2 in range(0, int(max_t2_given_n1) + 1, step_size): # Iterate with step_size
            total_cost = n1 * troop1_cost + n2 * troop2_cost
            if not (initial_resources - total_cost).has_negative_resources():
                remaining_vector = initial_resources - total_cost
                current_remaining_sum = remaining_vector.sum()
                current_abs_diff = abs(n1 - n2)

                if current_remaining_sum < min_remaining_sum_coarse:
                    min_remaining_sum_coarse = current_remaining_sum
                    best_n1_coarse = n1
                    best_n2_coarse = n2
                    min_abs_diff_coarse = current_abs_diff
                elif current_remaining_sum == min_remaining_sum_coarse:
                    if current_abs_diff < min_abs_diff_coarse:
                        best_n1_coarse = n1
                        best_n2_coarse = n2
                        min_abs_diff_coarse = current_abs_diff

    # --- 2. Fine Search around the best coarse point ---
    best_n1_fine = best_n1_coarse
    best_n2_fine = best_n2_coarse
    min_remaining_sum_fine = min_remaining_sum_coarse
    min_abs_diff_fine = min_abs_diff_coarse

    # Define search window (ensure non-negative)
    n1_min = max(0, best_n1_coarse - refine_window)
    n1_max = best_n1_coarse + refine_window
    n2_min_base = max(0, best_n2_coarse - refine_window)
    n2_max_base = best_n2_coarse + refine_window

    for n1 in range(n1_min, n1_max + 1): # Iterate finely (step=1)
        cost_for_n1 = n1 * troop1_cost
        remaining_after_n1 = initial_resources - cost_for_n1

        # Recalculate max n2 possible for this specific n1
        possible_to_build_t2 = not remaining_after_n1.has_negative_resources()
        if not possible_to_build_t2: continue

        max_t2_given_n1 = find_max_number_of_builds(remaining_after_n1, troop2_cost)

        # if max_t2_given_n1 == float('inf'):
        #     if np.all(cost2_vector <= 0): max_t2_given_n1 = 0
        #     else: max_t2_given_n1 = 0

        # Adjust n2 search range based on affordability and window
        n2_min = n2_min_base
        n2_max = min(int(max_t2_given_n1), n2_max_base) # Cannot exceed affordable limit

        for n2 in range(n2_min, n2_max + 1): # Iterate finely
            total_cost = n1 * troop1_cost + n2 * troop2_cost
            # No need to check affordability again IF max_t2_given_n1 was calculated correctly
            # But check just in case of float issues / edge cases
            if not (initial_resources - total_cost).has_negative_resources():
                remaining_vector = initial_resources - total_cost
                current_remaining_sum = remaining_vector.sum()
                current_abs_diff = abs(n1 - n2)

                if current_remaining_sum < min_remaining_sum_fine:
                    min_remaining_sum_fine = current_remaining_sum
                    best_n1_fine = n1
                    best_n2_fine = n2
                    min_abs_diff_fine = current_abs_diff
                elif current_remaining_sum == min_remaining_sum_fine:
                    if current_abs_diff < min_abs_diff_fine:
                        best_n1_fine = n1
                        best_n2_fine = n2
                        min_abs_diff_fine = current_abs_diff

    # --- Calculate final state for the best fine result ---
    final_cost = best_n1_fine * troop1_cost + best_n2_fine * troop2_cost
    final_remaining_resources = initial_resources - final_cost

    return best_n1_fine, best_n2_fine, min_remaining_sum_fine, final_remaining_resources, final_cost


def main():
    my_resources = Resources(
        5500,
        3900,
        7100,
        3000, 
    )

    troop_costs_spartans = {
        TroopsSpartans.Hoplite: Resources(110, 185, 110, 35),
        TroopsSpartans.Sentinel: Resources(185, 150, 35, 75),
        TroopsSpartans.Shieldsman:  Resources(145, 95, 245, 45), 
        TroopsSpartans.Twinsteel_Therion: Resources(130, 200, 400, 65),
        TroopsSpartans.ElpidaRider: Resources(555, 445, 330, 110),
        TroopsSpartans.CorinthianCrusher: Resources(660, 495, 995, 165),
        TroopsSpartans.Ram: Resources(525, 260, 790, 130),
        TroopsSpartans.Ballista: Resources(550, 1240, 825, 135),
        TroopsSpartans.Ephor: Resources(33450, 30665, 36240, 13935),
        TroopsSpartans.Settler: Resources(5115, 5580, 6045, 3255)
    }
    
    print("\n--- Coarse+Fine Approach Result (Step=5, Window=5) ---")
    n1_cf, n2_cf, rem_cf, res_cf, cost_cf = optimize_troops_coarse_then_fine(
        my_resources, 
        troop_costs_spartans[TroopsSpartans.ElpidaRider], 
        troop_costs_spartans[TroopsSpartans.Shieldsman], 
        step_size=5, 
        refine_window=5
    )
    print(f"Troop 1: {n1_cf}, Troop 2: {n2_cf}, Remaining Sum: {rem_cf:.0f}")
    

if __name__ == '__main__':
    main()
