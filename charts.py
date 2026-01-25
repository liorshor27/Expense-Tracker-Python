import plotly.express as px

def create_expense_pie_chart(category_totals):
    """
    Creates a pie chart from category totals.
    """
    # Convert the dictionary to lists required for the plot
    chart_data = {"Category": list(category_totals.keys()), 
                  "Amount": list(category_totals.values())}
    
    # Create the Pie Chart using Plotly Express
    fig = px.pie(
        chart_data, 
        values='Amount', 
        names='Category', 
        title='Expenses Distribution',
        color_discrete_sequence=px.colors.sequential.Greens_r 
    )
    
    # Update layout style:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#004d00") 
    )
    
    return fig
