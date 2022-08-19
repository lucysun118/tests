# -*- coding: utf-8 -*-

def process_flagged(questionnaire_sheet, flagged_rows_lst, master_lst, team, master_col_dict, input_flagged_col):

    #load AP Summary worksheet
    master_worksheet = 'Summary AP report'
    input_flagged_col = ord(input_flagged_col)-64
    ap_report = master_lst.get_sheet_by_name(master_worksheet)
    
    #DYNAMIC VALUES
    master_notes_col = 25 #Y
    #input_flagged_col = 8 #H - for Facilities and Tech (same col)
    supplier_id_col = 3 #C - Supplier_ID
    
    nonblanks = []
    blanks = []

    print(flagged_rows_lst)
    
    vendorData = supplier_row_dict(ap_report, master_col_dict)
    
    for row in flagged_rows_lst:
        input_notes = questionnaire_sheet.cell(row=row, column=input_flagged_col).value
        input_supplier_id = questionnaire_sheet.cell(row=row, column=supplier_id_col).value
        
        master_notes = ap_report.cell(row=vendorData[input_supplier_id], column=master_notes_col)

        #column 28 is AB (if_reassigned)
        ap_report.cell(row=vendorData[input_supplier_id], column=28).value = 'Yes'
        
        #extract the team-specific notes
        #if input_notes not in ['None', '', ' ', None]:
        updated_notes = f'Not {team}: {input_notes}'
        if input_notes in ['None', '', None]:
            input_notes = ' '
        
            #make sure there's nothing already in the notes column 
        if master_notes.value in ['None', '', None]:
            master_notes.value = updated_notes
            blanks.append((vendorData[input_supplier_id], updated_notes))
            
        elif f'Not {team}' in master_notes.value:
            continue
                
            #if team-specific notes already recorded, leave alone
        elif ' / ' in master_notes.value:
            continue
            
            #else need to append to keep previously existing info
        else:
            updated_notes = ' / '.join([master_notes.value, updated_notes])
            master_notes.value = updated_notes
            nonblanks.append((row, master_notes.value, updated_notes))
            
                
    #print(f'(Row, Note) Already with a Note: {nonblanks}')
    return master_lst

    #print(f'originally blank: {blanks}')
                
    #master_lst.save('N:/Groups/Operational Risk/Common/Vendor Metadata Gathering/Business Owner Templates/Master File2 Ek - Copy.xlsx')
        
    #return nonblanks
    
def supplier_row_dict(ap_report, master_col_dict):
    
    vendorData = {}

    for row in range(2, ap_report.max_row+1):
		#each row in the spreadsheet has data for one vendor
        #in this case, "value" = supplier_id and "key" = row num of master
        value = ap_report[master_col_dict + str(row)].value
		
        if value == None or value == 0:
            continue
        else:
            vendorData[value] = row
    
    return vendorData
        


# =============================================================================
#     input_master = "N:/Groups/Operational Risk/Common/Vendor Metadata Gathering/Business Owner Templates/Master File2 Ek - Copy.xlsx"
#     master_lst = openpyxl.load_workbook(input_master,keep_vba = True, read_only=False)
#     master_worksheet = 'Summary AP report'
#     ap_report = master_lst.get_sheet_by_name(master_worksheet)
#     master_col_dict_key = 'A'
# =============================================================================