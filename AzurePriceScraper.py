# -*- coding: utf-8 -*-
import logging
import bs4
from bs4 import BeautifulSoup
import urllib.request

class AzurePriceList:
    """Scrape the actual IaaS prices from the Azure Price list webpage"""

    BaseURL = "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/"
    
    product_url = {
        "CentOS or Ubuntu Linux":                           "linux",
        "Red Hat Enterprise Linux":                          "red-hat",
        "SUSE Linux Enterprise":                             "sles",
        "SUSE Linux Enterprise for SAP":                     "sles-sap",
        "SQL Server Enterprise Ubuntu Linux":                "sql-server-enterprise-linux",
        "SQL Server Standard Ubuntu Linux":                  "sql-server-standard-linux",
        "SQL Server Web Ubuntu Linux":                       "sql-server-web-linux",
        "SQL Server Enterprise Red Hat Enterprise Linux":    "sql-server-enterprise-redhat",
        "SQL Server Standard Red Hat Enterprise Linux":      "sql-server-standard-redhat",
        "SQL Server Web Red Hat Enterprise Linux":           "sql-server-web-redhat",
        "SQL Server Enterprise SUSE":                        "sql-server-enterprise-sles",
        "SQL Server Standard SUSE":                          "sql-server-standard-sles",
        "SQL Server Web SUSE":                               "sql-server-web-sles",
        "Windows Operating System":                          "windows",
        "BizTalk Enterprise":                                "biztalk-enterprise",
        "BizTalk Standard":                                  "biztalk-standard",
        "Oracle Java":                                       "oracle-java",
        "SharePoint":                                        "sharepoint",
        "SQL Server Enterprise":                             "sql-server-enterprise",
        "SQL Server Standard":                               "sql-server-standard",
        "SQL Server Web":                                    "sql-server-web"
    }

    def __init__(self, product_name, log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)
        if log_lvl is None:
            log_lvl = logging.WARNING
        self.log.setLevel(log_lvl)
        if not len(self.log.handlers):
            self.log.addHandler(logging.StreamHandler())
        self.log.info("Product name: %s", product_name)

        # URL = AzurePriceList base URL + product specific relative path
        self.url = AzurePriceList.BaseURL + AzurePriceList.product_url[product_name] + "/"
        self.log.info("URL: %s", self.url)

    def scrape(self):
        self.log.info("Scraping starts...")
        # source = urllib.request.urlopen(self.url).read()
        # soup = bs4.BeautifulSoup(source, 'lxml')
        # self.log.info("Soup: %s", soup)

        # Find main price table
        # price_table = soup.find("table", {"class":"sd-table"})
        # price_table = soup.find("table", {"class":"sd-table"}).tr.next_siblings
        # for row in price_table:
        #     if(type(cell) is not bs4.element.NavigableString:
        #         cell = [i.text for i in row.find_all('td')]
        #         print(cell)
        source = urllib.request.urlopen("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/").read()
        soup = BeautifulSoup(source, 'lxml')
        rows = soup.find(class_="sd-table").find_all('tr')[1:]

        for row in rows:
            # cell = [i.text for i in row.find_all('td')[1:]]
            cell = [i.text for i in row.find_all('td')[1:]]
            print("cell:", cell)

        # Process rows; 1st row is the table header
        # i_row = 0
        # for row in price_table.find("thead"):
        #     self.log.info("Row #%d, length: %d", i_row, len(row))
        #     self.log.info("Row: %s", row)
        #     i_cell = 0
        #     for cell in row:
        #         if(type(cell) is not bs4.element.NavigableString:
        #             # self.log.info("Cell type: %s", type(cell))
        #             self.log.info("Cell[%d]: %s (type: %s)", i_cell, cell, type(cell))
        #         i_cell = i_cell + 1
        #     i_row = i_row + 1
            # for row in price_table.findAll("tbody"):
        

            #     cells = row.findAll("td")
            #     if len(cells) == 5:
            #         city = cells[0].find(text=True)            
            #     if city == "Szentendre":
            #         print("The level of " + river + " at " + city + " is " + level + " centimeters.")


# machine_types = []
# machine_properties = []

# Start scraping, get prices
apl = AzurePriceList("Windows Operating System", log_lvl=logging.INFO)
apl.scrape()






#  
# class="sd-table"
#     <thead>
#         <tr>
#             <th>
#                 column name #1
#             </th>
#             ...
#             <th>
#                 column name #9
#             </th>
#         </tr>
#     </thead>
#     <tbody>
#         <tr>
#             <td>
#                 '+' sign (ignore)
#             </td>
#             <td>
#                 machine type (B1S)
#             </td>
#             <td>
#                 value #1 (core)
#             </td>
#             <td>
#                 value #2 (RAM, "%2f GiB")
#             </td>
#             ...
#             <td class="payg-price">
#                 <span class='price-data ' data-amount="{"regional":{"asia-pacific-east":0.023,"asia-pacific-southeast":0.018,...}' data-decimals="3" data-month-format="{0} /hó" data-hour-format="{0}/ óra" data-region-unavailable="–">$-</span>
#             </td>
#             <td class="discounted-price">
#                 <span class='price-data ' data-amount="{"regional":{"asia-pacific-east":0.023,"asia-pacific-southeast":0.018,...}' data-decimals="3" data-month-format="{0} /hó" data-hour-format="{0}/ óra" data-region-unavailable="–">$-</span>
#                 <span class="percent-savings"></span>
#             </td>
#             <td class="discounted-price">
#                 <span class='price-data ' data-amount="{"regional":{"asia-pacific-east":0.023,"asia-pacific-southeast":0.018,...}' data-decimals="3" data-month-format="{0} /hó" data-hour-format="{0}/ óra" data-region-unavailable="–">$-</span>
#                 <span class="percent-savings"></span>
#             </td>
#             <td class="discounted-price">
#                 <span class='price-data ' data-amount="{"regional":{"asia-pacific-east":0.023,"asia-pacific-southeast":0.018,...}' data-decimals="3" data-month-format="{0} /hó" data-hour-format="{0}/ óra" data-region-unavailable="–">$-</span>
#                 <span class="percent-savings"></span>
#             </td>
#         </tr>
#         <tr>
#             <td>
#                  B2S
#             </td>
#


# big_table = soup.find("table", {"class":"sd-table"})

# for row in table.findAll("tr"):
#     cells = row.findAll("td")
#     if len(cells) == 5:
#         city = cells[0].find(text=True)            
#         river = cells[1].find(text=True)            
#         section = cells[2].find(text=True)            
#         date = cells[3].find(text=True)            
#         level = cells[4].find(text=True)            
#         if city == "Szentendre":
#             print("The level of " + river + " at " + city + " is " + level + " centimeters.")