# coding: utf8
"""SaKKe: utilitaire de statistiques de devoirs

usage: sakke [--nom_devoir=<nom_devoir>] [--par_page=<par_page>] [--pages=<pages>] [--transform=<transform>] [--option=<name:value> ...] <exercice_bareme>

Options:
  -h --help                     Montre l'aide
  --nom_devoir=<nom_devoir>     Nom du devoir.
  --pages=<pages>               Combien de pages à considérer dans la feuille de calcul
                                (en commençant à gauche) [default: -1]
  --par_page=<par_page>         Nombre de résultats par page [default: 3]
  --transform=<transform>       Transformation à appliquer sur la note finale.
                                C'est une expression où x représente la note.
                                [default: x]
  --option=<name:value>         Option pour le rendu. Peut-être répétée.
                                Valeurs par défaut des options suportées
                                    * latex_documentclass_options:a4paper,10pt,landscape
                                    * latex_geometry_options:top=1cm,right=1cm,bottom=1cm,left=1cm
                                    * latex_font_size:tiny
  exercice_bareme               Chemin vers une feuille de calcul au bon format

"""
import sys
from pathlib import Path
from typing import Tuple

import pandas as pd
from docopt import docopt
from jinja2 import Environment, FileSystemLoader

from . import __version__

NOTE = 20
SAKKE_PATH = Path(__file__).parent.resolve()
TEMPLATES_DIR = Path(SAKKE_PATH) / "templates"

OPTIONS = {
    "latex_documentclass_options": "a4paper,10pt,landscape",
    "latex_font_size": "tiny",
    "latex_geometry_options": "top=1cm,right=1cm,bottom=1cm,left=1cm",
}

# new
COL_SUR_LA_COPIE = "Sur la copie"
COL_BAREME = "Bareme"
COL_SUCCESS = "Succès classe"
COL_EN_REALITÉ = "En réalité"
COL_SUCCESS_RELATIF = "Succès élève"
COL_TOTAL = "Total"
COL_SUR_20 = "/20"
COL_RANK = "Rang"

BAREME_TOTAL = 4
LABEL_PROBLEME = "problème"
LABEL_QUESTION = "question"
LABEL_BAREME = "barème"
LABEL_REUSSITE_ELEVE = "réussite élève"
LABEL_REUSSITE_CLASSE = "réussite classe"
LABEL_REUSSITE_NORM = "réussite normalisée"
LABEL_EN_REALITE = "en réalité"
LABEL_SUR_LA_COPIE = "sur la copie"
LABEL_TRANSFORM = "note finale"
LABEL_RANG = "rang"


def read_excel(spreadsheet: str, pages: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Read an excel file and returns tidy dataframe.

    Args:
        spreadsheet: path to the spreadsheet to analyze

    Returns:
        tidy version of
            - the "barème"
            - the students resuls
    """
    excel = pd.ExcelFile(spreadsheet)
    sheet_names = excel.sheet_names

    devoir_df = pd.DataFrame()
    bareme_df = pd.DataFrame()
    if pages > 0:
        sheet_names = sheet_names[0:pages]
    for sheet_name in sheet_names:
        raw_bareme = pd.read_excel(spreadsheet, sheet_name=sheet_name, nrows=1)
        raw_results = pd.read_excel(spreadsheet, sheet_name=sheet_name, skiprows=4)
        # clean the inputs
        # - remove Nan columns (bareme might start at an arbitrary columns)
        bareme = raw_bareme.dropna(axis="columns", how="all")
        bareme = bareme.set_index(bareme.columns[0]).transpose()
        # make it a serie
        bareme = bareme[bareme.columns[0]]
        bareme.index = bareme.index.rename(LABEL_QUESTION)
        # Result start at the first column
        # Nom, Prénom are the two columns that identifies the student.
        students_index = raw_results.columns.tolist()[0:2]
        students = raw_results.set_index(students_index)
        students.columns = bareme.index
        tidy = students.melt(
            ignore_index=False, var_name=LABEL_QUESTION, value_name=LABEL_SUR_LA_COPIE
        )
        tidy[LABEL_PROBLEME] = sheet_name
        devoir_df = pd.concat([devoir_df, tidy])
        bareme = bareme.to_frame()
        bareme[LABEL_PROBLEME] = sheet_name
        bareme_df = pd.concat([bareme_df, bareme])
    bareme_df = bareme_df.set_index([LABEL_PROBLEME], append=True)
    bareme_df.index = bareme_df.index.swaplevel(0, 1)
    # devoir_df is tidy
    #                      question  sur la copie problème
    # Nom      Prénom
    # Nom1     Prénom1        1           4.0      Pb1
    # Nom2     Prénom2        1           4.0      Pb1
    # ...                   ...           ...      ...
    # NOMx     Prénomx      7 e           0.0      Pb2

    # bareme_df is tidy
    #                       Valeur
    # problème question
    # Pb1      1            1.0
    #          2            2.5
    #          3            1.5
    #          4            1.0
    #          5a           3.0
    #          5b           0.5
    #          6            1.5
    #          7            2.0
    # Pb2      1            1.5
    #          2            0.5
    #          3            0.5
    #          4            2.0
    #          5a           1.0
    #          5bi          1.0
    #          5bii         2.0
    #          5c           0.5
    #          6a           1.0
    #          6b           0.5
    #          6c           0.5
    #          7a           1.5
    #          7b           1.5
    #          7c           0.5
    #          7d           1.0
    #          7 e          2.0
    return devoir_df, bareme_df


def bareme_builder(bareme_df):
    """Emit a function that will map questions to grade.

    Questions are identified by a tuple (probleme, question)
    """
    mapping = dict(zip(bareme_df.index.values, bareme_df.values.T[0]))
    return lambda x: mapping[x]


def reussite_builder(reussite_df):
    """Same but for the reussite."""
    mapping = dict(zip(reussite_df.index.values, reussite_df.values))
    return lambda x: mapping[x]


def enrichir(devoir_df, bareme_df):
    # build the function that maps a probleme, question -> note du bareme
    bareme_fnc = bareme_builder(bareme_df)

    # enrich the devoir_df
    devoir_df[LABEL_BAREME] = devoir_df.apply(
        lambda x: bareme_fnc((x[LABEL_PROBLEME], x[LABEL_QUESTION])), axis="columns"
    )
    devoir_df[LABEL_REUSSITE_ELEVE] = devoir_df[LABEL_SUR_LA_COPIE] / BAREME_TOTAL
    devoir_df[LABEL_EN_REALITE] = (
        devoir_df[LABEL_REUSSITE_ELEVE] * devoir_df[LABEL_BAREME]
    )

    # add the global réussit to this df
    reussite_df = devoir_df.groupby(by=[LABEL_PROBLEME, LABEL_QUESTION]).mean()[
        LABEL_REUSSITE_ELEVE
    ]
    reussite = reussite_builder(reussite_df)
    # for each row (one specific question of one specific probleme) adds a column with the global reussite
    devoir_df[LABEL_REUSSITE_CLASSE] = devoir_df.apply(
        lambda x: reussite((x[LABEL_PROBLEME], x[LABEL_QUESTION])), axis="columns"
    )

    return devoir_df


def aggrege(devoir_df, id_eleve, transform):
    # Get some global statistics
    # probleme_par_eleve
    #                                sur la copie  barème  réussite élève  en réalité  réussite classe
    # Nom      Prénom  problème
    # NOM1     Prénom1  Pb1               20.5    13.0           5.125      8.5000         4.978261
    #                   Pb2               47.0    17.5          11.750     11.1250         9.671196
    #                   Pb3               14.0    22.0           3.500      6.1875         6.774457
    # NOM2     Prénom2  Pb1               17.5    13.0           4.375      7.5000         4.978261
    probleme_par_eleve = devoir_df.groupby(id_eleve + [LABEL_PROBLEME]).sum()
    probleme_par_eleve[LABEL_REUSSITE_NORM] = (
        probleme_par_eleve[LABEL_REUSSITE_ELEVE] / probleme_par_eleve[LABEL_BAREME]
    )

    # devoirt_par_eleve
    #                                   sur la copie  barème  réussite élève  en réalité  réussite classe
    # Nom           Prénom
    # NOM1          Prénom1                 81.5    52.5          20.375     25.8125        21.423913
    # NOM2          Prénom2                 69.0    52.5          17.250     23.3750        21.423913
    devoir_par_eleve = devoir_df.groupby(id_eleve).sum()

    # We transform to adjust the final result
    devoir_par_eleve[LABEL_TRANSFORM] = (
        (devoir_par_eleve[LABEL_EN_REALITE] / devoir_par_eleve[LABEL_BAREME]) * NOTE
    ).apply(transform)
    # add the rank
    devoir_par_eleve[LABEL_RANG] = devoir_par_eleve[LABEL_TRANSFORM].rank(ascending=False, method="min").astype(int)

    return devoir_par_eleve, probleme_par_eleve


def all_in_one(exercices_baremes, pages, nom_devoir, transform):
    devoir_df, bareme_df = read_excel(exercices_baremes, pages)
    # get the indexes to be agnostic to the column name in excel
    id_eleve = devoir_df.index.names

    devoir_df = enrichir(devoir_df, bareme_df)

    devoir_par_eleve, probleme_par_eleve = aggrege(devoir_df, id_eleve, transform)

    # quelques stats globales
    metadata = dict(
        id_eleve=id_eleve,
        nom_devoir=f"{nom_devoir}",
        moyenne=devoir_par_eleve[LABEL_TRANSFORM].describe()["mean"],
        ecart_type=devoir_par_eleve[LABEL_TRANSFORM].describe()["std"],
    )
    return devoir_df, bareme_df, devoir_par_eleve, probleme_par_eleve, metadata


def generate_par_eleve(
    devoir_df, devoir_par_eleve, probleme_par_eleve, metadata, par_page, options
):
    # tous les problème du devoir
    problemes = devoir_df[LABEL_PROBLEME].unique()
    students = devoir_df.index.unique().values

    # TODO sanity check
    # - chaque élève a des notes pour chaque exercice

    par_question = dict()
    questions_par_eleve = dict()
    for probleme in problemes:
        # for this problem compute the result for each student
        # get the type of note as values
        # the question are now in column (pivot)
        #
        # question                          I1a       I1b       I1c       I2a       I2b       I2c        I3       II1      II2a      II2b      III1      III2
        # Nom  Prénom  type
        # Nom1 Prénom1 barème          1.000000  1.500000  1.500000  1.000000  2.000000  0.500000  2.000000  2.000000  2.000000  2.000000  2.000000  2.000000
        #      en réalité      0.500000  1.125000  1.500000  0.750000  2.000000  0.500000  0.000000  0.000000  2.000000  0.000000  0.000000  0.000000
        #      réussite        0.668478  0.442935  0.271739  0.538043  0.320652  0.195652  0.138587  0.589674  0.869565  0.548913  0.070652  0.067935
        #      réussite élève  0.500000  0.750000  1.000000  0.750000  1.000000  1.000000  0.000000  0.000000  1.000000  0.000000  0.000000  0.000000
        #      sur la copie    2.000000  3.000000  4.000000  3.000000  4.000000  4.000000  0.000000  0.000000  4.000000  0.000000  0.000000  0.000000
        _par_question = (
            devoir_df[devoir_df[LABEL_PROBLEME] == probleme]
            # on ne veut pas ça dans la sortie et c'est pas forcément facile à supprimer après
            .drop(LABEL_REUSSITE_ELEVE, axis="columns")
            .drop(LABEL_PROBLEME, axis="columns")
            .melt(
                id_vars=[LABEL_QUESTION],
                var_name=probleme,
                value_name="note",
                ignore_index=False,
            )
            .reset_index()
            .pivot(
                index=metadata["id_eleve"] + [probleme],
                columns=[LABEL_QUESTION],
                values=["note"],
            )
        )
        _par_question.columns = _par_question.columns.droplevel()
        par_question[probleme] = _par_question

        for student in students:
            questions_par_eleve.setdefault(student, [])
            result_student = _par_question.loc[student]
            result_student.index.name=""
            # for output
            idx = list(student) + [probleme]
            # on change le nom associé aux colonnes  pour l'affichage du tableau
            # ce sera par exemple Pb1(8.5/10) ou 8.5 est la note de l'étudiant
            # et 10 le total possible
            note = probleme_par_eleve.loc[[idx]][LABEL_EN_REALITE].squeeze()
            total = result_student.sum(axis="columns")[LABEL_BAREME]
            # pandas me garde un nom que je ne veux pas à l'export
            # je mets un espace du coup
            result_student[" "] = f"{probleme} / ({note}/{total})"
            result_student = result_student.set_index(" ", append=True).swaplevel(0, 1)
            result_student.index.name = ""
            result_student.columns.name = ""
            questions_par_eleve[student].append(result_student)

    entete_par_eleve = {}
    for student in students:
        entete_par_eleve[student] = dict(
            nom_devoir=f"{metadata['nom_devoir']}",
            nom=f"{' '.join(student)}",
            rang=f"rang: {devoir_par_eleve.loc[student][LABEL_RANG]:.0f}",
            note=f"note: {devoir_par_eleve.loc[student][LABEL_TRANSFORM]:.2f}",
            moyenne=f"moyenne: {metadata['moyenne']:.2f}",
            ecart_type=f"écart-type: {metadata['ecart_type']:.2f}",
        )

    # Rendering tex
    env = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_DIR))
    template = env.get_template("stats.tex.j2")
    rendered_text = template.render(
        questions_par_eleve=questions_par_eleve,
        entete_par_eleve=entete_par_eleve,
        par_page=par_page,
        options=options,
    )
    with open("out.tex", "w") as f:
        f.write(rendered_text)


def plot(devoir_par_eleve, probleme_par_eleve, metadata):
    import seaborn as sns
    import matplotlib.pyplot as plt

    plt.title(metadata["nom_devoir"])
    sns.histplot(data=devoir_par_eleve, x=LABEL_TRANSFORM)
    plt.savefig("devoir.pdf")
    plt.clf()
    plt.title(metadata["nom_devoir"])
    sns.stripplot(
        data=probleme_par_eleve.reset_index(), x=LABEL_PROBLEME, y=LABEL_REUSSITE_NORM
    ).set(title=metadata["nom_devoir"])
    plt.savefig("problemes.pdf")


def main():
    arguments = docopt(__doc__, version=__version__)
    print(arguments)
    exercices_baremes = arguments["<exercice_bareme>"]
    nom_devoir = arguments["--nom_devoir"]
    if nom_devoir is None:
        nom_devoir = Path(exercices_baremes).with_suffix("")
    transform = lambda x: eval(arguments["--transform"])
    par_page = int(arguments["--par_page"])
    pages = int(arguments["--pages"])
    # construction des options
    options = {}
    options.update(OPTIONS)
    options.update(dict(map(lambda x: x.split(":"), arguments["--option"])))
    print(options)
    if len(exercices_baremes) < 1:
        sys.exit(0)

    devoir_df, bareme_df, devoir_par_eleve, probleme_par_eleve, metadata = all_in_one(
        exercices_baremes, pages, nom_devoir, transform
    )

    generate_par_eleve(
        devoir_df, devoir_par_eleve, probleme_par_eleve, metadata, par_page, options
    )
    plot(devoir_par_eleve, probleme_par_eleve, metadata)


if __name__ == "__main__":
    # arguments = docopt(__doc__, version=0.1)
    # (arguments['<exercice:bareme>'])
    try:
        main()
    except Exception as e:
        print("Le programme s'est terminé avec une erreur : ")
        print(e)
