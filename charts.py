import json


from main import sorted_wifi_channels
from plot_ssid_counts import plot_ssid_counts
from ssid_counts import plot_primary_frequency_counts
from wifi_channel_counts import plot_wifi_channel_counts

# Load Wi-Fi Channel Occurrences data from JSON
with open("wifi_channel_data.json", "r") as json_file:
    wifi_channel_data = json.loads(json_file.read())
# Load GPS Accuracy data from JSON
with open("gps_accuracy_data.json", "r") as json_file:
    gps_accuracy_data = json.loads(json_file.read())

# Plot SSID counts chart
print(wifi_channel_data)
plot_ssid_counts(wifi_channel_data["hidden_ssid_count"], wifi_channel_data["non_hidden_ssid_count"])

# Call the functions to plot Wi-Fi channel and primary frequency occurrences
plot_wifi_channel_counts(sorted_wifi_channels)
plot_primary_frequency_counts(wifi_channel_data["sorted_primary_frequencies"])
