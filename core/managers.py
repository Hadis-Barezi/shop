from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, f_name, l_name, email, phone, password):
        if not f_name:
            raise ValueError("User must enter their first name.")

        if not l_name:
            raise ValueError("User must enter their last name.")

        if not email:
            raise ValueError("User must enter their email.")

        if not phone:
            raise ValueError("User must enter their phone number.")

        user = self.model(f_name=f_name, l_name=l_name, phone=phone, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, f_name, l_name, email, phone, password):
        user = self.create_user(f_name=f_name, l_name=l_name, phone=phone, email=self.normalize_email(email),
                                password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

