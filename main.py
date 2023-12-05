import xmltodict
import json
import os


print(os.getcwd())
p_directory = os.getcwd()
os_result = os.path.join(p_directory, "wifi_data")
print(os_result)
dir_list = os.listdir(os_result)
print(dir_list)

with open("C:/Users/musta/Desktop/gps/gps/GPSWpts-2023-11-12-all_36wpts.kml") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

    # print(json.dumps(data_dict, indent=4))

    placemarks = data_dict["kml"]["Document"]["Folder"]["Placemark"]

    accuracy_list = []

    for accuracy in placemarks:
        current_accuracy = float(accuracy["ExtendedData"]["Data"][0]["value"])
        accuracy_list.append(current_accuracy)
        # print(current_accuracy)

    max_accuracy = max(accuracy_list)
    min_accuracy = min(accuracy_list)
    average_accuracy = sum(accuracy_list) / len(accuracy_list)

    # print(f"\nMax GPS Accuracy: {max_accuracy}")
    # print(f"Min GPS Accuracy: {min_accuracy}")
    # print(f"Average GPS Accuracy: {average_accuracy}")


wifi_channels_count = {}  # Dictionary to store channel counts
primary_frequency_count = {}  # Dictionary to store primary frequency counts
signal_strength_values = []  # List to store signal strength values
wifi_data = []
hidden_ssid_count = 0
non_hidden_ssid_count = 0
wpa_count = 0
wpa2_count = 0
ssid_prefix_count = {}
unique_ssids = set()
ssid_occurrences = {}

for os_files in dir_list:

    with open(os.path.join(os_result,os_files),encoding="utf-8",mode= "r") as text_file:
        print(text_file)
        text = text_file.read()
        text = text.replace("\n\n","\n")
        text = text.split("\n")
        headers = text[0].split("|")
        # print(headers)



        del text[0]



        for line in text:
            print(line)
            values = line.split("|")
            record = {}
            for n, name in enumerate(headers):
                record[name] = values[n]
            #SSID Information
            ssid = record.get('SSID')
            if ssid and '*hidden*' in ssid.lower():
                hidden_ssid_count += 1
            else:
                non_hidden_ssid_count += 1

            # Check the security information
            security_info = record.get('Security')
            if security_info:
                if 'WPA-' in security_info:
                    wpa_count += 1
                elif 'WPA2-' in security_info:
                    wpa2_count += 1

            ssid_info = record.get('SSID')
            if ssid_info:
                # Extract the first 6 characters of the SSID
                ssid_prefix = ssid_info[:6].upper()  # Convert to uppercase for case-insensitivity

                # Count occurrences of SSID prefixes
                ssid_prefix_count[ssid_prefix] = ssid_prefix_count.get(ssid_prefix, 0) + 1

            # Check the SSID information
            ssid_info = record.get('SSID')
            if ssid_info:
                # If the SSID is already in the set, print a message
                if ssid_info in unique_ssids:
                    print(f"Duplicate SSID found: {ssid_info}")
                else:
                    # Add the SSID to the set of unique SSIDs
                    unique_ssids.add(ssid_info)

            wifi_channel = record.get('Primary Channel')
            primary_frequency = record.get('Primary Frequency')
            signal_strength = record.get('Strength')

            if wifi_channel:
                wifi_channels_count[wifi_channel] = wifi_channels_count.get(wifi_channel, 0) + 1

            if primary_frequency:
                primary_frequency_count[primary_frequency] = primary_frequency_count.get(primary_frequency, 0) + 1

            if signal_strength:
                signal_strength_value = int(signal_strength.rstrip('dBm'))
                signal_strength_values.append(signal_strength_value)

            wifi_data.append(record)


# print(wifi_data)

#Print WiFi Channel Counts
print("\nWiFi Channel Counts:")
sorted_wifi_channels = sorted(wifi_channels_count.items(), key=lambda x: x[1], reverse=True)
for channel, count in sorted_wifi_channels:

    print(f"Channel {channel}: {count} occurrences")

# Print Primary Frequency Counts
print("\nPrimary Frequency Counts:")
sorted_primary_frequencies = sorted(primary_frequency_count.items(), key=lambda x: x[1], reverse=True)
for frequency, count in sorted_primary_frequencies:

    print(f"Frequency {frequency}: {count} occurrences")

# Calculate and print mean signal strength
mean_signal_strength = sum(signal_strength_values) / len(signal_strength_values)
print(f"\nMean Signal Strength: {mean_signal_strength} dBm")

# Extracted GPS accuracy data
accuracy_values = [float(accuracy["ExtendedData"]["Data"][0]["value"]) for accuracy in placemarks]

channels, counts = zip(*sorted_wifi_channels)


# Save GPS Accuracy data to JSON
gps_accuracy_data = {"accuracy_values": accuracy_values}
with open("gps_accuracy_data.json", "w") as json_file:
    json.dump(gps_accuracy_data, json_file)

# Save Wi-Fi Channel Occurrences data to JSON
wifi_channel_data = {"channels": channels,
                     "counts": counts,
                     "sorted_wifi_channels":sorted_wifi_channels,
                     "hidden_ssid_count": hidden_ssid_count,
                     "non_hidden_ssid_count":non_hidden_ssid_count,
                     "sorted_primary_frequencies":sorted_primary_frequencies}
with open("wifi_channel_data.json", "w") as json_file:
    #json.dump(wifi_channel_data, json_file)
    json_file.write(json.dumps(wifi_channel_data))

# Print the counts of hidden and non-hidden SSIDs
print("\nSSID Hidden Status Counts:")
print(f"Hidden SSIDs: {hidden_ssid_count}")
print(f"Non-Hidden SSIDs: {non_hidden_ssid_count}")

# Print the counts of WPA and WPA2
print("\nSecurity Protocol Counts:")
print(f"WPA: {wpa_count}")
print(f"WPA2: {wpa2_count}")

# Sort SSID prefixes by occurrences and filter out those with less than 2 occurrences
sorted_prefixes = sorted((prefix, count) for prefix, count in ssid_prefix_count.items() if count >= 2)
sorted_prefixes = sorted(sorted_prefixes, key=lambda x: x[1], reverse=True)

# Print the sorted counts of SSID prefixes
print("\nSSID Prefix Counts (Sorted with at least 2 occurrences):")
for prefix, count in sorted_prefixes:
    print(f"{prefix}: {count} occurrences")

# Print information about duplicate SSIDs that I see 2 or more times during data collection
print("\nDuplicate SSID Information:")
for ssid, occurrences in ssid_occurrences.items():
    if occurrences > 1:
        print(f"SSID: {ssid}, Occurrences: {occurrences}")

