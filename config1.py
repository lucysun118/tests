from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#import plotly.express as px
#import streamlit as st

#st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# set up Flask app
# set up flask-SQLAlchemy connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owners_group2.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

# set up database names etc
owners_vendors = db.Table('owners_vendors',
    db.Column('vendor_id', db.Integer, db.ForeignKey('vendor.id')),
    db.Column('owner_id', db.Integer, db.ForeignKey('owner.id')),
    db.Column('vendor_template_id', db.Integer, db.ForeignKey('Vendor_template.id')))

class Vendor(db.Model):
    #__tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    master_rownum = db.Column("Master File RowNum", db.Integer)
    supplier_id = db.Column("Supplier String ID", db.String(50))
    name = db.Column("Name", db.String(120),nullable=False)
    alternate_name = db.Column("Alternate Name", db.String(200))
    supplier_category = db.Column("Supplier Category", db.String(120))
    phone = db.Column("Phone Number", db.String(120))
    email = db.Column("Email Address", db.String(120))
    created_on = db.Column("Created On", db.Integer)
    created_by = db.Column("Created By", db.String(120))
    comments = db.Column("Comments", db.String(120))
    country = db.Column("Country", db.String(120))
    priority = db.Column("Priority", db.String(10))
    due_date = db.Column("Due Date", db.String(10))
    url = db.Column("Company Website", db.String(200))
    notes = db.Column("Notes", db.String(200))
    if_sent = db.Column("Sent?", db.Boolean)
    if_remove = db.Column("Remove?", db.Boolean)
    if_reassigned = db.Column("Reassigned?", db.Boolean)
    if_completed = db.Column("Completed?", db.Boolean)
    owners = db.relationship('Owner', secondary=owners_vendors, backref='vendors')
    #templates = db.relationship('Vendor_template', secondary=owners_vendors, backref='vendors')
    template = db.relationship('Vendor_template', uselist=False, backref="vendor")

    def __init__(self, master_rownum, supplier_id, name, alternate_name, supplier_category, phone, email, created_on, created_by, comments, country, priority, due_date, url, notes,if_sent,if_remove,if_reassigned,if_completed):
        self.master_rownum = master_rownum
        self.supplier_id = supplier_id
        self.name = name
        self.alternate_name = alternate_name
        self.supplier_category = supplier_category
        self.phone = phone 
        self.email = email
        self.created_on = created_on
        self.created_by = created_by
        self.comments = comments
        self.country = country
        self.priority = priority
        self.due_date = due_date
        self.url = url
        self.notes = notes
        self.if_sent = if_sent
        self.if_remove = if_remove
        self.if_reassigned = if_reassigned
        self.if_completed = if_completed

class Owner(db.Model):
    #__tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(120))
    templates = db.relationship('Vendor_template', secondary=owners_vendors, backref='owner')
    #templates = db.relationship('Vendor_template', backref='owner', lazy=True)
    
    def __init__(self, name):
        self.name = name

class Vendor_template(db.Model):
    __tablename__ = 'Vendor_template'
    id = db.Column(db.Integer, primary_key=True)
    #owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))


    due_date = db.Column("Due Date", db.String(120))
    vendor_manager = db.Column("Primary Relationship Manager", db.String(120))
    manager_email = db.Column("Primary Relationship Manager Email", db.String(100))
    l1_service = db.Column("L1 Service Provided", db.String(150))
    l2_service = db.Column("L2 Service Provided", db.String(150))
    l3_service = db.Column("L3 Service Provided", db.String(150))
    service_description = db.Column("Detailed Services Description", db.String(250))
    onboarding_year = db.Column("Onboarding Year", db.String(10))
    p72_owner = db.Column("Point72 Primary Owner", db.String(100))
    countries = db.Column("Serviced Countries", db.String(200))
    countries_changes = db.Column("Changes to Countries?", db.String(5))
    offices = db.Column("Serviced Office Locations", db.String(150))
    offices_changes = db.Column("Changes to Offices?", db.String(5))
    in_house = db.Column("Provide in-house Services?", db.String(5))
    businesses = db.Column("Businesses Supported", db.String(150))
    products = db.Column("Products Provided", db.String(100))
    business_critical1 = db.Column("Business Critical 1?", db.String(5))
    business_critical2 = db.Column("Business Critical 2?", db.String(5))
    proprietary = db.Column("proprietary", db.String(5))
    internal_data = db.Column("Internal Data?", db.String(5))
    confidential = db.Column("Confidential?", db.String(5))
    another_service = db.Column("Another Service?", db.String(5))
    
    def __init__(self, due_date, vendor_manager,manager_email,l1_service,l2_service,l3_service,\
        service_description,onboarding_year,p72_owner,countries,countries_changes,\
        offices,offices_changes,in_house,businesses,products,business_critical1,\
        business_critical2,proprietary,internal_data,confidential,another_service):
        self.due_date = due_date
        self.vendor_manager = vendor_manager
        self.manager_email = manager_email
        self.l1_service = l1_service
        self.l2_service = l2_service
        self.l3_service=l3_service
        self.service_description=service_description
        self.onboarding_year=onboarding_year
        self.p72_owner=p72_owner
        self.countries=countries
        self.countries_changes=countries_changes
        self.offices=offices
        self.offices_changes=offices_changes
        self.in_house=in_house
        self.businesses=businesses
        self.products=products
        self.business_critical1=business_critical1
        self.business_critical2=business_critical2
        self.proprietary=proprietary
        self.internal_data=internal_data
        self.confidential=confidential
        self.another_service=another_service