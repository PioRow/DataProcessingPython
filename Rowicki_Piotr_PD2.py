### Data Processing in R and Python 2023Z
### Homework Assignment no. 2
###
### IMPORTANT
### This file should contain only solutions to tasks in the form of a functions
### definitions and comments to the code.
###
#
# Include imports here
import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------#
# Task 1
# -----------------------------------------------------------------------------#

def solution_1(Posts, Users):
    innerQuery = Posts[["OwnerUserId"]].merge(Users[["Id", "Location"]], left_on="OwnerUserId",
                                              right_on="Id", how="inner")
    # Alternatywnie
    # innerQuery=Posts[["OwnerUserId"]].set_index("OwnerUserId")
    # .join(Users[["Id","Location"]].set_index("Id"),how="inner")
    # Ale moim zadniem mniej przyjemne w użyciu, gdyż nie da się
    # bezposrednio w wywołaniu podać kluczy, po którch połączyć ramki

    # Puste warotsci przy wczytaniu zamienione na NaN
    Res = (innerQuery[["Location", "Id"]][innerQuery["Location"].notna()]
           .groupby(by="Location",as_index=False).count().rename(
        columns={"Id": "Count"}).sort_values(by="Count", ascending=False))
    Res = Res[0:10]
    Res.index = np.arange(10).tolist()
    return Res

# -----------------------------------------------------------------------------#
# Task 2
# -----------------------------------------------------------------------------#

def solution_2(Posts, PostLinks):
    """ Input the solution here """
    # ...
    # ...

# -----------------------------------------------------------------------------#
# Task 3
# -----------------------------------------------------------------------------#

def solution_3(Comments, Posts, Users):
    """ Input the solution here """
    # ...
    # ...
    
# -----------------------------------------------------------------------------#
# Task 4
# -----------------------------------------------------------------------------#

def solution_4(Posts, Users):
    """ Input the solution here """
    # ...
    # ...
    
# -----------------------------------------------------------------------------#
# Task 5
# -----------------------------------------------------------------------------#

def solution_5(Posts, Users):
    """ Input the solution here """
    # ...
    # ...
