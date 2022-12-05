import streamlit as st
import requests
import base64
from io import BytesIO
import pandas as pd
from datetime import datetime



@st.cache(suppress_st_warning=True)
def format_number(number):
    return f"{number:,}"


@st.cache(suppress_st_warning=True)
class IEXStock:
    def __init__(self, token, symbol, environment='production'):
        if environment == 'production':
            self.BASE_URL = 'https://cloud.iexapis.com/v1'
        else:
            self.BASE_URL = 'https://sandbox.iexapis.com/v1'

        self.token = token
        self.symbol = symbol

    @st.cache(suppress_st_warning=True)
    def get_logo(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/logo?token={self.token}"
        r = requests.get(url)
        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_quote(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/quote?token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_company_info(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/company?token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_company_news(self, last=10):
        url = f"{self.BASE_URL}/stock/{self.symbol}/news/last/{last}?token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_stats(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/advanced-stats?token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_fundamentalsquarterly(self, period='quarterly', last=4):
        url = f"{self.BASE_URL}/time-series/fundamentals/{self.symbol}/{period}?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_fundamentalsannual(self, period='annual', last=4):
        url = f"{self.BASE_URL}/time-series/fundamentals/{self.symbol}/{period}?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_fundamentalsannual1(self, period='annual', last=4):
        url = f"{self.BASE_URL}/time-series/FUNDAMENTAL_VALUATIONS/{self.symbol}/{period}?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_dividends(self, range='5y'):
        url = f"{self.BASE_URL}/stock/{self.symbol}/dividends/{range}?token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_institutional_ownership(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/institutional-ownership?token={self.token}"
        r = requests.get(url)

        return r.json()

    @st.cache(suppress_st_warning=True)
    def get_insider_transactions(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/insider-transactions?token={self.token}"
        r = requests.get(url)

        return r.json()

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download csv file</a>' # decode b'abc' => abc

STYLE = """
<style>
img {
    max-width: 150%;
}
</style>
"""

def main():

    access = 0
    #placeholder1 = st.sidebar.empty()
    #input2 = placeholder1.text_input('API_Key:')

    placeholder = st.empty()
    if access == 0:
        input1 = st.empty()
        t = input1.text_input('Key:', key=0)

    if (t == ''):
        if t != "":
            input1.empty()
        st.markdown(STYLE, unsafe_allow_html=True)
        symbol = st.sidebar.text_input("Symbol", value='MSFT')
        screen = st.sidebar.selectbox("View", ('Overview', 'News', 'Fundamentals', 'UT Analysis', 'Comparison Analysis'), index=0)
        #IEX_TOKEN = input2
        IEX_TOKEN = ''
        stock = IEXStock(IEX_TOKEN, symbol)
        #input2 = placeholder1.text_input('Login Successful', value='', key=1)
        access = 1
        tempSymbol = symbol

    if access == 1:
        st.title(screen)
        st.write('Ticker: ', symbol)

        if screen == 'Overview':

            logo = stock.get_logo()

            print("getting company from api, and then storing it in cache")
            company = stock.get_company_info()
            col1, col2 = st.columns([1, 4])

            with col1:
                st.image(logo['url'])

            with col2:
                st.subheader(company['companyName'])
                st.write(company['industry'])
                st.subheader('Description')
                st.write(company['description'])
                st.subheader('CEO')
                st.write(company['CEO'])

        if screen == 'News':


            news = stock.get_company_news()
            for article in news:
                st.subheader(article['headline'])
                dt = datetime.utcfromtimestamp(article['datetime'] / 1000).isoformat()
                st.write(f"Posted by {article['source']} at {dt}")
                st.write(article['url'])
                st.write(article['summary'])
                st.image(article['image'])




        if screen == 'UT Analysis':

            quarter = stock.get_fundamentalsquarterly('quarterly')
            annual = stock.get_fundamentalsquarterly('annual')
            annualArrayYear = [len(annual)]
            annualArrayRevenue = [len(annual)]
            annualArrayNetIncome = [len(annual)]
            for annualData in annual:
                annualArrayYear.append(annualData['fiscalYear'])
                annualArrayRevenue.append(annualData['revenue'] / 1000000)
                annualArrayNetIncome.append(annualData['incomeNet'] / 1000000)


            quote = stock.get_quote()
            quoteArrayPE = [len(quote)]
            PE = quote['peRatio']

            st.write('')
            st.write('')
            st.write('Key Financial Metrics (in millions)')
            st.write('')
            col1_1, col2_1, col3_1 = st.columns([2, 2, 2])
            with col1_1:


                net_income = annualArrayNetIncome[1]
                st.write('Valuation Overview (LFY)')
                #d = {"": [0, PE, net_income]}
                #df = pd.DataFrame(d, index=['EV/Sales', 'P/E', 'Net Income'])
                #st.dataframe(df)

            with col3_1:

                st.write('Equity Overview:')

            annual = stock.get_fundamentalsannual1('annual')
            #st.write(annual)

            annualArrayPE = [len(annual)]
            annualArrayPrice = [len(annual)]
            annualArrayMC = [len(annual)]
            annualArrayEVOS = [len(annual)]
            annualArrayEV = [len(annual)]

            for x in annual:
                annualArrayPE.append(round(x['pToE'], 3))
                annualArrayPrice.append(x['priceAccountingPeriodEnd'])
                annualArrayMC.append(round(x['marketCapPeriodEnd']/1000000))
                annualArrayEVOS.append(round(x['evToSales'], 3))
                annualArrayEV.append(round(x['enterpriseValue'] / 1000000))



            col1_2, col2_2, col3_2, col4_2, col5_2 = st.columns([1, 1, 2, 1, 1])
            with col1_2:
                st.write('EV/Sales:')
                st.write('P/E:')
                st.write('Net Income:')
            with col2_2:
                st.write(annualArrayEVOS[1])
                st.write(annualArrayPE[1])
                st.write(annualArrayNetIncome[1])
            with col4_2:
                st.write('Price:')
                st.write('M.Cap:')
                st.write('EV:')
            with col5_2:
                st.write(annualArrayPrice[1])
                st.write(annualArrayMC[1])
                st.write(annualArrayEV[1])
            st.write('')
            st.write('Revenue Growth:')

            col1_3, col2_3, col3_3, col4_3 = st.columns(4)
            with col1_3:
                st.write('Fiscal Year:')
                st.write('Total Revenue:')
                st.write('Growth:')
            with col2_3:
                st.write(annualArrayYear[3])
                st.write(annualArrayRevenue[3])

                percentChange = (annualArrayRevenue[3] - annualArrayRevenue[4]) / annualArrayRevenue[4]
                percentChange = percentChange * 100
                percentChange = round(percentChange, 2)
                st.write((percentChange), '%')
                percent3 = str(percentChange) + '%'

            with col3_3:
                st.write(annualArrayYear[2])
                st.write(annualArrayRevenue[2])

                percentChange = (annualArrayRevenue[2] - annualArrayRevenue[3]) / annualArrayRevenue[3]
                percentChange = percentChange * 100
                percentChange = round(percentChange, 2)
                st.write((percentChange), '%')
                percent2 = str(percentChange) + '%'

            with col4_3:
                st.write(annualArrayYear[1])
                st.write(annualArrayRevenue[1])

                percentChange = (annualArrayRevenue[1] - annualArrayRevenue[2]) / annualArrayRevenue[2]
                percentChange = percentChange * 100
                percentChange = round(percentChange, 2)
                st.write((percentChange), '%')
                percent1 = str(percentChange) + '%'

            st.write('')
            st.write('')
            ticker = "Ticker: " + symbol
            data = [['', '', '', '', '', ''],
                    ['Key Financial Metrics (in millions)', '', '', '', '',''],
                    ['', '', '', '', ''],
                    ['Valuation Overview (LFY)', '', '', '', '',''],
                    ['EV/Sales:', annualArrayEVOS[1], '','Price:',annualArrayPrice[1]],
                    ['P/E:', annualArrayPE[1], '', 'M.Cap:', annualArrayMC[1]],
                    ['Net Income:', annualArrayNetIncome[1], '', 'EV:',annualArrayEV[1]],
                    ['', '', '', '', '',''],
                    ['', '', '', '', '',''],
                    ['Revenue Growth:', '', '', '', '',''],
                    ['Fiscal Year:', annualArrayYear[3], annualArrayYear[2], annualArrayYear[1], '',''],
                    ['Total Revenue:', annualArrayRevenue[3], annualArrayRevenue[2], annualArrayRevenue[1], '',''],
                    ['Growth:', percent3, percent2, percent1, '',''],]
            df = pd.DataFrame(data, columns=['UT Analysis', ticker, '', '', '', ''], dtype=float)
            downloadlink = st.empty()
            downloadlink.markdown(get_table_download_link(df), unsafe_allow_html=True)


                # colInput1 = st.empty()
                # colInput1
                # if next == 1:
                #     input4 = st.empty()
                #     t1 = input4.text_input("Add Ticker", value="", key=3)
                # if t1 != "":
                #     input4.empty()


                    #with col1_4:


            #placeholder = st.empty()
            #if not st.checkbox("Run comparative ana"):
                #downloadLink.markdown(get_table_download_link(df), unsafe_allow_html=True)

        numAdded = 0
        start = 0

        if screen == 'Comparison Analysis':



            input2 = st.empty()
            col1_4, col2_4, col3_4, col4_4, col5_4 = input2.columns(5)
            with col3_4:
                ticker1 = st.empty()
                t1 = ticker1.text_input("Add Ticker", value="", key=2)
            with col4_4:
                ticker2 = st.empty()
                t2 = ticker2.text_input("Add Ticker", value="", key=3)
            with col5_4:
                ticker3 = st.empty()
                t3 = ticker3.text_input("Add Ticker", value="", key=4)

            st.write('')
            st.write('')
            ticker = "Ticker: " + symbol
            data = [['', '', '', '', '', ''],
                    ['Key Financial Metrics (in millions)', '', '', '', '', ''],
                    ['Valuation and Margins: (LFY)', '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['Symbol', 'row1', '', '', '', ''],
                    ['Price:', '', '', '', ''],
                    ['EV/ Sales:', '', '', '', ''],
                    ['EV/EBITDA:', '', '', '', ''],
                    ['Market Cap', '', '', '', '', ''],
                    ['P/E', '', '', '', '', ''],
                    ['Gross Margin', '', '', '', '', ''],
                    ['EBITDA Margin', '', '', '', '', ''],
                    ['Net Income', '', '', '', '', '']]
            df = pd.DataFrame(data, columns=['Comparison Analysis', ticker, '', '', '', ''], dtype=float)



            st.write('Valuation and Margins (LFY):')
            st.write('')
            input0 = st.empty()
            col1_5, col2_5, col3_5, col4_5, col5_5 = input0.columns(5)
            with col1_5:
                if start == 0:
                    st.write('Symbol:')
                    st.write('Price:')
                    st.write('EV/ Sales:')
                    st.write('EV/EBITDA:')
                    st.write('Market Cap:')
                    st.write('P/E:')
                    st.write('Gross Margin:')
                    st.write('EBITDA Margin:')
                    st.write('Net Income:')

            with col2_5:
                symbol0 = getdata(IEX_TOKEN, symbol)

                start = 1
                dataComp = [['', '', '', '', '', ''],
                        ['Key Financial Metrics (in millions)', '', '', '', '', ''],
                        ['Valuation and Margins: (LFY)', '', '', '', ''],
                        ['', '', '', '', '', ''],
                        ['Symbol', symbol0[0], '', '', '', ''],
                        ['Price', symbol0[1], '', '', ''],
                        ['EV/ Sales', symbol0[2], '', '', ''],
                        ['EV/EBITDA', symbol0[3], '', '', ''],
                        ['Market Cap', symbol0[4], '', '', '', ''],
                        ['P/E', symbol0[5], '', '', '', ''],
                        ['Gross Margin', symbol0[6], '', '', '', ''],
                        ['EBITDA Margin', symbol0[7], '', '', '', ''],
                        ['Net Income', symbol0[8], '', '', '', '']]
                df = pd.DataFrame(dataComp, columns=['Comparison Analysis', ticker, '', '', '', ''], dtype=float)

            with col3_5:
                if t1:
                    symbol1 = getdata(IEX_TOKEN, t1)
                    dataComp = [['', '', '', '', '', ''],
                                ['Key Financial Metrics (in millions)', '', '', '', '', ''],
                                ['Valuation and Margins: (LFY)', '', '', '', ''],
                                ['', '', '', '', '', ''],
                                ['Symbol', symbol0[0], symbol1[0], '', '', ''],
                                ['Price', symbol0[1], symbol1[1], '', ''],
                                ['EV/ Sales', symbol0[2], symbol1[2], '', ''],
                                ['EV/EBITDA', symbol0[3], symbol1[3], '', ''],
                                ['Market Cap', symbol0[4], symbol1[4], '', '', ''],
                                ['P/E', symbol0[5], symbol1[5], '', '', ''],
                                ['Gross Margin', symbol0[6], symbol1[6], '', '', ''],
                                ['EBITDA Margin', symbol0[7], symbol1[7], '', '', ''],
                                ['Net Income', symbol0[8], symbol1[8], '', '', '']]
                    df = pd.DataFrame(dataComp, columns=['Comparison Analysis', ticker, '', '', '', ''], dtype=float)


            with col4_5:
                if t2:
                    symbol2 = getdata(IEX_TOKEN, t2)
                    dataComp = [['', '', '', '', '', ''],
                                ['Key Financial Metrics (in millions)', '', '', '', '', ''],
                                ['Valuation and Margins: (LFY)', '', '', '', ''],
                                ['', '', '', '', '', ''],
                                ['Symbol', symbol0[0], symbol1[0], symbol2[0], '', ''],
                                ['Price', symbol0[1], symbol1[1], symbol2[1], ''],
                                ['EV/ Sales', symbol0[2], symbol1[2], symbol2[2], ''],
                                ['EV/EBITDA', symbol0[3], symbol1[3], symbol2[3], ''],
                                ['Market Cap', symbol0[4], symbol1[4], symbol2[4], '', ''],
                                ['P/E', symbol0[5], symbol1[5], symbol2[5], '', ''],
                                ['Gross Margin', symbol0[6], symbol1[6], symbol2[6], '', ''],
                                ['EBITDA Margin', symbol0[7], symbol1[7], symbol2[7], '', ''],
                                ['Net Income', symbol0[8], symbol1[8], symbol2[8], '', '']]
                    df = pd.DataFrame(dataComp, columns=['Comparison Analysis', ticker, '', '', '', ''], dtype=float)

            with col5_5:
                if t3:
                    symbol3 = getdata(IEX_TOKEN, t3)
                    dataComp = [['', '', '', '', '', ''],
                                ['Key Financial Metrics (in millions)', '', '', '', '', ''],
                                ['Valuation and Margins: (LFY)', '', '', '', ''],
                                ['', '', '', '', '', ''],
                                ['Symbol', symbol0[0], symbol1[0], symbol2[0], symbol3[0], ''],
                                ['Price', symbol0[1], symbol1[1], symbol2[1], symbol3[1]],
                                ['EV/ Sales', symbol0[2], symbol1[2], symbol2[2], symbol3[2]],
                                ['EV/EBITDA', symbol0[3], symbol1[3], symbol2[3], symbol3[3]],
                                ['Market Cap', symbol0[4], symbol1[4], symbol2[4], symbol3[4], ''],
                                ['P/E', symbol0[5], symbol1[5], symbol2[5], symbol3[5], ''],
                                ['Gross Margin', symbol0[6], symbol1[6], symbol2[6], symbol3[6], ''],
                                ['EBITDA Margin', symbol0[7], symbol1[7], symbol2[7], symbol3[7], ''],
                                ['Net Income', symbol0[8], symbol1[8], symbol2[8], symbol3[8], '']]
                    df = pd.DataFrame(dataComp, columns=['Comparison Analysis', ticker, '', '', '', ''], dtype=float)

            downloadlink = st.empty()
            downloadlink.markdown(get_table_download_link(df), unsafe_allow_html=True)






        if screen == 'Fundamentals':

            stats = stock.get_stats()
            st.header('Ratios')
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('P/E')
                st.write(stats['peRatio'])
                st.subheader('Forward P/E')
                st.write(stats['forwardPERatio'])
                st.subheader('PEG Ratio')
                st.write(stats['pegRatio'])
                st.subheader('Price to Sales')
                st.write(stats['priceToSales'])
                st.subheader('Price to Book')
                st.write(stats['priceToBook'])
            with col2:
                st.subheader('Revenue')
                st.write(format_number(stats['revenue']))
                st.subheader('Cash')
                st.write(format_number(stats['totalCash']))
                st.subheader('Debt')
                st.write(format_number(stats['currentDebt']))
                st.subheader('200 Day Moving Average')
                st.write(stats['day200MovingAvg'])
                st.subheader('50 Day Moving Average')
                st.write(stats['day50MovingAvg'])

            fundamentals = stock.get_fundamentalsquarterly('quarterly')
            for quarter in fundamentals:
                st.header(f"Q{quarter['fiscalQuarter']} {quarter['fiscalYear']}")
                st.subheader('Filing Date')
                st.write(quarter['filingDate'])
                st.subheader('Revenue')
                st.write(format_number(quarter['revenue']))
                st.subheader('Net Income')
                st.write(format_number(quarter['incomeNet']))


def getdata(stock):
    quarter = stock.get_fundamentalsquarterly('quarterly')
    annual = stock.get_fundamentalsquarterly('annual')
    annualArrayYear = [len(annual)]
    annualArrayRevenue = [len(annual)]
    annualArrayNetIncome = [len(annual)]
    for annualData in annual:
        annualArrayYear.append(annualData['fiscalYear'])
        annualArrayRevenue.append(annualData['revenue'] / 1000000)
        annualArrayNetIncome.append(annualData['incomeNet'] / 1000000)

    quote = stock.get_quote()
    quoteArrayPE = [len(quote)]
    PE = quote['peRatio']

    annual = stock.get_fundamentalsannual1('annual')
    # st.write(annual)

    annualArrayPE = [len(annual)]
    annualArrayPrice = [len(annual)]
    annualArrayMC = [len(annual)]
    annualArrayEVOS = [len(annual)]
    annualArrayEV = [len(annual)]

    for x in annual:
        annualArrayPE.append(round(x['pToE'], 3))
        annualArrayPrice.append(x['priceAccountingPeriodEnd'])
        annualArrayMC.append(round(x['marketCapPeriodEnd'] / 1000000))
        annualArrayEVOS.append(round(x['evToSales'], 3))
        annualArrayEV.append(round(x['enterpriseValue'] / 1000000))

def getdata(IEX_TOKEN, stock1):
    ticker = stock1
    stock1 = IEXStock(IEX_TOKEN, stock1)
    quarter1 = stock1.get_fundamentalsquarterly('quarterly')
    annual1 = stock1.get_fundamentalsquarterly('annual')

    annualArrayYear1 = [len(annual1)]
    annualArrayRevenue1 = [len(annual1)]
    annualArrayNetIncome1 = [len(annual1)]
    annualArrayGrossmargin1 = [len(annual1)]


    for annualData1 in annual1:
        annualArrayYear1.append(annualData1['fiscalYear'])
        annualArrayRevenue1.append(annualData1['revenue'] / 1000000)
        annualArrayNetIncome1.append(annualData1['incomeNet'] / 1000000)
        annualArrayGrossmargin1.append(round(annualData1['profitGrossPerRevenue'],4))

    quote1 = stock1.get_quote()
    quoteArrayPE1 = [len(quote1)]
    PE1 = quote1['peRatio']

    annual1 = stock1.get_fundamentalsannual1('annual')
    # st.write(annual)

    annualArrayPE1 = [len(annual1)]
    annualArrayPrice1 = [len(annual1)]
    annualArrayEBITDA1 = [len(annual1)]
    annualArrayMC1 = [len(annual1)]
    annualArrayEVOS1 = [len(annual1)]
    annualArrayEV1 = [len(annual1)]
    annualArrayEBITDAMargin1 = [len(annual1)]

    for x1 in annual1:
        annualArrayPE1.append(round(x1['pToE'], 3))
        annualArrayPrice1.append(x1['priceAccountingPeriodEnd'])
        annualArrayMC1.append(round(x1['marketCapPeriodEnd'] / 1000000))
        annualArrayEVOS1.append(round(x1['evToSales'], 3))
        annualArrayEV1.append(round(x1['enterpriseValue'] / 1000000))
        annualArrayEBITDA1.append(round(x1['evToEbitda'], 4))
        annualArrayEBITDAMargin1.append(round(x1['ebitdaMargin'], 4))
    st.write(ticker)
    st.write(annualArrayPrice1[1])
    st.write(annualArrayEVOS1[1])
    st.write(annualArrayEBITDA1[1])
    st.write(annualArrayMC1[1])
    st.write(annualArrayPE1[1])
    st.write(annualArrayGrossmargin1[1])
    st.write(annualArrayEBITDAMargin1[1])
    st.write(annualArrayNetIncome1[1])

    data = [ticker,annualArrayPrice1[1],annualArrayEVOS1[1], annualArrayEBITDA1[1], annualArrayMC1[1], annualArrayPE1[1], annualArrayGrossmargin1[1], annualArrayNetIncome1[1], annualArrayNetIncome1[1]]
    return data

if __name__ == "__main__":
    main()