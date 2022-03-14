# Static Thrust Test Stand
Used to measure static thrust of a propeller. RPM data found here https://docs.google.com/spreadsheets/d/1qRCRGGBxDaXqzT6ZN4GYqFSRvBQVMMZf4AISBBoSiTY/edit#gid=0

## Reading Data
Assuming you have everthing wired correctly, simply run the following command
```
python3 thrust_test.py
```
and do a keyboard interrupt (CTRL+C) to break out of the infinite loop when you 
are done reading data. Data will be saved to a folder called "data" in the 
current working directory.

If you run 
```
python3 thrust_test.py debug
```
it will print out random integer values for thrust instead of actually reading
the load cell. This is helpful for debugging.

## Plotting
To plot the most recently saved data, run the following command
```
python3 plot_data.py last 
```
You also could just run 
```
python3 plot_data.py 
```
and you will be prompted to select a file to plot with a file explorer box.
Lastly, you also could pass the path to the file you would like to plot
```
python3 plot_data.py "./data/my_data.txt"
```
