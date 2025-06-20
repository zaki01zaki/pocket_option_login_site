
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# إعداد المتصفح بدون واجهة
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = None  # الجلسة المشتركة

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    global driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://pocketoption.com/en/login/")

    time.sleep(2)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "sign-in__submit").click()
    time.sleep(5)  # انتظار تسجيل الدخول

    if "dashboard" in driver.current_url:
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        driver.quit()
        return templates.TemplateResponse("login.html", {"request": request, "error": "Login failed. Please try again."})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
