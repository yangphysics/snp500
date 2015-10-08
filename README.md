S&P 500 
=======
Python code to get a list of S&P 500 companies upto arbitrary date (back to year 2000).
The input information needed is the Wikipedia page of List of S&P 500 companies 
[https://en.wikipedia.org/wiki/List_of_S%26P_500_companies].
And the required python packages are Pandas, Beautiful Soup and Urllib.

To test on the terminal:
```bash
    python snp500.py
```

To add in your python code:

```python
date = '2014-08-01'
print('\n TEST-II:\n   We want to get S&P 500 list on date {0}'.format(date))
snp = snp500(date=date)
print(' the first 20 items in the list: {0}\n'.format(snp[:20]))
```
