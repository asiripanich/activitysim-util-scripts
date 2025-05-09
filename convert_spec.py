# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "polars==1.29.0",
# ]
# ///

import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import polars.selectors as cs
    import re
    from collections import Counter
    return Counter, mo, pl, re


@app.cell(hide_code=True)
def _(Counter, re):
    def convert_to_underscore_case(string_list):
        """
        Converts a list of strings to underscore case.
        This version also converts colons and other common separators.

        Args:
          string_list: A list of strings.

        Returns:
          A new list with strings converted to underscore case.
        """
        if not isinstance(string_list, list):
            raise TypeError("Input must be a list of strings.")
        if not all(isinstance(s, str) for s in string_list):
            raise ValueError("All elements in the list must be strings.")

        underscore_case_list = []
        for s_original in string_list:
            # Check if the string starts with '#' (comment)
            if s_original.startswith("#"):
                underscore_case_list.append(s_original)
                continue  # Move to the next string

            s = s_original

            # 1. Replace common separators (space, hyphen, colon) with underscore
            s = s.replace(" ", "_").replace("-", "_").replace(":", "_")

            # 2. Handle CamelCase and PascalCase: insert underscore before uppercase letters
            #    (but not at the beginning of the string if it's already uppercase,
            #     and not if the previous character was already an underscore).
            s = re.sub(r"(?<!^)(?<!_)(?=[A-Z])", "_", s)

            # 3. Convert to lowercase
            s = s.lower()

            # 4. Replace any other non-alphanumeric characters (except underscore) with underscore
            #    This will catch other symbols that might not have been explicitly handled.
            s = re.sub(
                r"[^\w_]+", "_", s
            )  # \w matches alphanumeric characters and underscore

            # 5. Remove any leading/trailing underscores that might have been created
            s = s.strip("_")

            # 6. Consolidate multiple consecutive underscores into a single underscore
            s = re.sub(r"_+", "_", s)

            underscore_case_list.append(s)
        return underscore_case_list


    def uniquify_string_list_with_numbering(string_list):
        """
        Ensures all strings in a list are unique by appending a suffix like '_1', '_2'
        to duplicated strings. The original order of elements is preserved.

        Args:
          string_list: A list of strings.

        Returns:
          A new list with strings made unique by numbering duplicates.
          Strings that were already unique remain unchanged.
        """
        if not isinstance(string_list, list):
            raise TypeError("Input must be a list of strings.")
        if not all(isinstance(s, str) for s in string_list):
            raise ValueError("All elements in the list must be strings.")

        if not string_list:
            return []

        # Count frequencies of each string
        counts = Counter(string_list)

        # Keep track of the current suffix number for each duplicated string
        suffix_counters = {}

        result_list = []

        for item in string_list:
            # If the string appears more than once, it's a duplicate
            if counts[item] > 1:
                # Get the current suffix for this item, defaulting to 0 if not seen yet
                current_suffix = suffix_counters.get(item, 0) + 1
                suffix_counters[item] = current_suffix
                result_list.append(f"{item}_{current_suffix}")
            else:
                # If the string is unique, add it as is
                result_list.append(item)

        return result_list
    return convert_to_underscore_case, uniquify_string_list_with_numbering


@app.cell
def _(mo):
    spec_file = mo.ui.file(kind="area", filetypes=['.csv'])
    return (spec_file,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Select an ActivitySim specification file to convert

    If you have a specification file that with coefficient values embedded like below.

    | Description                                                                    | Expression                          | M            | N            | H    |
    | :----------------------------------------------------------------------------- | :---------------------------------- | :----------- | :----------- | :--- |
    | Full-time worker alternative-specific constants                                | ptype == 1                          | 0.885080091  | 0.531583624  |      |
    | Part-time worker alternative-specific constants                                | ptype == 2                          | -0.920808727 | 1.117988879  |      |
    | University student alternative-specific constants                              | ptype == 3                          | 1.898468936  | -0.380144113 |      |
    | Non-working adult alternative-specific constants                               | ptype == 4                          | -4.352       | -0.332324197 |      |
    | Retired alternative-specific constants                                         | ptype == 5                          | -7.499       | -1.143572039 |      |

    But you want to have the coefficient values extracted out to another file like these:

    **spec.csv**

    | Label                                                                   | Description                                                                    | Expression                             | M                                                                       | N                                                                       | H    |
    | :---------------------------------------------------------------------- | :----------------------------------------------------------------------------- | :------------------------------------- | :---------------------------------------------------------------------- | :---------------------------------------------------------------------- | :--- |
    | util_full_time_worker_alternative_specific_constants                    | Full-time worker alternative-specific constants                                | ptype == 1                             | util_full_time_worker_alternative_specific_constants_M                  | util_full_time_worker_alternative_specific_constants_N                  |      |
    | util_part_time_worker_alternative_specific_constants                    | Part-time worker alternative-specific constants                                | ptype == 2                             | util_part_time_worker_alternative_specific_constants_M                  | util_part_time_worker_alternative_specific_constants_N                  |      |
    | util_university_student_alternative_specific_constants                  | University student alternative-specific constants                              | ptype == 3                             | util_university_student_alternative_specific_constants_M                | util_university_student_alternative_specific_constants_N                |      |
    | util_non_working_adult_alternative_specific_constants                   | Non-working adult alternative-specific constants                               | ptype == 4                             | util_non_working_adult_alternative_specific_constants_M                 | util_non_working_adult_alternative_specific_constants_N                 |      |
    | util_retired_alternative_specific_constants                             | Retired alternative-specific constants                                         | ptype == 5                             | util_retired_alternative_specific_constants_M                           | util_retired_alternative_specific_constants_N                           |      |

    **coefficients.csv**

    | coefficient_name                                          | value         | constrain |
    | :-------------------------------------------------------- | :------------ | :-------- |
    | util_full_time_worker_alternative_specific_constants_M    | 0.885080091   | F         |
    | util_full_time_worker_alternative_specific_constants_N    | 0.531583624   | F         |
    | util_part_time_worker_alternative_specific_constants_M    | -0.920808727  | F         |
    | util_part_time_worker_alternative_specific_constants_N    | 1.117988879   | F         |
    | util_university_student_alternative_specific_constants_M  | 1.898468936   | F         |
    | util_university_student_alternative_specific_constants_N  | -0.380144113  | F         |
    | util_non_working_adult_alternative_specific_constants_M   | -4.352        | F         |
    | util_non_working_adult_alternative_specific_constants_N   | -0.332324197  | F         |
    | util_retired_alternative_specific_constants_M             | -7.499        | F         |
    | util_retired_alternative_specific_constants_N             | -1.143572039  | F         |

    Then this script is here to help you. :)
    """
    )
    return


@app.cell
def _(spec_file):
    spec_file
    return


@app.cell
def _():
    ## Your input spec
    return


@app.cell
def _(pl, spec_file):
    input_spec = pl.read_csv(
        spec_file.value[0].contents
    )
    input_spec
    return (input_spec,)


@app.cell
def _(mo):
    mo.md(r"""Added the 'Label' column by converting the 'Description' column to underscore case and ensured there were no duplicate names.""")
    return


@app.cell
def _(
    convert_to_underscore_case,
    input_spec,
    pl,
    uniquify_string_list_with_numbering,
):
    label = convert_to_underscore_case(input_spec["Description"].to_list())
    label = uniquify_string_list_with_numbering(label)
    spec = input_spec.with_row_index().with_columns(Label=pl.concat_str(pl.lit("util_"), pl.Series(label)))
    spec
    return (spec,)


@app.cell
def _(pl, spec):
    choice_cols = [
        x for x in spec.columns if x not in ["Label", "Description", "Expression", "index"]
    ]

    coefficients = (
        spec.select(["index", "Label"] + choice_cols)
        .unpivot(index=["index", "Label"])
        .with_columns(
            coefficient_name=pl.concat_str(pl.col("Label"), pl.lit("_"), pl.col("variable")),
            constrain=pl.when(
                (pl.col("value") == -999)
                | (pl.col("value") == 0)
                | (pl.col("Label").str.contains("calibration_constant"))
            )
            .then(pl.lit("T"))
            .otherwise(pl.lit("F")),
        )
    )
    return choice_cols, coefficients


@app.cell
def _(mo):
    mo.md(r"""## Here's your new specification file""")
    return


@app.cell
def _(choice_cols, coefficients, pl, spec):
    final_spec = (
        coefficients.filter(~pl.col("value").is_null())
        .pivot("variable", index="Label", values="coefficient_name")
        .join(spec.select("index", "Label", "Description", "Expression"), on="Label")
        .sort("index")
        .select(["Label", "Description", "Expression"] + choice_cols)
    )

    final_spec
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Here's your new specification file
    All coefficients with value equal to -999 or 0 will have 'T' as their constrain.
    """
    )
    return


@app.cell
def _(coefficients, pl):
    final_coefficients = coefficients.sort("index").select("coefficient_name", "value", "constrain").filter(~pl.col("value").is_null())
    final_coefficients
    return


if __name__ == "__main__":
    app.run()
