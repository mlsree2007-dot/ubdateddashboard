import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Book Locator", layout="centered")
st.title("📚 Smart Book Locator Dashboard")

api_url = "https://smart-5.onrender.com/search"

# Search bar
book_id = st.text_input("🔍 Enter Book ID to locate")

if st.button("Search"):
    if book_id:
        try:
            response = requests.get(f"{api_url}?tag_id={book_id}")
            if response.status_code == 200:
                data = response.json()
                st.subheader("📘 Book Information")
                st.success(f"Book ID: {data['tag_id']}")
                st.info(f"📍 Location: {data['location']}")
                st.caption(f"🕒 Last BLE scan: {data['timestamp']}")

                # Shelf presence logic
                rssi = data.get("rssi", -100)
                if rssi > -65:
                    st.success("✅ Book is on the shelf")
                else:
                    st.warning("📦 Book is not on the shelf")

                # Simulated RSSI chart
                st.subheader("📊 BLE Signal Over Time")
                time = list(range(10))
                rssi_values = [-85, -78, -70, -65, -60, -55, -50, -60, -70, -80]
                zones = []
                for r in rssi_values:
                    if r <= -80:
                        zones.append("Shelf C3")
                    elif r <= -65:
                        zones.append("Shelf B2")
                    else:
                        zones.append("Shelf A1")

                fig, ax = plt.subplots()
                ax.plot(time, rssi_values, marker='o', color='blue')
                for i, zone in enumerate(zones):
                    ax.annotate(zone, (time[i], rssi_values[i]), textcoords="offset points", xytext=(0,10), ha='center')
                ax.set_xlabel("Time (minutes)")
                ax.set_ylabel("RSSI (dBm)")
                ax.set_title("Simulated BLE Signal Strength")
                ax.grid(True)
                st.pyplot(fig)

            else:
                st.error("Failed to fetch data from API.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a Book ID.")
