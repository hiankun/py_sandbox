[2021-04-18]

# Setup conda env

* The following steps to avoid confliction between libraries:
    ```
    conda create -n streamlit_env
    conda activate streamlit_env
    conda install -c conda-forge streamlit opencv geopandas matplotlib
    pip install streamlit-webrtc
    ```

[2021-04-26]

# Follow streamlit-component tutorial

[A hands-on introduction to Streamlit Components](https://streamlit-components-tutorial.netlify.app)

* The default version of Node in Lubuntu 18.04 is too old to run `npm install`.
* Use [this approach](https://askubuntu.com/a/1009527) to install the latest version:
  ```
  curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
  source ~/.bashrc
  nvm install node
  ```

# Error from Tyepscript
* When trying `npm run start`, there're the error:
  ```
    >  7 | import type * as PrettyFormat from './types';
  ```
* Failed method: According to the following post, I updated the version of Typescript to latest version via ``.
[https://stackoverflow.com/a/60856373/9721896](https://stackoverflow.com/a/60856373/9721896)

  But it didn't work.
* Worked method: Edit `frontend/node_modules/pretty-format/build/index.d.ts` to change
  ```
  import type * as PrettyFormat from './types';
  ```
  to
  ```
  import * as PrettyFormat from './types';
  ```

