from typing import List, Tuple

class FinancialCalculator():
    '''
    The program calculates how long it takes for a person to become a millionaire by investing a certain amount every month.
    Furthermore, it gives her the option to say how long she would maintain this monthly investment rhythm and what her results would be.
    By default, a Brazil CDB (Bank Deposit Certificate) income tax (IR) discount is considered:
        Up to 180 n_day_counters: 22.5%
        From 181 to 360 n_day_counters: 20%
        From 361 to 720 n_day_counters: 17.5%
        More than 721 n_day_counters: 15%
    Note: IR is only applied to profit.
    IOF is disregarded because time periods tend to be long.
    It is assumed that there is no administration fee.
    Daily liquidity income is considered to occur only on business n_day_counters (weekends are not considered).
    '''
    def __init__(
            self, initial_value: float, monthly_invest: float,
            tax_rate: float, desired_final_value: float,
            years: float
            ) -> None:
        self.initial_value: float = initial_value
        self.monthly_invest: float = monthly_invest
        self.tax_rate: float = tax_rate/365
        self.desired_final_value: float = desired_final_value
        self.n_days: int = int(years*365)

    def calc_invest(
            self
            ) -> Tuple[List[int], List[float], Tuple[int, float]]:
        '''
        Calculates and returns the amount resulting from the monthly investment
        during the time period entered by the user.
        '''
        desired_x, desired_y, found = None, None, False
        curr_value = self.initial_value
        lst_years = [0]
        lst_values = [curr_value]
        for i in range(self.n_days):
            # Select the day to ensure it is a business day.
            if (i % 6 != 0 and i % 6 != 1) or i < 6:
                total_daily_profit = curr_value * self.tax_rate
                if i <= 180:
                    real_profit = total_daily_profit * 0.775
                elif 180 < i <= 360:
                    real_profit = total_daily_profit * 0.8
                elif 360 < i <= 720:
                    real_profit = total_daily_profit * 0.825
                elif i > 720:
                    real_profit = total_daily_profit * 0.85

                curr_value += real_profit
                if i % 29 == 0 and i != 0:
                    curr_value += self.monthly_invest
                
                if not found and curr_value >= self.desired_final_value:
                    found = True
                    desired_x, desired_y = round(i/365, 3), curr_value
                
                lst_years.append(round(i/365, 3)), lst_values.append(round(curr_value, 3))
        
        return (
            lst_years, lst_values,
            (desired_x, desired_y)
            )