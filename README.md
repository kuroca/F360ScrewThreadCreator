# F360ScrewThreadCreator

*Under Construction. ETA: April 2024*

Calculations implemented using formulas from: [Thread Calculator](https://www.omnicalculator.com/construction/thread) (Written by Kenneth Alambra)


## Motivation

### Lack of Custom Thread Support in Fusion 360
In Fusion 360 there are a decent number of preset screw thread sizes, but when manufaturing parts to fit existing devices (i.e. threaded lens adapters for cameras, lens filter adapters, telescope part, etc.), chances are that the thread you need is not an existing preset within Fusion. You can create an XML file to define your own presets, however this is a relatively tedious process especially if you find yourself doing this often. In addition, whenever Fusion updates your custom presets won't be moved to the current install.

### Easily Adjusting Tolerances for 3D printing
Adujsting tolerances for screw threads is not easily achieveable natively, and oftentimes 3d printed screw theads come out too tight (in my experience often to the point of not working at all). I have seen some janky workarounds to avoid threads that are too tight, but I'd rather have things be easily reproducable.

## Planned Feature Set

- Automatically move user presets when Fusion updates
- Allow user to create metric (sorry Imperial enjoyers) screw threads by specifying thread diameter, pitch, and tolerance class
