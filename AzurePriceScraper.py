# v3
# -*- coding: utf-8 -*-
import logging
import urllib.request
from bs4 import BeautifulSoup
#test comment - szalonta
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

    machine = []
    pricelist = []

    def __init__(self, product_name, log_lvl=logging.INFO):
        # Start logging
        self.log = logging.getLogger(__name__)
        if log_lvl is None:
            log_lvl = logging.WARNING
        self.log.setLevel(log_lvl)
        if len(self.log.handlers) == 0:
            self.log.addHandler(logging.StreamHandler())
        self.log.info("Product name: %s", product_name)

        # URL = AzurePriceList base URL + product specific relative path
        self.url = AzurePriceList.BaseURL + AzurePriceList.product_url[product_name] + "/"
        self.log.info("URL: %s", self.url)

    def scrape(self):
        self.log.info("Scraping starts...")
        source = urllib.request.urlopen("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/").read()
        soup = BeautifulSoup(source, 'lxml')
        
        # Scrape pricing header row
        # Drop 1st column 
        row = soup.find(class_="sd-table").find_all('th')[1:]
        i = 0
        for cell in row:
            self.machine.append(cell.text)
            i = i + 1
        
        # Log header
        self.log.info("Header:")
        for i in range(len(self.machine)):
            self.log.info("%d: \"%s\"", i, self.machine[i])

        # Scrape machine pricing information
        #while True:
            # Drop 1st column
            row = soup.find(class_="sd-table").find_all('td')[1:]
            for cell in row:
                self.machine.append(cell.text)
            
            #if fail_condition:
            #    break

        # Add machine prices to pricelist 
        self.pricelist.append(self.machine)

        # Log pricelist
        # for i in range(len(self.pricelist)):
        #    for j in range(len(self.pricelist[i])):
        #         self.log.info("machine[%d] = %s", i, self.pricelist[i][j])


#
# Main
# 

# Start scraping, get prices
apl = AzurePriceList("Windows Operating System", log_lvl=logging.INFO)
apl.scrape()

#
#=====================================
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