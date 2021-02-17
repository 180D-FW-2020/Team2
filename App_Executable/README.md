conda list
- lists all packages

## Command to package everything
pyinstaller "main.py" --onefile --add-data='ID.txt:$pwd' 
cp ./dist/main ./main