# -*- coding: utf-8 -*-
"""streamlit_altair.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KiJCGzPr79u2mN7nXBz-smug7tEclhJE
"""

#!pip install -q streamlit

import streamlit as st

import altair as alt
import pandas as pd

# Sample monthly Stock data (GOOG, APPL, AMZN, IBM, MSFT) from 2004 to 2010
from vega_datasets import data

@st.cache_data # Streamlit will only download the data once since the data will be saved in a cache

def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source

def main():
  stock_data = get_data()
  st.title("Streamlit with altair")

  # Events in altair
  hover = alt.selection_single(
      fields=["date"],
      nearest=True,
      on="mouseover",
      empty="none",
  )

  lines = (
      alt.Chart(stock_data, title="Evolution of stock prices")
      .mark_line()
      .encode(
          x="date",
          y="price",
          color="symbol",
      )
  )

  points = lines.transform_filter(hover).mark_circle(size=65)

  tooltips = (
      alt.Chart(stock_data)
      .mark_rule()
      .encode(
          x="yearmonthdate(date)",
          y="price",
          opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
          tooltip=[
              alt.Tooltip("date", title="Date"),
              alt.Tooltip("price", title="Price (USD)"),
          ],
      )
      .add_selection(hover)
  )

  # Combine the lines, points, and tooltips into a single chart.
  data_layer = lines + points + tooltips

  # Build the annotation layer
  ANNOTATIONS = [
      ("Sep 01, 2007", 450, "🙂", "Something's going well for GOOG & AAPL."),
      ("Nov 01, 2008", 220, "🙂", "The market is recovering."),
      ("Dec 01, 2007", 750, "😱", "Something's going wrong for GOOG & AAPL."),
      ("Dec 01, 2009", 680, "😱", "A hiccup for GOOG."),
  ]
  annotations_df = pd.DataFrame(
      ANNOTATIONS, columns=["date", "price", "marker", "description"]
  )
  annotations_df.date = pd.to_datetime(annotations_df.date)

  annotation_layer = (
      alt.Chart(annotations_df)
      .mark_text(size=20, dx=-10, dy=0, align="left")
      .encode(x="date:T", y=alt.Y("price:Q"), text="marker", tooltip="description")
  )

  # Define the combined chart.
  combined_chart = data_layer + annotation_layer
  # enable panning and zooming
  # combined_chart = (data_layer + annotation_layer).interactive()

  # Display the chart in Streamlit.
  st.altair_chart(combined_chart, use_container_width=True)

if __name__ == "__main__":
    main()
