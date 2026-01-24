from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import UserProfile, Course

class Index(View):
    def get(self, request):
        if request.session.get("user_logged_in"):
            return redirect("PRO:home")
        else:
            return redirect("PRO:login")



class Home(TemplateView):
    template_name = 'PRO/home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("PRO:login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["quick_courses"] = Course.objects.filter(is_active=True).order_by("-id")[:6]

        q = (self.request.GET.get("q") or "").strip()
        ctx["q"] = q

        if q:
            ctx["search_results"] = Course.objects.filter(is_active=True).filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            ).order_by("-id")
        else:
            ctx["search_results"] = []

        return ctx

class Admin(TemplateView):
    template_name = "PRO/admin_panel.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user_logged_in"):
            return redirect("PRO:login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user_id = self.request.session.get("user_id")

        profile = None
        if user_id:
            profile = UserProfile.objects.filter(id=user_id).first()

        ctx["profile"] = profile
        ctx["courses"] = Course.objects.all().order_by("-id")
        return ctx

    def post(self, request, *args, **kwargs):
        action = (request.POST.get("action") or "").strip()

        if action == "update_profile":
            user_id = request.session.get("user_id")
            if not user_id:
                return redirect("PRO:admin_panel")

            profile = UserProfile.objects.filter(id=user_id).first()
            if not profile:
                return redirect("PRO:admin_panel")

            profile.first_name = request.POST.get("first_name", "").strip()
            profile.last_name = request.POST.get("last_name", "").strip()
            profile.username = request.POST.get("username", "").strip()
            profile.phone_num = request.POST.get("phone_num", "").strip()

            profile.save()
            return redirect("PRO:admin_panel")

        if action == "add_course":
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()

            if title:
                Course.objects.create(title=title, description=description)
            return redirect("PRO:admin_panel")

        if action == "update_course":
            course_id = request.POST.get("course_id")
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            is_active = request.POST.get("is_active") == "on"

            course = Course.objects.filter(id=course_id).first()
            if course and title:
                course.title = title
                course.description = description
                course.is_active = is_active
                course.save()
            return redirect("PRO:admin_panel")

        if action == "delete_course":
            course_id = request.POST.get("course_id")
            Course.objects.filter(id=course_id).delete()
            return redirect("PRO:admin_panel")

        return redirect("PRO:admin_panel")


class Courses(TemplateView):
    template_name = 'PRO/courses.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("PRO:login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        q = (self.request.GET.get("q") or "").strip()
        ctx["q"] = q

        courses_qs = Course.objects.filter(is_active=True).order_by("-id")

        if q:
            courses_qs = courses_qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        ctx["courses"] = courses_qs

        return ctx
    

class Register(View):
    def get(self, request):
        return render(request, "PRO/register.html")

    def post(self, request):
        data = request.POST
        try:
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            id_num = data.get("id_num")
            phone_num = data.get("phone_num")
            username = data.get("username")
            password = data.get("password")

            user = UserProfile.objects.filter(username=username).first()
            id_num = UserProfile.objects.filter(id_num=id_num).first()
            phone_num = UserProfile.objects.filter(phone_num=phone_num).first()

            if user:
                raise ValueError("کاربر با این نام کاربری وجود دارد")
            
            if id_num:
                raise ValueError("کاربر با این کد ملی وجود دارد")
        
            if phone_num:
                raise ValueError("کاربر بااین شماره تماس وجود دارد")
            
            user = UserProfile.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                id_num=id_num,
                phone_num=phone_num,
            )

            request.session["user_logged_in"] = True
            request.session["user_id"] = user.id

            return redirect("PRO:home")
        
        except Exception as e:
            return render(
                request,
                "PRO/register.html",
                {
                    "error": str(e),
                    "info": data,
                },
            )


class Login(View):
    def get(self, request):
        return render(request, "PRO/login.html")

    def post(self, request):
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = UserProfile.objects.filter(username=username, password=password).first()

            if not user:
                raise ValueError("نام کاربری یا رمز عبور اشتباه است")

            request.session["user_logged_in"] = True
            request.session["user_id"] = user.id

            return redirect("PRO:home")
        
        except Exception as e:
            return render(
                request,
                "PRO/login.html",
                {
                    "error": str(e),
                },
            )
    
class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect("PRO:login")