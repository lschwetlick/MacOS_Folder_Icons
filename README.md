# MacOS_Folder_Icons

## folder_icon_maker
Takes an icon file and superimposes it onto the generic MacOS folder symbol. Then generates the .icns files that can be used to customize the file icons that show up in Finder.

```
usage: folder_icon_maker [-h] -i FILENAME -o OUTPUT

optional arguments:
  -h, --help                        show this help message and exit
  -i FILENAME, --icon FILENAME      icon input file
  -o OUTPUT, --output OUTPUT        output file name (without file ending)
```

## Example
In the terminal enter:
```
    python3 folder_icon_maker -i "User/Documents/MacOS_Folder_Icons/resources/github_logo.png" -o "github"
```
to recieve an icns file of this image:

![icns_example](icns_example.png)