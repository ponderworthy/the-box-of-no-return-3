# the-box-of-no-return-3

The Box of No Return III is a Linux synth platform suitable for live musicianship, designed to handle patches with enormous demands, and switch between them with zero delay and zero cutout.  Its current production design is discussed at https://lsn.ponderworthy.com.  This repository was created to receive the files for its second major edition, which is using the [pipewire](https://pipewire.org/) audio architecture at its core.  The BNR using these files is up and running, is not in regular use yet, but will be soon.

## the name

The original name for the project was "Supermega Rumblic Organ", or SRO, after its first patch.  But a Strings patch was soon added.  It is called the Box of No Return because after playing it, its creator cannot go back to his former instrumentation, at least not for long.

## why this project and its benefits

To build more and better.  The rest is details :-)

From the beginning, the BNR was desired to handle patches of maximum, profound and terrible, tonal content.  If you find yourself reducing the profundity of your patches because your machine won't do better, this project may be very good for you, especially if you play live.  Current patches include one with three simultaneous Yoshimis, another with five simultaneous large FluidSynth soundfonts, and the ability to mix the two and a third together.  Many prayers granted, and much help from the Linux Audio community, study, work, and trial and error, has gone into making this happen reliably and well.

The first major edition of this project used a single JACK process to connect all of its audio software components.  The reliability of this was just sufficient, and it tended to crash a lot, not due to lack of CPU power or RAM, but because JACK alone, even JACK2, could not distribute the load to use available resources. The [second major edition](https://github.com/ponderworthy/the-box-of-no-return) used multiple JACK processes in tandem, connected, and worked very well for a number of years.  This method was called [MultiJACK](https://github.com/ponderworthy/MultiJACK).  But then Pipewire, a project of exciting possibility in Linux audio, reached mainstream, in its first major distro, RedHat. This had come about just when I was building a new BNR, and it is shockingly efficient and capable, it is producing a much better result than MultiJACK did.  It will communicate using any of the common Linux audio APIs, and if your virtual wiring betwewen apps is complex, it will handle it marvelously well, applying whatever CPU and buffering resources it needs in dynamic fashion.  Pipewire is so much more efficient, that polyphony is doubled on the new box as it stands, and may incrfease even further.

## general notes on setup

* These files are designed principally to build a MIDI tone synthesizer as a headless Linux box, which 
one connects via either MIDI interface or USB cord to an appropriate keyboard controller.  The box must be set up to good Linux production audio standards.  As of this writing, the Manjaro default kernel does very well, and it is used with a sysctl.conf.d file with the [full wired networking set desribed here](https://notes.ponderworthy.com/linux-networking-speed-and-responsiveness), the only change being swappiness set at 10.  

* The "Strings" patch uses soundfonts which are too big to fit in this github repo.  They are called within the experimental Calf plugin which handles fluidsynth.  Currently I am using a very small subset of the [SSO](http://sso.mattiaswestlund.net/), converted to SF2.  This probably will change in the future.

* To run the whole BNR as here coded, you'll want at least a quad-core, 3GHz, 8G RAM probably.  It can be scaled up or down. 

* All files in this repository need to be placed in a folder named BNR, located just off a user profile root.

* If headless run is indicated, the machine needs to boot into a user profile, without password, and the environment needs to run shell script "boot" at boot.  Otherwise just run ~/BNR/boot to get it all under way.  

* Any dot-files (e.g., .calfpresets) need to be placed in the root of the user profile 
used for this purpose.

* One of the more difficult challenges was solved in earlier iterations of the BNR: startup.  Each JACK client has to "settle" at startup before the next one begins loading.  The python library jpctrl.py was created to handle this, and is used in BOOT-GENERAL.py.



