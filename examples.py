# FILE PATH: N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES


# 1. GENERATE EXAMPLE BUSINESS OWNER (TECH) TEMPLATE

from generatetemplates import templates
# templates(masterpath, masterworksheet, owner_name_col)
templates("N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES\TWOmasterSpreadsheet.xlsx", "Summary AP report", "S")

# 2. GENERATE COMPANY URLS
from generatecompanyurls import generatecompanyurls

    # loadfromExcel(input_path, output_path, target_sheet, start_row, companynames_column, outputurl_column,end_row)
generatecompanyurls("N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES\OUT_Business Owners Questionnaire_Technology.xlsm",\
    "N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES\OUT_Business Owners Questionnaire_Technology.xlsm",\
         "Questionnaire", 5, "D", "G", 8)  

# 3. PROGRESS CHECKER AND UPDATE SPREADSHEET
from excelstatusbar import generate_status

generate_status("N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES\TWOmasterSpreadsheet.xlsx",\
     "Summary AP report",\
         "N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\EXAMPLES\THREETechnologyReceivedTemplate.xlsm",\
             "Questionnaire", "Technology", "H", 8)