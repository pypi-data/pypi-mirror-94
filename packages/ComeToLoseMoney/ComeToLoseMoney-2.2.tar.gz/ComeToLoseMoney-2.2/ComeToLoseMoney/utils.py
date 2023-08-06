import pendulum
from .CustomExceptions import DateFormatException


class Date(object):
    @staticmethod
    def range(start_date: str, end_date: str, format="YYYYMMDD", units="days") -> list:
        """[summary]

        Args:
            start_date (str): [date format YYYYMMDD]
            end_date (str): [date format YYYYMMDD]  
            format (str): [the output format]         
            units (str): [
                Supported units for range() are: years, months, weeks, days, hours, minutes and seconds
            ]
        Returns:
            list: [a list of the date from start_date to end_date]
        """
        if len(start_date)!=8 or len(end_date)!=8:
            raise DateFormatException(f"Wrong date format, the standard format is YYYYMMDD, but we got {start_date} and {end_date}")
        input_format: str = "YYYYMMDD"
        start_: pendulum.datetime = pendulum.from_format(start_date, input_format)
        end_: pendulum.datetime =  pendulum.from_format(end_date, input_format)
        period_ = pendulum.period(start_, end_)
        return [dt.format(format) for dt in period_.range(units)]


if __name__ == "__main__":
    print(Date.range(start_date = "20200101", end_date="2020123"))