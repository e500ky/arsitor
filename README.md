# Arsitor

Arsitor is a simple text editor built using Python with the `customtkinter` library. It provides a clean and modern interface with essential features for text editing, file management, and customizable settings.

## Features
- Open and save files with UTF-8 encoding
- Auto-detect file changes and update the editor title accordingly
- Customizable appearance settings (theme, font size, font family, tab size, etc.)
- Simple bottom toolbar with file operations and cursor position tracking
- Run executable files directly from the editor
- Keyboard shortcuts for essential functions

## Installation
### Requirements
Make sure you have Python installed on your system. You can install the required dependencies using:
```sh
pip install customtkinter
```

### Running the Application
To start the application, run:
```sh
python main.py
```

## Keyboard Shortcuts
- `Ctrl + S` : Save file
- `Ctrl + Shift + S` : Save file as
- `Ctrl + O` : Open file
- `F1 / Alt + S` : Open settings
- `F5` : Run file (if executable)

## Customization
Arsitor allows users to change the following settings:
- **Theme Mode**: Light, Dark, or System
- **Font Size**: Adjustable font size for better readability
- **Font Family**: Choose your preferred font style
- **Tab Size**: Define the number of spaces for a tab
- **Border Space**: Adjust padding around the editor
- **Corner Radius**: Modify UI element rounding

Settings are stored in a `settings.json` file and persist between sessions.

## Contributing
If you'd like to contribute, feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License.
