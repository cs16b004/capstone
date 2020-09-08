from django import forms

class OrderForm(forms.Form):
    TYPE_CHOICES = [("LM", "Limit"),("MR","Market"),]
    CAT_CHOICES  = [("Buy","Buy"), ("Sell","Sell")]
    order_category     = forms.CharField(required=True, max_length=10, widget=forms.Select(choices=CAT_CHOICES))
    order_quantity     = forms.IntegerField(required=True)
    order_type         = forms.CharField(required=True, widget=forms.Select(choices= TYPE_CHOICES), max_length=10)
    order_price        = forms.FloatField(required=True)
    No_extra           = forms.BooleanField(required=True)
    All_or_none        = forms.BooleanField(required=False)
    Minimum_fill       = forms.IntegerField(required=False)
    Disclosed_Quantity = forms.IntegerField(required=False)
    