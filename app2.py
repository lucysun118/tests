from flask import render_template, request, redirect
#from flask_sqlalchemy import SQLAlchemy
import excelstatusbar
import generatetemplates
import openpyxl
#import pandas as pd
import json
#from flask_sqlalchemy import SQLAlchemy
#import pandas as pd
#from config1 import app, db, Vendor, Vendor_template, Owner
from config1 import app
from setup import db, Vendor, Vendor_template, Owner
#from config1 import app
#import setup
#import config1

#setup.setup("N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\Master File2 Ek - Copy.xlsx")


#df.to_sql(name='master_file', con=db.engine, index=False, if_exists='replace')

# can access the session with Flask-SQLAlchemy as db.session

# get list of owners from the Owner db
""" OWNERS = [
    "Facilities",
    "Technology"
] """

OWNERS = [o.name for o in Owner.query.all()]
        
@app.route("/") 
def index2():
    return render_template("index2.html")

@app.route("/gen_templates")
def gen_templates():
    return render_template("gen_templates_index.html")

@app.route("/gen_templates_report", methods=["POST"])
def gen_templates_report():
    input_master = request.form.get("input_master")
    master_worksheet = request.form.get("master_worksheet")

    param_col = request.form.get("param_col")
    notes_params = request.form.get("notes_params")
    owners_params = request.form.get("owners_params")

    generatetemplates.templates(input_master,master_worksheet,param_col,notes_params,owners_params)
    return redirect("/success")

@app.route("/progress_checker")
def progress_checker():
    return render_template("progress_checker_index.html", owners=OWNERS)


@app.route('/db', methods=["GET", "POST"]) 
def index():
    vendor_attr=list(vars(Vendor).keys())[2:20]
    vendors=Vendor.query
    owners = Owner.query
    #owner_attr=list(vars(Owner).keys())[1:]
    #vendor_template_attr=list(vars(Vendor_template).keys())[1:]
    if request.method == 'POST':

        checked_vendors = json.loads(request.form.get('vendors_checkboxes'))
        checked_vendor_owners = list(map(lambda x: x['Owner'], checked_vendors))
        all_vendor_templates = list(Owner.query.filter_by(name=o).first().templates for o in checked_vendor_owners)
        #checked_supplier_ids = list(map(lambda x: x['supplier_id'], checked_vendors))
        #print(f'{checked_supplier_ids}', file=sys.stdout)

        return render_template('process_owners.html', all_vendor_templates=all_vendor_templates, owners=owners)
        
    return render_template("index.html",vendor_attr=vendor_attr,vendors=vendors) 

@app.route('/process_vendors', methods=["GET", "POST"])
def process_owners():

    #for supplier_id in checked_vendor_owners:
        #owner = Vendor.query.filter_by(supplier_id=supplier_id).first().owners[0]

    #if request.method == 'POST':
        #print(request.form.getlist('checks[]'), file=sys.stdout)
        
        #checks = request.POST.getlist('checks')

    #checked_vendors = json.loads(request.POST.get('vendors_checkboxes'))
    #print(f'{checks}', file=sys.stdout)
    #sys.stdout.flush()
    # process the chosen products
    return redirect('/success')


@app.route("/process_updates")
def process_updates():
    return render_template("progress_checker_index.html", owners=OWNERS)

@app.route("/progress_report", methods=["POST"])
def progress_report():
    
    masterpath = request.form.get("masterpath")
    masterworksheet = request.form.get("masterworksheet")

    templatepath = request.form.get("templatepath")
    templateworksheet = request.form.get("templateworksheet")

    owner = request.form.get("owner")

    input_flagged_col = str(request.form.get("input_flagged_col"))

    last_row = int(request.form.get("last_row"))

        # ====================== LOAD EXCEL FILES =======================================================
    #load master
    #master_lst = openpyxl.load_workbook(str(masterpath))
    

    # get owner name for 
        
    #load team-specific
    wb = openpyxl.load_workbook(str(templatepath), keep_vba = True, read_only=False)
    questionnaire_sheet = wb[str(templateworksheet)]

    if_reassigned_col = 'AB'
    if_completed_col = 'AC'
    # =============================================================================

    # first, generate status report .txt file and return: (1) vendor id of those that are completed, (2) vendor ids of those that are flagged

    master_lst, completed_supplier_ids, flagged_supplier_ids = excelstatusbar.generate_status(masterpath,masterworksheet,templatepath,templateworksheet,owner, input_flagged_col, last_row)
    ap_report = master_lst[str(masterworksheet)]

    # update db
        # iterate over input sheet with vendors and fill after getting the template object for each
    #template_ids = [d.template.id for d in Owner.query.filter_by(name=owner).first().vendors]

    #setup.setup(masterpath)

    addnl_service = False

    for row in range(5, last_row):
        supplier_id = questionnaire_sheet['C'+str(row)].value

        # if supplier_name value is blank in input column, don't put it into db
        if supplier_id in [None, 'None', '']:
            continue

        # if owner is not the Vendor's most recent owner, add it to the list
        if owner != Vendor.query.filter_by(supplier_id=supplier_id).first().owners[-1].name:

            new_vendor_template = Vendor_template(due_date=None,vendor_manager=None,manager_email=None, l1_service=None,l2_service=None,l3_service=None,\
                service_description=None,onboarding_year=None,p72_owner=None,countries=None,countries_changes=None,\
                offices=None,offices_changes=None,in_house=None,businesses=None,products=None,business_critical1=None,\
                business_critical2=None,proprietary=None,internal_data=None,confidential=None,another_service=None)
            
            Vendor.query.template = new_vendor_template
            owner_obj = Owner.query.filter_by(name=owner).first()
            owner_obj.templates.append(new_vendor_template)
            vendor_obj = Vendor.query.filter_by(supplier_id=supplier_id).first()
            vendor_obj.owners.append(owner_obj)
        
        #if prev had an addnl service, create another vendor_template with the same Vendor class and same owner
        if addnl_service:

            new_vendor_template = Vendor_template(due_date=None,vendor_manager=None,manager_email=None, l1_service=None,l2_service=None,l3_service=None,\
                service_description=None,onboarding_year=None,p72_owner=None,countries=None,countries_changes=None,\
                offices=None,offices_changes=None,in_house=None,businesses=None,products=None,business_critical1=None,\
                business_critical2=None,proprietary=None,internal_data=None,confidential=None,another_service=None)
            
            Vendor.query.template = new_vendor_template
            owner_obj = Owner.query.filter_by(name=owner).first()
            owner_obj.templates.append(new_vendor_template)
                
            addnl_service = False

        #get the template object from supplier_id
        template = Vendor.query.filter_by(supplier_id=supplier_id).first().template

        #fill in Vendor_template db for each vendor in the input sheet
        template.due_date = questionnaire_sheet['F'+str(row)].value
        template.vendor_manager = questionnaire_sheet['H'+str(row)].value
        template.manager_email = questionnaire_sheet['I'+str(row)].value
        template.l1_service = questionnaire_sheet['J'+str(row)].value
        template.l2_service = questionnaire_sheet['K'+str(row)].value
        template.l3_service=questionnaire_sheet['L'+str(row)].value
        template.service_description=questionnaire_sheet['M'+str(row)].value
        template.onboarding_year=questionnaire_sheet['N'+str(row)].value
        template.p72_owner=questionnaire_sheet['O'+str(row)].value
        template.countries=questionnaire_sheet['P'+str(row)].value
        template.countries_changes=questionnaire_sheet['Q'+str(row)].value
        template.offices=questionnaire_sheet['R'+str(row)].value
        template.offices_changes=questionnaire_sheet['S'+str(row)].value
        template.in_house=questionnaire_sheet['T'+str(row)].value
        template.businesses=questionnaire_sheet['U'+str(row)].value
        template.products=questionnaire_sheet['V'+str(row)].value
        template.business_critical1=questionnaire_sheet['W'+str(row)].value
        template.business_critical2=questionnaire_sheet['X'+str(row)].value
        template.proprietary=questionnaire_sheet['Y'+str(row)].value
        template.internal_data=questionnaire_sheet['Z'+str(row)].value
        template.confidential=questionnaire_sheet['AA'+str(row)].value
        template.another_service=questionnaire_sheet['AB'+str(row)].value

        #if there is an addnl service, add another vendor_template 
        if questionnaire_sheet['AB'+str(row)].value == 'Yes':
            addnl_service = True


            # iterate over completed vendor ids and input 'Yes' value in the if_completed col
    for supplier_id in completed_supplier_ids:
        vendor_query = Vendor.query.filter_by(supplier_id=supplier_id).first()
        master_rownum = vendor_query.master_rownum
        ap_report[if_completed_col+str(master_rownum)] = 'Yes'
        vendor_query.if_completed = True
        vendor_query.if_sent = True

        # iterate over flagged vendor ids and input 'Yes' value in the if_reassigned col
    for supplier_id in flagged_supplier_ids:
        vendor_query = Vendor.query.filter_by(supplier_id=supplier_id).first()
        master_rownum = vendor_query.master_rownum
        ap_report[if_reassigned_col+str(master_rownum)] = 'Yes'
        vendor_query.if_reassigned = True

    db.session.commit()

    master_lst.save('N:/Groups/Operational Risk/Common/Vendor Metadata Gathering/Business Owner Templates/Master File2 Ek - Copy.xlsx')

    #for template_id in template_ids:#
        #template = Vendor_template.query.get(template_id)

    # update master file 

    return redirect('/success')

"""     try:
        excelstatusbar.generate_status(masterpath,masterworksheet,templatepath,templateworksheet,team)
        return redirect("/success")
    except:
        return redirect("/failure") """


    #owners_rows_dict = generatetemplates.templates.make_owners_rows_dict()

""" try:
        # get 
        
        #generate status report .txt file
        excelstatusbar.generate_status(masterpath,masterworksheet,templatepath,templateworksheet,owner)


        return redirect("/success")
    except:
        return redirect("/failure") """


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/failure")
def failure():
    return render_template("failure.html")



#====================== KEEP ====================#
# ensures the app will run on port 5000, a less priviledged port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)