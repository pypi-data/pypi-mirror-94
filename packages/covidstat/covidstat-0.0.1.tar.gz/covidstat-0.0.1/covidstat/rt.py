import pandas as pd
import numpy as np
import scipy.stats
import datetime

class CovidStat:
    
    def __init__(self, shape=1.87, scale=3.57, interval=14, ndays_cov=6.6, ndays_cov_err=1.88):
        self.SHAPE = shape
        self.SCALE = scale
        self.INTERVAL = interval
        self.NDAYS_COV = ndays_cov
        self.NDAYS_COV_ERR = ndays_cov_err
            
    def __date_range(self, start_date, end_date):
        sdate = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        edate = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        delta = edate - sdate

        date_range = []
        for i in range(delta.days + 1):
            day = sdate + datetime.timedelta(days=i)
            date_range.append(day.date())
        
        return date_range
        
    def estimate_R(self, daily_cases, start_date, end_date):
        x = list(range(self.INTERVAL))
        y = np.convolve(np.clip(daily_cases, 0, None), np.ones(self.INTERVAL) / self.INTERVAL, mode='valid')
        y = np.concatenate((np.full(self.INTERVAL - 1, np.nan), y))
        y = np.where(y == 0, np.nan, y)
        y = np.log(y)
        
        dat, err = np.full(len(y), np.nan), np.full(len(y), np.nan)
        for i in range(self.INTERVAL, len(daily_cases)):
            dat[i], _, _, _, err[i] = scipy.stats.linregress(x, y[i - self.INTERVAL:i])
            
        rt_covidstat = lambda x: (1.0 + x * self.SCALE) ** self.SHAPE
        
        rt = rt_covidstat(dat)
        rt_err = rt * np.sqrt(((dat * self.NDAYS_COV_ERR)**2 + (err * self.NDAYS_COV)**2))
        rt_ci_high_68 = rt + rt_err + (((rt_err / rt)**2) * rt / 2)
        rt_ci_low_68  = rt - rt_err + (((rt_err / rt)**2) * rt / 2)
        rt_ci_high_95 = rt + (2 * rt_err) + (2 * ((rt_err / rt)**2) * rt)
        rt_ci_low_95  = rt - (2 * rt_err) + (2 * ((rt_err / rt)**2) * rt)
        date_range = self.__date_range(start_date, end_date)
        
        return pd.DataFrame(
            {
                'date': date_range,
                'mean': rt,
                'lower_68': rt_ci_low_68,
                'upper_68': rt_ci_high_68,
                'lower_95': rt_ci_low_95,
                'upper_95': rt_ci_high_95,
            }
        )