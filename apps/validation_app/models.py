from django.db import models

# Create your models here.

class MembershipManager(models.Manager):
    def validate_membership(self, postData):
        # Original validation logic applies
        # Name must be present and at least 2 characters long
        # Description must be present and at least 8 characters
        # price must be present
        print(postData)
        # 1. create errors dictionary
        errors = {}
        # 2. validate post information
        if len(postData['name']) == 0:
            errors['name'] = "Name must be present"
        elif len(postData['name'])<2:
            errors['name'] = "Name must be at least 2 characters long"

        if len(postData['rate']) == 0:
            errors['rate'] = "rate must be present"
        
        if len(postData['description']) == 0:
            errors['description'] = "Description is required"
        elif len(postData['description']) < 8:
            errors['description'] = "Description must be at least 8 characters long"
        print(errors)
        # 3. If errors exists, package them in a dictionary
        if len(errors): 
            result = {
                'errors': errors
            }
            return result
        # 4. If no errors, create the membership here
        else:
            member = self.create(name = postData['name'], description = postData['description'], rate = postData['rate'])
            result = {
                'the_member': member
            }
            return result

class Membership(models.Model):
    name = models.CharField(max_length = 255)
    rate = models.FloatField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MembershipManager()