# Draw fonts
* `draw_fonts.py`: Select a font, and show them using `chr()`.

# Terminal fonts
* `FullGreek-Terminus12x6.psf` was copied and extracted from `/usr/share/consolefonts/FullGreek-Terminus12x6.psf.gz`.
* `console-fonts-utils/` was downloaded from 
  [Linux Console Font Utilities](https://www.zap.org.au/projects/console-fonts-utils/).
  * Convert psf to txt (under `./fonts/` folder):
    ```
    ../console-fonts-utils/psf2psftx FullGreek-Terminus24x12.psf FullGreek-Terminus24x12.txt 
    ```
* Example of setting terminal fonts: `/bin/setfont /usr/share/consolefonts/FullCyrAsia-Terminus12x6.psf.gz`
* [Terminus Font Home Page](http://terminus-font.sourceforge.net/)
