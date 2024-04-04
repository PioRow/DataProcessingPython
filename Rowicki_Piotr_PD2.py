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
           .groupby(by="Location", as_index=False).count().rename(
        columns={"Id": "Count"}).sort_values(by="Count", ascending=False, ignore_index=True))
    Res = Res[0:10]
    return Res


# -----------------------------------------------------------------------------#
# Task 2
# -----------------------------------------------------------------------------#

def solution_2(Posts, PostLinks):
    # wewnętrzna kwerenda
    RelatedTab = (PostLinks[["RelatedPostId", "Id"]].groupby("RelatedPostId", as_index=False)
                  .count().rename(columns={"RelatedPostId": "PostId", "Id": "NumLinks"}))

    # jak poprzednio można użyć metody join
    Res = RelatedTab.merge(Posts, how="inner", left_on="PostId", right_on="Id")

    Res = (Res[Res.PostTypeId == 1][["Title", "NumLinks"]].
           sort_values(by="NumLinks", ascending=False, ignore_index=True))
    return Res


# -----------------------------------------------------------------------------#
# Task 3
# -----------------------------------------------------------------------------#

def solution_3(Comments, Posts, Users):
    Res = (Comments[["PostId", "Score", ]].groupby(["PostId"], as_index=False).sum()
    .rename(columns={"Score": "CommentsTotalScore"})
    .merge(Posts, how="inner", left_on="PostId", right_on="Id")
    .query("PostTypeId == 1", )[["OwnerUserId", "Title", "CommentCount", "ViewCount", "CommentsTotalScore"]]
    .merge(Users, how="inner", left_on="OwnerUserId", right_on="Id")
    .sort_values(by="CommentsTotalScore", ascending=False, ignore_index=True)
    [["Title", "CommentCount", "ViewCount", "CommentsTotalScore", "DisplayName", "Reputation", "Location"]])

    # dopiero podczas implementowania tego zapytania, odnalazłem metodę query, która pozwolila implementowac
    # zapytanie,podobnie jak w dplyr, jako nieprzerwany ciag instrukcji.
    return Res[0:10]


# -----------------------------------------------------------------------------#
# Task 4
# -----------------------------------------------------------------------------#

def solution_4(Posts, Users):
    QnA=Posts[["PostTypeId","OwnerUserId"]]
    Q=QnA.query("PostTypeId == 1").groupby("OwnerUserId",as_index=False).count().rename(columns={"PostTypeId":"QuestionsNumber"})
    A=QnA.query("PostTypeId == 2").groupby("OwnerUserId",as_index=False).count().rename(columns={"PostTypeId":"AnswersNumber"})
    Res=(Q.merge(A,on="OwnerUserId",how="inner").query("QuestionsNumber<AnswersNumber").
         sort_values(by="AnswersNumber",ascending=False,ignore_index=True)[0:5]
        .merge(Users,left_on="OwnerUserId",right_on="Id",how="inner")
        [["DisplayName", "QuestionsNumber", "AnswersNumber", "Location",
        "Reputation", "UpVotes", "DownVotes"]])
    return Res


# -----------------------------------------------------------------------------#
# Task 5
# -----------------------------------------------------------------------------#

def solution_5(Posts, Users):
    AnsCount=(Posts[["PostTypeId","ParentId"]].query("PostTypeId == 2").groupby("ParentId", as_index=False)
              .count().rename(columns={"PostTypeId":"AnswerCount"}))
    PostAuth=Posts.merge(AnsCount,left_on="Id",right_on="ParentId")[["AnswerCount_y","Id","OwnerUserId"]].rename(columns={"AnswerCount_y":"AnswerCount"})

    # W przeciwienstiwe do bibliotek R, panadas konwertuje puste komórki ramki nan NaN. jest to o tyle uciazliwe,
    # że przez nie można użyc groupby na wszystkich ineteresujących nas wierszach, poneiważ interesujące nas mają własnie
    # puste komórki. Pozostaje uzycie takiego dosc nieeleganckiego rozwiązania
    Res=Users.merge(PostAuth,left_on="AccountId",right_on="OwnerUserId",how="inner")[["AccountId","AnswerCount"]].groupby(["AccountId"], as_index=False).mean().rename(columns={"AnswerCount":"AverageAnswersCount"}).sort_values(by="AverageAnswersCount",ascending=False,ignore_index=True)[0:10]

    Tmp=Users[["AccountId","DisplayName","Location"]]
    Res=Res.merge(Tmp,on="AccountId")[["AccountId","DisplayName","Location","AverageAnswersCount"]]
    return Res
