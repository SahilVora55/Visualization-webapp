import streamlit as st
import pandas as pd
import plotly.express as px

# Define a function to plot different graphs between columns
def plot_graphs(df, x_cols, y_cols, graph_type, plot_size):
    fig = px.line(df, x=x_cols, y=y_cols) if graph_type == "line" else px.scatter(df, x=x_cols, y=y_cols)
    if graph_type == "line-scatter":
        fig = px.scatter(df, x=x_cols, y=y_cols)
        fig.add_trace(px.line(df, x=x_cols, y=y_cols).data[0])
    fig.update_layout(width=plot_size[0], height=plot_size[1])
    st.plotly_chart(fig)

# Define a function to plot a boxplot of the selected columns
def plot_boxplot(df, column, plot_size):
    fig = px.box(df, y=column)
    fig.update_layout(width=plot_size[0], height=plot_size[1])
    st.plotly_chart(fig)

# Create a Streamlit app
st.title("Data Visualization App")

# Upload the data
uploaded_file = st.file_uploader("Choose a file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display the dataframe
    st.write(df)

    # Select the columns to plot
    st.sidebar.subheader('Select Plot Parameters')
    x_cols = st.sidebar.selectbox("Select the X-axis column(s)", df.columns)
    y_cols = st.sidebar.multiselect("Select the Y-axis column(s)", df.columns)

    # Select the type of graph to plot
    graph_type = st.sidebar.selectbox("Select the type of graph", ["line", "scatter", "line-scatter"])
    
    # Select the plot size
    plot_size_x = st.sidebar.slider("Select the width of plot", 100, 1000, 700)
    plot_size_y = st.sidebar.slider("Select the height of plot", 100, 1000, 450)
    plot_size = (plot_size_x, plot_size_y)

    # Plot the graph
    if st.sidebar.button("Plot Graph"):
        plot_graphs(df, x_cols, y_cols, graph_type, plot_size)

    # Select the column to plot a boxplot
    st.sidebar.subheader('Boxplot')
    boxplot_col = st.sidebar.selectbox("Select the column for boxplot", df.columns)

    # Plot the boxplot
    if st.sidebar.button("Plot Boxplot",):
        plot_boxplot(df, boxplot_col, plot_size)
