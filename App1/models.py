from django.db import models
import  re
import bcrypt
class Usermanager(models.Manager):
    def labour_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']

        if len(postData['name']) < 2:
            errors["name"] = "user first_name should be at least 2characters"
        if len(postData['age']) < 2:
            errors["age"] = "age should be at least 2characters"

        if len(postData['number']) < 9:
            errors["number"] = "number should be at least 9characters"
        
        if len(postData['Address']) < 2:
            errors["Address"] = "Address should be at least 2characters"


        if len(postData['skill']) < 2:
            errors["skill"] = "skill should be at least 2characters"

        if len(postData['password']) < 8:
            errors["password"] = "user password should be at least 8characters"
        if len(postData['cpassword']) <8:
            errors["cpassword"] = "user cpassword should be at least 8characters"
        
        
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if not any(characters.isupper() for characters in postData['password']):
            errors['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            errors['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            errors['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            errors['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        return errors




    def companies_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']

        if len(postData['name']) < 2:
            errors["name"] = "name should be at least 2characters"

        if len(postData['Address']) < 2:
            errors["Address"] = "Address should be at least 2characters"


        if len(postData['scope']) < 2:
            errors["scope"] = "scope of work should be at least 2characters"

        if len(postData['password']) < 8:
            errors["password"] = "user password should be at least 8characters"
        if len(postData['cpassword']) <8:
            errors["cpassword"] = "user cpassword should be at least 8characters"
        
        
        if not EMAIL_REGEX.match(postData['Email']):    # test whether a field matches the pattern            
            errors['Email'] = "Invalid email address!"
        if not any(characters.isupper() for characters in postData['password']):
            errors['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            errors['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            errors['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            errors['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        return errors

class labour(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    Address=models.CharField(max_length=255)
    contact_num=models.IntegerField()
    password=models.CharField(max_length=255)
    cpassword=models.CharField(max_length=255)
    skill=models.CharField(max_length=255)
    objects = Usermanager()


class company(models.Model):
    Name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    Address=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    cpassword=models.CharField(max_length=255)
    scope_of_work=models.CharField(max_length=255)
    objects = Usermanager()



class position(models.Model):
    Name=models.CharField(max_length=255)
    descriptions=models.CharField(max_length=255)
    required_skills=models.CharField(max_length=255)
    deadline=models.DateTimeField(auto_now=False,blank=True)
    labours=models.ManyToManyField(labour,related_name='positions')
    companies=models.ForeignKey(company,related_name='positions',on_delete=models.DO_NOTHING)

def add_position(request):
    Name=request.POST['name']
    descriptions=request.POST['description']
    required_skills=request.POST['skill']
    deadline=request.POST['date']
    id=request.session['companyid']
    companies=company.objects.get(id=id)
    return position.objects.create(Name=Name,descriptions=descriptions,required_skills=required_skills,companies=companies,deadline=deadline)

def apply_to_position(request,position_id):
    id=request.session['laborid']
    this_position=position.objects.get(id=position_id)
    this_labour=labour.objects.get(id=id)
    return this_position.labours.add(this_labour)




# register new user
def Register(request):
    name= request.POST['name']
    email = request.POST['email']
    Address=request.POST['Address']
    contact_num=request.POST['number']
    skill=request.POST['skill']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (request.POST['cpassword'] == password):
        return labour.objects.create(name = name ,Address=Address, email = email ,contact_num=contact_num,skill=skill, password = pw_hash )

def company_Register(request):
    Name= request.POST['name']
    email = request.POST['Email']
    Address=request.POST['Address']
    scope_of_work=request.POST['scope']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (request.POST['cpassword'] == password):
        return company.objects.create(Name=Name,Address=Address, email = email ,scope_of_work=scope_of_work, password = pw_hash )


def lab_Login(request):
    lab = labour.objects.filter(email = request.POST['email'])
    if lab:
        loged_labor = lab[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_labor.password.encode()):
            request.session['laborid'] = loged_labor.id
            return loged_labor.id
    else:
        return None



def comp_Login(request):
    comp = company.objects.filter(Name=request.POST['name'])
    if comp:
        loged_company = comp[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_company.password.encode()):
            request.session['companyid'] = loged_company.id
            return loged_company.id
    else:
        return None



def get_labour_info(request):
    return labour.objects.all()
    

def get_position_info(request):
    return position.objects.all()

def get_position(request,position_id):
    return position.objects.get(id=position_id)


def get_companie(request):
    id=request.session['companyid']
    return company.objects.get(id=id)