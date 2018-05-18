from django.db import models

# Create your models here.
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class MembershipManager(models.Manager):
    def validate_registration(self, postData):
        # Original validation logic applies
        # Name must be present and at least 2 characters long
        # rate must be present
        print(postData)
        # 1. create errors dictionary
        errors = {}
        # 2. validate post information
        if len(postData['name']) == 0:
            errors['name'] = "Name must be present"
        elif len(postData['name'])<2:
            errors['name'] = "Name must be at least 2 characters long"

        # THIS IS NEW FOR REGISTERING
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be of a proper format"
        else:
            users_with_same_email = self.filter(email=postData['email'])
            if len(users_with_same_email)>0:
                errors['email'] = 'Email is already taken'
        if postData['password'] != postData['password_confirm']:
            errors['password'] = 'Password fields must match'
        if len(postData['password'])<8:
            errors['password'] = 'Password must be at least 8 characters long'
        
        print(errors)
        # 3. Check if errors exist, if they do, add them to messages
        if len(errors):
            result = {
                'errors': errors
            }
        else:
            # THIS IS ALSO NEW, WE NEED TO ADD BCRYPT TO HASH PW
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            member = self.create(
                name = postData['name'], 
                email = postData['email'], 
                password=hashed_pw
            )
            result = {
                'the_user' : member
            }
        return result

            

class Membership(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MembershipManager()