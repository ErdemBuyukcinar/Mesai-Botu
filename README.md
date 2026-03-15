# Discord Work Shift Tracker Bot 🏢 

A comprehensive and interactive Discord bot designed to track the working hours, shifts, and attendance of server members. It logs all activities into an SQLite database, calculates total time spent, and allows administrators to export the data into detailed Excel reports.

## ✨ Features

* **Interactive Control Panel:** Members can easily check in (✅) and check out (❌) using a clean, embedded reaction panel.
* **Automated Time Calculation:** Automatically calculates the exact duration of each shift (Hours:Minutes:Seconds) upon check-out.
* **Database Logging:** Securely stores user IDs, display names, dates, start times, end times, and total durations using SQLite.
* **Excel Export:** Converts the database into a `.xlsx` spreadsheet and sends it directly to the Discord channel.
* **Smart Error Handling & Anti-Spam:** * Prevents users from starting multiple shifts at the same time.
  * Prevents users from ending a shift they haven't started.
  * Automatically removes the user's reaction from the panel to keep the interface clean.
  * Auto-deletes temporary notification messages (like "You started a shift") after 5 seconds to prevent channel clutter.
* **Role-Based Security:** All management commands and global error handling are restricted to users with the "Administrator" permission.

## 🛠️ Admin Commands

**Note:** All commands below require the **Administrator** permission.

* `!panel`: Deploys the interactive check-in/check-out embed message to the current channel. Members interact with this panel.
* `!excel`: Queries the entire SQLite database, generates an Excel (`.xlsx`) report of all logged shifts, and uploads it to the channel.
* `!temizle`: Wipes all records from the database. (Warning: This action cannot be undone).

## 🚀 Setup and Installation

1. Clone or download this repository.
2. Install the required Python packages:
   ```bash
   pip install discord.py pandas openpyxl
3. Open mesaibotu.py and insert your bot token at the bottom inside bot.run('your_token').
4. You can run your bot.
