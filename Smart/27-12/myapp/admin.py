from django.contrib import admin
from .models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Register your models here.
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'password', 'phone', 'address', 'status', 'created_at','role','id_proof','proof']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','description']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['category_id','seller_id','title','description','type','location','price','status','created_at']

@admin.register(PropertyImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['property','image']


def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 14),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.beige),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ['property_id', 'buyer_id', 'purchase_date','amount',]

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.property_id.title, obj.buyer_id.name, obj.purchase_date,obj.amount])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"



@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['property_id','buyer_id','purchase_date','start_date','end_date','amount','payment_mode','ownership_transfer_date','status','razorpay_payment_id']
    actions = [export_to_pdf]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['purchase_id','amount','payment_date','transaction_id','status','user_id']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['buyer_id','property_id','rating','comment','feedback_date']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['buyer_id','property_id','added_date']


@admin.register(Customer_Support)
class Customer_supportAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','mobile_number','email','query','created_date']
