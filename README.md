# Paper Plane Ocean Odyssey - Motion Controller & Game Display

This repository contains the files required to play **Paper Plane Ocean Odyssey**, an interactive 3D flight game built with Three.js. The game uses an Android device's gyroscope telemetry as a physical motion controller to steer a paper plane over the ocean.

## Repository Contents

*   **`app-release.apk`**: The controller application to be installed on your Android device. It captures gyroscope/accelerometer sensor data and streams it over the network.
*   **`index.html`**: The 3D game client to be opened in a web browser on your monitor/display device (Mac, Windows, or Linux).

---

## Step-by-Step Connection & Setup Guide

To establish a low-latency connection between your Android device (controller) and your display device (monitor/computer), follow these instructions:

### 1. Set Up the Network Connection (Hotspot)
For the lowest latency and most reliable connection, connect both devices directly using a Wi-Fi Hotspot:
1. On your **Android device**, enable your **Wi-Fi Hotspot** (Portable Hotspot).
2. On your **Display device (computer)**, open your Wi-Fi settings and connect to the Android device's hotspot network.

### 2. Install and Start the Android Controller
1. Transfer and install **`app-release.apk`** on your Android device.
2. Open the **Sensor Bridge** application on your phone.
3. Tap the **Start Stream** or **Connect** button in the app.
4. Once the stream starts, the app will display a local IP address (typically `192.168.43.1` when using a hotspot). Note this IP address down.

### 3. Open the Game and Connect Telemetry
1. Double-click and open **`index.html`** in your web browser on the display device.
2. You will be greeted by the **Connect Telemetry** screen asking for the **Android Host IP**.
3. Enter the IP address shown on your Android device's screen into the input field.
4. Click **Connect**.
5. Once connected:
    * The status indicator will turn green and show **CONNECTED**.
    * The game menu will appear. Tap **Set Sail** to begin flying!

---

## Gameplay & Controls

### Motion Steering
*   **Roll (Tilt Left / Right):** Steers the paper plane left and right.
*   **Pitch (Tilt Forward / Backward):** Dives down or climbs up to adjust altitude.
*   **Keyboard Fallback:** If the controller is disconnected, you can use the **Arrow keys** or **WASD** to fly.

### Objectives
*   Fly through the **Golden Rings** to score points (+10 per ring) and gain speed boosts.
*   **Avoid crashing** into the ocean surface or missing a ring. Touching the water or failing to enter a ring results in a crash.
*   Adjust the **Tilt Sensitivity** and **Input Smoothing** via the Calibration Panel before taking off to suit your preferences.

---

## Troubleshooting

*   **Connection Fails / Times Out:**
    *   Ensure your computer is successfully connected to the Android Wi-Fi Hotspot.
    *   Verify that the IP entered in `index.html` matches the IP displayed on the Android app exactly.
    *   Ensure that no firewall or security software on your computer is blocking incoming WebSocket connections on port `8765`.
