build:
    pandoc --from markdown+smart --to=html5 --css=static/css/styling.css -s \
        index.md \
        -o index.html