#def setup(masterpath):
import pandas as pd
import sys

#print(sys.path)
sys.path.append('U:/pythonproj/')

from config1 import db, Vendor, Owner, Vendor_template
db.create_all()

# load excel file into df
df = pd.read_excel(
    io="N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\Master File2 Ek - Copy.xlsx",
    engine='openpyxl',
    sheet_name='Summary AP report',
    header=0
)

df = df.where(pd.notnull(df), None)

# fill tables with df info

for row in df.itertuples():
    # check if new_name already exists in Owners table, if not add:
    # if already exists, append existing Owner object to the vendor
    new_name = row[24] if row[24] != None else (row[12] if row[12] != 0 else row[20])

    owner_exists = False if (Owner.query.filter_by(name=new_name).all() == []) else True
    if not owner_exists:
        new_owner = Owner(name=new_name)
        
    else:
        new_owner = Owner.query.filter_by(name=new_name).first()

    # if new_vendor doesn't already exist in Vendors table, add:
    # if already exists, update record with new one
    vendor_name = row[2]
    existing_vendor = Vendor.query.filter_by(name=vendor_name).first()
    vendor_exists = False if (Vendor.query.filter_by(name=vendor_name).all() == []) else True

    if vendor_exists:
        existing_vendor.master_rownum = row.Index+2
        existing_vendor.supplier_id = row[1]
        existing_vendor.name = row[2]
        existing_vendor.alternate_name = row[3]
        existing_vendor.supplier_category = row[4]
        existing_vendor.phone = row[5]
        existing_vendor.email = row[6]
        existing_vendor.created_on = row[7]
        existing_vendor.created_by = row[8]
        existing_vendor.comments = row[9]
        existing_vendor.country = row[10]
        existing_vendor.priority = row[11]
        existing_vendor.due_date = row[13]
        existing_vendor.url = row[23]
        existing_vendor.notes = row[25]
        existing_vendor.if_sent = True if row[26]=='Yes' else False
        existing_vendor.if_remove = True if row[27]=='Yes' else False
        existing_vendor.if_reassigned = True if row[28]=='Yes' else False
        existing_vendor.if_completed = True if row[29]=='Yes' else False 

        if new_owner not in existing_vendor.owners:
            existing_vendor.owners.append(new_owner)

    else:
        new_vendor = Vendor(master_rownum=row.Index+2, supplier_id=row[1], name=vendor_name, alternate_name=row[3], supplier_category=row[4], phone=row[5], email=row[6],created_on=row[7],created_by=row[8],comments=row[9],country=row[10],priority=row[11],due_date=row[13], url=row[23],notes=row[24],if_sent=True if row[25]=='Yes' else False,if_remove=True if row[25]=='Yes' else False,if_reassigned=True if row[27]=='Yes' else False,if_completed=True if row[28]=='Yes' else False) 
        
        new_vendor_template = Vendor_template(due_date=None,vendor_manager=None,manager_email=None, l1_service=None,l2_service=None,l3_service=None,\
        service_description=None,onboarding_year=None,p72_owner=None,countries=None,countries_changes=None,\
        offices=None,offices_changes=None,in_house=None,businesses=None,products=None,business_critical1=None,\
        business_critical2=None,proprietary=None,internal_data=None,confidential=None,another_service=None)

        new_vendor.template = new_vendor_template
        
        new_owner.templates.append(new_vendor_template)
        
        #new_vendor.owners.append(new_owner)

        if new_owner not in new_vendor.owners:
            new_vendor.owners.append(new_owner)
        
        db.session.add(new_vendor)

    
    # if vendor did not exist, add to db
    # initialize all vendor_template values as null if vendor did not exist
    """ if not vendor_exists:

        new_vendor_template = Vendor_template(due_date=None,vendor_manager=None,manager_email=None, l1_service=None,l2_service=None,l3_service=None,\
        service_description=None,onboarding_year=None,p72_owner=None,countries=None,countries_changes=None,\
        offices=None,offices_changes=None,in_house=None,businesses=None,products=None,business_critical1=None,\
        business_critical2=None,proprietary=None,internal_data=None,confidential=None,another_service=None)

        new_owner.templates.append(new_vendor_template)
        
        #new_vendor_template.owner = new_owner

        
        new_vendor.templates.append(new_vendor_template)
        #new_vendor.owners.append(new_owner)

        #new_vendor_template.vendor = new_vendor

        db.session.add(new_vendor) """
        #db.session.add(new_vendor_template)

db.session.commit()

#setup("N:\Groups\Operational Risk\Common\Vendor Metadata Gathering\Business Owner Templates\Master File2 Ek - Copy.xlsx")
