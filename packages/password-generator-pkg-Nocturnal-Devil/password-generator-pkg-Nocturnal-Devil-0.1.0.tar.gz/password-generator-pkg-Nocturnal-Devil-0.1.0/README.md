# Password-Generator

### Python Integration

Password generator which takes in a string and hashes it using MD5 algorithm

---

## Author: [Devil-Shinji](https://github.com/Devil-Shinji)

---

## Requirements
```bash
pip install -r requirements.txt
```

---

## Usage
- Cd into Python directory

- Run the program using either
```bash
python password_generator.py
```
or create an executable using pyinstaller [Add all necessary modules as hidden imports from requirements.txt]
```bash
pyinstaller --onefile password_generator.py --hidden-import pyperclip
```
and run the executable
```bash
./password_generator.exe
```

---

## License
See [LICENSE.md](LICENSE.md) for more details