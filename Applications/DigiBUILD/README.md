# DREEM

![image](https://user-images.githubusercontent.com/120646072/207902143-beea4f1d-7065-468d-913c-c0a13cb06fea.png)

## Contents
- [Contents](#contents)
- [About](#about)
- [Quick start](#quick-start)
- [Documentation](#documentation)
- [Citing DREEM](#citing-bsam)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## About
The Dynamic high-Resolution dEmand-sidE Management (DREEM) model is a hybrid bottom up model that combines the key features of both statistical and engineering models. The model serves as an entry point in Demand-Side Management modeling in the building sector, by expanding the computational capabilities of existing Building Energy System models to assess the benefits and limitations of demand-flexibility, primarily for consumers, and for other power actors involved. The novelty of the DREEM model lies mainly in its modularity, as its structure is decomposed into individual modules characterized by the main principles of component- and modular-based system modeling approach, namely “the interdependence of decisions within modules; the independence of decisions between modules; and the hierarchical dependence of modules on components embodying standards and design rules.”

This modular approach allows for more flexibility in terms of possible system configurations and computational efficiency towards a wide range of scenarios studying different aspects of end-use. It also provides the ability to incorporate future technological breakthroughs in a detailed manner, such as the inclusion of heat pumps or electric vehicles, in view of energy transitions envisioning the full electrification of the heating and transport sectors. The latter makes the DREEM model competitive compared to other models in the field, since scientific literature acknowledges that there are limitations to how much technological detail can be incorporated without running into computational and other difficulties. The model also supports the capability of producing output for a group of buildings and could also serve as a basis for modeling domestic energy demand within the broader field of urban, national or regional energy systems in different geographical (climate) and socioeconomic contexts. It is maintained by the [Techno-Economics of Energy Systems laboratory (TEESlab)](https://teeslab.unipi.gr) at the University of Piraeus and is freely available on GitHub. 

## Quick start
* Install a Modelica based modeling and simulation environment.
* Download the modelica "Buildings" library from [here](https://github.com/lbl-srg/modelica-buildings). 
* Download DREEM from Github and save it in a folder of your preference.
* Run DREEM.mo file.

## Documentation
Read the full documentation [here](http://teeslab.unipi.gr/wp-content/uploads/2022/12/DREEM-Documentation_v1.0.pdf).

## Citing DREEM
In academic literature please cite DREEM as: 
>[![article DOI](https://img.shields.io/badge/article-10.1016/j.enconman.2019.112339-blue)](https://doi.org/10.1016/j.enconman.2019.112339) Stavrakas, V., & Flamos, A. (2020). A modular high-resolution demand-side management model to quantify benefits of demand-flexibility in the residential sector. Energy Conversion and Management, 205, 112339. [https://doi.org/10.1016/j.enconman.2019.112339](https://doi.org/10.1016/j.enconman.2019.112339)


## License
The **DREEM source code** consists of the *DREEM.mo* file and is licensed under the GNU Affero General Public License:

    Copyright (C) 2022 Technoeconomics of Energy Systems laboratory - University of Piraeus Research Center (TEESlab-UPRC)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
 The **DREEM model** is built upon **Modelica Buildings library**, a free open-source library available under the **3 clause BSD License**. Read the **3 clause BSD License** terms [here](https://simulationresearch.lbl.gov/modelica/license.html).

## Acknowledgements
The development of DREEM has been partially funded by the following sources:
* The EC funded Horizon 2020 Framework Programme for Research and Innovation (EU H2020) Project titled "Sustainable energy transitions laboratory" (SENTINEL) with Grant Agreement No. 837089
* The EC funded Horizon 2020 Framework Programme for Research and Innovation (EU H2020) Project titled "Transition pathways and risk analysis for climate change policies" (TRANSrisk) with Grant Agreement No. 642260       
