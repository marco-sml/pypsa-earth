# PyPSA-Earth-Sec: A Sector-Coupled Open Optimisation Model of the Global Energy System

## Development Status: Version 0.0.5

Disclaimer: PyPSA-Earth-Sec is still under development.

The model currently covers one country, Morocco, in a simplistic representation with only 4 nodes (simplistic). A prerequisite for a successful model run is built network generated by pypsa-africa. Currently, no real demand data is used for the country inspected, instead, we use dummy data that is either taken from a different country relying on the data used in pypsa-eur-sec or generated using heuristics.

The model now includes the following energy carriers: \n
        **Electricity**, **Hydrogen**, **Fossil gas**, **Fossil oil** and **Carbon**.

The demand sectors covered are: **residential**, **industry**, **land transport**, **aviation** and **shipping** 

The diagram below depicts one representative clustered node showing the combination of carriers and sectors covered in the model as well as the generation and conversion technologies included. 

