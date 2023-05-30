# #EGWIN

This project provides tools for analyzing Counter-Strike: Global Offensive (CS:GO) game data. It generates insights and visualizations about player behavior and strategies, with a particular focus on team movement and weapon usage. The results and data for the relevant questions reagarding the assessment are in the output.txt and Team2_CT_Cluster_BombsiteB.png. The justification required for using external libraries is in the text file "Library Usage Justification". The answers to the written questions are in "Short Answer".

## Prerequisites

- Python 3.8 or later
- pandas
- matplotlib
- seaborn
- scikit-learn

You can install the required Python packages using pip:

```bash
pip install pandas matplotlib seaborn scikit-learn
```

# Getting Started
Clone this repository to your local machine:
`git clone https://github.com/sweetkruts/EG_Intern_Assessment`

# Usage
Run main file with desired characteristics: team (Team1/Team2), side (T/CT), bombsite. The class provides several methods for analyzing the game data:

```
team_boundary_percentage(team, side): Calculates the percentage of rounds where at least one player from the specified team and side entered the boundary.

average_bombsite_entry(team, side, bombsite): Calculates the average round time at which at least two players from the specified team and side entered the specified bombsite.

ct_heatmap(team, side, bombsite): Generates a heatmap of the positions of the players from the specified team and side in the specified bombsite.
```

Results will be written to an output file named 'output.txt'. The heatmap will be saved as "TeamName_Side_Bombsite.png".
