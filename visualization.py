import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import base64
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def plot_graphs(df, x_cols, y_cols, graph_type, plot_size):
    fig = px.line(df, x=x_cols, y=y_cols) if graph_type == "line" else px.scatter(df, x=x_cols, y=y_cols)
    if graph_type == "line-scatter":
        fig.add_trace(px.line(df, x=x_cols, y=y_cols).data[0])
    fig.update_layout(width=plot_size[0], height=plot_size[1], plot_bgcolor='#FFFFFF', paper_bgcolor='#F2F2F2',
                      xaxis=dict(showgrid=True, gridcolor='#DDDDDD', linecolor='#999999', linewidth=1,
                                 mirror=True, title_font=dict(size=14)),
                      yaxis=dict(showgrid=True, gridcolor='#DDDDDD', linecolor='#999999', linewidth=1,
                                 mirror=True, title_font=dict(size=14)),
                      font=dict(size=12),
                      margin=dict(t=50, b=50, r=50, l=50),
                      hoverlabel=dict(bgcolor='#FFFFFF', font_size=12, font_family="Arial"))

    st.plotly_chart(fig)

    # Download button
    filename = f"{graph_type}.png"
    data = fig.to_image(format="png")
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">Download Plot</a>'
    st.markdown(href, unsafe_allow_html=True)

def plot_boxplot(df, column, plot_size):
    fig = px.box(df, y=column)
    fig.update_layout(width=plot_size[0], height=plot_size[1], plot_bgcolor='#FFFFFF', paper_bgcolor='#F2F2F2',
                      xaxis=dict(showgrid=False, zeroline=False, linecolor='#999999', linewidth=1,
                                 mirror=True, tickfont=dict(size=12)),
                      yaxis=dict(showgrid=True, gridcolor='#DDDDDD', linecolor='#999999', linewidth=1,
                                 mirror=True, tickfont=dict(size=12)),
                      font=dict(size=12),
                      margin=dict(t=50, b=50, r=50, l=50),
                      hoverlabel=dict(bgcolor='#FFFFFF', font_size=12, font_family="Arial"))

    st.plotly_chart(fig)

    # Download button
    filename = "Boxplot.png"
    data = fig.to_image(format="png")
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">Download Plot</a>'
    st.markdown(href, unsafe_allow_html=True)

def plot_histogram(df, column, plot_size):
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    fig = px.histogram(df, x=column, nbins=30, marginal="rug", opacity=0.7, color_discrete_sequence=["#FCB711"])
    fig.update_layout(width=plot_size[0], height=plot_size[1], plot_bgcolor='#FFFFFF', paper_bgcolor='#F2F2F2',
                      xaxis=dict(showgrid=True, gridcolor='#DDDDDD', linecolor='#999999', linewidth=1,
                                 mirror=True, title_font=dict(size=14)),
                      yaxis=dict(showgrid=True, gridcolor='#DDDDDD', linecolor='#999999', linewidth=1,
                                 mirror=True, title_font=dict(size=14)),
                      font=dict(size=12),
                      margin=dict(t=50, b=50, r=50, l=50),
                      hoverlabel=dict(bgcolor='#FFFFFF', font_size=12, font_family="Arial"))
    st.plotly_chart(fig)
    
    # Download button
    filename = "Histogram.png"
    data = fig.to_image(format="png")
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">Download Plot</a>'
    st.markdown(href, unsafe_allow_html=True)
  

st.set_page_config(page_title="Data Visualization Web App", page_icon=":bar_chart:", layout="wide")

uploaded_file = st.file_uploader("Choose a file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if st.checkbox('**Display data**'):
        st.dataframe(df, height=220)
    col1, col_extra, col2 = st.columns([6,1,9])    
    with col1:
        graph_type = st.selectbox("**Select the type of graph**", ["line", "scatter", "line-scatter", "boxplot", "histplot","Heatmap (correlation metrix)"])
        if graph_type in ["boxplot", "histplot"]:
            cols = st.selectbox("Select the column to plot", df.columns)
        if graph_type in ["line", "scatter"]:
            col3, col4 = st.columns(2)
            with col3:
                # Select X-axis column
                x_cols = st.selectbox("Select the X-axis column(s)", df.columns)
            with col4:
                # Select Y-axis column(s)
                y_cols = st.multiselect("Select the Y-axis column(s)", df.columns)
        if graph_type in ["line-scatter"]:
            col7, col8 = st.columns(2)
            with col7:
                # Select X-axis column
                x_cols = st.selectbox("Select the X-axis column(s)", df.columns)
            with col8:
                # Select Y-axis column(s)
                default_y_cols = [df.columns[1]]
                y_cols = st.multiselect("Select the Y-axis column(s)", df.columns, default=default_y_cols)

        if graph_type in ["Heatmap (correlation metrix)"]:            
            # Compute correlation matrix
            corr_matrix = df.corr()

            # Get correlation values for 'Rate of Penetration'
            ROP = st.selectbox('Please select the column that contains the values for the **rate of penetration**.',df.columns)
            corr_values = corr_matrix[ROP]

            # Select columns with correlation greater than 0.25
            suggested_cols = corr_values[(corr_values > 0.25)|(corr_values < -0.25)].drop(ROP)

            # Display the suggested columns
            st.markdown('<p style="color: green"><b>Suggested columns which has good correlation with Rate of Penetration:</b></p>', unsafe_allow_html=True)
            st.write(suggested_cols)



        col5,col6 = st.columns(2)
        with col5:
            plot_size_x = st.slider("Select the width of plot", 100, 1000, 700)
        with col6:
            plot_size_y = st.slider("Select the height of plot", 100, 1000, 450)
        plot_size = (plot_size_x, plot_size_y)

        Graph = st.checkbox("**Display Graph**",True)


    with col2:
        st.write('<h3>Graph:</h3>', unsafe_allow_html=True)
        if Graph:
            if graph_type in ["line", "scatter", "line-scatter"]:
                plot_graphs(df, x_cols, y_cols, graph_type, plot_size)
            elif graph_type == "boxplot":
                plot_boxplot(df, cols, plot_size)
            elif graph_type == "histplot":
                plot_histogram(df, cols, plot_size)
            else:
                # Display heatmap
                fig, ax = plt.subplots()
                sns.heatmap(df.corr(), cmap='YlGnBu', annot=True, ax=ax)
                st.pyplot(fig)

                # Download button
                filename = "Heatmap.png"
                canvas = FigureCanvas(fig)
                png_output = BytesIO()
                canvas.print_png(png_output)
                data = png_output.getvalue()
                b64 = base64.b64encode(data).decode()
                href = f'<a href="data:file/png;base64,{b64}" download="{filename}">Download Plot</a>'
                st.markdown(href, unsafe_allow_html=True)


    # add vertical line between the columns
    st.markdown("""<style> .stHorizontal { display: none; } </style>""", unsafe_allow_html=True)
    col1.markdown("""<hr style='height: 2px; background-color: #8c8c8c;'></hr>""", unsafe_allow_html=True)
