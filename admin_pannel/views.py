import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
from datetime import datetime
import calendar

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')   # this is UserMobileNo
        password = request.POST.get('pass1')      # this is UserPin

        api_url = "https://www.gyaagl.app/goldvault_api/adminlogin"

        # Headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Data
        payload = {
            "UserMobileNo": username,
            "UserPin": password
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            res_json = response.json()

            if res_json.get("message_code") == 1000:
                # ✅ Login success
                user_name = res_json["message_data"]["Name"]

                # Store in session
                request.session["user_name"] = user_name
                request.session["user_mobile"] = username

                messages.success(request, f"Welcome {user_name}!")
                return redirect('dashboard')
            else:
                messages.error(request, res_json.get("message_text", "Login failed"))
                return redirect('login')

        except Exception as e:
            messages.error(request, f"API error: {e}")
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    request.session.flush()  # clears all session data
    messages.success(request, "You have successfully signed out")
    return redirect('login')

def dashboard(request):
    return render(request, 'dashboard.html')

def jeweller_list(request):
    companies = []  # default empty list

    # months: [(1, "January"), (2, "February"), ...]
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    # years: 2025–2027
    years = [2025, 2026, 2027]

    # get current year and month
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # defaults
    selected_month = current_month
    selected_year = current_year

    if request.method == "POST":
        selected_year = int(request.POST.get("SearchYear"))
        selected_month = int(request.POST.get("SearchMonth"))

    api_url = "https://www.gyaagl.app/goldvault_api/clientregisterations"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    payload = {
        "SearchYear": selected_year,
        "SearchMonth": selected_month
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res_json = response.json()

        if res_json.get("message_code") == 1000:
            companies = res_json.get("message_data", [])
        else:
            messages.error(request, res_json.get("message_text", "No records found"))
    except Exception as e:
        messages.error(request, f"API error: {e}")

    return render(
        request,
        "client/jeweller_list.html",
        {
            "companies": companies,
            "months": months,
            "years": years,
            "selected_month": selected_month,
            "selected_year": selected_year,
        }
    )
    
def user_list(request, id):
    users = []

    # get current year and month
    now = datetime.now()
    current_year = str(now.year)
    current_month = str(now.month)

    # If no POST request, set defaults
    if request.method == "POST":
        SearchYear = request.POST.get("SearchYear") or current_year
        SearchMonth = request.POST.get("SearchMonth") or current_month
    else:
        SearchYear = current_year
        SearchMonth = current_month

    payload = {
        "ClientCode": id,
        "SearchYear": SearchYear,
        "SearchMonth": SearchMonth,
    }

    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.post(
            "https://www.gyaagl.app/goldvault_api/registerations",
            json=payload,   # send JSON
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("message_code") == 1000:
                users = data.get("message_data", [])
            else:
                messages.error(request, data.get("message_text", "No data found"))
        else:
            messages.error(request, f"API error: {response.status_code}")
    except Exception as e:
        messages.error(request, f"Error fetching data: {str(e)}")

    context = {
        "users": users,
        "client_id": id,
        "years": [2025, 2026, 2027],  # can be dynamic too
        "months": [(i, calendar.month_name[i]) for i in range(1, 13)],  # ✅ month list with names
        "SearchYear": SearchYear,
        "SearchMonth": SearchMonth,
    }
    return render(request, "client/user_list.html", context)