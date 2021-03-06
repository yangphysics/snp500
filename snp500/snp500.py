import pandas as pd
from bs4 import BeautifulSoup
import urllib

def print_symbol(sl):
    ''' print S&P 500 list in a table form (each row contains 20 symbols)'''
    print('*'*120)
    print('  '),
    for i,s in enumerate(sl):
        print('{0:5}'.format(s)),
        if (i+1)%20 == 0: print('\n  '),
    print('\n'+'*'*120)

class SNP500:
    def __init__(self, is_print=False):
        self.is_print = is_print
        #  read in webpage and create the BeautifulSoup object
        web = urllib.urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        self.soup = BeautifulSoup(web.read(), 'html.parser')
        
        #  get changing history of SNP500 list (available only back to 2000)
        self.dif = self.snp500_change_his()

        #  get current version of SNP500 list and put ticker symbols in snp0
        self.snp500 = self.get_snp500_current()
        self.snp0 = list(self.snp500[0]) 
        self.update()
        
    def get_snp500_current(self):
        #  readin table containing the S&P 500 company list
        loc = self.soup.find(id="S.26P_500_Component_Stocks")
        table = loc.parent.findNext('table')
        rows = table.find_all('tr')[1:]  #  ignore the first row (blank line)

        #  convert table in web-format to list
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values

        #  convert the list to the Pandas dataframe
        snp500 = pd.DataFrame.from_records(data)
        return snp500
    
    def snp500_change_his(self):
        #  readin table containing the S&P 500 company changing history list
        loc = self.soup.find(id="Recent_and_announced_changes_to_the_list_of_S.26P_500_Components")
        table2 = loc.parent.findNext('table')
        rows2 = table2.find_all('tr')[2:]  #  ignore the first two rows (blank and head lines)

        #  convert table in web-format to list
        data2 = []
        for idx,row in enumerate(rows2):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            # pick up cases who share the dates (signature: missing date+month+year)
            if '20' not in cols[0]:
                #print(idx,len(cols),cols[0])
                data2.append([data2[idx-1][0]] + [ele for ele in cols]) 
            else:
                data2.append([pd.to_datetime(cols[0])] + [ele for ele in cols[1:]]) 

        #  convert the list to the Pandas dataframe
        dif = pd.DataFrame.from_records(data2)
        return dif
    
        
    #  get up-to-'date' S&P 500 list
    def update(self):
        #   the current list might not contain the very recent change
        #   here we check this, if it is the case, we apply recent changes
        N = 5  #  check first 5 items in the changing list
        ds = self.dif.ix[:N,[0,1,3]]
        
        snp = self.snp0
        #  apply the changes on the newest list
        for idx in range(N):
            s_new = ds.ix[idx,1]
            s_old = ds.ix[idx,3]
            if s_new not in snp:
                if self.is_print: print(' The current S&P 500 is not really up-to-date!!!')
                if s_old == '': 
                    if self.is_print: print('  Add  {0:5} '.format(s_new))
                    snp.append(s_new) 
                    assert(s_new in snp)
                else:
                    if s_new != s_old:  #  avoid cases like GAS -> GAS
                        if self.is_print: print('  Replace {0:5} by {1:5}'.format(s_old,s_new))
                        snp = [s_new if x==s_old else x for x in snp]
                        assert(s_new  in snp)
                        assert(s_old not in snp)

    def benchmark(self):
        #   bench-mark to the list extracted from 
        #      http://marketcapitalizations.com/historical-data/historical-components-sp-500/
        #   since data only provided for Jan. 1 for each year from 2008 to 2015,
        #   we will only do the five bench-mark test.
        #years = range(2008, 2016)
        years = [2012]
        #   read in the bench-mark data
        snp_benchmark_all = pd.read_csv('./data/snp500_benchmark.csv')
        #   do the bench-mark
        for year in years:
            yr = str(year)
            snp_bm = list(snp_benchmark_all['Ticker'][snp_benchmark_all[yr].notnull()])
            #  'TGNA','ZBH', 'WRK', 'FOX', 'CMCSK' and 'NWS' are missing from this list?? add them
            snp_bm.append('TGNA')
            snp_bm.append('ZBH')
            snp_bm.append('WRK')
            snp_bm.append('FOX')
            snp_bm.append('CMCSK')
            snp_bm.append('NWS')
            if year < 2015:
                snp_bm = ['GOOG' if x=='GOOGL' else x for x in snp_bm]   #   'GOOG' is the old name
            snp_bm = sorted([x.replace('.','-') for x in snp_bm])
            snp = self.__call__(yr+'-01-01')
            print(' difference ({0}): {1}'.format(yr, list(set(snp)-set(snp_bm))))
            print('')
            print('  **snp_bm[{0}]** ==> '.format(len(snp_bm)))
            print_symbol(snp_bm)
            print('\n')
            print('  **snp[{0}]**    ==> '.format(len(snp)))
            print_symbol(snp)
            print('\n')
            #assert(len(snp)==len(snp_bm))
            #assert(snp==snp_bm)

    
    #  get up-to-'date' S&P 500 list
    def __call__(self, date='2015-09-15'):
        snp = [x for x in self.snp0]
        ds = self.dif.ix[:,[0,1,3]]

        snp.append('GCI')
        snp.append('MWV')
        snp.append('ZMH')
        #  KRFT is delisted on '2015-07-02', this is not shown up in the Wikipedia page
        #  add it manually
        if date < '2015-07-02':
            snp.append('KRFT')
        #  it looks "KHC" is on list on '2015-07-06', so remove it manully if needed
        if date < '2015-07-02':
            snp = [x for x in snp if x!='KHC']

        #  apply the changes on the newest list
        N = len(ds[ds[0]>=date])
        for idx in range(N):
            date = ds.ix[idx,0]
            s_new = ds.ix[idx,1]
            s_old = ds.ix[idx,3]
            if s_old == '': 
                if self.is_print: 
                    print('  {0:3}  ** Delete  {1:5} on  {2}'.format(idx,s_new,date.strftime('%m-%d-%Y')))
                snp = [x for x in snp if x!=s_new]
                assert(s_new not in snp)
            else:
                if s_new != s_old:  #  avoid GAS -> GAS case
                    if s_new == 'JOYG': s_new = 'JOY'   #  another bug of this Wikipedia page
                    if self.is_print: 
                        print('  {0:3}  replace {1:5} by {2:5} on  {3}'.format(idx,s_new,s_old,date.strftime('%m-%d-%Y')))
                    snp = [s_old if x==s_new else x for x in snp]
                    #if s_old=='AYE': print(sorted(snp))
                    assert(s_new not in snp)
                    assert(s_old in snp)
        return sorted(snp)
    
    
    
def bench_mark():
    #  create the SNP500 object
    print('')
    snp500 = SNP500(is_print=True)
    snp500.benchmark()
    

def test():
    #  create the SNP500 object
    print('')
    snp500 = SNP500(is_print=True)

    date1 = '2015-09-15'
    print('\n\n'+'='*60)
    print('   TEST-I:\n   We want to get S&P 500 list on date {0}'.format(date1))
    print('='*60)
    snp1 = snp500(date=date1)
    print('\n  **S&P_list[{0}]** ==> '.format(len(snp1)))
    print_symbol(snp1)

    date2 = '2014-08-01'
    print('\n\n'+'='*60)
    print('   TEST-II:\n   We want to get S&P 500 list on date {0}'.format(date2))
    print('='*60)
    snp2 = snp500(date=date2)
    print('\n  **S&P_list[{0}]** ==> '.format(len(snp2)))
    print_symbol(snp2)

if __name__ == '__main__':
    test()
    #bench_mark()



