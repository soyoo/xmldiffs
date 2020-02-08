# xmldiffs
A tool for compare two XML files or compare XML files under two folder. This tool use `xmltodict` transfer XML file to python's dictionary, then simple compare dictionary if is equal.

##### Usage

```
xmldiffs --path1=.\example\dir1\file.xml --path2=.\example\dir2\file.xml
```

or

```
xmldiffs --path1=.\example\dir1          --path2=.\example\dir2
```

##### Third parties

```
pip install click
pip install loguru
pip install pyinstaller
pip install xmltodict
```

