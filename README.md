# bingocardmaker
Generates random bingo cards based on CSV files
This is a simple bingo card maker

Usage: makebingo.py [options] gridContentFile1.csv [gridContentFile2.csv]

Options:
  -h, --help            show this help message and exit
  -W GRIDWIDTH, --width=GRIDWIDTH
                        Grid Width
  -H GRIDHEIGHT, --height=GRIDHEIGHT
                        Grid height
  -e EMPTYCASES, --empty=EMPTYCASES
                        Empty Cases
  -n GRIDCOUNT, --number=GRIDCOUNT
                        Number of grids to generate
  -C CSVSEP, --CSV_SEPARATOR=CSVSEP
                        Separator for input CSV files

CSV Input files should be formatted as :
Content of a cell; Point value
