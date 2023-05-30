import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
import numpy as np


class ProcessGameState:
    def __init__(self, file_path):
        """
        Initialize the class and preprocess the game state data
        :param file_path: String, path to the game state data file
        """
        self.data = pd.read_parquet(file_path)
        self.extract_weapons()

    def _is_in_boundary(self, x, y):
        """
        Check whether a point is within the specified boundary
        :param x: Float, X-coordinate of the point
        :param y: Float, Y-coordinate of the point
        :return: Boolean, True if the point is within the boundary, False otherwise
        """
        return -825 <= x <= -720 and -2370 <= y <= -2170

    def extract_weapons(self):
        """
        Extract weapon classes from the inventory column and add them to new columns in the dataframe
        """

        def _inventory_weapons(inventory):
            if inventory is None:
                return []
            return [item['weapon_name'] for item in inventory if item['weapon_class'] in ['Rifle', 'SMG']]

        self.data['weapons'] = self.data['inventory'].apply(_inventory_weapons)
        self.data['weapon_count'] = self.data['weapons'].apply(len)

    def team_boundary_percentage(self, team, side):
        """
        Calculate the percentage of rounds where a specified team on a specified side entered a certain boundary
        :param team: String, 'Team1' or 'Team2'
        :param side: String, 'T' or 'CT'
        :return: Float, the percentage of rounds
        """
        # Select data for the specified team and side
        data_side = self.data[(self.data['side'] == side) & (self.data['team'] == team)].copy()

        # Calculate the number of unique rounds where the team entered the boundary
        data_side.loc[:, 'entered_boundary'] = data_side.apply(lambda row: self._is_in_boundary(row['x'], row['y']),
                                                               axis=1)
        unique_boundary_entry_rounds = data_side[data_side['entered_boundary'] == True]['round_num'].nunique()

        # Calculate the total number of unique rounds
        total_rounds = self.data['round_num'].nunique()

        # Return the percentage of rounds where the team entered the boundary
        return (unique_boundary_entry_rounds / total_rounds) * 100 if total_rounds > 0 else 0

    def average_bombsite_entry(self, team, side, bombsite):
        """
        Calculate the average time it takes for at least two players of a specified team on a specified side to enter a certain bombsite
        :param team: String, 'Team1' or 'Team2'
        :param side: String, 'T' or 'CT'
        :param bombsite: String, name of the bombsite
        :return: Float, the average time in seconds
        """
        data_team_side = self.data[(self.data['team'] == team) & (self.data['side'] == side)]
        bombsite_entries = data_team_side[data_team_side['area_name'] == bombsite]
        rifles_smgs_entries = bombsite_entries[bombsite_entries['weapon_count'] >= 1]

        if rifles_smgs_entries.empty:
            return None

        entry_times = []
        current_round = None
        player_count = 0

        for index, row in rifles_smgs_entries.iterrows():
            if current_round != row['round_num']:
                if player_count >= 2:
                    entry_times.append(previous_row['seconds'])
                current_round = row['round_num']
                player_count = 1
                previous_row = row
                continue
            player_count += 1
            previous_row = row

        if player_count >= 2:
            entry_times.append(previous_row['seconds'])

        if not entry_times:
            return None

        return sum(entry_times) / len(entry_times)

    def ct_heatmap(self, team, side, bombsite, n_clusters=3):
        """
        Generate a heatmap of player positions at a specified bombsite for a specified team on a specified side
        :param team: String, 'Team1' or 'Team2'
        :param side: String, 'T' or 'CT'
        :param bombsite: String, name of the bombsite
        :param n_clusters: Integer, number of clusters for the KMeans algorithm (default is 3 for 3 players defending the bombsite)
        :return: None
        """
        data_side = self.data[(self.data['team'] == team) & (self.data['side'] == side)]
        bombsite_data = data_side[data_side['area_name'] == bombsite]

        if bombsite_data.empty:
            return

        X = bombsite_data[['x', 'y']].values
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(X)
        labels = kmeans.predict(X)
        centers = kmeans.cluster_centers_

        plt.figure(figsize=(10, 8))
        plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
        plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
        plt.title(f'{team} {side} Player Cluster - {bombsite}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.savefig(f'{team}_{side}_Cluster_{bombsite}.png')
        plt.close()

