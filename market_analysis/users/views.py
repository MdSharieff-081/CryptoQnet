from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from .models import UserOTP
import random
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def user_login_page(request):
    return render(request,'user_login.html')

@csrf_exempt
def check_user_credentials(request):
    email = request.GET.get("email")
    password = request.GET.get("password")

    user = authenticate(username=email, password=password)
    if user:
        return HttpResponse("valid")
    return HttpResponse("invalid")
@csrf_exempt
def check_register_fields(request):
    email = request.GET.get("email")
    name = request.GET.get("name")
    mobile = request.GET.get("mobile")
    password = request.GET.get("password")

    if not all([email, name, mobile, password]):
        return HttpResponse("empty")

    if User.objects.filter(username=email).exists():
        return HttpResponse("exists")

    return HttpResponse("ok")


# ------------------ OTP SEND ------------------
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
import random
from .models import UserOTP


def user_send_otp(request):
    try:
        email = request.GET.get("email")
        if not email:
            return HttpResponse("failed")

        otp = str(random.randint(100000, 999999))

        # Put DB inside try
        UserOTP.objects.filter(email=email).delete()
        UserOTP.objects.create(email=email, otp=otp)
        print('otp is ',otp)
        send_mail(
            "Your OTP Verification",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return HttpResponse("sent")

    except Exception as e:
        print("OTP ERROR:", e)
        return HttpResponse("email_error")




# ------------------ OTP VERIFY ------------------
def user_verify_otp(request):
    email = request.GET.get("email")
    otp = request.GET.get("otp")

    if UserOTP.objects.filter(email=email, otp=otp).exists():
        UserOTP.objects.filter(email=email).delete()
        return HttpResponse("verified")

    return HttpResponse("invalid")


# ------------------ REGISTER ------------------
def user_register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            return render(request, "user_login.html", {"error": "User already exists"})

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
            mobile=mobile,
            status="PENDING"     
        )

        return render(request, "user_login.html", {"success": "Registration successful. Wait for admin approval."})


# ------------------ LOGIN ------------------
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user:
            # 👇 Status check
            if user.status == "APPROVED":
                login(request, user)
                return redirect('/user-dashboard/')
            elif user.status == "PENDING":
                return render(request, "user_login.html", {
                    "error": "Your account is pending admin approval"
                })
            else:
                return render(request, "user_login.html", {
                    "error": "Your account has been denied by admin"
                })

        return render(request, "user_login.html", {"error": "Invalid Login Credentials"})
def user_dashboard(request):
    return render(request,'userDashboard.html')
def user_predict(request):
    return render(request,'user_predict.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def user_profile(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.mobile = request.POST.get("mobile")

        new_password = request.POST.get("new_password")
        if new_password:
            user.set_password(new_password)

        user.save()

        # ✅ set flag
        request.session['profile_updated'] = True
        return redirect("user_profile")

    # ✅ READ & REMOVE flag here
    profile_updated = request.session.pop('profile_updated', False)

    return render(request, "user_profile.html", {
        "profile_updated": profile_updated
    })



def result_view(request):
    import pennylane as qml
    import numpy as np
    import joblib
    import os

    from django.shortcuts import render
    from django.conf import settings
    from admins.models import ModelMetrics

    predicted_price = None
    current_price = None
    mae = rmse = mape = None
    error = None

    if request.method == "POST":
        try:
            # 🔥 Get selected coin
            coin_type = request.POST.get("coin_type")

            if not coin_type:
                error = "Please select a cryptocurrency."
                return render(request, "result.html", {"error": error})

            # 🔥 Get close price
            close_price = request.POST.get("close")

            if not close_price:
                error = "Close price is required."
                return render(request, "result.html", {"error": error})

            close_price = float(close_price)
            current_price = close_price

            # 🔥 Dynamically select model based on coin
            model_path = os.path.join(
                settings.MEDIA_ROOT,
                "models",
                f"{coin_type}_CryptoQNet.pkl"
            )

            if not os.path.exists(model_path):
                error = f"{coin_type} model not trained yet."
                return render(request, "result.html", {"error": error})

            # 🔥 Load model
            saved_data = joblib.load(model_path)
            weights = saved_data["weights"]
            scaler = saved_data["scaler"]

            window_size = len(weights)

            # 🔥 Scale input properly
            scaled_value = scaler.transform(
                np.array([[close_price]])
            )

            input_window = np.repeat(
                scaled_value[0][0],
                window_size
            )

            # 🔥 Quantum Device
            dev = qml.device("default.qubit", wires=window_size)

            @qml.qnode(dev)
            def circuit(x, weights):
                qml.AngleEmbedding(x, wires=range(window_size))
                for i in range(window_size):
                    qml.RY(weights[i], wires=i)
                return qml.expval(qml.PauliZ(0))

            pred_scaled = circuit(input_window, weights)
            pred_scaled = (pred_scaled + 1) / 2

            dummy = np.zeros((1, 1))
            dummy[0][0] = pred_scaled

            predicted_price = scaler.inverse_transform(dummy)[0][0]
            predicted_price = round(float(predicted_price), 2)

            # 🔥 Fetch metrics for selected coin
            metrics = ModelMetrics.objects.filter(
                coin_type=coin_type,
                model_name="QML"
            ).first()

            if metrics:
                mae = metrics.mae_1day
                rmse = metrics.rmse
                mape = metrics.mape

        except Exception as e:
            error = str(e)

    return render(request, "result.html", {
        "predicted_price": predicted_price,
        "current_price": current_price,
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "error": error
    })
