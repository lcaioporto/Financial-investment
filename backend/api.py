from fastapi import FastAPI, Request, Form
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from financial_calculator import FinancialCalculator
from fastapi.responses import HTMLResponse
from utils import Utils

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

@app.get('/')
def root(request: Request):
    return templates.TemplateResponse(request=request, name="form_page.html")

@app.post('/submit')
def process_input(
    request: Request, initial_amount: str = Form(...), monthly_invest: str = Form(...),
    tax: str = Form(...), years: str = Form(...), desired_final_value: str = Form(...)
    ):
    initial_amount = float(initial_amount)
    monthly_invest = float(monthly_invest)
    tax = float(tax)/100
    years = float(years)
    desired_final_value = float(desired_final_value)
    print("Initial amount", initial_amount)
    print("Monthly investment", monthly_invest)
    print("Tax", tax)
    print("Years", years)
    print("Desired final", desired_final_value)

    finance_calc = FinancialCalculator(
        initial_amount, monthly_invest, tax, desired_final_value, years
        )
    lst_years, lst_values, des_pos = finance_calc.calc_invest()
    des_x, des_y = des_pos[0], des_pos[1]

    # Generate plot and get its HTML
    plot_div = Utils.get_plotly_html(
        x_data=lst_years, y_data=lst_values, title="Financial report",
        x_label="Year", y_label="Money", highlight_x=des_x,
        highlight_y=des_y
    )

    # Create the full HTML document
    response_html_content = f"""
    <html>
        <head>
            <title>Your finance plan</title>
            <link rel="stylesheet" href="static/style_graphic_res.css">
        </head>
        <body>
            {plot_div}
        </body>
    </html>
    """
    return HTMLResponse(content=response_html_content)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)