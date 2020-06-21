#packages:
#  rpi_ws281x
#  adafruit-circuitpython-neopixel
#
#  jeffdr@gmail.com

import board
import neopixel
import math
import time
import random

pixelCount = 50
pixels = neopixel.NeoPixel( board.D18, pixelCount,
                            brightness=1, pixel_order = neopixel.RGB,
                            auto_write=False )

def convertColor( c ):
    c = 0.0 if c < 0.0 else c;
    c = 1.0 if c > 1.0 else c;
    return c*255;


def setColor( x, y, r, g, b ):
    if y < 0 or y >= 5 or x < 0 or x >= 10:
        return;
    ix = y * 10;
    if y % 2:
        ix += x;
    else:
        ix += 9-x;
    pixels[ix] = (convertColor(r), convertColor(g), convertColor(b));


def fillAllColors( r, g, b ):
    pixels.fill( (convertColor(r), convertColor(g), convertColor(b)) );


def multiColor():
    #a simple color test
    while True:
        t = time.time();
        freq = 3.141592 / 5.0;
        for y in range(0,5):
            for x in range(0,10):
                wavex = 0.5 + 0.5*math.cos( x*freq+t );
                wavey = 0.5 + 0.5*math.cos( y*freq+t );
                c = wavex * wavey;
                setColor( x,y, c,1.0-c,c );
        pixels.show();
        time.sleep( 1.0/60.0 );


def lightning():
    flash = 0.0;
    tlast = time.time();
    random.seed();
    while True:
        
        #fade out our flashes
        t = time.time();
        dt = t - tlast;
        flash *= math.exp( -7.0 * dt );
        
        #generate a new strike (odds are higher during previous strikes)
        odds = 0.013;
        if flash > 0.3:
            odds += 0.14;
        elif flash > 0.01:
            odds += 0.09;
        if( random.random() < odds ):
            #choose a brightness
            bright = 0.2 + 0.8*random.random();
            
            #choose a random distance and attenuate (1/d^2)
            dist = 0.5 + 9.5 * random.random();
            attenuation = 1.0 / (dist * dist);
            
            flash += bright * attenuation;
        
        #display and wait for next frame
        fillAllColors( flash, flash, flash );
        pixels.show();
        tlast = t;
        time.sleep( 1.0/60.0 );
    

lightning();

