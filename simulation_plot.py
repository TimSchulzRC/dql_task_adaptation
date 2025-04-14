import matplotlib.pyplot as plt
from simulation_const import DQL_MODEL
from simulation_util import calc_task_complexities

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