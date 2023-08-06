***************************
API reference
***************************

DataFrame & Series related functions
====================================

.. autosummary::
   :toctree: both

   trashpanda.add_blank_rows
   trashpanda.get_intersection
   trashpanda.get_unique_index_positions
   trashpanda.cut_after
   trashpanda.cut_before
   trashpanda.meld_along_columns
   trashpanda.remove_duplicated_indexes


Series related functions
========================

.. autosummary::
   :toctree: series

   trashpanda.add_missing_indexes_to_series
   trashpanda.cut_series_after_max
   trashpanda.find_index_of_value_in_series
   trashpanda.override_left_with_right_series

DataFrame related functions
===========================

.. autosummary::
   :toctree: dataframe

   trashpanda.add_columns_to_dataframe
   trashpanda.cut_dataframe_after_max
   trashpanda.meld_along_column
   trashpanda.override_left_with_right_dataframe