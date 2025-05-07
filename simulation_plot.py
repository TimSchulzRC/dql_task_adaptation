import matplotlib.pyplot as plt
from simulation_const import DQL_MODEL
from simulation_util import calc_task_complexities
import numpy as np
import scipy.stats as stats

def plot_simulation_log(simulationLog: dict[str, list[list[float]]], learnerId: int):
    task_count = len(simulationLog[learnerId]["tasks"])
    plt.figure(figsize=(16, 9))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, key in enumerate(DQL_MODEL):
        color = colors[i % len(colors)]

        aggregated_competency_values = []
        aggregated_task_values = []
        aggregated_competency_plus_bonus_values = []
        for i in range(task_count):
            # Get competency value
            competency_values = simulationLog[learnerId]["competencies"][i][key]
            competency_aggregated = sum(
                competency_values)/len(competency_values)
            aggregated_competency_values.append(competency_aggregated)

            # Get task complexity value
            task_values = calc_task_complexities(
                simulationLog[learnerId]["tasks"][i])[key]
            task_aggregated = sum(task_values)/len(task_values)
            aggregated_task_values.append(task_aggregated)

            scaffolding_bonus_values = simulationLog[learnerId]["scaffolding_bonuses"][i][key]
            # Add the scaffolding bonus to the competency value
            competency_plus_bonus_values = [
                a + b for a, b in zip(scaffolding_bonus_values, competency_values)]
            competency_plus_bonus_aggregated = sum(
                competency_plus_bonus_values)/len(competency_plus_bonus_values)
            aggregated_competency_plus_bonus_values.append(
                competency_plus_bonus_aggregated)

        plt.plot(range(task_count), aggregated_competency_values,
                 color=color, label=f'{key} competency')
        plt.plot(range(task_count), aggregated_task_values,
                 '.', color=color, label=f'{key} task')
        plt.plot(range(task_count), aggregated_competency_plus_bonus_values,
                 '--', color=color, label=f'{key} competency + scaffolding bonus')

    plt.ylim(0, 1)
    plt.xlim(0, task_count-1)
    plt.ylabel("Competency")
    plt.xlabel("Step")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(
        f"sql_task_adaptation_{learnerId}.png", dpi=300, bbox_inches="tight")
    
    
def plot_mean_simulation_log(simulationLog):
    learner_count = len(simulationLog)
    # Find the maximum task count among all learners
    max_task_count = max(len(log["tasks"]) for log in simulationLog)
    
    plt.figure(figsize=(16, 9))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    # For each DQL category
    for i, key in enumerate(DQL_MODEL):
        color = colors[i % len(colors)]
        
        # Initialize lists to store aggregated values
        mean_competency_values = [[] for _ in range(max_task_count)]
        mean_task_values = [[] for _ in range(max_task_count)]
        mean_competency_plus_bonus_values = [[] for _ in range(max_task_count)]
        
        # Collect values for each learner and task
        for learner_id in range(learner_count):
            learner_task_count = len(simulationLog[learner_id]["tasks"])
            
            for task_id in range(learner_task_count):
                # Get competency value
                competency_values = simulationLog[learner_id]["competencies"][task_id][key]
                competency_aggregated = sum(competency_values)/len(competency_values)
                mean_competency_values[task_id].append(competency_aggregated)
                
                # Get task complexity value
                task_values = calc_task_complexities(simulationLog[learner_id]["tasks"][task_id])[key]
                task_aggregated = sum(task_values)/len(task_values)
                mean_task_values[task_id].append(task_aggregated)
                
                # Get scaffolding bonus
                scaffolding_bonus_values = simulationLog[learner_id]["scaffolding_bonuses"][task_id][key]
                # Add scaffolding bonus to competency
                competency_plus_bonus_values = [a + b for a, b in zip(scaffolding_bonus_values, competency_values)]
                competency_plus_bonus_aggregated = sum(competency_plus_bonus_values)/len(competency_plus_bonus_values)
                mean_competency_plus_bonus_values[task_id].append(competency_plus_bonus_aggregated)
        
        # Calculate means across learners for each task
        mean_competency_across_learners = [sum(values)/len(values) if values else 0 for values in mean_competency_values]
        mean_task_across_learners = [sum(values)/len(values) if values else 0 for values in mean_task_values]
        mean_competency_plus_bonus_across_learners = [sum(values)/len(values) if values else 0 for values in mean_competency_plus_bonus_values]
        
        # Plot only valid data points (up to the maximum task count with data)
        valid_task_count = max(i for i, values in enumerate(mean_competency_values) if values) + 1
        
        plt.plot(range(valid_task_count), mean_competency_across_learners[:valid_task_count],
                color=color, label=f'{key} competency')
        plt.plot(range(valid_task_count), mean_task_across_learners[:valid_task_count],
                '.', color=color, label=f'{key} task')
        plt.plot(range(valid_task_count), mean_competency_plus_bonus_across_learners[:valid_task_count],
                '--', color=color, label=f'{key} competency + scaffolding bonus')
    
    plt.ylim(0, 1)
    plt.xlim(0, valid_task_count-1)
    plt.ylabel("Mean Competency")
    plt.xlabel("Task Number")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("sql_task_adaptation_mean.png", dpi=300, bbox_inches="tight")
    
def plot_mean_across_categories(simulationLog):
    """
    Plot the mean values across all DQL categories to show overall competency progression.
    """
    learner_count = len(simulationLog)
    # Find the maximum task count among all learners
    max_task_count = max(len(log["tasks"]) for log in simulationLog)
    
    plt.figure(figsize=(12, 7))
    
    # Initialize lists to store aggregated values
    mean_competency_values = [[] for _ in range(max_task_count)]
    mean_task_values = [[] for _ in range(max_task_count)]
    mean_competency_plus_bonus_values = [[] for _ in range(max_task_count)]
    
    # Collect values for each learner, task, and across all categories
    for learner_id in range(learner_count):
        learner_task_count = len(simulationLog[learner_id]["tasks"])
        
        for task_id in range(learner_task_count):
            # Average across all categories for this task
            task_competency_avg = []
            task_complexity_avg = []
            task_competency_bonus_avg = []
            
            for key in DQL_MODEL:
                # Get competency value
                competency_values = simulationLog[learner_id]["competencies"][task_id][key]
                competency_aggregated = sum(competency_values)/len(competency_values)
                task_competency_avg.append(competency_aggregated)
                
                # Get task complexity value
                task_values = calc_task_complexities(simulationLog[learner_id]["tasks"][task_id])[key]
                task_aggregated = sum(task_values)/len(task_values)
                task_complexity_avg.append(task_aggregated)
                
                # Get scaffolding bonus
                scaffolding_bonus_values = simulationLog[learner_id]["scaffolding_bonuses"][task_id][key]
                # Add scaffolding bonus to competency
                competency_plus_bonus_values = [a + b for a, b in zip(scaffolding_bonus_values, competency_values)]
                competency_plus_bonus_aggregated = sum(competency_plus_bonus_values)/len(competency_plus_bonus_values)
                task_competency_bonus_avg.append(competency_plus_bonus_aggregated)
            
            # Average across all categories
            mean_competency_values[task_id].append(sum(task_competency_avg)/len(task_competency_avg))
            mean_task_values[task_id].append(sum(task_complexity_avg)/len(task_complexity_avg))
            mean_competency_plus_bonus_values[task_id].append(sum(task_competency_bonus_avg)/len(task_competency_bonus_avg))
    
    # Calculate means across learners for each task
    mean_competency_across_learners = [sum(values)/len(values) if values else 0 for values in mean_competency_values]
    mean_task_across_learners = [sum(values)/len(values) if values else 0 for values in mean_task_values]
    mean_competency_plus_bonus_across_learners = [sum(values)/len(values) if values else 0 for values in mean_competency_plus_bonus_values]
    
    # Plot only valid data points (up to the maximum task count with data)
    valid_task_count = max(i for i, values in enumerate(mean_competency_values) if values) + 1
    
    plt.plot(range(valid_task_count), mean_competency_across_learners[:valid_task_count],
            'b-', linewidth=2, label='Overall competency')
    plt.plot(range(valid_task_count), mean_task_across_learners[:valid_task_count],
            'r:', linewidth=2, label='Overall task complexity')
    plt.plot(range(valid_task_count), mean_competency_plus_bonus_across_learners[:valid_task_count],
            'g--', linewidth=2, label='Overall competency + scaffolding bonus')
    
    plt.ylim(0, 1)
    plt.xlim(0, valid_task_count-1)
    plt.ylabel("Mean Competency Across Categories")
    plt.xlabel("Task Number")
    plt.title("Overall Competency Progression (All Categories Combined)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("sql_task_adaptation_all_categories_mean.png", dpi=300, bbox_inches="tight")
    
    
def plot_starting_competencies_distribution(simulationLog):
    """
    Plot the distribution of starting competencies across all learners,
    aggregated over all categories.
    """
    plt.figure(figsize=(12, 7))
    
    # Extract starting competencies for each learner across all categories
    all_starting_competencies = []
    
    for learner_id in range(len(simulationLog)):
        # Get first task competencies
        if simulationLog[learner_id]["competencies"]:
            first_competencies = simulationLog[learner_id]["competencies"][0]
            learner_avg_competency = []
            
            for key in DQL_MODEL:
                if key in first_competencies:
                    values = first_competencies[key]
                    avg_value = sum(values) / len(values) if values else 0
                    learner_avg_competency.append(avg_value)
            
            # Average across all categories for this learner
            if learner_avg_competency:
                all_starting_competencies.append(sum(learner_avg_competency) / len(learner_avg_competency))
    
    # Create histogram and calculate KDE for smoother distribution line
    plt.hist(all_starting_competencies, bins=100, alpha=0.5, density=True, label='Histogramm')
    
    # Add KDE curve if there's enough data
    if len(all_starting_competencies) > 5:
        kde = stats.gaussian_kde(all_starting_competencies)
        x = np.linspace(0, 1, 1000)
        plt.plot(x, kde(x), 'r-', linewidth=2, label='Verteilung')
    
    plt.axvline(sum(all_starting_competencies) / len(all_starting_competencies), 
                color='green', linestyle='dashed', linewidth=2, label='Mittelwert')
    
    plt.xlim(0, 1)
    plt.ylabel("Dichte", fontsize=20)
    plt.xlabel("Initiales Kompetenzniveau (Durchschnitt über alle Syntaxelemente)", fontsize=20)
    # plt.title("Verteilung der Anfangskompetenzen aller Lernenden")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig("starting_competencies_distribution.png", dpi=300, bbox_inches="tight")
    
    
    
def plot_detailed_starting_competencies_distribution(simulationLog):
    """
    Plot the distribution of all individual starting competency values across learners
    without aggregating across categories.
    """
    plt.figure(figsize=(12, 7))
    
    # First, determine total number of competency values to avoid resizing arrays
    number_elements_dql_model = 0
    for key in DQL_MODEL:
        number_elements_dql_model += len(DQL_MODEL[key])
    total_values = number_elements_dql_model * len(simulationLog)
    
    # Pre-allocate array with correct size
    all_starting_competencies = np.zeros(total_values)
    
    # Fill the array without resizing
    idx = 0
    for learner_id in range(len(simulationLog)):
        if simulationLog[learner_id]["competencies"]:
            first_competencies = simulationLog[learner_id]["competencies"][0]
            for key in DQL_MODEL:
                if key in first_competencies:
                    values_length = len(first_competencies[key])
                    all_starting_competencies[idx:idx+values_length] = first_competencies[key]
                    idx += values_length
    
    # Create histogram and calculate KDE for smoother distribution line
    plt.hist(all_starting_competencies, bins=100, alpha=0.5, density=True, label='Histogramm')
    
    # Add KDE curve if there's enough data
    if len(all_starting_competencies) > 5:
        kde = stats.gaussian_kde(all_starting_competencies)
        x = np.linspace(0, 1, 1000)
        plt.plot(x, kde(x), 'r-', linewidth=2, label='Verteilung')
    
    plt.axvline(np.mean(all_starting_competencies), 
                color='green', linestyle='dashed', linewidth=2, label='Mittelwert')
    
    plt.xlim(0, 1)
    plt.ylabel("Dichte", fontsize=20)
    plt.xlabel("Initiale Kompetenzwerte (alle Syntaxelemente)", fontsize=20)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig("detailed_starting_competencies_distribution.png", dpi=300, bbox_inches="tight")

    
def plot_scaffolding_bonus_distribution(simulationLog):
    """
    Plot the distribution of scaffolding bonuses across all learners and tasks,
    aggregated over all categories.
    """
    plt.figure(figsize=(12, 7))
    
    # Extract all scaffolding bonus values
    all_bonus_values = []
    
    for learner_id in range(len(simulationLog)):
        for task_id in range(len(simulationLog[learner_id]["scaffolding_bonuses"])):
            task_bonuses = simulationLog[learner_id]["scaffolding_bonuses"][task_id]
            
            for key in DQL_MODEL:
                if key in task_bonuses:
                    # Add all individual bonus values to the list
                    all_bonus_values.extend(task_bonuses[key])
    
    # Filter out zero values to focus on actual bonuses
    nonzero_bonuses = [b for b in all_bonus_values if b > 0]
    
    if nonzero_bonuses:
        # Create histogram and calculate KDE for smoother distribution line
        plt.hist(nonzero_bonuses, bins=50, alpha=0.5, density=True, label='Histogramm')
        
        # Add KDE curve if there's enough data
        if len(nonzero_bonuses) > 5:
            kde = stats.gaussian_kde(nonzero_bonuses)
            x = np.linspace(min(nonzero_bonuses), max(nonzero_bonuses), 1000)
            plt.plot(x, kde(x), 'r-', linewidth=2, label='Verteilung')
        
        plt.axvline(sum(nonzero_bonuses) / len(nonzero_bonuses), 
                    color='green', linestyle='dashed', linewidth=2, label='Mittelwert')
        
        plt.ylabel("Dichte", fontsize=20)
        plt.xlabel("Scaffolding-Bonus Werte", fontsize=20)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.tight_layout()
        plt.savefig("scaffolding_bonus_distribution.png", dpi=300, bbox_inches="tight")
    else:
        plt.text(0.5, 0.5, "No scaffolding bonuses found in the data", 
                ha='center', va='center', fontsize=16)
        plt.tight_layout()
        plt.savefig("scaffolding_bonus_distribution.png", dpi=300, bbox_inches="tight")
        
        
        
