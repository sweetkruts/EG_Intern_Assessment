from process_game_state import ProcessGameState

if __name__ == "__main__":
    # Replace with the path to your game data file
    file_path = r"C:\Users\willy\Downloads\game_state_frame_data.parquet"


    # Create an instance of the class and process the data
    game_state = ProcessGameState(file_path)

    # Define team, side, and bombsite
    team = 'Team2'  # or 'Team1'
    side = 'T'     # or 'CT'
    bombsite = 'BombsiteB'  # or 'BombsiteA'

    # Perform the analysis
    boundary_percentage = game_state.team_boundary_percentage(team, side)
    average_time = game_state.average_bombsite_entry(team, side, bombsite)

    # Write the results to a file
    with open('output.txt', 'w') as file:
        file.write(f"{boundary_percentage}% of rounds saw at least one {team} player on {side} side entering the boundary.\n")
        if average_time is not None:
            file.write(f"On average, at least two {team} players on {side} side with either a Rifle or SMG entered {bombsite} at {average_time} seconds into the round.\n")
        else:
            file.write(f"No instances found where at least two {team} players on {side} side entered {bombsite}.\n")

    # Generate the heatmap
    game_state.ct_heatmap(team, side, bombsite)
