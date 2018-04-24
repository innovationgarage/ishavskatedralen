# Aurora

Downloading test videos from [here](https://data-portal.phys.ucalgary.ca/auroramax/movies)

## Getting started (Live video to light - no templates)
- Connect the cathedral
- Find out which serial port talks to the cathedral:

      dmesg | grep tty

- Give permission to the user to talk to this port:

      sudo chmod 666 /dev/ttyACM[X]

- Run the test code:

      python src/vid2seq.py

- Check out the available arguments:

  	python src/vid2seq.py --help
	
## Generate 