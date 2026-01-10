import plotly.express as px

def create_expense_pie_chart(category_totals):
    """
    Generates a styled interactive pie chart for expense distribution.

    Args:
        category_totals (dict): A dictionary where keys are categories and values are amounts.

    Returns:
        plotly.graph_objects.Figure: The styled pie chart figure ready for rendering.
    """
    #Convert the dictionary to lists required for the plot
    chart_data = {"Category": list(category_totals.keys()), 
                  "Amount": list(category_totals.values())}
    
    #Create the Pie Chart using Plotly Express
    fig = px.pie(
        chart_data, 
        values='Amount', 
        names='Category', 
        title='Expenses Distribution',
        color_discrete_sequence=px.colors.sequential.Greens_r # הפלטה הירוקה שלנו
    )
    
    #Update layout style:
    #1. Set background to transparent to blend with the app's CSS theme
    #2. Set font color to match the app's dark green headers
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#004d00") 
    )
    
    return fig