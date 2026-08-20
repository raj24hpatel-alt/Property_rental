from django.shortcuts import render,redirect
from django.conf import settings
from pyexpat.errors import messages
from .models import *
import razorpay
from django.contrib import messages
from datetime import datetime


# Create your views here.
def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def property(request, id):
    property = Property.objects.get(id=id)

    bookings = Purchase.objects.filter(property_id=property)

    booked_ranges = []
    for b in bookings:
        booked_ranges.append({
            "start": b.start_date.strftime("%Y-%m-%d"),
            "end": b.end_date.strftime("%Y-%m-%d"),
        })

    images = property.images.all()   # ✅ GET ALL IMAGES

    return render(request, "properties-details.html", {
        "property": property,
        "images": images,   # ✅ PASS IMAGES
        "booked_ranges": booked_ranges
    })
def propertiesvs1(request):
    return render(request,"properties-v1.html")
def propertiesvs2(request):
    categories = Category.objects.all()
    properties = Property.objects.all()
    print(properties)
    context = {
        "categories": categories,
        "properties": properties,
    }
    return render(request, "properties-v2.html", context)
def register(request):
    return render(request,"register.html")
def login(request):
    return render(request,"login.html")
def service(request):
    return render(request,"service.html")
def singleservice(request):
    return render(request,"single-service.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Registration

def Register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        role = request.POST.get("Role")
        shop_name = request.POST.get("shop_name")
        property_rights = request.POST.get("property_rights")
        status = request.POST.get("status")

        # Safe file handling
        id_proof = request.FILES.get("id_proof")

        # ✅ Check if email already exists
        if Registration.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("/register")

        # ✅ Hash password
        hashed_password = make_password(password)

        # ✅ Role-based insert
        if role == '1':
            Registration.objects.create(
                name=name,
                email=email,
                password=hashed_password,
                phone=phone,
                address=address,
                status=status,
                role=role,
                id_proof=id_proof,
                shop_name="N/A",
                property_rights="N/A"
            )
        else:
            Registration.objects.create(
                name=name,
                email=email,
                password=hashed_password,
                phone=phone,
                address=address,
                status=status,
                role=role,
                id_proof=id_proof,
                shop_name=shop_name,
                property_rights=property_rights
            )

        messages.success(request, "Registration Successful")
        return redirect("/login")

    return render(request, "register.html")
def logindata(request):
        email=request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)

        try:
            userdata = Registration.objects.get(email=email, password=password)
            messages.success(request, "login successfull")
            print("login Done")

            request.session["log_id"] = userdata.id
            request.session["log_name"] = userdata.name
            request.session["log_email"] = userdata.email
            request.session["log_role"] = userdata.role
            request.session["log_password"] = userdata.password

            print("session started:", request.session["log_id"])
            print("Login Successfully")
            return redirect("/")

        except:
            userdata = None
            messages.error(request, "Invalid Email or Password")
        if userdata is not None:
            print("Login successfully")

        return render(request, "login.html")
def logout(request):
    try:
        del(request.session["log_id"])
        del(request.session["log_name"])
        del(request.session["log_email"])
        del(request.session["log_role"])
    except:
        pass
    return redirect("/")
def addproperty(request):
    fetchdata = Category.objects.all()

    context = {
        "data":fetchdata
    }
    return render(request,"add-properties.html",context)

def insertproperty(request):
    fetchdata = Category.objects.all()
    if request.method == "POST":

        category_id = request.POST.get("category_id")
        title = request.POST.get("title")
        description = request.POST.get("textarea")
        type = request.POST.get("type")
        location = request.POST.get("location")
        price = request.POST.get("price")
        status = request.POST.get("status")

        images = request.FILES.getlist("Images")

        seller_id = request.session.get("log_id")

        if not all([category_id, title, description, type, location, price, status]):
            messages.error(request, "All fields are required!")
            return redirect("add-properties")

        try:
            seller = Registration.objects.get(id=seller_id)
            category = Category.objects.get(id=category_id)

            property_obj = Property.objects.create(
                category_id=category,
                seller_id=seller,
                title=title,
                description=description,
                type=type,
                location=location,
                price=price,
                status=status
            )

            # ✅ SAVE MULTIPLE IMAGES
            for img in images:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=img
                )

            messages.success(request, "Property Added Successfully...")
            return redirect("/manageproperties")

        except Exception as e:
            print("ERROR:", e)
            messages.error(request, "Something went wrong!")

    context = {
        "data": fetchdata
    }
    return render(request, "add-properties.html", context)

def manageproperties(request):
    seller_loggedin = request.session.get("log_id")
    fetchdata = Property.objects.filter(seller_id_id=seller_loggedin)

    context = {
        "data": fetchdata
    }
    return render(request, "manageproperties.html", context)
def removeproperties(request, id):
    seller_loggedin = request.session.get("log_id")

    # ✅ Check login first
    if not seller_loggedin:
        messages.error(request, "Please login first!")
        return redirect("login")

    try:
        property_obj = Property.objects.get(id=id, seller_id_id=seller_loggedin)
        property_obj.delete()
        messages.success(request, "Property Removed Successfully..")

    except Property.DoesNotExist:
        messages.error(request, "Property not found or unauthorized!")

    # ✅ IMPORTANT: Always redirect after delete
    return redirect("/manageproperties")
def editproperties(request, id):
    seller_loggedin = request.session.get("log_id")

    category = Category.objects.all()
    property = Property.objects.get(id=id, seller_id_id=seller_loggedin)

    images = property.images.all()  # ✅ GET ALL IMAGES

    context = {
        "category": category,
        "property": property,
        "images": images
    }
    return render(request, "editproperties.html", context)


def updateproperties(request):
    if request.method == "POST":
        seller_loggedin = request.session.get("log_id")
        propertyid = request.POST.get("propertyid")

        try:
            propertydetails = Property.objects.get(
                id=propertyid,
                seller_id=seller_loggedin
            )

            # ✅ Update basic fields
            propertydetails.category_id_id = request.POST.get("category_id")
            propertydetails.title = request.POST.get("title")
            propertydetails.description = request.POST.get("description")
            propertydetails.type = request.POST.get("type")
            propertydetails.location = request.POST.get("location")
            propertydetails.price = request.POST.get("price")
            propertydetails.status = request.POST.get("status")

            propertydetails.save()

            # ===============================
            # ✅ MULTIPLE IMAGE ADD
            # ===============================
            images = request.FILES.getlist("Images")  # 👈 IMPORTANT

            for img in images:
                PropertyImage.objects.create(
                    property=propertydetails,
                    image=img
                )

            messages.success(request, "Property Updated Successfully...")

        except Property.DoesNotExist:
            messages.error(request, "Unauthorized or invalid property!")

        return redirect("/manageproperties")

    return redirect("manageproperties")

def delete_image(request, id):
    img = PropertyImage.objects.get(id=id)
    img.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def placeorder(request):
    propertyid = request.POST.get("propertyid")
    userid = request.session["log_id"]
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    amount = request.POST.get("amount")

    # ✅ CONVERT STRING → DATETIME
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # ✅ 🔴 VALIDATION (MAIN PART)
    is_booked = Purchase.objects.filter(
        property_id=propertyid,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).exists()

    if is_booked:
        messages.error(request, "This property is already booked for selected dates!")
        return redirect(request.META.get('HTTP_REFERER'))

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
    order_amount = int(float(amount) * 100)
    razorpay_order = client.order.create({
        "amount": order_amount,
        "currency": "INR",
        "receipt": f"order_rcptid_{userid}",
        "payment_capture": "1",
    })
    storedata = Purchase(
        property_id=Property(id=propertyid),
        buyer_id=Registration(id=userid),
        start_date=start_date,
        end_date=end_date,
        amount=amount,
        payment_mode="Online Payment",
        approval_status="Unapproved",
        status="Booked",
        razorpay_payment_id=razorpay_order['id'],
    )
    storedata.save()
    return render(request, "payment.html", {
        "razorpay_order_id": razorpay_order['id'],
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID,
        "currency": "INR",
    })
def payment_success(request):
    return redirect(propertiesvs2)

def sellerhistory(request):
    seller_id = request.session.get("log_id")

    data = Purchase.objects.filter(
        property_id__seller_id_id=seller_id   # 🔥 correct way
    )

    # calculate total days
    for booking in data:
        if booking.start_date and booking.end_date:
            booking.total_days = (booking.end_date - booking.start_date).days
        else:
            booking.total_days = 0

    context = {
        "data": data
    }

    return render(request, "sellerhistory.html", context)

def userbookinghistory(request):
    userid = request.session.get("log_id")

    data = Purchase.objects.filter(
        buyer_id_id=userid   # 🔥 correct way
    )

    # optional: calculate total days
    for booking in data:
        if booking.start_date and booking.end_date:
            booking.total_days = (booking.end_date - booking.start_date).days
        else:
            booking.total_days = 0

    context = {
        "data": data
    }
    return render(request, "bookinghistory.html", context)

def addwishlist(request, id):
    userid = request.session["log_id"]

    property = Property.objects.get(id=id)
    buyer = Registration.objects.get(id=userid)

    if not Wishlist.objects.filter(property_id=property, buyer_id=buyer).exists():
        Wishlist.objects.create(
            property_id=property,
            buyer_id=buyer
        )

    return redirect("/wishlistpage")
def wishlistpage(request):
    user_id = request.session["log_id"]
    data = Wishlist.objects.filter(buyer_id=user_id)

    return render(request, "wishlist.html", {"data": data})

def removewishlist(request, id):
    try:
        item = Wishlist.objects.get(
            id=id,
            buyer_id=request.session.get("log_id")
        )
        item.delete()
    except:
        pass

    return redirect("wishlistpage")

# from .models import Feedback

def givefeedback(request):
    userid = request.session["log_id"]
    user = Registration.objects.get(id=userid)

    properties = Purchase.objects.filter(buyer_id=user, status='Booked')

    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        purchase_id = request.POST.get('property_id')  # ✅ from dropdown

        # 🔴 safety check
        if not purchase_id:
            messages.error(request, "Please select property!")
            return redirect('givefeedback')

        try:
            purchase = Purchase.objects.get(id=purchase_id)
        except Purchase.DoesNotExist:
            messages.error(request, "Invalid property selected!")
            return redirect('givefeedback')

        # ✅ CORRECT INSERT QUERY
        Feedback.objects.create(
            buyer_id=user,
            property_id=purchase.property_id,   # ✔ actual property
            rating=rating,
            comment=comment
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('/')

    return render(request, 'givefeedback.html', {"properties": properties})

def viewfeedback(request):
    feedbacks = Feedback.objects.select_related('property_id', 'buyer_id').all().order_by('-feedback_date')

    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'viewfeedback.html', context)
from django.shortcuts import get_object_or_404, redirect

def update_booking_status(request, booking_id, status):
    # 1. Fetch the specific booking
    booking = get_object_or_404(Purchase, id=booking_id)

    # 2. Update the status in the model
    booking.approval_status = status

    # 3. Logic: If approved, you might also want to change the overall 'status' to Booked
    if status == "Approved":
        booking.status = "Booked"
    elif status == "Rejected":
        booking.status = "Cancelled"  # Or whatever your logic requires

    booking.save()
    return redirect('/viewbookinghistory')
    # 4. Redirect back to the booking history page
    return render(request,"index.html")  # Replace with the name of your list view

def invoice(request, id):
    userid = request.session.get("log_id")
    # Fetch the booking
    booking = Purchase.objects.get(id=id, buyer_id=userid)

    # Use the database ID to create a sequential invoice number
    # .zfill(4) is optional: it makes it INV0001, INV0002, etc.
    # If you want just INV1, use f"INV{booking.id}"
    invoice_number = f"INV{str(booking.id).zfill(4)}"

    total_days = (booking.end_date - booking.start_date).days + 1
    price = int(booking.property_id.price)
    total_amount = price * total_days

    context = {
        "booking": booking,
        "total_days": total_days,
        "price_formatted": "{:,}".format(price),
        "total_amount_formatted": "{:,}".format(total_amount),
        "invoice_number": invoice_number,
        "invoice_date": booking.start_date, # Or timezone.now().date()
    }
    return render(request, "invoice.html", context)
def contact_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile_number = request.POST.get("mobile_number")
        email = request.POST.get("email")
        query = request.POST.get("query")
        # Save data
        Customer_Support.objects.create(
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            email=email,
            query=query,
        )

        messages.success(request, "Your message has been sent successfully!")

        return redirect('/')  # make sure URL name is 'contact'

    return render(request, 'contact-us.html')

# Forgot Password Page
def forgotpassword(request):
    return render(request, "forgotpassword.html")

def forgotpassword(request):
    return render(request, "forgotpassword.html")


def resetpassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("password")

        try:
            user = Registration.objects.get(email=email)

            # ❌ SAME PASSWORD CHECK
            if user.password == new_password:
                messages.error(request, "New password cannot be same as old password")
                return redirect('forgotpassword')

            # ✅ UPDATE PASSWORD
            user.password = new_password
            user.save()

            messages.success(request, "Password Reset Successful")
            return redirect('login')

        except Registration.DoesNotExist:
            messages.error(request, "Email not found")
            return redirect('forgotpassword')

    return redirect('forgotpassword')