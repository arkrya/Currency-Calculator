# Currency-Calculator
The Real-Time Currency Calculator is a program providing up-to-date exchange rates for approximately 60 currencies. It utilizes a pre-filled text file for initial data and allows users to update information by clicking the refresh button. The interface includes two currency selection buttons, facilitating easy conversion, and an entry widget for inputting the amount to be converted. A swap button enables users to switch between currencies, automatically clearing the entry box and result label for convenience. This calculator offers a user-friendly experience, combining functionality and simplicity for efficient currency conversion. The refresh button fetches the latest data, ensuring users access the most recent exchange rates effortlessly.

# Requirements:
- **Packages:**
  - Tkinter
  - PIL - Pillow
  - Pandas

- **Internet Requirement:**
  - Necessary for fetching the latest data and updating the output.txt file.

- **Output.txt File:**
  - Required to initialize the calculator with previously stored offline data.

# Points to Remember:
- Organize all files in a single folder for better management.
- When clicking currency buttons, always select an option before reclicking; failure to do so may cause the program to freeze, necessitating a restart.
