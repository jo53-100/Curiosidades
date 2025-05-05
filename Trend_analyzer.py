import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
from datetime import datetime
import os


class MusicListeningAnalyzer:
    """
    A class for analyzing monthly music listening habits from streaming services.

    This script works with CSV exports from various streaming platforms,
    particularly focusing on monthly playlists for temporal analysis.
    """

    def __init__(self, file_path):
        """
        Initialize the analyzer with a CSV file.

        Parameters:
        -----------
        file_path : str
            Path to the CSV file containing listening data
        """
        self.file_path = file_path
        self.df = None
        self.monthly_data = {}

        # Define month order at the class level so it's available to all methods
        self.month_order = {
            'Ene': 1, 'Feb': 2, 'Mar': 3, 'Abr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Ago': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12
        }

        # Try to read the file
        try:
            self.df = pd.read_csv(file_path)
            print(f"Successfully loaded data with {len(self.df)} entries")
        except Exception as e:
            print(f"Error loading file: {e}")
            return

        # Show the basic structure
        print("\nColumns in the dataset:")
        print(self.df.columns.tolist())

        # Determine month from playlist name
        if 'Playlist name' in self.df.columns:
            self.extract_months_from_playlists()

    def extract_months_from_playlists(self):
        """Extract month and year information from playlist names (format: 'MonYY')"""
        # Create a pattern that captures both month and year
        month_pattern = r'^(Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)(\d{2})$'

        # Extract both components
        month_year_df = self.df['Playlist name'].str.extract(month_pattern, expand=True)

        # If extraction was successful
        if not month_year_df.empty and month_year_df.shape[1] == 2:
            # Name the columns
            month_year_df.columns = ['month', 'year']

            # Add both columns to the dataframe
            self.df['month'] = month_year_df['month']
            self.df['year'] = month_year_df['year'].apply(lambda x: f"20{x}" if x is not None else None)

            # Create a combined column for chronological sorting
            self.df['month_year'] = self.df.apply(
                lambda row: f"{row['month']}{row['year']}" if pd.notna(row['month']) and pd.notna(
                    row['year']) else None,
                axis=1
            )

    def analyze(self):
        """Perform comprehensive analysis of listening data"""
        if self.df is None:
            print("No data to analyze.")
            return

        # Run all analysis methods
        self.basic_stats()
        self.artist_analysis()
        self.album_analysis()
        self.monthly_trends()
        self.track_repetition_analysis()
        self.generate_visualizations()

    def basic_stats(self):
        """Calculate and display basic statistics"""
        print("\n====== BASIC STATISTICS ======")

        total_tracks = len(self.df)
        unique_tracks = self.df['Track name'].nunique()
        unique_artists = self.df['Artist name'].nunique()

        print(f"Total tracks: {total_tracks}")
        print(f"Unique tracks: {unique_tracks}")
        print(f"Unique artists: {unique_artists}")

        # Diversity scores
        track_diversity = (unique_tracks / total_tracks) * 100
        artist_diversity = (unique_artists / total_tracks) * 100

        print(f"\nTrack diversity score: {track_diversity:.2f}%")
        print(f"Artist diversity score: {artist_diversity:.2f}%")

        # Count unique month-year combinations if available
        if 'month_year' in self.df.columns:
            month_year_count = self.df['month_year'].nunique()
            print(f"Data spans {month_year_count} unique month-year combinations")
        elif 'month' in self.df.columns:
            months_count = self.df['month'].nunique()
            print(f"Data spans {months_count} months")

    def artist_analysis(self):
        """Analyze artist distribution and preferences"""
        print("\n====== ARTIST ANALYSIS ======")

        # Top artists
        artist_counts = self.df['Artist name'].value_counts()
        top_artists = artist_counts.head(10)

        print("Top 10 most played artists:")
        for i, (artist, count) in enumerate(top_artists.items(), 1):
            print(f"{i}. {artist}: {count} appearances")  # Changed "plays" to "appearances"

        # Artist loyalty metrics
        top_artist = artist_counts.index[0]
        top_artist_plays = artist_counts.iloc[0]
        top_artist_percentage = (top_artist_plays / len(self.df)) * 100

        print(f"\nTop artist loyalty: {top_artist_percentage:.2f}% of plays dedicated to {top_artist}")

        # Top 3 artists loyalty
        top3_plays = artist_counts.iloc[0:3].sum()
        top3_percentage = (top3_plays / len(self.df)) * 100

        print(f"Top 3 artists loyalty: {top3_percentage:.2f}% of plays")

    def album_analysis(self):
        """Analyze album listening patterns"""
        print("\n====== ALBUM ANALYSIS ======")

        # Top albums
        album_counts = self.df['Album'].value_counts()
        top_albums = album_counts.head(10)

        print("Top 10 most played albums:")
        for i, (album, count) in enumerate(top_albums.items(), 1):
            print(f"{i}. {album}: {count} appearances")  # Changed "plays" to "appearances"

    def monthly_trends(self):
        """Analyze listening trends across months"""
        if 'month_year' in self.df.columns:
            print("\n====== MONTHLY TRENDS ======")

            # Get data for each month-year combination
            monthly_stats = {}
            for month_year in self.df['month_year'].unique():
                if pd.isna(month_year):
                    continue

                month_df = self.df[self.df['month_year'] == month_year]
                month = month_year[:3]  # Extract month part
                year = month_year[3:]  # Extract year part

                monthly_stats[month_year] = {
                    'month': month,
                    'year': year,
                    'tracks': len(month_df),
                    'unique_tracks': month_df['Track name'].nunique(),
                    'unique_artists': month_df['Artist name'].nunique(),
                }

            # Sort month-years chronologically
            def month_year_sorter(month_year):
                if pd.isna(month_year):
                    return float('inf')

                month = month_year[:3]
                year = month_year[3:]

                return int(year) * 100 + self.month_order.get(month, 0)

            sorted_month_years = sorted(monthly_stats.keys(), key=month_year_sorter)

            print("Monthly listening statistics:")
            for month_year in sorted_month_years:
                stats = monthly_stats[month_year]
                month = stats['month']
                year = stats['year']

                print(f"\n{month} {year}:")
                print(f"  - Tracks: {stats['tracks']}")
                print(f"  - Unique artists: {stats['unique_artists']}")
                print(f"  - Unique tracks: {stats['unique_tracks']}")

                # Calculate artist diversity for this month
                artist_diversity = (stats['unique_artists'] / stats['tracks']) * 100
                print(f"  - Artist diversity: {artist_diversity:.2f}%")

        elif 'month' in self.df.columns:
            print("\n====== MONTHLY TRENDS ======")

            # Get data for each month
            monthly_stats = {}
            for month in self.df['month'].unique():
                month_df = self.df[self.df['month'] == month]
                monthly_stats[month] = {
                    'tracks': len(month_df),
                    'unique_tracks': month_df['Track name'].nunique(),
                    'unique_artists': month_df['Artist name'].nunique(),
                }

            # Sort months chronologically
            sorted_months = sorted(monthly_stats.keys(), key=lambda x: self.month_order.get(x, 13))

            print("Monthly listening statistics:")
            for month in sorted_months:
                stats = monthly_stats[month]
                print(f"\n{month}:")
                print(f"  - Tracks: {stats['tracks']}")
                print(f"  - Unique artists: {stats['unique_artists']}")
                print(f"  - Unique tracks: {stats['unique_tracks']}")

                # Calculate artist diversity for this month
                artist_diversity = (stats['unique_artists'] / stats['tracks']) * 100
                print(f"  - Artist diversity: {artist_diversity:.2f}%")
        else:
            print("\nNo monthly data available for trend analysis.")

    def track_repetition_analysis(self):
        """Find tracks that appear across multiple playlists/months"""
        print("\n====== TRACK REPETITION ANALYSIS ======")

        if 'month_year' in self.df.columns:
            # Group by track and count unique month-years
            track_month_years = self.df.groupby('Track name')['month_year'].nunique()
            repeated_tracks = track_month_years[track_month_years > 1].sort_values(ascending=False)

            if len(repeated_tracks) == 0:
                print("No tracks appear in multiple month-year combinations.")
                return

            print(f"Found {len(repeated_tracks)} tracks that appear in multiple month-year combinations.")
            print("\nTop 10 most frequently repeated tracks:")

            for i, (track, count) in enumerate(repeated_tracks.head(10).items(), 1):
                # Get the month-years this track appears in
                month_years = self.df[self.df['Track name'] == track]['month_year'].unique()

                # Sort them chronologically
                def month_year_sorter(month_year):
                    if pd.isna(month_year):
                        return float('inf')

                    month = month_year[:3]
                    year = month_year[3:]

                    return int(year) * 100 + self.month_order.get(month, 0)

                sorted_month_years = sorted([my for my in month_years if not pd.isna(my)],
                                            key=month_year_sorter)

                # Format for display (e.g., "Feb 2024, Mar 2024")
                formatted_month_years = [f"{my[:3]} {my[3:]}" for my in sorted_month_years]

                print(f"{i}. '{track}' appears in {count} month-year combinations: {', '.join(formatted_month_years)}")

            # Get artist for top repeated tracks
            print("\nMost loyal artist relationships (tracks repeated across month-years):")
            repeated_artist_counts = {}

            for track, _ in repeated_tracks.items():
                artist = self.df[self.df['Track name'] == track]['Artist name'].iloc[0]
                if artist in repeated_artist_counts:
                    repeated_artist_counts[artist] += 1
                else:
                    repeated_artist_counts[artist] = 1

            sorted_repeated_artists = sorted(repeated_artist_counts.items(), key=lambda x: x[1], reverse=True)

            for i, (artist, count) in enumerate(sorted_repeated_artists[:5], 1):
                print(f"{i}. {artist}: {count} tracks repeated across month-years")

        elif 'month' in self.df.columns:
            # Group by track and count unique months
            track_months = self.df.groupby('Track name')['month'].nunique()
            repeated_tracks = track_months[track_months > 1].sort_values(ascending=False)

            if len(repeated_tracks) == 0:
                print("No tracks appear in multiple months.")
                return

            print(f"Found {len(repeated_tracks)} tracks that appear in multiple months.")
            print("\nTop 10 most frequently repeated tracks across months:")

            for i, (track, count) in enumerate(repeated_tracks.head(10).items(), 1):
                # Get the months this track appears in
                months = self.df[self.df['Track name'] == track]['month'].unique()

                # Sort them chronologically
                sorted_months = sorted([m for m in months if not pd.isna(m)],
                                       key=lambda x: self.month_order.get(x, 13))

                print(f"{i}. '{track}' appears in {count} months: {', '.join(sorted_months)}")

            # Get artist for top repeated tracks
            print("\nMost loyal artist relationships (tracks repeated across months):")
            repeated_artist_counts = {}

            for track, _ in repeated_tracks.items():
                artist = self.df[self.df['Track name'] == track]['Artist name'].iloc[0]
                if artist in repeated_artist_counts:
                    repeated_artist_counts[artist] += 1
                else:
                    repeated_artist_counts[artist] = 1

            sorted_repeated_artists = sorted(repeated_artist_counts.items(), key=lambda x: x[1], reverse=True)

            for i, (artist, count) in enumerate(sorted_repeated_artists[:5], 1):
                print(f"{i}. {artist}: {count} tracks repeated across months")
        else:
            print("No monthly data available for repetition analysis.")

    def generate_visualizations(self):
        """Generate data visualizations for listening patterns"""
        print("\n====== GENERATING VISUALIZATIONS ======")

        # Create output directory if it doesn't exist
        output_dir = "music_analytics_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        # Set visualization style
        plt.style.use('seaborn-v0_8-darkgrid')

        # 1. Artist distribution pie chart
        self._create_artist_distribution_chart(output_dir)

        # 2. Monthly listening trends
        if 'month_year' in self.df.columns:
            self._create_monthly_trends_chart(output_dir)
        elif 'month' in self.df.columns:
            self._create_monthly_trends_chart_simple(output_dir)

        # 3. Album distribution
        self._create_album_distribution_chart(output_dir)

        print(f"\nVisualizations saved to directory: {output_dir}")

    def _create_artist_distribution_chart(self, output_dir):
        """Create pie chart of top artists"""
        plt.figure(figsize=(10, 7))

        # Get top 5 artists and combine the rest as "Others"
        artist_counts = self.df['Artist name'].value_counts()
        top_artists = artist_counts.head(5)
        others_count = artist_counts[5:].sum()

        # Combine data
        labels = list(top_artists.index) + ['Others']
        sizes = list(top_artists.values) + [others_count]

        # Create pie chart
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
                shadow=True, explode=[0.05] * len(labels))
        plt.axis('equal')
        plt.title('Artist Distribution in Listening History', fontsize=16)

        # Save the chart
        plt.savefig(os.path.join(output_dir, 'artist_distribution.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def _create_monthly_trends_chart(self, output_dir):
        """Create chart showing monthly listening trends with year information"""
        if 'month_year' not in self.df.columns:
            return

        # Use the month_year column for grouping
        monthly_tracks = self.df.groupby('month_year').size()
        monthly_artists = self.df.groupby('month_year')['Artist name'].nunique()

        # Create a custom sorter for month-year combinations
        def month_year_sorter(month_year):
            if pd.isna(month_year):
                return float('inf')  # Put NaN values at the end

            month = month_year[:3]
            year = month_year[3:]

            return int(year) * 100 + self.month_order.get(month, 0)

        ordered_month_years = sorted(monthly_tracks.index, key=month_year_sorter)
        ordered_tracks = [monthly_tracks[month_year] for month_year in ordered_month_years]
        ordered_artists = [monthly_artists[month_year] for month_year in ordered_month_years]

        # Format x-axis labels for readability (e.g., "Feb '24")
        x_labels = [f"{my[:3]} '{my[5:]}" for my in ordered_month_years]

        # Create the plot
        fig, ax1 = plt.subplots(figsize=(14, 7))
        ax2 = ax1.twinx()

        # Plot tracks as bars
        bars = ax1.bar(range(len(ordered_tracks)), ordered_tracks, color='steelblue', alpha=0.7)
        ax1.set_ylabel('Number of Tracks', color='steelblue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='steelblue')

        # Plot unique artists as a line
        line = ax2.plot(range(len(ordered_artists)), ordered_artists, 'o-', color='crimson', linewidth=2)
        ax2.set_ylabel('Number of Unique Artists', color='crimson', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='crimson')

        # Set x-axis labels
        ax1.set_xticks(range(len(ordered_tracks)))
        ax1.set_xticklabels(x_labels, rotation=45, ha='right')

        # Add title and grid
        plt.title('Monthly Listening Trends', fontsize=16)
        ax1.grid(True, linestyle='--', alpha=0.6)

        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color='steelblue', alpha=0.7, label='Tracks'),
            Line2D([0], [0], color='crimson', marker='o', linewidth=2, label='Unique Artists')
        ]
        ax1.legend(handles=legend_elements, loc='upper left')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'monthly_trends.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def _create_monthly_trends_chart_simple(self, output_dir):
        """Create chart showing monthly listening trends without year information"""
        if 'month' not in self.df.columns:
            return

        # Group by month
        monthly_tracks = self.df.groupby('month').size()
        monthly_artists = self.df.groupby('month')['Artist name'].nunique()

        # Order months chronologically
        ordered_months = sorted(monthly_tracks.index, key=lambda x: self.month_order.get(x, 13))
        ordered_tracks = [monthly_tracks[month] for month in ordered_months]
        ordered_artists = [monthly_artists[month] for month in ordered_months]

        # Create the plot
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()

        # Plot tracks
        bars = ax1.bar(ordered_months, ordered_tracks, color='steelblue', alpha=0.7)
        ax1.set_xlabel('Month', fontsize=12)
        ax1.set_ylabel('Number of Tracks', color='steelblue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='steelblue')

        # Plot unique artists
        line = ax2.plot(ordered_months, ordered_artists, 'o-', color='crimson', linewidth=2)
        ax2.set_ylabel('Number of Unique Artists', color='crimson', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='crimson')

        # Add title and grid
        plt.title('Monthly Listening Trends', fontsize=16)
        ax1.grid(True, linestyle='--', alpha=0.6)

        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color='steelblue', alpha=0.7, label='Tracks'),
            Line2D([0], [0], color='crimson', marker='o', linewidth=2, label='Unique Artists')
        ]
        ax1.legend(handles=legend_elements, loc='upper left')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'monthly_trends.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def _create_album_distribution_chart(self, output_dir):
        """Create horizontal bar chart of top albums"""
        plt.figure(figsize=(12, 8))

        # Get top 10 albums
        album_counts = self.df['Album'].value_counts().head(10)

        # Create horizontal bar chart
        plt.barh(album_counts.index[::-1], album_counts.values[::-1], color='mediumseagreen')
        plt.xlabel('Number of Appearances', fontsize=12)  # Changed "Plays" to "Appearances"
        plt.ylabel('Album', fontsize=12)
        plt.title('Top 10 Most Played Albums', fontsize=16)

        # Add count labels to the end of each bar
        for i, v in enumerate(album_counts.values[::-1]):
            plt.text(v + 0.5, i, str(v), va='center')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'album_distribution.png'), dpi=300, bbox_inches='tight')
        plt.close()


# Example usage
if __name__ == "__main__":
    try:
        file_path = input("Indica la ruta al archivo csv: ").strip("'").strip('"').strip()
        analyzer = MusicListeningAnalyzer(file_path)
        analyzer.analyze()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()