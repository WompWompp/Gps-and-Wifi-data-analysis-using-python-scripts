import matplotlib.pyplot as plt


def plot_primary_frequency_counts(sorted_primary_frequencies):
    for frequency, count in sorted_primary_frequencies:
        print(f"Frequency {frequency}: {count} occurrences")

    plt.bar(*zip(*sorted_primary_frequencies), color='skyblue')
    plt.title('Primary Frequency Occurrences')
    plt.xlabel('Frequency')
    plt.ylabel('Occurrences')
    plt.show()
