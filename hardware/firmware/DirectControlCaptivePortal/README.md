Each byte represents the template from 1 to 253. 0 means empty. 254 means ignore current, example:
R,G,B
254,0,5 <- keeps the current R, clears G and sets B channel to the template 5

R=255 sets special stuff:

    R,G,B
    255,255,255 <- initialization [NOT USED]

Fader:

    255,10,0-1 <- enable or disable fade in-out
    255,11,0-255 <- fade speed (all channels)
    255,12,0-255 <- fade speed (red) [NOT USED]
    255,13,0-255 <- fade speed (green) [NOT USED]
    255,19,0-255 <- fade speed (blue) [NOT USED]

Noise:

    255,110,0-1 <- enable or disable background noise
    255,111,0-255 <- set background noise speed
    255,112,0-255 <- set background noise speed variability
    255,113,0-255 <- set background noise intensity

Scroller:

    255,120,0-1 <- enable or disable scroller
    255,121,0-255 <- set scroller speed
    255,122,0-255 <- set scroller speed variability
