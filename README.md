# Aurora

Downloading test videos from [here](https://data-portal.phys.ucalgary.ca/auroramax/movies)

## Use MQTT client

      python src/demoMQTT.py --boost_green True --year 2018 --month 4 --day 21
      
use the date you want!      
      
## Getting started (Live video to light - no templates)
- Connect the cathedral
- Find out which serial port talks to the cathedral:

      dmesg | grep tty

- Give permission to the user to talk to this port:

      sudo chmod 666 /dev/ttyACM[X]

- Run the test code:

      python src/vid2template.py

- Check out the available arguments:

      python src/vid2template.py --help

- What vid2template.py does:
  * downloads the video for that date
  * generates sequences
  * sends a stream of light to a locally-connected cathedral
  * saves all measurements in **dataframes/**
  * saves all non-zero sequences (per channel) for template generation in **sequences/**
  
## Generate templates from sequences

      python src/seq2template.py --color g --n_cluster 250

- Check out the available arguments:

      python src/seq2template.py --help


## Live video to light (with template replacements)

   	python src/vid2template.py --use_template True

