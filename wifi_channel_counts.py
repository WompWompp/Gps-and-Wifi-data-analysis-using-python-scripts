import matplotlib.pyplot as plt


def plot_wifi_channel_counts(sorted_wifi_channels):
    for channel, count in sorted_wifi_channels:
        print(f"Channel {channel}: {count} occurrences")
    print(zip(*sorted_wifi_channels))
    plt.bar(*zip(*sorted_wifi_channels), color='skyblue')
    plt.title('Wi-Fi Channel Occurrences')
    plt.xlabel('Channel')
    plt.ylabel('Occurrences')
    plt.show()
