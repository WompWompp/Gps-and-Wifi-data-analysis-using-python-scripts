import matplotlib.pyplot as plt


def plot_ssid_counts(hidden_ssid_count, non_hidden_ssid_count):
    labels = ['Hidden SSIDs', 'Non-Hidden SSIDs']
    counts = [hidden_ssid_count, non_hidden_ssid_count]

    plt.bar(labels, counts, color=['red', 'green'])
    plt.title('SSID Hidden Status Counts')
    plt.xlabel('SSID Status')
    plt.ylabel('Count')

    # Add a header
    plt.text(0, max(counts) + 10, 'Users who have knowledge about security', ha='center')

    plt.show()
