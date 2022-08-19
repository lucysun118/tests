
""" input_path = "N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES\ONEDynamicExcelTemplate.xlsm"
output_path = "N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES\ONEDynamicExcelTemplate.xlsm"
target_sheet = 'Questionnaire'
start_row = 5
end_row=8
companynames_column = 'D'
outputurl_column = 'G' """


def generatecompanyurls(input_path, output_path, target_sheet, start_row, companynames_column, outputurl_column,end_row):
    from googlesearch import search
    import openpyxl
    import warnings

    def loadfromExcel(input_path, output_path, target_sheet, start_row, companynames_column, outputurl_column,end_row):

        warnings.simplefilter("ignore")

        master_lst = openpyxl.load_workbook(input_path, keep_vba=True, read_only=False)

        #load worksheets
        names_and_urls = master_lst.get_sheet_by_name(target_sheet)

        for row_num in range(start_row, end_row+1):

            name = names_and_urls[str(companynames_column)+str(row_num)].value

            #get company website url
            min_url = getURLs(name)
            print(row_num, name, min_url)

            #put the urls in the corresponding 2nd columns for each row
            ##names_and_urls['B'+str(row_num)] = min_url
            names_and_urls[str(outputurl_column)+str(row_num)].value = str(min_url)

        #print(f'All URLs: {urls_arr}')
        #print(f'Min URL: {min_url}')

        master_lst.save(output_path)

    def getURLs(companyName):
        #companyName = "/n software inc."

        urls=[]
        for i in search(companyName,tld="com",num=3,stop=5,pause=2):
            urls.append(i)
        #print(urls)
        return sorted(urls, key=len)[0]

    loadfromExcel(input_path, output_path, target_sheet, start_row, companynames_column, outputurl_column,end_row)

""" def main():
    loadfromExcel(input_path, output_path, target_sheet, start_row, companynames_column, outputurl_column,end_row)  

main() """

